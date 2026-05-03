# Council Synthesis — Taxonomy Harness

- **Date:** 2026-05-03
- **Telegram topic:** 🧬 Taxonomy Harness / AI 분석 준비도
- **Topic ID:** 3624
- **Status:** Initial council synthesis complete

## 1. Council Status

Three council tracks were requested:

1. **Strategic council** — failed due model usage limit before producing content.
2. **Implementation/Productization council** — completed.
3. **Market/GTM council** — completed.

This synthesis uses the two completed council opinions plus the initial project review. Strategic council can be rerun later with a different model if needed.

## 2. Overall Verdict

**Go — but start as a paid readiness workshop backed by a reusable harness, not as SaaS.**

The wedge is strong because the market is moving from “AI can query analytics tools” to “AI needs trustworthy event semantics.” The product should not be sold as generic taxonomy cleanup. It should be positioned as:

> **AI Analyst 도입 전 데이터 신뢰성 점검 + AI-readable event contract 구축**

The strongest first offer is:

> **Mixpanel AI Analyst Readiness Workshop**

## 3. Core Positioning

### Strong language

- “Claude가 Mixpanel을 보기 전에, Claude가 오해하지 않을 이벤트 계약을 먼저 만듭니다.”
- “AI 분석 파트너가 믿고 읽을 수 있는 제품 데이터 언어를 만듭니다.”
- “AI Analyst 도입 전 데이터 신뢰성 점검.”
- “대시보드가 아니라, AI가 분석할 수 있는 data contract.”

### Avoid

- “taxonomy 개선 워크샵” — 중요하지만 안 급해 보임.
- “데이터 거버넌스” — 스타트업 buyer에게 무겁고 느림.
- “AI-readiness score” 단독 — 장식처럼 보일 수 있음.

## 4. Recommended First Product

### Package to sell first

**Workshop Package / 500만 원 anchor**

Includes:

- Mixpanel event/property export 기반 스캔
- duplicate / ambiguity / owner 누락 / naming 문제 진단
- 2–3시간 워크샵
- canonical event map v1
- AI analyst 질문 20개 validation
- migration action plan
- AI-readiness score

First 1–2 customers can be discounted to 200–300만 원 as pilot cases.

### Alternative packages

| Package | Price idea | Scope |
|---|---:|---|
| Starter Audit | 200만 원 | export scan + risk report + score |
| Workshop Package | 500만 원 | audit + workshop + canonical map + validation |
| Readiness Sprint | 1000만 원+ | 1–2 week deeper funnel redesign + tracking plan + owner log |

## 5. MVP Scope

### Include

- Mixpanel only
- export-first ingestion, MCP as optional live demo/QA
- event/property scan
- duplicate and ambiguity detection
- one core funnel canonical map
- event/property dictionary
- AI analyst question set, about 20 questions
- before/after answer consistency check
- score rubric
- markdown/csv artifacts
- public sample report using demo dataset

### Exclude

- SaaS dashboard
- automatic migration
- Amplitude/GA4 simultaneous support
- full AI analyst product
- real-time monitoring
- all funnels redesign
- warehouse integrations

## 6. Harness Architecture

Use a fixed 5-stage pipeline:

1. **Ingest**
   - `events.csv`
   - `properties.csv`
   - event usage frequency if available

2. **Detect**
   - duplicate events
   - ambiguous properties
   - naming convention violations
   - missing owner/description
   - funnel ambiguity

3. **Normalize**
   - `canonical-map.csv`
   - `property-dictionary.csv`
   - `taxonomy-contract.md`

4. **Validate**
   - `ai-questions.md`
   - before/after consistency test
   - unsupported inference flags

5. **Package**
   - `validation-report.md`
   - `migration-plan.md`
   - `decision-log.md`

## 7. Score Rubric

Avoid vague maturity scores. Use explainable diagnostic scoring.

Minimum dimensions:

1. **Coverage** — core funnel/event definition coverage
2. **Clarity** — ambiguous event/property ratio
3. **Consistency** — answer stability across paraphrased questions
4. **Governance** — owner/description/deprecated state

Output format example:

```text
AI-readable score: 62/100
Risk level: Medium
Top score losses:
- signup/register duplicate semantics
- source property overloaded across channels/campaigns
- onboarding conversion definition missing owner
```

## 8. Workshop Operating Model

The workshop should not start from raw data live. It should be **70% pre-processing, 30% live decision session**.

### Pre-work

- collect export/schema
- collect top 5 business questions
- run scan
- prepare duplicate/ambiguity report

### 2–3 hour session

1. scan result walkthrough
2. core funnel/event decision
3. canonical naming agreement
4. AI question validation simulation
5. owner + migration priority assignment

### After session

- final report
- migration/action plan
- optional 2-week follow-up

## 9. Customer Trigger

Customers pay when they are about to trust AI with analytics and fear confident wrong answers.

Best trigger moments:

- “We want Claude/ChatGPT to analyze Mixpanel.”
- “Our tracking plan is old.”
- “Different teams interpret conversion differently.”
- “Founder/PM does not trust dashboard numbers.”
- “Data team keeps explaining event caveats manually.”

## 10. Risks

| Risk | Mitigation |
|---|---|
| Important but not urgent | Sell as AI analyst risk/readiness, not cleanup |
| Looks like consulting | Use harness artifacts, score, repeatable files |
| Score feels subjective | Base score on consistency tests and explicit checks |
| Migration blocked by org politics | Include owner/decision-log and next sprint actions |
| Too narrow with Mixpanel | Treat Mixpanel as initial wedge, not final TAM |

## 11. Next Moves

1. Build a **1-page workshop offer**.
2. Create a **sample public report** using demo product data.
3. Define **20 AI analyst validation questions**.
4. Draft the first score rubric.
5. Identify 5 warm leads using Mixpanel/Amplitude.
6. Optional: rerun strategic council with a non-rate-limited model.

## 12. Result Card

- **Pattern surfaced:** AI analytics adoption creates a new upstream need: event semantics and taxonomy must become machine-readable contracts.
- **Unknown unknown:** Which customer trigger is strongest — AI analyst adoption, dashboard distrust, or old tracking-plan cleanup?
- **Next move:** Make this sellable as a 1-page `Mixpanel AI Analyst Readiness Workshop` offer plus sample report.
