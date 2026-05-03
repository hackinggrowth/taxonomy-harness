# Taxonomy Harness / AI Analytics Readiness

> Claude가 Mixpanel을 읽기 전에, Claude가 헷갈리지 않는 데이터 언어를 먼저 만든다.

## 0. Project Metadata

- **Project name:** Taxonomy Harness / AI Analytics Readiness Workshop
- **Telegram topic:** 🧬 Taxonomy Harness / AI 분석 준비도
- **Topic ID:** 3624
- **Chat ID:** -1003896960594
- **Created:** 2026-05-03
- **Owner:** Paul Jung / MarketFitLab
- **Status:** Project review + council stage

## 1. Background

Agentic AI 시대에는 Mixpanel MCP, Amplitude MCP, GA4 export 같은 연결을 통해 AI가 제품 데이터를 읽고 요약하고 질문에 답할 수 있다.

하지만 현장에서는 오히려 taxonomy를 다시 세팅하는 문제가 더 중요해지고 있다.

과거에는 이벤트 이름이 조금 거칠어도 실무자가 몸으로 메웠다.

- “이 signup은 사실 register랑 같은 뜻이에요.”
- “이 source는 캠페인 source가 아니라 유입 채널이에요.”
- “이 conversion은 onboarding complete랑 같이 봐야 해요.”

AI 분석 파트너가 본격화되면 이 방식은 잘 작동하지 않는다. AI는 모르면 멈추기보다, 엉킨 정의 위에서도 그럴듯한 답을 만들 수 있다.

따라서 다음 경쟁력은 단순히 리포트를 빨리 뽑는 팀이 아니라, **AI가 읽을 수 있게 데이터를 정리한 팀**에서 나올 가능성이 크다.

## 2. Core Thesis

분석 자동화가 쉬워질수록 데이터 설계의 중요성은 더 커진다.

문제는 “AI가 분석을 못 한다”가 아니라:

> AI가 믿고 읽을 수 있는 이벤트/속성/전환 의미 계약이 없다.

Taxonomy Harness는 팀의 이벤트 데이터를 AI가 안정적으로 읽고 질문에 답할 수 있는 형태로 재정렬하는 워크샵 + 하네스다.

## 3. Product Concept

### Working names

1. **Taxonomy Harness**
2. **AI Analytics Readiness Kit**
3. **AI-readable Data Taxonomy Workshop**

### One-liner

Mixpanel/Amplitude/GA4 데이터를 AI 분석 파트너가 안전하게 읽을 수 있도록 이벤트 taxonomy를 진단·정규화·검증하는 2~3시간 워크샵과 자동 리포트 하네스.

### Sales line

> “Claude가 Mixpanel을 읽게 하기 전에, Claude가 헷갈리지 않는 데이터 언어를 먼저 만듭니다.”

## 4. Target Customers

### Primary

- Mixpanel/Amplitude/GA4를 이미 쓰는 스타트업
- AI 분석 도입을 검토하는 PO/PM/데이터/그로스 팀
- 이벤트 tracking plan이 오래되어 팀 내부 해석이 엇갈리는 조직

### Buyer/User candidates

- Head of Product
- Growth Lead
- Data Analyst / Analytics Engineer
- Founder/COO at early-stage SaaS or consumer app

## 5. Problem Symptoms

- 같은 행동이 여러 이벤트명으로 기록됨: `signup`, `register`, `complete_signup`
- 속성명이 추상적임: `type`, `source`, `status`, `category`
- funnel 단계가 명확하지 않음
- owner 없는 이벤트가 많음
- deprecated event가 계속 남아 있음
- AI가 같은 질문에 일관되지 않게 답함
- 실무자 설명 없이는 분석 결과를 신뢰하기 어려움

## 6. Harness Flow

### 1) Ingest

- Mixpanel schema / event list / property list / sample queries 수집
- MCP 또는 export 기반 수집
- 가능하면 최근 30~90일 기준 event usage frequency 포함

### 2) Detect

- 중복 이벤트 탐지
- ambiguous property 탐지
- naming convention 위반 탐지
- owner/description 누락 탐지
- funnel ambiguity 탐지
- AI hallucination risk 높은 지점 표시

