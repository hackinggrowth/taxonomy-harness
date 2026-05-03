# Mixpanel MCP Guidance

Mixpanel MCP can be useful for schema inspection and before/after demos, but it should not be the MVP dependency.

## Phase 1

Use CSV exports and deterministic checks.

## Phase 2

Use read-only MCP for schema validation and approved prompt packs.

## Guardrails

- Read-only token.
- Pre-approved query templates.
- PII redaction.
- No mutation.
- Human approval before sharing generated reports externally.
