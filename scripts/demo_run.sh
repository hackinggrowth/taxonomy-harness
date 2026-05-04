#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p outputs
python3 scripts/validate_taxonomy.py --events examples/events.csv --properties examples/properties.csv --questions examples/business_questions.md --out outputs/issues.csv --metadata-out outputs/validation_metadata.json
python3 scripts/score_readiness.py --events examples/events.csv --properties examples/properties.csv --issues outputs/issues.csv --metadata outputs/validation_metadata.json --out outputs/readiness_score.json
python3 scripts/generate_report.py --score outputs/readiness_score.json --issues outputs/issues.csv --questions examples/business_questions.md --out outputs/ai_readiness_report.md
echo "Demo complete. See outputs/"
