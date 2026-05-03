# Taxonomy Harness

> Before Claude reads your Mixpanel data, make sure your event taxonomy is a language Claude can understand.

Taxonomy Harness is an open-source starter kit for making product analytics data **AI-readable**. It helps product, growth, and data teams diagnose messy event taxonomies, produce a lightweight data contract, and prepare for AI analyst workflows with Claude, Mixpanel MCP, or exported analytics data.

## Why this exists

AI analysts can query tools like Mixpanel, Amplitude, or warehouse exports, but they can also confidently answer from broken assumptions when event semantics are unclear.

Common failure modes:

- `signup`, `register`, and `complete_signup` all mean roughly the same thing.
- Properties like `type`, `source`, and `status` have different meanings across events.
- Funnel stages are implicit in someone’s head, not written in a data contract.
- Deprecated events remain active.
- Owners, descriptions, and property dictionaries are missing.

This repo provides a practical harness for detecting those issues and turning them into workshop-ready decisions.

## What is included

- **Claude Skill**: repeatable instructions for taxonomy diagnosis and report generation.
- **Deterministic scripts**: CSV checks and readiness scoring using Python standard library only.
- **Templates**: event inventory, property dictionary, readiness report, decision log, workshop agenda.
- **Synthetic examples**: safe sample Mixpanel-like exports.
- **Workshop package**: prework checklist, facilitation guide, package options, demo script.
- **Docs**: architecture, privacy model, Mixpanel MCP guidance, rubric, roadmap.

## Quick start

```bash
git clone https://github.com/hackinggrowth/taxonomy-harness.git
cd taxonomy-harness
bash scripts/demo_run.sh
```

Run checks manually:

```bash
python3 scripts/validate_taxonomy.py --events examples/events.csv --properties examples/properties.csv --out outputs/issues.csv
python3 scripts/score_readiness.py --events examples/events.csv --properties examples/properties.csv --issues outputs/issues.csv --out outputs/readiness_score.json
python3 scripts/generate_report.py --score outputs/readiness_score.json --issues outputs/issues.csv --questions examples/business_questions.md --out outputs/ai_readiness_report.md
```

## Repository structure

```text
skill/       Claude Skill instructions and templates
scripts/     deterministic validation, scoring, and report generation
examples/    synthetic sample inputs
docs/        architecture, safety, MCP, rubric, roadmap
workshop/    paid workshop packaging and facilitation assets
outputs/     generated demo artifacts, gitignored except .gitkeep
```

## Safety model

The MVP is **export-first**. It does not connect to Mixpanel or mutate tracking plans. Live MCP usage is treated as an advanced, read-only validation layer.

Recommended defaults:

- Use synthetic or approved exports only.
- Redact PII before analysis.
- Keep API tokens outside this repo.
- Treat AI suggestions as drafts requiring human approval.
- Separate observed facts from inferred recommendations.

## Non-goals

This repo intentionally does **not** provide:

- A web app or SaaS dashboard.
- Automatic taxonomy rewrite or mutation.
- A universal “correct taxonomy” generator.
- Live write access to analytics tools.
- Customer-specific private examples.

## License

MIT. See [LICENSE](LICENSE).
