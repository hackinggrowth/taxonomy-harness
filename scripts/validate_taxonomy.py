#!/usr/bin/env python3
"""Validate event taxonomy CSV exports with deterministic checks."""
from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

GENERIC_PROPERTIES = {"type", "source", "status", "category", "name", "value", "id"}
PII_TOKENS = {
    "email",
    "phone",
    "address",
    "birthday",
    "birthdate",
    "ssn",
    "ip",
    "ip_address",
    "resident_id",
    "passport",
    "credit_card",
    "card_number",
    "user_email",
}
PII_ALLOWLIST = {
    "button_name",
    "page_name",
    "section_name",
    "screen_name",
    "campaign_name",
    "experiment_name",
    "plan_name",
    "product_name",
    "company_name",
}
BASE_EVENT_FIELDS = ["event_name"]
BASE_PROPERTY_FIELDS = ["event_name", "property_name"]
RECOMMENDED_EVENT_FIELDS = ["description", "status"]
RECOMMENDED_PROPERTY_FIELDS = ["property_type", "description"]
OPTIONAL_GOVERNANCE_FIELDS = ["owner"]
ACTION_VERBS = {
    "add",
    "begin",
    "cancel",
    "click",
    "complete",
    "create",
    "delete",
    "finish",
    "open",
    "purchase",
    "register",
    "request",
    "send",
    "signup",
    "start",
    "submit",
    "update",
    "view",
}
SYNONYM_GROUPS = [
    {"signup", "register"},
    {"complete", "finish", "completed", "finished"},
    {"view", "viewed", "open", "opened"},
    {"request", "requested", "submit", "submitted"},
]


