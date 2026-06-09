# Spec Bundle: Customer Support Ticket Summarizer

Date: 2026-06-09
Source: Section B completed templates from AI 340 Artifacts Handout

## 1) Feature Specification

### Feature Name
Customer Support Ticket Summarizer

### Goals
1. Reduce average agent handoff preparation time from approximately 12 minutes to under 3 minutes for Tier 1 and Tier 2 support tickets.
2. Provide a structured summary that includes issue timeline, customer sentiment, prior commitments, and unresolved questions.

### Non-Goals
1. The AI does not draft customer responses.
2. The AI does not prioritize or route tickets.
3. The AI does not handle Tier 3 escalations or tickets flagged by compliance.

### Constraints
1. Must not store or log PII beyond the active session (GLBA).
2. Must integrate into existing Salesforce Service Cloud workflow (no new UI).
3. Summary generation must complete in under 3 seconds (p95).
4. Must use the company-approved LLM gateway (no direct model API calls).

### Assumptions and Impact If Wrong
1. Assumption: Average ticket thread is under 20 messages.
   Impact if wrong: Summarization quality may degrade; chunking strategy required.
2. Assumption: Support agents use Salesforce during handoffs.
   Impact if wrong: Alternative delivery channels (mobile/email) may be needed.
3. Assumption: Historical ticket data is accessible via API.
   Impact if wrong: Data extraction becomes a separate workstream.

### Success Metrics
1. Handoff prep time decreases by 75% (Salesforce time-tracking).
2. Summary accuracy rated 4/5 or higher in weekly spot checks (sample size 50).
3. Zero PII leakage incidents in first 90 days.

### Known Gaps Identified During Stress Test
1. Clarify whether email addresses and phone numbers are in redaction scope.
2. Clarify treatment of partial account numbers.
3. Define behavior for multilingual threads.
4. Define behavior when handoff starts before resolution is reached.

## 2) EARS Requirements

### RQ-1 Event-Driven Summary Generation
- Pattern: Event-driven
- Requirement:
  - When a support agent initiates a handoff in Salesforce, the Ticket Summarizer shall generate a structured summary containing issue timeline, customer sentiment (positive/neutral/negative), prior commitments made by any agent, and unresolved questions within 3 seconds.
- Example (correct behavior):
  - Input: 8-message billing dispute thread; callback promised; credit applied; customer reports not received.
  - Output includes timeline, sentiment as Negative, prior commitments, and unresolved contradiction.
- Counter-example (incorrect behavior):
  - Output claims issue is resolved and omits contradiction.

### RQ-2 Unwanted Behavior PII Redaction
- Pattern: Unwanted behavior
- Requirement:
  - If source ticket content contains PII (SSN, account numbers, full addresses, date of birth), the Ticket Summarizer shall redact PII using [REDACTED-type] tokens and log a PII-detected event to the audit trail.
- Example (correct behavior):
  - "Customer [REDACTED-NAME], SSN [REDACTED-SSN], account [REDACTED-ACCOUNT]."
  - Audit log records PII categories detected and redaction action.
- Counter-example (incorrect behavior):
  - Partial masking that leaves identifiable fragments.
- Needs clarification:
  - Are email and phone always PII in this policy context?
  - Are last-4 account digits permitted or always redacted?

### RQ-3 State-Driven Fallback
- Pattern: State-driven
- Requirement:
  - While the LLM API is unavailable or latency exceeds 10 seconds, the Ticket Summarizer shall display "AI summary unavailable - manual review required" and log outage event with timestamp and error code.
- Example (correct behavior):
  - API returns HTTP 503; fallback message shown; log includes timestamp, error code, fallback_triggered=true.
- Counter-example (incorrect behavior):
  - Infinite loading spinner with no timeout or fallback.

## 3) User Stories and Acceptance Criteria

### US-1 Generate Structured Handoff Summary
As a support agent handling a ticket handoff, I want an AI-generated structured summary of the ticket thread, so that I can review case history in under 3 minutes.

#### Acceptance Criteria (Given/When/Then)
1. AC-1 Happy Path
   - Given a ticket thread with 5-20 messages across 2 or more agents
   - When handoff is initiated in Salesforce
   - Then a summary is generated within 3 seconds including timeline, sentiment, prior commitments, and unresolved questions.
2. AC-2 PII Redaction
   - Given the ticket contains SSN, account numbers, or date of birth
   - When summary is generated
   - Then all PII is replaced with [REDACTED-type] tokens and a PII-detected audit event is logged.
3. AC-3 AI-Specific Contradictions
   - Given ticket statements conflict with account records
   - When summary is generated
   - Then conflicting content is marked [CONFLICTING], both versions are shown, and a "Needs human verification" banner is included.
