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
    parser.add_argument("--input", dest="metadata_alias", help="Optional validation metadata for provenance; score/issues still come from generated artifacts")
    parser.add_argument("--score", default="outputs/readiness_score.json", help="Readiness score JSON")
    parser.add_argument("--issues", default="outputs/issues.csv", help="Issue CSV")
    parser.add_argument("--questions", required=False, help="Business questions Markdown")
    parser.add_argument("--out", "--output", dest="out", default="outputs/ai_readiness_report.md", help="Output report Markdown path")
    args = parser.parse_args()

    metadata_path = Path(args.metadata_alias) if args.metadata_alias else None
    if metadata_path and not metadata_path.exists():
        raise SystemExit(f"Validation metadata file not found: {metadata_path}")

    score_path = Path(args.score)
    if not score_path.exists():
        raise SystemExit(f"Score file not found: {score_path}")
    score = json.loads(score_path.read_text(encoding="utf-8"))
    issues = read_issues(Path(args.issues))
    by_severity = Counter(i.get("severity", "unknown") for i in issues)
    questions_provided = bool(args.questions and Path(args.questions).exists() and Path(args.questions).read_text(encoding="utf-8").strip())
    questions = Path(args.questions).read_text(encoding="utf-8") if questions_provided else "_No business questions provided. Answerability check was skipped and not scored._\n"

    reliable = [i for i in issues if i.get("confidence") == "high"][:10]
    top = reliable or issues[:10]
    rows = "\n".join(
        f"| {i.get('severity', '')} | {i.get('confidence', '')} | {i['issue_type']} | {i['subject']} | {i['recommendation']} |"
        for i in top
    )
    dims = score["dimensions"]
    skipped = score.get("skipped_checks", [])
    workflow = score.get("closed_loop_workflow", [])
    workflow_rows = "\n".join(
        f"| {step.get('stage', '')} | {step.get('artifact', '')} | {step.get('decision', '')} |"
        for step in workflow
    )
    iteration = score.get("iteration_metrics", {})
    success = score.get("success_metrics", {})
    skipped_rows = "\n".join(f"- {item}" for item in skipped) if skipped else "- None"
    provenance = f"- Validation metadata: `{metadata_path}`" if metadata_path else "- Validation metadata: not provided"

    report = f"""# AI Analytics Readiness Report

## Scope Boundary

This report checks **Mixpanel Lexicon / event dictionary readiness** for AI-assisted analytics. It does **not** validate raw event delivery, duplicate firing, null rates, timestamp quality, identity stitching, or production volume anomalies.

## Closed-Loop Workflow

Taxonomy Harness is meant to be run as a closed loop: **ingest → classify → review → measure → iterate**. The scripts produce the observed issue log and score; humans approve taxonomy decisions before the next export is measured again.

| Stage | Artifact | Human decision |
|---|---|---|
{workflow_rows if workflow_rows else '| ingest | CSV exports | Confirm scope |'}

## Summary

{provenance}
- Overall score: **{score['overall_score']} / 100**
- Readiness level: **{score['readiness_level']}**
- Inputs: {score['inputs']['events']} events, {score['inputs']['properties']} custom properties, {score['inputs']['issues']} issues
- Severity counts: high={by_severity['high']}, medium={by_severity['medium']}, low={by_severity['low']}

## Success Metrics For This Iteration

- Ready threshold met: **{iteration.get('ready_score_threshold_met', False)}** (target score ≥ {success.get('minimum_ready_score', 75)})
- High-confidence high issues: **{iteration.get('high_confidence_high_issues', 0)}** (target ≤ {success.get('target_high_confidence_high_issues', 0)})
- Missing required descriptions: **{iteration.get('missing_required_descriptions', 0)}** (target ≤ {success.get('target_missing_required_descriptions', 0)})

## Dimension Scores

| Dimension | Score |
|---|---:|
| Coverage | {dims['coverage']} |
| Clarity | {dims['clarity']} |
| Consistency | {dims['consistency']} |
| Governance | {dims['governance']} |

Scores are directional. Use them to prioritize a cleanup conversation, not as an absolute benchmark.

## Top Reliable Findings

| Severity | Confidence | Type | Subject | Recommendation |
|---|---|---|---|---|
{rows if rows else '| - | - | - | No issues found | - |'}

## Skipped Checks

{skipped_rows}

## Business Questions Used For Validation

{questions}

## Interpreting PII Findings

PII findings are **PII-risk candidates**, not legal or compliance determinations. Review them with your data/privacy owner before using exports in AI workflows.

## Interpretation Discipline

- **Observed:** issue rows and score inputs generated from supplied CSV files.
- **Inferred:** recommendations about canonical events and migration priority.
- **Unknown:** actual customer intent, historical migration constraints, and downstream warehouse usage unless provided by humans.

## Recommended Next Step

Review the top findings, approve a small cleanup batch in Mixpanel Lexicon, export the taxonomy again, and re-run the harness to measure movement.
"""
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"Wrote report to {out}")


if __name__ == "__main__":
    main()
