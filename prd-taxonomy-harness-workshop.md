# PRD — Taxonomy Harness & AI Analytics Readiness Workshop

- **Project:** Taxonomy Harness / AI Analytics Readiness
- **Owner:** MarketFitLab / Paul Jung
- **Draft date:** 2026-05-03
- **Status:** PRD draft v0.1
- **Primary wedge:** Mixpanel AI Analyst Readiness

---

## 1. Executive Summary

Taxonomy Harness는 Mixpanel 같은 제품 분석 데이터를 Claude/AI Analyst가 안정적으로 읽을 수 있도록 이벤트·속성·퍼널 의미를 진단, 정규화, 검증하는 반복 가능한 하네스다.

이 프로젝트는 하나의 프로젝트 안에서 두 개의 제품 트랙으로 운영한다.

1. **Track A — Claude Skill / Reusable Harness**  
   export-first 데이터 입력을 받아 taxonomy 문제를 탐지하고, canonical map·property dictionary·validation report 같은 표준 산출물을 생성하는 재사용 가능한 분석 하네스.

2. **Track B — Paid Workshop / Consulting Package**  
   고객의 실제 Mixpanel taxonomy를 사전 스캔한 뒤 2–3시간 라이브 세션에서 핵심 이벤트 계약과 migration action plan을 합의하는 유료 워크샵.

핵심 포지셔닝은 “taxonomy cleanup”이 아니라 다음이다.

> Claude가 Mixpanel을 읽기 전에, Claude가 오해하지 않을 이벤트 계약을 먼저 만든다.

---

## 2. Problem Statement

Agentic AI와 MCP 연결로 AI가 Mixpanel, Amplitude, GA4 데이터를 직접 읽고 분석하는 일이 쉬워지고 있다. 그러나 이벤트 taxonomy가 불명확하면 AI는 잘못된 전제 위에서도 그럴듯한 답을 생성할 수 있다.

현장에서 자주 나타나는 문제는 다음과 같다.

- 같은 행동이 여러 이벤트명으로 기록됨: `signup`, `register`, `complete_signup`
- 추상적이고 중복 의미를 가진 속성: `type`, `source`, `status`, `category`
- funnel 단계와 conversion 정의가 팀마다 다름
- owner, description, deprecated status가 없는 이벤트가 많음
- 실무자 설명 없이는 분석 결과를 신뢰하기 어려움
- AI analyst가 같은 질문에 일관되지 않게 답함

따라서 AI 분석 도입 전에는 “AI가 믿고 읽을 수 있는 이벤트/속성/전환 의미 계약”이 필요하다.

---

## 3. Product Tracks

## Track A — Claude Skill / Reusable Harness

### Goal

고객 또는 내부 컨설턴트가 export 파일과 기본 context를 제공하면, Claude가 정해진 절차로 taxonomy 진단과 산출물 초안을 생성하도록 한다.

### Primary users

- MarketFitLab 내부 컨설턴트
- PM/PO/Growth Lead
- Data Analyst / Analytics Engineer
- AI analyst 도입을 준비하는 founder/operator

### Product form

초기 형태는 Claude Skill 또는 skill-like workflow다.

- 입력 파일: CSV/JSON/Markdown export
- 출력 파일: Markdown/CSV report templates
- 실행 환경: Claude 프로젝트 또는 OpenClaw/로컬 workspace
- 고급 옵션: Mixpanel MCP 연결을 통한 schema/usage/query validation

---

## Track B — Paid Workshop / Consulting Package

### Goal

고객이 AI analyst 도입 전 데이터 신뢰성 리스크를 빠르게 확인하고, 핵심 funnel/event contract v1과 migration plan을 합의하게 한다.

### Primary buyers

- Head of Product
- Founder/COO
- Growth Lead
- Data/Analytics Lead

### Product form

2–3시간 유료 워크샵 + 사전 스캔 + 후속 산출물 패키지.

권장 첫 상품명:

> **Mixpanel AI Analyst Readiness Workshop**

---

## 4. MVP Scope

## 4.1 MVP Includes

### Data source

- **MVP 기본:** Mixpanel export-first ingestion
  - event list
  - property list
  - sample tracking plan
  - recent event usage frequency, if available
  - top business questions
