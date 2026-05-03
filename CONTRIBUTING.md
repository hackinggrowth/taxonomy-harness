# Contributing

Thanks for improving Taxonomy Harness.

## Principles

1. Keep examples synthetic and privacy-safe.
2. Prefer deterministic checks before AI-generated judgment.
3. Do not add API keys, private exports, customer names, or workspace-specific paths.
4. Keep scripts runnable with Python standard library when possible.
5. Separate observed issues from inferred recommendations.

## Development

Run the demo before opening a PR:

```bash
bash scripts/demo_run.sh
```

If you add a new check, include a small synthetic example and explain the signal in `docs/readiness-rubric.md`.
