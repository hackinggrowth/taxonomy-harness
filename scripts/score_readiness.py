#!/usr/bin/env python3
"""Score AI analytics readiness from taxonomy inputs and issue logs."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"Input file not found: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(f)]


def read_optional_json(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    json_path = Path(path)
    if not json_path.exists():
        return {}
    return json.loads(json_path.read_text(encoding="utf-8"))


def clamp(value: int | float) -> int:
    return max(0, min(100, round(value)))


def weighted_average(dimensions: dict[str, int], weights: dict[str, int]) -> int:
    total_weight = sum(weights.values()) or 1
    return clamp(sum(dimensions[key] * weights[key] for key in dimensions) / total_weight)


def score(events: list[dict[str, str]], properties: list[dict[str, str]], issues: list[dict[str, str]], metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    metadata = metadata or {}
    capabilities = metadata.get("capabilities", {})
    counts = Counter(i.get("issue_type", "unknown") for i in issues)
    severity = Counter(i.get("severity", "unknown") for i in issues)
    total_events = max(1, len(events))
    total_properties = max(1, len(properties))

    has_event_descriptions = capabilities.get("has_event_descriptions", any("description" in e for e in events))
    has_property_descriptions = capabilities.get("has_property_descriptions", any("description" in p for p in properties))
    has_owner_field = capabilities.get("has_owner_field", any("owner" in e for e in events) or any("owner" in p for p in properties))
    has_property_types = capabilities.get("has_property_types", any("property_type" in p for p in properties))
    has_business_questions = capabilities.get("has_business_questions", False)

    event_desc_ratio = sum(1 for e in events if e.get("description")) / total_events if has_event_descriptions else 1
    property_desc_ratio = sum(1 for p in properties if p.get("description")) / total_properties if has_property_descriptions else 1
    event_owner_ratio = sum(1 for e in events if e.get("owner")) / total_events if has_owner_field else 1

    duplicate_count = counts["likely_duplicate_event_names"] + counts["possible_fragmented_event_naming"]

    coverage = clamp(100 * ((event_desc_ratio + property_desc_ratio) / 2) - severity["high"] * 2)
    clarity = clamp(
        100
        - counts["generic_property_name"] * 6
        - counts["likely_duplicate_event_names"] * 10
        - counts["possible_fragmented_event_naming"] * 5
        - counts["missing_event_description"] * 5
    )
    consistency = clamp(100 - counts["inconsistent_property_type"] * 20 - duplicate_count * 8) if has_property_types else 100
    governance = clamp(100 * event_owner_ratio - counts["missing_event_owner"] * 2 - counts["missing_property_owner"] * 1 - counts["deprecated_event_still_active"] * 15)

    dimensions = {
        "coverage": coverage,
        "clarity": clarity,
        "consistency": consistency,
        "governance": governance,
    }
    weights = {"coverage": 30, "clarity": 30, "consistency": 25, "governance": 15}
    overall = weighted_average(dimensions, weights)

    level = "ready"
    if overall < 50:
        level = "not_ready"
    elif overall < 75:
        level = "needs_cleanup"

    skipped_checks = list(metadata.get("skipped_checks", []))
    if not has_business_questions and "answerability: business questions not provided" not in skipped_checks:
        skipped_checks.append("answerability: business questions not provided")
    if not has_owner_field and "owner_governance: owner column not present" not in skipped_checks:
        skipped_checks.append("owner_governance: owner column not present")

    return {
        "overall_score": overall,
        "readiness_level": level,
        "dimensions": dimensions,
        "weights": weights,
        "issue_counts": dict(counts),
        "severity_counts": dict(severity),
        "inputs": {"events": len(events), "properties": len(properties), "issues": len(issues)},
        "capabilities": capabilities,
        "skipped_checks": skipped_checks,
        "scope": metadata.get("scope", "Mixpanel Lexicon / event dictionary readiness; not raw event QA"),
        "notes": [
            "Scores are directional and meant to prioritize cleanup decisions, not rank teams.",
            "Missing optional schema fields are skipped or lightly weighted rather than treated as hard failures.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Score taxonomy readiness for AI analytics.")
    parser.add_argument("--events", required=True, help="Path to event inventory CSV")
    parser.add_argument("--properties", required=True, help="Path to property dictionary CSV")
    parser.add_argument("--issues", required=True, help="Path to issue CSV generated by validate_taxonomy.py")
    parser.add_argument("--metadata", required=False, help="Optional validation metadata JSON generated by validate_taxonomy.py")
    parser.add_argument("--out", default="outputs/readiness_score.json", help="Output JSON path")
    args = parser.parse_args()

    result = score(read_csv(Path(args.events)), read_csv(Path(args.properties)), read_csv(Path(args.issues)), read_optional_json(args.metadata))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote readiness score {result['overall_score']} ({result['readiness_level']}) to {out}")


if __name__ == "__main__":
    main()