- **Optional / Advanced:** Mixpanel MCP
  - live schema inspection
  - usage frequency validation
  - sample query execution
  - before/after AI analyst question validation

### Harness functions

1. Ingest exported event/property data
2. Detect duplicate events and ambiguous properties
3. Detect naming convention violations
4. Detect missing owner/description/deprecated status
5. Identify core funnel ambiguity
6. Propose canonical event map v1
7. Draft property dictionary
8. Draft taxonomy contract
9. Run or simulate AI analyst validation questions
10. Generate readiness score and migration action plan

### Deliverables

- `taxonomy-contract.md`
- `canonical-events.csv`
- `property-dictionary.csv`
- `ai-questions.md`
- `validation-report.md`
- `migration-plan.md`
- `decision-log.md`
- `readiness-score.md`

---

## 4.2 Non-goals

MVP에서는 아래를 하지 않는다.

- SaaS dashboard 개발
- 고객 데이터 자동 migration
- Amplitude/GA4/warehouse 동시 지원
- full AI analyst 제품 개발
- real-time monitoring
- 모든 funnel redesign
- 모든 이벤트의 완전한 governance system 구축
- 고객 프로덕션 시스템에 직접 쓰기 작업

---

## 5. Personas & Jobs-to-be-Done

## Persona 1 — Head of Product / Founder

### Situation

AI로 제품 데이터를 빠르게 질문하고 싶지만, 기존 tracking plan과 dashboard 숫자를 완전히 신뢰하지 못한다.

### JTBD

“Claude가 Mixpanel을 읽게 하기 전에, 핵심 전환과 이벤트 정의가 틀리지 않았는지 확인하고 싶다.”

### Success

- 핵심 funnel 정의가 명확해짐
- 팀 간 conversion 해석 차이가 줄어듦
- AI analyst를 어디까지 믿어도 되는지 판단 가능

---

## Persona 2 — Growth Lead / PM

### Situation

실험과 campaign 분석을 자주 하지만 source/status/type 같은 속성이 팀마다 다르게 쓰인다.

### JTBD

“AI에게 질문했을 때 잘못된 segment나 funnel로 답하지 않게, 이벤트와 속성 의미를 정리하고 싶다.”

### Success

- campaign/source/channel 속성의 의미가 분리됨
- 주요 질문 세트에 대해 안정적인 답변 가능
- migration priority가 정리됨

---

## Persona 3 — Data Analyst / Analytics Engineer

### Situation

매번 이벤트 caveat를 설명해야 하고, AI 분석 도입 시 hallucination risk가 걱정된다.

### JTBD

“이벤트 taxonomy의 위험 지점을 구조적으로 진단하고, stakeholder가 합의할 수 있는 contract로 만들고 싶다.”

### Success

- ambiguous property와 duplicate event 목록 확보
- owner/description/deprecated 상태 정리
- tracking plan 개선 backlog 생성

---

## 6. End-to-End Workflow

## 6.1 Harness Pipeline

### 1) Ingest

Inputs:

- `events.csv`
- `properties.csv`
- `tracking-plan.csv` or `tracking-plan.md`
- `event-usage.csv`, optional
- `business-questions.md`
- `funnel-definition.md`, optional

MVP ingestion principle:

> Export-first ingestion is the default. MCP is optional and advanced.

### 2) Detect

Checks:

- duplicate or near-duplicate event names
- overloaded property names
- vague event/property names
- missing description
- missing owner
- missing deprecated status
- inconsistent tense or naming convention
- core funnel ambiguity
- AI unsupported inference risk

### 3) Normalize

Outputs:

- canonical event naming proposal
- merge/deprecate/keep decision proposal
- property dictionary draft
- funnel stage definitions
- taxonomy contract draft

### 4) Validate

Validation methods:

- AI analyst question set, about 20 questions
- paraphrase consistency check
- unsupported inference flags
- before/after answer quality comparison
- score rubric calculation

### 5) Package

Final artifacts:

- readiness score
- top risks
- canonical map
- migration plan
- decision log
- workshop-ready discussion agenda

---

## 7. Data Inputs & Outputs

## 7.1 Required MVP Inputs

