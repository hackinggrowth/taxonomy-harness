#!/usr/bin/env python3
"""Regression checks from first real Mixpanel Lexicon feedback."""
from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tests" / "outputs"
OUT.mkdir(parents=True, exist_ok=True)
issues_path = OUT / "feedback_issues.csv"
metadata_path = OUT / "feedback_metadata.json"
score_path = OUT / "feedback_score.json"

subprocess.run(
    [
        "python3",
        "scripts/validate_taxonomy.py",
        "--events",
        "tests/fixtures/feedback_events_no_owner.csv",
        "--properties",
        "tests/fixtures/feedback_properties_no_owner.csv",
        "--out",
        str(issues_path),
        "--metadata-out",
        str(metadata_path),
    ],
    cwd=ROOT,
    check=True,
)
subprocess.run(
    [
        "python3",
        "scripts/score_readiness.py",
        "--events",
        "tests/fixtures/feedback_events_no_owner.csv",
        "--properties",
        "tests/fixtures/feedback_properties_no_owner.csv",
        "--issues",
        str(issues_path),
        "--metadata",
        str(metadata_path),
        "--out",
        str(score_path),
    ],
    cwd=ROOT,
    check=True,
)

with issues_path.open(newline="", encoding="utf-8") as f:
    issues = list(csv.DictReader(f))
subjects = {row["subject"] for row in issues}
issue_types = {row["issue_type"] for row in issues}

assert "request_demo.request_email" in subjects
assert "email_open.email" in subjects
assert "request_demo.button_name" not in subjects
assert "demo_request.page_name" not in subjects
assert "email_send.section_name" not in subjects
assert not any("email_open <> email_send" in subject for subject in subjects)
assert any("request_demo <> demo_request" in subject or "demo_request <> request_demo" in subject for subject in subjects)
assert "missing_event_owner" not in issue_types
assert "missing_property_owner" not in issue_types

score = json.loads(score_path.read_text(encoding="utf-8"))
assert score["overall_score"] > 0
assert "owner_governance: owner column not present" in score["skipped_checks"]
assert "answerability: business questions not provided" in score["skipped_checks"]
assert [step["stage"] for step in score["closed_loop_workflow"]] == ["ingest", "classify", "review", "measure", "iterate"]
assert score["success_metrics"]["minimum_ready_score"] == 75
assert "high_confidence_high_issues" in score["iteration_metrics"]
print("feedback regression checks passed")
