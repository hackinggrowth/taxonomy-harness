# Architecture

Taxonomy Harness has three layers:

1. **Deterministic harness**: CSV validation, issue log, readiness scoring.
2. **Claude Skill layer**: interpretation workflow, artifact generation, workshop preparation.
3. **Workshop layer**: human decision process for canonical taxonomy and migration planning.

The MVP is export-first. Mixpanel MCP is an optional read-only validation interface, not the core engine.