| Input | Format | Required | Notes |
|---|---|---:|---|
| Event list | CSV/JSON/MD | Yes | Event name, description if available |
| Property list | CSV/JSON/MD | Yes | Property name, type, sample values if available |
| Top business questions | Markdown | Yes | 5–10 questions the team wants AI to answer |
| Core funnel definition | Markdown/CSV | Recommended | Existing activation/conversion steps |
| Event usage frequency | CSV | Optional | 30–90 day count by event |
| Current tracking plan | CSV/MD | Optional | If available |

## 7.2 Optional Mixpanel MCP Inputs

Mixpanel MCP can be used after export-first MVP is working.

Potential uses:

- fetch current schema metadata
- inspect event/property usage
- validate whether export is stale
- run sample queries for AI analyst validation
- compare query answers against taxonomy contract assumptions

Constraints:

- MCP must be treated as an advanced path, not MVP dependency
- no secret/API key should be stored in project artifacts
- customer approval is required before live data access
- export-based fallback must always exist

## 7.3 Outputs

| Output | Format | Purpose |
|---|---|---|
| Taxonomy contract | Markdown | Human/AI-readable event semantics |
| Canonical events | CSV | keep/merge/deprecate/rename map |
| Property dictionary | CSV | property definitions, allowed values, owner |
| AI question set | Markdown | validation questions and paraphrases |
| Validation report | Markdown | consistency, ambiguity, unsupported inference |
| Migration plan | Markdown | prioritized implementation actions |
| Decision log | Markdown | live workshop decisions and unresolved issues |
| Readiness score | Markdown | explainable diagnostic score |

---

## 8. Claude Skill Design

## 8.1 Skill Trigger

The skill should trigger on requests like:

- “Audit this Mixpanel taxonomy for AI analyst readiness.”
- “Create a canonical event map from these event exports.”
- “Validate whether Claude can safely analyze this product data.”
- “Turn this tracking plan into an AI-readable taxonomy contract.”
- “Run Taxonomy Harness on this export.”

## 8.2 Skill Inputs

Minimum inputs:

1. Event export file
2. Property export file
3. Top business questions
4. Optional current tracking plan
5. Optional funnel definition

Advanced inputs:

1. Mixpanel MCP connection, if approved
2. Event usage frequency
3. Sample query results
4. Existing dashboard definitions

## 8.3 Skill Steps

1. **Read input files** and identify available columns
2. **Normalize schema** into internal tables:
   - events
   - properties
   - funnel steps
   - business questions
3. **Run detection checklist**:
   - duplicate events
   - ambiguous properties
   - naming issues
   - missing governance fields
   - funnel ambiguity
4. **Generate candidate canonical map**
5. **Generate property dictionary draft**
6. **Draft taxonomy contract** in human/AI-readable language
7. **Generate validation question set**
8. **Score readiness** with explainable rubric
9. **Create migration plan** with priority and owner placeholders
10. **Package artifacts** using fixed templates

## 8.4 Expected Outputs

The Claude Skill should create or update the following artifact templates:

```text
/artifacts/
  taxonomy-contract.md
  canonical-events.csv
  property-dictionary.csv
  ai-questions.md
  validation-report.md
  migration-plan.md
  decision-log.md
  readiness-score.md
```

## 8.5 File / Artifact Templates

### `canonical-events.csv`

Columns:

```text
current_event,canonical_event,action,reason,funnel_stage,owner,priority,notes
```

Allowed `action` values:

- keep
- rename
- merge
- deprecate
- split
- needs_decision

### `property-dictionary.csv`

Columns:

```text
property_name,canonical_name,type,definition,allowed_values,scope,owner,ambiguity_risk,notes
```

### `readiness-score.md`

Sections:

- Overall score
- Risk level
- Coverage
- Clarity
- Consistency
- Governance
- Top score losses
- Recommended next actions

### `validation-report.md`

Sections:

- Question set summary
- Stable answers
- Unstable answers
- Unsupported inference cases
- Required data definitions
- Before/after comparison, if available

## 8.6 Safety & Privacy Considerations

- Default to export files, not live production access
- Do not store API keys, tokens, or private credentials in artifacts
- Treat customer event/property data as confidential
- Avoid copying raw user-level event logs unless explicitly required and approved
- Prefer schema/metadata over raw PII-bearing records
- Redact or omit user identifiers, emails, phone numbers, payment details
- Clearly mark assumptions as assumptions
- Do not perform write/migration operations against customer analytics tools in MVP
- Mixpanel MCP usage requires explicit customer approval and scoped access

