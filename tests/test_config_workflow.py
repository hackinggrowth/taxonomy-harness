#!/usr/bin/env python3
"""Regression checks for config-driven closed-loop workflow metadata."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tests" / "outputs"
OUT.mkdir(parents=True, exist_ok=True)
metadata_path = OUT / "workflow_metadata.json"
issues_path = OUT / "workflow_issues.csv"
score_path = OUT / "workflow_score.json"
report_path = OUT / "workflow_report.md"

subprocess.run(
    [
        "python3",
        "scripts/validate_taxonomy.py",
        "--input",
        "examples/events.csv",
        "--properties",
        "examples/properties.csv",
        "--questions",
        "examples/business_questions.md",
        "--out",
        str(issues_path),
        "--metadata-out",
        str(metadata_path),
    ],
    cwd=ROOT,
    check=True,
)
metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
assert metadata["config"]["loaded"] is True
assert metadata["score_weights"]["coverage"] == 30
assert [step["stage"] for step in metadata["closed_loop_workflow"]] == ["ingest", "classify", "review", "measure", "iterate"]

subprocess.run(
    [
        "python3",
        "scripts/score_readiness.py",
        "--input",
        str(metadata_path),
        "--issues",
        str(issues_path),
        "--out",
        str(score_path),
    ],
    cwd=ROOT,
    check=True,
)
score = json.loads(score_path.read_text(encoding="utf-8"))
assert score["weights"]["coverage"] == 30
assert score["iteration_metrics"]["ready_score_threshold_met"] in {True, False}

subprocess.run(
    [
        "python3",
        "scripts/generate_report.py",
        "--input",
        str(metadata_path),
        "--score",
        str(score_path),
        "--issues",
        str(issues_path),
        "--questions",
        "examples/business_questions.md",
        "--output",
        str(report_path),
    ],
    cwd=ROOT,
    check=True,
)
report = report_path.read_text(encoding="utf-8")
assert "ingest → classify → review → measure → iterate" in report
assert "Success Metrics For This Iteration" in report
print("workflow regression checks passed")