4. AC-4 Fallback
   - Given the LLM API is unavailable or response exceeds 10 seconds
   - When handoff is initiated
   - Then UI displays "AI summary unavailable - manual review required" and outage is logged with timestamp and error code.

#### Edge Cases
1. Empty ticket history: show "No ticket history available".
2. Single very long message (>5000 words): summarize and mark [TRUNCATED] if context window limit is hit.
3. Non-English ticket: summarize in English and note detected source language.
4. Attachments-only ticket: show "Ticket contains attachments only - manual review required".

#### NFR Metadata
- Latency: p95 < 3 seconds
- Privacy: GLBA-compliant redaction
- Auditability: log input hash, output, and model version
- Rollback: feature flag to disable summarization
- Cost: less than $0.03 per summary at 800 handoffs/day

### US-2 Protect Compliance and Service Continuity
As a compliance officer and support lead, I want guaranteed redaction and deterministic fallback behavior, so that handoffs remain compliant and operational during AI degradation.

#### Acceptance Criteria (Given/When/Then)
1. AC-1 Compliance Redaction
   - Given a ticket contains in-scope PII
   - When a summary is produced
   - Then no raw in-scope PII appears in output, and redaction tokens are used consistently.
2. AC-2 Audit Trail Integrity
   - Given a summary is generated
   - When logging occurs
   - Then log includes timestamp, request identifier, model version, and redaction/fallback events when applicable.
3. AC-3 Service Degradation Handling
   - Given gateway unavailability or timeout > 10 seconds
   - When summarization is requested
   - Then user receives fallback message immediately after timeout threshold and can proceed with manual handoff.

#### Edge Cases
1. PII detector false negative risk: send uncertain entities to conservative redaction path when confidence is below threshold.
2. Repeated transient gateway failures: prevent repeated retries from blocking user workflow.

#### NFR Metadata
- Latency: timeout threshold fixed at 10 seconds for failover
- Privacy: zero tolerance for leaked in-scope PII
- Auditability: immutable event records for redaction and fallback paths
- Rollback: disable AI path with feature flag, retain manual workflow
- Cost: monitor fallback/retry rates to avoid unexpected spend

## 4) Architectural Decision Record

### ADR-001: Use Company LLM Gateway Instead of Direct Model API Calls

- Status: Accepted
- Context:
  - Summarizer needs LLM access. Two options: company gateway (adds approximately 200ms latency, includes auth/logging/rate limiting/compliance) or direct API calls (lower latency, higher operational/compliance burden).
- Decision:
  - Use company LLM gateway.
- Options considered:
  - Option A: Company gateway
    - Pros: built-in compliance and audit trail, no direct key management, rate limiting included.
    - Cons: added latency, less model flexibility, dependency on gateway team/SLA.
  - Option B: Direct API
    - Pros: lower latency, faster model switching.
    - Cons: requires custom compliance/audit/key management, estimated 2-3 sprints plus maintenance.
- Rationale:
  - 200ms latency is acceptable within 3-second budget; compliance and operational risks are reduced significantly.
- Consequences:
  - Accept dependency on gateway uptime and supported model catalog.
- Revisit triggers:
  - Gateway latency consistently above 1 second.
  - Required model unavailable in gateway.
  - Gateway SLA below 99.9%.

## 5) Spec Quality Checklist Result

### AI Implementability
- Pass: AI can implement requirements without clarifying questions.
- Pass: AC are precise enough to generate tests.
- Pass: Non-goals are explicit.
- Pass: Unknowns are marked where needed.

### Completeness
- Pass: Goals are specific and measurable.
- Pass: Requirements include examples and counter-examples.
- Pass: Edge cases include empty input, contradictions, and AI failure.
- Pass: NFR metadata attached to stories.

### Testability
- Pass: AC written in Given/When/Then form.
- Pass: Test generation from AC alone is feasible.
- Pass: Fallback behavior is explicitly specified.

### Enterprise Readiness
- Pass: Compliance constraints documented.
- Pass: Audit trail requirements documented.
- Pass: Rollback plan documented.
- Pass: Tradeoff documented in ADR.

## 6) Open Clarifications (Must Resolve Before Implementation)

1. Confirm full PII taxonomy for this feature scope (email, phone, credit card, partial identifiers).
2. Confirm policy for partial account number exposure (last 4 digits allowed or not allowed).
3. Confirm required log schema and retention for audit system of record.
4. Confirm exact behavior and UX text for multilingual summaries.

## 7) Definition of Ready

This spec bundle is implementation-ready if and only if:
1. Open clarifications in Section 6 are resolved and recorded.
2. Test cases are generated directly from AC and reviewed by support + compliance stakeholders.
3. Feature flag, audit logging, and fallback paths are included in first implementation slice.