### 3) Normalize

- canonical event map 생성
- naming convention 제안
- event/property dictionary 작성
- “이 이벤트는 무엇을 의미하는가” 자연어 정의
- conversion/funnel 단계 재정렬

### 4) Validate

- AI analyst 질문 세트 20개 실행
- 같은 질문을 다르게 물었을 때 답변 일관성 체크
- before/after answer quality 비교
- unsupported inference / ambiguous answer 표시

### 5) Output

- Taxonomy Contract 문서
- Migration Plan
- Tracking Plan 개선안
- AI Analyst Prompt / MCP Usage Guide
- AI-readiness Score
- Before/After 리포트

## 7. Workshop MVP

초기 SaaS보다 2~3시간 유료 워크샵이 적합하다.

### Workshop structure

1. 현재 taxonomy 스캔
2. 핵심 funnel/event map 워크샵
3. AI 질문 시뮬레이션
4. 중복/충돌/모호성 리포트
5. canonical taxonomy v1 합의
6. migration/action plan 정리

### Deliverables

- `taxonomy-contract.md`
- `canonical-events.csv`
- `property-dictionary.csv`
- `ai-questions.md`
- `validation-report.md`
- `migration-plan.md`

## 8. Why Harness, Not Just Consulting

이 문제는 컨설턴트의 감으로 매번 다르게 푸는 게 아니라 반복 가능한 공정으로 만들 수 있다.

Harness means:

- 입력 형식 표준화
- 탐지 체크리스트 표준화
- AI 질문 세트 표준화
- 산출물 템플릿 표준화
- before/after 검증 표준화

## 9. Early Product Shape

### Phase 1 — Manual workshop

- 고객 1~3곳 파일럿
- 수동 리포트 + 템플릿 기반 산출물
- 고객이 실제로 아파하는 trigger 확인

### Phase 2 — Semi-automated harness

- Mixpanel MCP/export 연결
- schema scan script
- report generator
- AI-readiness score

### Phase 3 — SaaS/light tool

- workspace upload/connect
- taxonomy dashboard
- diff + migration tracking
- AI analyst validation suite

## 10. Non-goals

- 처음부터 BI 도구 만들기 아님
- AI analyst 전체 제품 만들기 아님
- 모든 데이터 웨어하우스 통합 아님
- 처음부터 Amplitude/GA4/Mixpanel 전부 지원하지 않음
- 고객 taxonomy를 자동으로 migration하는 것까지 MVP에 넣지 않음

## 11. Key Risks

| Risk | Why it matters | Mitigation |
|---|---|---|
| 고객이 문제를 급하게 느끼지 않을 수 있음 | taxonomy는 중요하지만 미뤄지는 주제 | “AI analyst 도입 전 점검”으로 trigger 잡기 |
| 컨설팅처럼 보일 수 있음 | 반복 매출/제품화 약함 | harness artifacts + score + templates로 제품화 |
| Mixpanel에 너무 좁아질 수 있음 | TAM 제한 | 초기 wedge로는 오히려 좋음. 이후 Amplitude/GA4 확장 |
| AI-readiness score가 허술해질 수 있음 | 신뢰도 하락 | 질문 세트 + before/after consistency 기반으로 산출 |
| 실제 event migration은 정치적임 | 여러 팀 합의 필요 | workshop에서 owner/decision log 포함 |

## 12. Open Questions

1. 첫 wedge는 Mixpanel 전용으로 갈 것인가?
2. 워크샵 가격은 얼마가 적당한가? 예: 200만/500만/1000만 원
3. 첫 고객은 기존 MFL 고객/커뮤니티에서 찾을 수 있는가?
4. AI-readiness score의 최소 평가 항목은 무엇인가?
5. 산출물을 public sample로 만들 수 있는 demo dataset이 필요한가?

## 13. Result Card

- **Pattern surfaced:** AI 분석 자동화가 쉬워질수록 taxonomy 계약이 병목이 된다.
- **Unknown unknown:** 고객이 이 문제를 “지금 돈 내고 고쳐야 하는 문제”로 느끼는 순간이 무엇인지 검증 필요.
- **Next move:** 위원회 검토 후 1-page workshop offer + sample report template 작성.

