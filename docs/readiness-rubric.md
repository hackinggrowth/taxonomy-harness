# Readiness Rubric

Scores are directional. Use them to prioritize a cleanup conversation, not as an absolute benchmark.

## Coverage

Do key events and properties have descriptions and enough funnel coverage?

Missing descriptions reduce coverage. If an export does not include description columns, those checks are skipped instead of treated as hard failures.

## Clarity

Are event and property names specific enough for an AI analyst to interpret without tribal knowledge?

Generic property names, ambiguous event names, and fragmented naming reduce clarity. Similar-event checks are intentionally conservative to avoid grouping semantically different actions such as `email_open` and `email_send`.

## Consistency

Are names, property types, and funnel semantics used consistently?

Type consistency is evaluated only when property type columns exist.

## Governance

Are owners, status, and migration decisions documented?

Owner fields are useful but optional. Missing owner columns should not collapse the total score; if owner columns are present, owner gaps are treated as low-severity governance warnings.

## Skipped checks

Some checks may be reported as skipped:

- Owner governance when owner fields are absent.
- Business-question answerability when no business questions are provided.
- Property type consistency when no property type field is present.

Skipped checks are not scored as failures.
