#!/usr/bin/env python3
"""Validate event taxonomy CSV exports with deterministic checks."""
from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

GENERIC_PROPERTIES = {"type", "source", "status", "category", "name", "value", "id"}
PII_PATTERNS = ["email", "phone", "name", "address", "birthday", "birth", "ssn", "ip"]
REQUIRED_EVENT_FIELDS = ["event_name", "description", "owner", "status"]
REQUIRED_PROPERTY_FIELDS = ["event_name", "property_name", "property_type", "description", "owner"]


def read_csv(path: Path, required: list[str]) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"Input file not found: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [field for field in required if field not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit(f"{path} is missing required columns: {', '.join(missing)}")
        return [{k: (v or "").strip() for k, v in row.items()} for row in reader]


def normalize_name(name: str) -> str:
    name = name.lower().strip()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    tokens = [t for t in name.split("_") if t and t not in {"ed", "complete", "completed"}]
    return "_".join(tokens)


def issue(issue_type: str, severity: str, subject: str, evidence: str, recommendation: str) -> dict[str, str]:
    return {
        "issue_type": issue_type,
        "severity": severity,
        "subject": subject,
        "evidence": evidence,
        "recommendation": recommendation,
    }


def find_issues(events: list[dict[str, str]], properties: list[dict[str, str]]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []

    for row in events:
        name = row["event_name"]
        if not row.get("description"):
            issues.append(issue("missing_event_description", "medium", name, "description is blank", "Add a human-readable event definition."))
        if not row.get("owner"):
            issues.append(issue("missing_event_owner", "medium", name, "owner is blank", "Assign a business or data owner."))
        if row.get("status", "").lower() == "deprecated" and int(row.get("volume_30d") or 0) > 0:
            issues.append(issue("deprecated_event_still_active", "high", name, f"volume_30d={row.get('volume_30d')}", "Stop sending deprecated events or document migration window."))

    names = [row["event_name"] for row in events]
    for i, left in enumerate(names):
        for right in names[i + 1 :]:
            ratio = SequenceMatcher(None, normalize_name(left), normalize_name(right)).ratio()
            if ratio >= 0.72:
                issues.append(issue("duplicate_like_event_names", "high", f"{left} <> {right}", f"similarity={ratio:.2f}", "Choose one canonical event or document semantic differences."))

    property_types: dict[str, set[str]] = defaultdict(set)
    for row in properties:
        pname = row["property_name"]
        event_name = row["event_name"]
        ptype = row.get("property_type", "") or "unknown"
        property_types[pname].add(ptype)
        if pname.lower() in GENERIC_PROPERTIES:
            issues.append(issue("generic_property_name", "medium", f"{event_name}.{pname}", "property name is generic", "Rename to a more specific semantic name, e.g. acquisition_source."))
        if any(pattern in pname.lower() for pattern in PII_PATTERNS):
            issues.append(issue("pii_risk_property", "high", f"{event_name}.{pname}", "property name suggests direct identifier or PII", "Redact, hash, or remove before AI analysis."))
        if not row.get("description"):
            issues.append(issue("missing_property_description", "low", f"{event_name}.{pname}", "description is blank", "Add property definition and allowed values."))
        if not row.get("owner"):
            issues.append(issue("missing_property_owner", "low", f"{event_name}.{pname}", "owner is blank", "Assign owner for property semantics."))

    for pname, types in property_types.items():
        if len(types) > 1:
            issues.append(issue("inconsistent_property_type", "high", pname, f"types={', '.join(sorted(types))}", "Normalize type or split into distinct property names."))

    return issues


def write_issues(path: Path, issues: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["issue_type", "severity", "subject", "evidence", "recommendation"])
        writer.writeheader()
        writer.writerows(issues)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate event taxonomy CSV exports.")
    parser.add_argument("--events", required=True, help="Path to event inventory CSV")
    parser.add_argument("--properties", required=True, help="Path to property dictionary CSV")
    parser.add_argument("--out", default="outputs/issues.csv", help="Output issue CSV path")
    args = parser.parse_args()

    events = read_csv(Path(args.events), REQUIRED_EVENT_FIELDS)
    properties = read_csv(Path(args.properties), REQUIRED_PROPERTY_FIELDS)
    issues = find_issues(events, properties)
    write_issues(Path(args.out), issues)
    high = sum(1 for i in issues if i["severity"] == "high")
    medium = sum(1 for i in issues if i["severity"] == "medium")
    low = sum(1 for i in issues if i["severity"] == "low")
    print(f"Wrote {len(issues)} issues to {args.out} (high={high}, medium={medium}, low={low})")


if __name__ == "__main__":
    main()