def read_csv(path: Path, required: list[str]) -> tuple[list[dict[str, str]], list[str]]:
    if not path.exists():
        raise SystemExit(f"Input file not found: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        missing = [field for field in required if field not in fieldnames]
        if missing:
            raise SystemExit(f"{path} is missing required columns: {', '.join(missing)}")
        return [{k: (v or "").strip() for k, v in row.items()} for row in reader], fieldnames


def tokens(name: str) -> list[str]:
    return [t for t in re.split(r"[^a-z0-9]+", name.lower().strip()) if t]


def canonical_token(token: str) -> str:
    for group in SYNONYM_GROUPS:
        if token in group:
            return sorted(group)[0]
    return token


def normalize_name(name: str) -> str:
    ignored = {"ed"}
    return "_".join(canonical_token(t) for t in tokens(name) if t not in ignored)


def action_token(name: str) -> str:
    for token in tokens(name):
        canonical = canonical_token(token)
        if canonical in ACTION_VERBS:
            return canonical
    return ""


def pii_risk(property_name: str) -> tuple[bool, str]:
    lowered = property_name.lower().strip()
    if lowered in PII_ALLOWLIST:
        return False, "allowlisted semantic name"
    token_list = tokens(lowered)
    token_set = set(token_list)
    joined_bigrams = {f"{left}_{right}" for left, right in zip(token_list, token_list[1:])}
    matches = sorted((token_set | joined_bigrams) & PII_TOKENS)
    if matches:
        return True, f"matched high-confidence token(s): {', '.join(matches)}"
    return False, ""


def issue(issue_type: str, severity: str, subject: str, evidence: str, recommendation: str, confidence: str = "medium") -> dict[str, str]:
    return {
        "issue_type": issue_type,
        "severity": severity,
        "confidence": confidence,
        "subject": subject,
        "evidence": evidence,
        "recommendation": recommendation,
    }


def detect_capabilities(event_fields: list[str], property_fields: list[str], business_questions: bool) -> dict[str, bool]:
    return {
        "has_event_descriptions": "description" in event_fields,
        "has_property_descriptions": "description" in property_fields,
        "has_owner_field": "owner" in event_fields or "owner" in property_fields,
        "has_status_field": "status" in event_fields,
        "has_property_types": "property_type" in property_fields,
        "has_business_questions": business_questions,
    }


def find_issues(events: list[dict[str, str]], properties: list[dict[str, str]], capabilities: dict[str, bool]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []

    for row in events:
        name = row["event_name"]
        if capabilities["has_event_descriptions"] and not row.get("description"):
            issues.append(issue("missing_event_description", "medium", name, "description is blank", "Add a human-readable event definition.", "high"))
        if capabilities["has_owner_field"] and not row.get("owner"):
            issues.append(issue("missing_event_owner", "low", name, "owner is blank", "Assign a business or data owner if your governance model uses owners.", "medium"))
        if capabilities["has_status_field"] and row.get("status", "").lower() == "deprecated" and int(row.get("volume_30d") or 0) > 0:
            issues.append(issue("deprecated_event_still_active", "high", name, f"volume_30d={row.get('volume_30d')}", "Stop sending deprecated events or document migration window.", "high"))

    names = [row["event_name"] for row in events]
    for i, left in enumerate(names):
        for right in names[i + 1 :]:
            left_action = action_token(left)
            right_action = action_token(right)
            if left_action and right_action and left_action != right_action:
                continue
            left_tokens = sorted(canonical_token(t) for t in tokens(left))
            right_tokens = sorted(canonical_token(t) for t in tokens(right))
            same_tokens = left_tokens == right_tokens
            ratio = SequenceMatcher(None, normalize_name(left), normalize_name(right)).ratio()
            if same_tokens:
                issues.append(issue("likely_duplicate_event_names", "high", f"{left} <> {right}", "same normalized token set", "Choose one canonical event or document semantic differences.", "high"))
            elif ratio >= 0.86:
                issues.append(issue("likely_duplicate_event_names", "high", f"{left} <> {right}", f"similarity={ratio:.2f}", "Choose one canonical event or document semantic differences.", "high"))
            elif ratio >= 0.78 and left_action == right_action:
                issues.append(issue("possible_fragmented_event_naming", "medium", f"{left} <> {right}", f"similarity={ratio:.2f}", "Review whether these represent the same business action.", "medium"))

    property_types: dict[str, set[str]] = defaultdict(set)
    for row in properties:
        pname = row["property_name"]
        event_name = row["event_name"]
        ptype = row.get("property_type", "") or "unknown"
        property_types[pname].add(ptype)
        if pname.lower() in GENERIC_PROPERTIES:
            issues.append(issue("generic_property_name", "medium", f"{event_name}.{pname}", "property name is generic", "Rename to a more specific semantic name, e.g. acquisition_source.", "high"))
        is_pii, evidence = pii_risk(pname)
        if is_pii:
            issues.append(issue("pii_risk_candidate", "high", f"{event_name}.{pname}", evidence, "Review, redact, hash, or remove before AI analysis. This is a candidate, not a compliance finding.", "high"))
        if capabilities["has_property_descriptions"] and not row.get("description"):
            issues.append(issue("missing_property_description", "low", f"{event_name}.{pname}", "description is blank", "Add property definition and allowed values.", "high"))
        if capabilities["has_owner_field"] and not row.get("owner"):
            issues.append(issue("missing_property_owner", "low", f"{event_name}.{pname}", "owner is blank", "Assign owner for property semantics if your governance model uses owners.", "medium"))

    if capabilities["has_property_types"]:
        for pname, types in property_types.items():
            if len(types) > 1:
                issues.append(issue("inconsistent_property_type", "high", pname, f"types={', '.join(sorted(types))}", "Normalize type or split into distinct property names.", "high"))

    return issues


def write_issues(path: Path, issues: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["issue_type", "severity", "confidence", "subject", "evidence", "recommendation"])
        writer.writeheader()
        writer.writerows(issues)


def write_metadata(path: Path, capabilities: dict[str, bool], events: list[dict[str, str]], properties: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data: dict[str, Any] = {
        "scope": "Mixpanel Lexicon / event dictionary readiness; not raw event QA",
        "inputs": {
            "events": len(events),
            "properties": len(properties),
            "reserved_properties_excluded": "unknown",
        },
        "capabilities": capabilities,
        "skipped_checks": [],
    }
    if not capabilities["has_owner_field"]:
        data["skipped_checks"].append("owner_governance: owner column not present")
    if not capabilities["has_business_questions"]:
        data["skipped_checks"].append("answerability: business questions not provided")
    if not capabilities["has_property_types"]:
        data["skipped_checks"].append("property_type_consistency: property_type column not present")
    import json

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate event taxonomy CSV exports.")
    parser.add_argument("--events", required=True, help="Path to event inventory CSV")
    parser.add_argument("--properties", required=True, help="Path to property dictionary CSV")
    parser.add_argument("--out", default="outputs/issues.csv", help="Output issue CSV path")
    parser.add_argument("--metadata-out", default="outputs/validation_metadata.json", help="Output validation metadata JSON path")
    parser.add_argument("--questions", required=False, help="Optional business questions Markdown path")
    args = parser.parse_args()

    events, event_fields = read_csv(Path(args.events), BASE_EVENT_FIELDS)
    properties, property_fields = read_csv(Path(args.properties), BASE_PROPERTY_FIELDS)
    has_questions = bool(args.questions and Path(args.questions).exists() and Path(args.questions).read_text(encoding="utf-8").strip())
    capabilities = detect_capabilities(event_fields, property_fields, has_questions)
    issues = find_issues(events, properties, capabilities)
    write_issues(Path(args.out), issues)
    write_metadata(Path(args.metadata_out), capabilities, events, properties)
    high = sum(1 for i in issues if i["severity"] == "high")
    medium = sum(1 for i in issues if i["severity"] == "medium")
    low = sum(1 for i in issues if i["severity"] == "low")
    print(f"Wrote {len(issues)} issues to {args.out} (high={high}, medium={medium}, low={low})")
    print(f"Wrote validation metadata to {args.metadata_out}")


if __name__ == "__main__":
    main()
