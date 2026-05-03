#!/usr/bin/env python3
"""Generate a Markdown AI readiness report from score and issue artifacts."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def read_issues(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"Issue file not found: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate AI analytics readiness Markdown report.")
    parser.add_argument("--score", required=True, help="Readiness score JSON")
    parser.add_argument("--issues", required=True, help="Issue CSV")
    parser.add_argument("--questions", required=False, help="Business questions Markdown")
    parser.add_argument("--out", default="outputs/ai_readiness_report.md", help="Output report Markdown path")
    args = parser.parse_args()

    score_path = Path(args.score)
    if not score_path.exists():
        raise SystemExit(f"Score file not found: {score_path}")
    score = json.loads(score_path.read_text(encoding="utf-8"))
    issues = read_issues(Path(args.issues))
    by_severity = Counter(i.get("severity", "unknown") for i in issues)
    questions = Path(args.questions).read_text(encoding="utf-8") if args.questions and Path(args.questions).exists() else "_No business questions provided._\n"

    top = issues[:10]
    rows = "\n".join(f"| {i['severity']} | {i['issue_type']} | {i['subject']} | {i['recommendation']} |" for i in top)
    dims = score["dimensions"]

    report = f"""# AI Analytics Readiness Report

## Summary

- Overall score: **{score['overall_score']} / 100**
- Readiness level: **{score['readiness_level']}**
- Inputs: {score['inputs']['events']} events, {score['inputs']['properties']} properties, {score['inputs']['issues']} issues
- Severity counts: high={by_severity['high']}, medium={by_severity['medium']}, low={by_severity['low']}

## Dimension Scores

| Dimension | Score |
|---|---:|
| Coverage | {dims['coverage']} |
| Clarity | {dims['clarity']} |
| Consistency | {dims['consistency']} |
| Governance | {dims['governance']} |

## Top Issues

| Severity | Type | Subject | Recommendation |
|---|---|---|---|
{rows if rows else '| - | - | No issues found | - |'}

## Business Questions Used For Validation

{questions}

## Interpretation Discipline

- **Observed:** issue rows and score inputs generated from supplied CSV files.
- **Inferred:** recommendations about canonical events and migration priority.
- **Unknown:** actual customer intent, historical migration constraints, and downstream warehouse usage unless provided by humans.

## Recommended Next Step

Run a 90-minute decision session to choose canonical funnel events, assign owners, and mark deprecated events for migration.
"""
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"Wrote report to {out}")


if __name__ == "__main__":
    main()
