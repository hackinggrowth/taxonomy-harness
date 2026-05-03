---
name: taxonomy-harness
description: Diagnose product analytics event taxonomies and generate AI-readiness artifacts before Claude or an AI analyst reads Mixpanel-style data.
---

# Taxonomy Harness Skill

Use this skill when a user wants to evaluate whether product analytics data is ready for AI analysis, especially Mixpanel event exports, tracking plans, or event/property dictionaries.

## Triggers

- “Can Claude analyze our Mixpanel data?”
- “Check our event taxonomy.”
- “Prepare data for Mixpanel MCP / AI analyst.”
- “Find duplicate or confusing event names.”
- “Create an AI-readable data contract.”

## Required inputs

Ask for or locate:

1. Event inventory CSV with `event_name`, `description`, `owner`, `status`.
2. Property dictionary CSV with `event_name`, `property_name`, `property_type`, `description`, `owner`.
3. Business questions or funnel context.
4. Optional tracking plan or previous naming convention.

If live Mixpanel MCP is available, use read-only access only after explicit human approval. Prefer exports for MVP use.

## Safety rules

- Never request or store API tokens in project files.
- Do not analyze direct identifiers unless they are redacted or explicitly approved.
- Flag PII-risk properties before using AI interpretation.
- Do not mutate Mixpanel, tracking plans, warehouses, or production schemas.
- Separate **observed**, **inferred**, and **unknown**.
- Treat canonical taxonomy suggestions as drafts requiring human owner approval.

## Workflow

1. **Ingest**: inspect supplied CSV/Markdown inputs.
2. **Detect**: run deterministic checks first: missing definitions, duplicate-ish events, generic properties, missing owners, PII-risk fields, inconsistent property types.
3. **Normalize**: propose canonical event map and property dictionary changes.
4. **Validate**: test whether business questions can be answered unambiguously from the taxonomy.
5. **Package**: create readiness report, issue log, decision log, and workshop agenda.

## Output artifacts

- `ai_readiness_report.md`
- `taxonomy_issue_log.csv`
- `event_inventory.csv`
- `property_dictionary.csv`
- `decision_log.md`
- optional `mixpanel_mcp_prompt_pack.md`

## Quality bar

A good answer should tell the user:

- Which issues are directly observed in the data.
- Which recommendations are inferred.
- Which decisions require a human owner.
- Which events/properties are unsafe for AI analysis without redaction.
- What to fix before connecting Claude/Mixpanel MCP.