---

## 9. Workshop Operating Model

The workshop should be 70% pre-processing and 30% live decision session. The live session should not start from raw data.

## 9.1 Pre-work

Timeline: 2–5 business days before session

Inputs requested from customer:

- Mixpanel event/property export
- existing tracking plan, if any
- top 5–10 business questions
- core funnel definition
- known pain points
- stakeholder list

MarketFitLab preparation:

1. Run harness scan
2. Prepare duplicate/ambiguity report
3. Draft initial canonical event map
4. Draft property dictionary risk list
5. Prepare AI validation questions
6. Identify top 5 decision points for live session

Pre-work output:

- preliminary scan report
- workshop agenda
- decision worksheet

## 9.2 Live Session — 2–3 Hours

Recommended agenda:

1. **Context alignment** — what AI analyst should and should not answer
2. **Scan walkthrough** — duplicates, ambiguity, owner gaps, naming issues
3. **Core funnel decision** — activation/conversion/retention event definitions
4. **Canonical event map review** — keep/rename/merge/deprecate decisions
5. **Property dictionary review** — overloaded properties and allowed values
6. **AI question validation simulation** — show where answers become unstable
7. **Migration priority assignment** — owner, effort, next sprint candidates
8. **Decision log confirmation** — unresolved issues and follow-up owners

## 9.3 Post-work

Timeline: within 3–5 business days after session

Final deliverables:

- finalized `taxonomy-contract.md`
- finalized `canonical-events.csv`
- finalized `property-dictionary.csv`
- `validation-report.md`
- `migration-plan.md`
- `decision-log.md`
- executive summary / readiness score

Optional follow-up:

- 2-week implementation check-in
- Mixpanel MCP validation session
- tracking plan rewrite sprint
- AI analyst prompt/playbook setup

---

## 10. Readiness Score Rubric

Avoid vague maturity scoring. The score must be explainable and tied to observed taxonomy risks.

Suggested dimensions:

| Dimension | Weight | Description |
|---|---:|---|
| Coverage | 25 | Core funnel and key business questions are covered by defined events/properties |
| Clarity | 25 | Event/property names and definitions are unambiguous |
| Consistency | 25 | AI answers remain stable across paraphrased questions and equivalent queries |
| Governance | 25 | Owner, description, deprecated status, and decision log exist |

Example output:

```text
AI-readable score: 62/100
Risk level: Medium
Top score losses:
- signup/register duplicate semantics
- source property overloaded across channel and campaign source
- onboarding conversion definition missing owner
Recommended next action:
- Agree on canonical activation event and deprecate duplicate signup events
```

---

## 11. Pricing / Package Hypothesis

## 11.1 Starter Audit

- **Price hypothesis:** KRW 2M
- **Scope:** export scan + risk report + readiness score
- **Best for:** teams that need a quick diagnostic before committing to workshop

## 11.2 Workshop Package

- **Price hypothesis:** KRW 5M anchor
- **Scope:** audit + 2–3 hour workshop + canonical map + validation + migration plan
- **Best for:** teams preparing AI analyst/MCP analytics usage

## 11.3 Readiness Sprint

- **Price hypothesis:** KRW 10M+
- **Scope:** 1–2 week deeper funnel redesign, tracking plan rewrite, owner log, optional MCP validation
- **Best for:** teams with messy tracking plan and active implementation capacity

Pilot pricing:

- First 1–2 customers can be discounted to KRW 2–3M in exchange for testimonial, anonymized sample, and feedback.

---

## 12. How Harness and Workshop Reinforce Each Other

The two tracks should not compete. They create a loop.

## Harness → Workshop

- Makes diagnosis repeatable
- Reduces prep time
- Produces concrete artifacts before the live session
- Turns subjective consulting into evidence-backed decisions
- Creates before/after validation that makes value visible

## Workshop → Harness

- Reveals real customer language and decision patterns
- Tests which findings customers care about enough to pay for
- Improves templates and score rubric
- Creates anonymized sample reports and sales proof
- Identifies which checks should become automated first

## Strategic loop

1. Workshop sells the urgent business problem
2. Harness standardizes delivery
3. Repeated workshops improve the harness
4. Harness artifacts make the workshop more scalable
5. Mature harness can become Claude Skill, internal tool, or light SaaS later

---

## 13. Success Metrics

## Business metrics

- 3 pilot customers identified
- 1 paid pilot closed
- 2 anonymized sample reports created
- Workshop conversion rate from warm leads
- Average delivery time per workshop

## Product metrics

- % of required inputs successfully ingested
- number of duplicate/ambiguous findings detected
- time to produce preliminary report
- artifact completeness score
- AI answer consistency improvement before/after taxonomy contract

## Customer success metrics

- customer agrees with top 5 risks
- canonical event map accepted by stakeholders
- migration plan has named owners
- customer uses taxonomy contract in AI analyst prompts or MCP workflows

---

## 14. Risks & Mitigations

| Risk | Why it matters | Mitigation |
|---|---|---|
| Problem feels important but not urgent | Taxonomy cleanup is often postponed | Position around AI analyst readiness and confident wrong answers |
| Looks like generic consulting | Harder to scale and price | Use fixed harness, templates, score, artifacts |
| Score feels subjective | Reduces trust | Tie score to explicit checks and validation questions |
| Export data is incomplete | Findings may be weak | State assumptions, request usage frequency, optionally validate via MCP |
| MCP access creates privacy/security friction | Can block adoption | Keep export-first as MVP; make MCP optional |
| Migration is politically hard | Teams may not implement recommendations | Include decision log, owner, priority, and next sprint actions |
| Too narrow with Mixpanel | TAM concern | Treat Mixpanel as wedge; design templates portable to Amplitude/GA4 later |
| AI validation overpromises | Could imply false certainty | Mark unsupported inference and keep human review in loop |

---

## 15. Open Questions

1. Which trigger sells best: AI analyst adoption, dashboard distrust, or old tracking-plan cleanup?
2. Should first public offer be “Mixpanel AI Analyst Readiness Workshop” only, or broader “AI Analytics Readiness Workshop”?
3. What minimum columns are required for event/property exports?
4. How should we generate a public demo dataset without exposing customer data?
5. Which 20 AI analyst validation questions should become the default set?
6. Should MCP validation be a paid add-on or included in the Workshop Package?
7. Who is the strongest first buyer: founder, Head of Product, Growth Lead, or Data Lead?

---

## 16. Next Implementation Steps

## Documentation / Sales

1. Draft 1-page workshop offer
2. Create public sample report using demo data
3. Draft customer intake form
4. Draft workshop agenda template
5. Draft artifact templates under a project `templates/` directory

## Harness / Skill

1. Define minimum input schema for event and property exports
2. Create sample demo export files
3. Draft Claude Skill `SKILL.md` outline
4. Define detection checklist as deterministic rules first
5. Define AI validation question template
6. Define readiness score calculation rubric

## GTM / Validation

1. Identify 5 warm leads using Mixpanel/Amplitude
2. Offer 1–2 discounted pilots
3. Capture objections and urgency triggers
4. Create anonymized before/after examples
5. Decide whether Mixpanel MCP validation should be demo-only or delivery component

---

## 17. MVP Acceptance Criteria

The MVP is ready for first paid pilot when:

- [ ] customer intake form exists
- [ ] export input schema is defined
- [ ] demo dataset exists
- [ ] preliminary scan report template exists
- [ ] canonical event map template exists
- [ ] property dictionary template exists
- [ ] AI question set v1 exists
- [ ] readiness score rubric v1 exists
- [ ] workshop agenda exists
- [ ] final deliverable package structure exists
- [ ] privacy/safety notes are included in customer-facing materials

---

## 18. Result Card

- **Pattern surfaced:** AI analytics adoption turns event taxonomy from internal hygiene into an AI trust and safety prerequisite.
- **Unknown unknown:** Whether buyers pay more urgently for “AI analyst readiness” or for “dashboard/tracking distrust cleanup.”
- **Next move:** Package this as a 1-page Mixpanel AI Analyst Readiness Workshop offer, then build a demo dataset and sample report to support the first warm-lead pilots.
