# **AI 340: ARTIFACTS HANDOUT**

\[Placeholder for Date of Delivery\]

### [SECTION A: BLANK EXAMPLES](#section-a:-blank-examples)

1. [Activity: Feature Spec Worksheet](#1.-activity:-feature-spec-worksheet)  
2. [Activity: EARS Requirements Worksheet](#2.-activity:-ears-requirements-worksheet)  
3. [Activity: User Story \+ AC](#3.-activity:-user-story-+-ac-worksheet)   
4. [Activity: ADR Worksheet](#4.-activity:-adr-worksheet)  
5. [Activity: Spec Quality Checklist](#5.-activity:-spec-quality-checklist)

### [SECTION B: COMPLETED TEMPLATES](#section-b:-completed-templates)

1. [Activity: Feature Spec Answer Guide (Completed)](#1.-activity:-feature-spec-answer-guide-\(completed\))  
2. [Activity: EARS Requirements Answer Guide (Completed)](#2.-activity:-ears-requirements-answer-guide-\(completed\))  
3. [Activity: User Story \+ AC Answer Guide (Completed)](#3.-activity:-user-story-+-ac-answer-guide-\(completed\))  
4. [Activity: ADR Answer Guide (Completed)](#4.-activity:-adr-answer-guide-\(completed\))  
5. [Activity: Spec Quality Checklist Answer Guide (Completed)](#5.-activity:-spec-quality-checklist-answer-guide-\(completed\))

### [APPENDIX](#appendix) 

1. [EARS Quick Reference Card](#1.-ears-quick-reference-card)  
2. [Scenario Packets](#2.-scenario-packets)  
   1. [SP.1 Customer Support Summarizer (Instructor Demo)](#sp.1-customer-support-summarizer-\(instructor-demo-—-used-in-all-4-module-demos\))  
   2. [SP.2 Invoice Data Extraction (Student Exercise)](#sp.2-invoice-data-extraction-\(student-exercise-—-used-in-all-4-module-exercises\))  
3. [Compiled Weak vs. Strong Examples](#3.-compiled-weak-vs.-strong-examples)  
   1. [Module 1: Specs — Goals and Non-Goals](#module-1:-specs-—-goals-and-non-goals)  
   2. [Module 2: Requirements — EARS Notation](#module-2:-requirements-—-ears-notation)  
   3. [Module 3: User Stories \+ Acceptance Criteria](#module-3:-user-stories-+-acceptance-criteria)  
   4. [Module 4: Process — Quality Gates](#module-4:-process-—-quality-gates)

## 

## **Section A: BLANK EXAMPLES** {#section-a:-blank-examples}

(*for participants to complete*)

---

### **1\. Activity: Feature Spec Worksheet** {#1.-activity:-feature-spec-worksheet}

**Activity:** Module 1: Spec Surgery

**Context:** A vague feature request has landed in your backlog. Your job is to decompose it into a structured specification that both a human development team and an AI coding agent can build from without asking clarifying questions. The distinction that this practices: moving from ambiguous intent to explicit, bounded scope.

**Instructions:**

1. Read the scenario packet for your assigned feature request. Identify the domain, business outcome, roles, and enterprise context.  
2. Use your AI coding assistant as a collaborator: paste the vague request and ask it to help decompose it into goals, non-goals, constraints, assumptions, and success metrics. Do not accept the AI's output uncritically — push back, add your own knowledge, refine.  
3. Fill out every field in the table below. Each field must be specific and measurable, not vague or aspirational.  
4. When your draft is complete, use AI to stress-test it: prompt "Review this specification. What assumptions am I making that I haven't stated? What edge cases am I missing? What would you need clarified before you could implement this?" Fix what you find.  
5. At the 20-minute mark, swap specs with the group next to you. Their job is to act as your AI agent: read your spec and identify anything that would make them guess.

**Your Answers:**

| Field | Your Answer |
| :---- | :---- |
| Feature name |  |
| Goal 1 (specific, measurable) |  |
| Goal 2 (specific, measurable) |  |
| Non-goal 1 (what AI should NOT build) |  |
| Non-goal 2 (what AI should NOT build) |  |
| Non-goal 3 (what AI should NOT build) |  |
| Constraint 1 (tied to enterprise context) |  |
| Constraint 2 (tied to enterprise context) |  |
| Assumption 1 |  |
| If Assumption 1 is wrong... |  |
| Assumption 2 |  |
| If Assumption 2 is wrong... |  |
| Assumption 3 |  |
| If Assumption 3 is wrong... |  |
| Success metric 1 (measurable) |  |
| Success metric 2 (measurable) |  |
| AI stress-test findings (list gaps the AI identified) |  |
| Peer review feedback (from swap) |  |

**Debrief Questions:**

| Question | Your Notes |
| :---- | :---- |
| Which section was hardest to write — goals, non-goals, or assumptions? Why? |  |
| What gaps did the AI stress-test reveal that you hadn't considered? |  |
| What would happen if an AI agent tried to implement from your spec before you added non-goals? |  |

### 

### **2\. Activity: EARS Requirements Worksheet** {#2.-activity:-ears-requirements-worksheet}

**Activity:** Module 2: Requirements Translation

**Context:** Your spec from Module 1 says WHAT to build but is not precise enough to code from. This worksheet practices converting informal requirements into EARS (Easy Approach to Requirements Syntax) notation — the format AI coding agents and tools like AWS Kiro and GitHub Spec Kit use — with concrete examples and counter-examples that eliminate ambiguity.

**Instructions:**

1. Select 3 requirements from your Module 1 spec that are most important to the feature.  
2. For each requirement, identify which EARS pattern applies (Ubiquitous, Event-driven, State-driven, Unwanted behavior, or Optional). Use the EARS Quick Reference Card in the Appendix.  
3. Rewrite each requirement in full EARS notation: trigger \+ system \+ behavior, with specific fields, thresholds, and formats.  
4. For each requirement, write one concrete example showing correct behavior and one counter-example showing incorrect behavior. Use your AI tool to help generate these.  
5. Mark at least one unknown with a \[NEEDS CLARIFICATION\] marker instead of guessing.  
6. At the 20-minute mark, run the AI Implementability Test: paste your 3 EARS requirements into your AI tool and prompt "Based only on these requirements, write the function signatures and a test outline. Don't ask me any questions — just implement what's specified." If the AI asks a question or guesses, that is a gap in your requirement.

**Requirement 1:**

| Field | Your Answer |
| :---- | :---- |
| Original informal requirement |  |
| EARS pattern (ubiquitous / event / state / unwanted / optional) |  |
| EARS requirement (full notation) |  |
| Example (correct behavior) |  |
| Counter-example (incorrect behavior) |  |
| \[NEEDS CLARIFICATION\] items (if any) |  |

**Requirement 2:**

| Field | Your Answer |
| :---- | :---- |
| Original informal requirement |  |
| EARS pattern (ubiquitous / event / state / unwanted / optional) |  |
| EARS requirement (full notation) |  |
| Example (correct behavior) |  |
| Counter-example (incorrect behavior) |  |
| \[NEEDS CLARIFICATION\] items (if any) |  |

**Requirement 3:**

| Field | Your Answer |
| :---- | :---- |
| Original informal requirement |  |
| EARS pattern (ubiquitous / event / state / unwanted / optional) |  |
| EARS requirement (full notation) |  |
| Example (correct behavior) |  |
| Counter-example (incorrect behavior) |  |
| \[NEEDS CLARIFICATION\] items (if any) |  |

**AI Implementability Test Results:**

| Field | Your Answer |
| :---- | :---- |
| Did the AI ask any clarifying questions? (If yes, list them) |  |
| Did the AI guess on anything? (If yes, list what it assumed) |  |
| Gaps identified — what did you fix? |  |

**Debrief Questions:**

| Question | Your Notes |
| :---- | :---- |
| Which EARS pattern was hardest to apply? Why? |  |
| What did the AI Implementability Test reveal about your requirements that you didn't expect? |  |
| How do examples and counter-examples change the way an AI agent interprets a requirement? |  |

### 

### **3\. Activity: User Story \+ AC Worksheet** {#3.-activity:-user-story-+-ac-worksheet}

**Activity:** Module 3: Story & Criteria Workshop  
**Context:** Your EARS requirements from Module 2 define what the system must do, but they are not yet in the format that best converts to code. This worksheet practices converting EARS requirements into user stories with Given/When/Then acceptance criteria that serve dual duty: as the human team's definition of done AND as the AI agent's test specification.

**Instructions:**

1. Select 2 of your EARS requirements from Module 2 — the most interesting or complex ones.  
2. For each, write a user story in the format: As a \[role\], I want \[capability\], so that \[benefit\].  
3. Write at least 3 Given/When/Then acceptance criteria per story. Include: one happy path, one error/fallback path, and one AI-specific criterion (confidence, contradictory data, or human-in-the-loop).  
4. Add at least 2 edge cases per story using the AI edge case taxonomy: empty input, contradictory input, unexpected format, very long input, missing input, model failure.  
5. Attach NFR metadata to each story: latency, privacy, auditability, rollback, cost.  
6. At the 20-minute mark, run the Test Generation Test: paste your acceptance criteria into your AI tool and prompt "Generate a test specification from these criteria alone." If the generated tests do not match your intent, your criteria are ambiguous — fix them.

**Story 1:**

| Field | Your Answer |
| :---- | :---- |
| Source EARS requirement |  |
| User story (As a / I want / So that) |  |

**Story 1 — Acceptance Criteria:**

| AC \# | Given | When | Then |
| :---- | :---- | :---- | :---- |
| AC-1 (happy path) |  |  |  |
| AC-2 (error/fallback) |  |  |  |
| AC-3 (AI-specific) |  |  |  |
| AC-4 (additional, if needed) |  |  |  |

**Story 1 — Edge Cases:**

| \# | Scenario | Expected Behavior | Why It Matters |
| :---- | :---- | :---- | :---- |
| E-1 |  |  |  |
| E-2 |  |  |  |

**Story 1 — NFR Metadata:**

| NFR | Value |
| :---- | :---- |
| Latency |  |
| Privacy |  |
| Auditability |  |
| Rollback |  |
| Cost |  |

**Story 2:**

| Field | Your Answer |
| :---- | :---- |
| Source EARS requirement |  |
| User story (As a / I want / So that) |  |

**Story 2 — Acceptance Criteria:**

| AC \# | Given | When | Then |
| :---- | :---- | :---- | :---- |
| AC-1 (happy path) |  |  |  |
| AC-2 (error/fallback) |  |  |  |
| AC-3 (AI-specific) |  |  |  |
| AC-4 (additional, if needed) |  |  |  |

**Story 2 — Edge Cases:**

| \# | Scenario | Expected Behavior | Why It Matters |
| :---- | :---- | :---- | :---- |
| E-1 |  |  |  |
| E-2 |  |  |  |

**Story 2 — NFR Metadata:**

| NFR | Value |
| :---- | :---- |
| Latency |  |
| Privacy |  |
| Auditability |  |
| Rollback |  |
| Cost |  |

**Test Generation Test Results:**

| Field | Your Answer |
| :---- | :---- |
| Did the AI-generated tests match your intent? |  |
| Mismatches identified (list) |  |
| Fixes applied to AC |  |

**Debrief Questions:**

| Question | Your Notes |
| :---- | :---- |
| How does writing AC in Given/When/Then format change the way you think about "done"? |  |
| Which edge case was hardest to specify? What makes AI-specific edge cases different from traditional ones? |  |
| What did the Test Generation Test reveal — did the AI generate tests you didn't intend, or miss tests you expected? |  |

### 

### **4\. Activity: ADR Worksheet** {#4.-activity:-adr-worksheet}

**Activity:** Module 4: Spec Bundle Assembly  
**Context:** Throughout the spec process, you made decisions involving tradeoffs. This worksheet practices documenting those decisions in a lightweight ADR (Architectural Decision Record) so that future team members — and future AI agents reading your project configuration — understand why you chose what you chose and when to reconsider.

**Instructions:**

1. Identify the most significant tradeoff decision you made during the exercise. Look for decisions where you chose between two reasonable options with different consequences.  
2. Write the context: what problem or question forced the decision?  
3. State the decision clearly in one sentence.  
4. List the options you considered with pros and cons for each.  
5. Explain your rationale: why did you choose this option over the others?  
6. Define revisit triggers: what would change your mind?

**Your Answers:**

| Field | Your Answer |
| :---- | :---- |
| ADR title (ADR-NNN: Decision summary) |  |
| Context (what problem forced this decision?) |  |
| Decision (one sentence) |  |

**Options Considered:**

|  | Option A | Option B |
| :---- | :---- | :---- |
| Description |  |  |
| Pros |  |  |
| Cons |  |  |

**Rationale and Consequences:**

| Field | Your Answer |
| :---- | :---- |
| Rationale (why this option?) |  |
| Consequences (what tradeoffs are you accepting?) |  |
| Revisit triggers (what would make you reconsider?) |  |

**Debrief Questions:**

| Question | Your Notes |
| :---- | :---- |
| Why is it important to document decisions that "feel obvious" at the time? |  |
| How would an AI agent benefit from reading this ADR in an AGENTS.md file? |  |

### 

### **5\. Activity: Spec Quality Checklist** {#5.-activity:-spec-quality-checklist}

**Activity:** Module 4: Spec Bundle Assembly (Swap \+ Review phase)  
**Context:** This checklist is your team's "definition of ready" for spec bundles. A story does not enter a sprint until it passes this checklist. Use it to review another team's spec bundle and provide specific, actionable feedback.

**Instructions:**

1. Exchange spec bundles with another group.  
2. Go through every item on the checklist below. Mark Pass, Fail, or N/A.  
3. For every Fail, write a specific note explaining the gap — not "needs more detail" but exactly what is missing or ambiguous.  
4. Deliver 3 specific, actionable pieces of feedback to the other team.

**AI Implementability:**

| Check | Pass / Fail / N/A | Notes |
| :---- | :---- | :---- |
| Can an AI agent implement each requirement without asking questions? |  |  |
| Are all acceptance criteria precise enough to generate tests from? |  |  |
| Are non-goals explicitly stated (what the agent should NOT build)? |  |  |
| Are unknowns marked with \[NEEDS CLARIFICATION\], not left as gaps? |  |  |

**Completeness:**

| Check | Pass / Fail / N/A | Notes |
| :---- | :---- | :---- |
| Goals are specific and measurable (not "make it work well") |  |  |
| Every requirement has at least one example and one counter-example |  |  |
| Edge cases cover: empty input, bad input, AI failure, contradictions |  |  |
| NFR metadata is attached to every story (latency, privacy, auditability, rollback, cost) |  |  |

**Testability:**

| Check | Pass / Fail / N/A | Notes |
| :---- | :---- | :---- |
| Every AC follows Given/When/Then format |  |  |
| Test Generation Test passed: AI can generate a matching test suite from AC alone |  |  |
| Fallback behavior is specified (what happens when the AI fails) |  |  |

**Enterprise Readiness:**

| Check | Pass / Fail / N/A | Notes |
| :---- | :---- | :---- |
| Compliance constraints are stated (regulatory, data, access) |  |  |
| Audit trail requirements are specified |  |  |
| Rollback plan exists |  |  |
| Key tradeoffs documented in ADRs |  |  |

**Feedback Summary:**

| \# | Specific Feedback Item |
| :---- | :---- |
| 1 |  |
| 2 |  |
| 3 |  |

**Debrief Questions:**

| Question | Your Notes |
| :---- | :---- |
| What was the most common type of gap you found in the other team's bundle? |  |
| How would using this checklist every sprint change your team's spec quality over time? |  |

## 

## **Section B: COMPLETED TEMPLATES** {#section-b:-completed-templates}

*(Reference examples — do not edit, Blank templates are in Section A)*

### **1\. Activity: Feature Spec Answer Guide (Completed)** {#1.-activity:-feature-spec-answer-guide-(completed)}

**Example:** Customer Support Summarizer (Instructor Demo)

| Field | Example Answer |
| :---- | :---- |
| Feature name | Customer Support Ticket Summarizer |
| Goal 1 (specific, measurable) | Reduce average agent handoff preparation time from \~12 minutes to under 3 minutes for Tier 1 and Tier 2 support tickets. |
| Goal 2 (specific, measurable) | Provide a structured summary that highlights: issue timeline, customer sentiment, prior commitments made, and unresolved questions. |
| Non-goal 1 (what AI should NOT build) | AI does not draft the response to the customer. That is a separate feature (future phase). |
| Non-goal 2 (what AI should NOT build) | AI does not prioritize or route tickets. Routing stays with the existing rules engine. |
| Non-goal 3 (what AI should NOT build) | AI does not handle Tier 3 escalations or any ticket flagged by compliance. |
| Constraint 1 (tied to enterprise context) | Must not store or log PII beyond the active session (regulatory: GLBA compliance). |
| Constraint 2 (tied to enterprise context) | Must integrate with existing Salesforce Service Cloud — no new UIs. |
| Constraint 3 (tied to enterprise context) | Summary generation must complete in under 3 seconds (p95). |
| Constraint 4 (tied to enterprise context) | Must use the company-approved LLM API (internal gateway, not direct model calls). |
| Assumption 1 | Average ticket thread is under 20 messages. |
| If Assumption 1 is wrong... | Summarization quality degrades; may need chunking strategy. |
| Assumption 2 | Support agents have Salesforce open during handoffs. |
| If Assumption 2 is wrong... | Need to consider mobile / email delivery. |
| Assumption 3 | Historical ticket data is accessible via API. |
| If Assumption 3 is wrong... | Data extraction becomes a separate workstream. |
| Success metric 1 (measurable) | Handoff prep time decreases by 75% (measured via Salesforce time-tracking). |
| Success metric 2 (measurable) | Summary accuracy rated 4+ out of 5 by agents in weekly spot-checks (sample of 50). |
| Success metric 3 (measurable) | Zero PII leakage incidents in first 90 days. |
| AI stress-test findings | AI surfaced: email addresses and phone numbers not listed in PII categories; partial account numbers may evade exact-match redaction; what happens if the ticket thread is in multiple languages; what if the handoff is initiated before the ticket is fully resolved. |
| Peer review feedback | (Completed during class swap exercise) |

**Why non-goals matter:** An AI agent will eagerly build anything you do not explicitly exclude. A human developer might intuit that drafting customer responses is out of scope. An agent will not — it sees "summarize tickets so agents can handle handoffs" and thinks "Maybe I should also draft the handoff message\!" Non-goals are guardrails that prevent scope creep in AI-assisted development.

**Why assumptions need "if wrong" impacts:** Assumptions are bets. Documenting the impact of being wrong turns invisible risks into visible action items. If the average ticket thread is actually 50+ messages rather than under 20, the entire summarization approach may need to change — and you want to know that before development starts, not after.

### 

### **2\. Activity: EARS Requirements Answer Guide (Completed)** {#2.-activity:-ears-requirements-answer-guide-(completed)}

**Example:** Customer Support Summarizer (Instructor Demo)

**Requirement 1 — Event-driven:**

| Field | Example Answer |
| :---- | :---- |
| Original informal requirement | The system should generate a summary when a ticket is handed off. |
| EARS pattern | Event-driven |
| EARS requirement | When a support agent initiates a handoff in Salesforce, the Ticket Summarizer shall generate a structured summary containing: issue timeline, customer sentiment (positive/neutral/negative), prior commitments made by any agent, and unresolved questions — within 3 seconds. |
| Example (correct behavior) | Input: 8-message ticket thread about a billing dispute. Customer was promised a callback by Friday. Credit was applied Feb 2 but customer says it wasn't received. Expected output: Timeline: Billing dispute opened Jan 5 → Credit applied Feb 2 → Customer follow-up Feb 10\. Sentiment: Negative (escalating). Prior commitments: Callback promised by Friday (Jan 10). Unresolved: Customer states credit not received; account shows credit applied. |
| Counter-example (incorrect behavior) | Output that says "Issue resolved — credit applied Feb 2" — this is wrong because it collapses a contradiction into a false conclusion. The requirement says "unresolved questions" must be surfaced, not papered over. |
| \[NEEDS CLARIFICATION\] items | None for this requirement. |

**Requirement 2 — Unwanted behavior:**

| Field | Example Answer |
| :---- | :---- |
| Original informal requirement | Don't include PII in summaries. |
| EARS pattern | Unwanted behavior |
| EARS requirement | If the source ticket contains personally identifiable information (SSN, account numbers, full addresses, date of birth), the Ticket Summarizer shall redact the PII in the summary output, replacing it with \[REDACTED-type\] tokens (e.g., \[REDACTED-SSN\]), and shall log a PII-detected event to the audit trail. |
| Example (correct behavior) | Input ticket: "Customer John Smith, SSN 123-45-6789, called about account \#9876543." Output summary: "Customer \[REDACTED-NAME\], SSN \[REDACTED-SSN\], called about account \[REDACTED-ACCOUNT\]." Audit log entry: "PII detected: SSN, account number. Redaction applied." |
| Counter-example (incorrect behavior) | Output that partially redacts: "Customer John S., SSN ***\-**\-6789, called about account \#987*\*\*\*." Partial redaction is not compliant — any PII fragment is a violation under GLBA. |
| \[NEEDS CLARIFICATION\] items | AI stress-test surfaced: Are email addresses and phone numbers in scope for PII redaction? Are partial account numbers (last 4 digits) acceptable or must those be redacted too? Decision needed from compliance. |

**Requirement 3 — State-driven:**

| Field | Example Answer |
| :---- | :---- |
| Original informal requirement | Handle it gracefully when the model is down. |
| EARS pattern | State-driven |
| EARS requirement | While the LLM API is unavailable or response latency exceeds 10 seconds, the Ticket Summarizer shall display a fallback message: "AI summary unavailable — manual review required" and shall log the outage event with timestamp and error code. |
| Example (correct behavior) | LLM API returns HTTP 503\. UI displays: "AI summary unavailable — manual review required." Log entry: "2025-03-15T14:22:08Z | ERROR | LLM\_UNAVAILABLE | http\_status=503 | fallback\_triggered=true".  |
| Counter-example (incorrect behavior) | System spins indefinitely waiting for a response, showing a loading indicator with no timeout. The agent is stuck and cannot proceed with the handoff. |
| \[NEEDS CLARIFICATION\] items | None for this requirement. |

**AI Implementability Test Results (Example):**

| Field | Example Answer |
| :---- | :---- |
| Did the AI ask any clarifying questions? | No — the requirements were precise enough for the AI to generate function signatures and test outlines without questions. |
| Did the AI guess on anything? | The AI assumed a specific logging framework (structured JSON logs) which was not specified. This is acceptable as an implementation detail. |
| Gaps identified | None critical. Minor: could specify log format explicitly if the team has a standard. |

**Why examples and counter-examples matter:** Examples show the AI agent the shape of correct output — not just the rule, but what compliance with the rule looks like in practice. Counter-examples prevent the most common misinterpretation. Together, they eliminate the ambiguity that causes AI agents to produce plausible-but-wrong implementations.

**Why \[NEEDS CLARIFICATION\] is better than guessing:** An AI agent reading a gap in a requirement will fill it with its best guess. A \[NEEDS CLARIFICATION\] marker turns an invisible gap into a visible action item. The team resolves it before development starts, preventing rework.

### 

### **3\. Activity: User Story \+ AC Answer Guide (Completed)** {#3.-activity:-user-story-+-ac-answer-guide-(completed)}

**Example:** Customer Support Summarizer (Instructor Demo)

**Story 1:**

| Field | Example Answer |
| :---- | :---- |
| Source EARS requirement | When a support agent initiates a handoff in Salesforce, the Ticket Summarizer shall generate a structured summary containing: issue timeline, customer sentiment, prior commitments, and unresolved questions — within 3 seconds. |
| User story | As a support agent handling a ticket handoff, I want to see an AI-generated structured summary of the ticket thread, so that I can review the case history in under 3 minutes instead of reading the entire thread. |

**Story 1 — Acceptance Criteria:**

| AC \# | Given | When | Then |
| :---- | :---- | :---- | :---- |
| AC-1 (happy path) | A ticket thread with 5-20 messages across 2+ agents | The handoff is initiated in Salesforce | A summary is generated within 3 seconds containing: issue timeline (chronological, with dates), customer sentiment (positive/neutral/negative), prior commitments (with agent name and date), unresolved questions (bulleted list) |
| AC-2 (PII redaction) | A ticket thread containing SSN, account numbers, or date of birth | The summary is generated | All PII is replaced with \[REDACTED-type\] tokens, and a PII-detected event is logged to the audit trail |
| AC-3 (AI-specific: conflicting data) | A ticket thread where customer statements contradict account records | The summary is generated | Conflicting information is flagged as "\[CONFLICTING\]" with both versions shown, and the summary includes a "Needs human verification" banner |
| AC-4 (fallback) | The LLM API is unavailable or response exceeds 10 seconds | The handoff is initiated | The UI displays "AI summary unavailable — manual review required" and the outage is logged with timestamp and error code |

**Story 1 — Edge Cases:**

| \# | Scenario | Expected Behavior | Why It Matters |
| :---- | :---- | :---- | :---- |
| E-1 | Empty ticket (no messages) | Display "No ticket history available" | Prevents hallucinated summary from no input |
| E-2 | Single very long message (5000+ words) | Summarize with a \[TRUNCATED\] note if exceeding context window | Prevents silent data loss when input exceeds model limits |
| E-3 | Ticket in non-English language | Detect language, summarize in English, note original language | Supports global support teams across 3 time zones |
| E-4 | Ticket contains only attachments, no text | Display "Ticket contains attachments only — manual review required" | Prevents hallucination from no-text input |

**Story 1 — NFR Metadata:**

| NFR | Value |
| :---- | :---- |
| Latency | load \< 3 seconds |
| Privacy | PII redaction required (GLBA) |
| Auditability | All summaries logged with input hash \+ output \+ model version |
| Rollback | Feature flag — can disable AI summarization and revert to manual |
| Cost | \< $0.03 per summary at projected volume (800 handoffs/day) |

**Why Given/When/Then matters for AI-assisted development:** Each AC is a test specification. An AI agent can read AC-1 and generate a test: set up a thread with 5-20 messages, trigger a handoff, assert that the output contains four specific fields and was generated within 3 seconds. This is ATDD — Acceptance Test Driven Development — and it only works when AC is written at this level of precision.

**Why AI-specific criteria matter:** AC-3 (conflicting data) and AC-4 (fallback) are criteria that traditional user stories often omit. AI systems fail in ways traditional software does not: they hallucinate, they produce confidently wrong answers, they degrade rather than crash. Specifying these behaviors at the story level ensures they are built and tested, not discovered in production.

### 

### **4\. Activity: ADR Answer Guide (Completed)** {#4.-activity:-adr-answer-guide-(completed)}

**Example:** Customer Support Summarizer (Instructor Demo)

| Field | Example Answer |
| :---- | :---- |
| ADR title | ADR-001: Use company LLM gateway vs. direct model API calls |
| Context | The ticket summarizer needs to call an LLM. We can use the company's centralized LLM gateway (which adds \~200ms latency but handles auth, logging, rate limiting, and compliance) or call the model API directly (faster, but we own all the operational concerns). |
| Decision | Use the company LLM gateway. |

**Options Considered:**

|  | Company Gateway | Direct API |
| :---- | :---- | :---- |
| Description | Route all LLM calls through the centralized company gateway | Call the model provider's API directly from the summarizer service |
| Pros | Compliance handled, audit trail built-in, no API key management, rate limiting included, SOX-friendly | Lower latency (\~200ms savings), more model flexibility, no dependency on gateway team |
| Cons | Added latency (\~200ms), less model choice, dependency on gateway team's availability and SLAs | Must build own logging/compliance layer, API key rotation, SOX audit trail — estimated 2-3 sprints of work plus ongoing maintenance |

**Rationale and Consequences:**

| Field | Example Answer |
| :---- | :---- |
| Rationale | The 200ms latency penalty is acceptable — we are still under our 3s budget with margin. Building our own compliance and audit layer would cost 2-3 sprints and create ongoing maintenance burden. The gateway team has SLAs we can rely on. |
| Consequences | We accept dependency on the gateway team's uptime and model availability. We lose the ability to quickly switch models if a better option becomes available. |
| Revisit triggers | If gateway latency exceeds 1s consistently; if we need a model the gateway does not support; if the gateway team's SLA drops below 99.9%. |

**Why ADRs matter for AI-assisted development:** When an AI agent reads project configuration (CLAUDE.md, AGENTS.md), it needs to understand not just what the current architecture is, but why. Without an ADR, a future developer or AI agent might see the gateway dependency and "optimize" it away by switching to direct API calls — reintroducing all the compliance risks the team deliberately avoided.

**Why revisit triggers matter:** Decisions are not permanent. Revisit triggers make it explicit under what conditions the team should reconsider. This prevents both premature re-debate ("Can't we just call the API directly?") and stale decisions that persist long after circumstances have changed.

### 

### **5\. Activity: Spec Quality Checklist Answer Guide (Completed)** {#5.-activity:-spec-quality-checklist-answer-guide-(completed)}

**Example:** Customer Support Summarizer — completed quality review

**AI Implementability:**

| Check | Pass / Fail / N/A | Notes |
| :---- | :---- | :---- |
| Can an AI agent implement each requirement without asking questions? | Pass | All 3 EARS requirements are precise: specific trigger, system, behavior, and thresholds. AI Implementability Test confirmed — AI generated function signatures and test outlines without asking questions. |
| Are all acceptance criteria precise enough to generate tests from? | Pass | All AC use Given/When/Then. Test Generation Test confirmed — AI generated matching test specification for all 4 AC and all 4 edge cases. |
| Are non-goals explicitly stated (what the agent should NOT build)? | Pass | 3 non-goals stated: no response drafting, no routing, no Tier 3/compliance-flagged tickets. |
| Are unknowns marked with \[NEEDS CLARIFICATION\], not left as gaps? | Pass | One \[NEEDS CLARIFICATION\] marker on thread length limit — explicitly flagged rather than guessed. |

**Completeness:**

| Check | Pass / Fail / N/A | Notes |
| :---- | :---- | :---- |
| Goals are specific and measurable | Pass | Both goals include measurable targets: "under 3 minutes" and specific summary fields. |
| Every requirement has at least one example and one counter-example | Pass | All 3 EARS requirements have examples and counter-examples. Counter-examples specifically address the most likely AI misinterpretation. |
| Edge cases cover: empty input, bad input, AI failure, contradictions | Pass | 4 edge cases: empty ticket, very long message, non-English, attachments-only. AI failure covered by AC-4 (fallback). Contradictions covered by AC-3 (conflicting data). |
| NFR metadata is attached to every story | Pass | Latency, privacy, auditability, rollback, and cost all specified with concrete values. |

**Testability:**

| Check | Pass / Fail / N/A | Notes |
| :---- | :---- | :---- |
| Every AC follows Given/When/Then format | Pass | All 4 AC use Given/When/Then consistently. |
| Test Generation Test passed | Pass | AI generated matching tests for all AC and edge cases without asking questions. |
| Fallback behavior is specified | Pass | AC-4 specifies exact fallback message and logging behavior when LLM is unavailable. |

**Enterprise Readiness:**

| Check | Pass / Fail / N/A | Notes |
| :---- | :---- | :---- |
| Compliance constraints are stated | Pass | GLBA compliance, PII redaction, company LLM gateway (not direct API). |
| Audit trail requirements are specified | Pass | All summaries logged with input hash \+ output \+ model version. PII-detected events logged separately. |
| Rollback plan exists | Pass | Feature flag — can disable AI summarization and revert to manual workflow. |
| Key tradeoffs documented in ADRs | Pass | ADR-001 documents the gateway vs. direct API decision with options, rationale, and revisit triggers. |

**Feedback Summary (Example):**

| \# | Specific Feedback Item |
| :---- | :---- |
| 1 | Consider adding an edge case for tickets that contain only internal notes (no customer messages) — the summarizer might produce a misleading "customer sentiment" from agent-to-agent communication. |
| 2 | The cost NFR ($0.03 per summary) does not account for PII redaction processing overhead — verify with the gateway team whether PII detection adds to the per-call cost. |
| 3 | AC-2 (PII redaction) should specify behavior for PII types not in the explicit list — e.g., if a customer pastes a credit card number, is that covered? Consider adding a catch-all category. |

**Why this checklist works as a team habit:** The checklist is not a one-time exercise — it is the team's "definition of ready." Every spec bundle is reviewed against it before stories enter the iteration. Over time, teams internalize the quality standards and the checklist becomes faster to complete. But this process helps catch the gaps that slip through when people are moving fast.

## 

## **APPENDIX** {#appendix}

### **1\. EARS Quick Reference Card** {#1.-ears-quick-reference-card}

EARS \= Easy Approach to Requirements Syntax

| Pattern | Syntax | When to use |
| :---- | :---- | :---- |
| Normal Behavior | The \[system\] shall \[behavior\] | Always-on behaviors |
| Event-driven | When \[event\], the \[system\] shall \[behavior\] | Triggered actions |
| State-driven | While \[state\], the \[system\] shall \[behavior\] | Conditional behaviors |
| Unwanted behavior | If \[condition\], the \[system\] shall \[behavior\] | Error handling, safety |
| Optional | Where \[feature\], the \[system\] shall \[behavior\] | Configurable features |

### 

### **2\. Scenario Packets** {#2.-scenario-packets}

#### **SP.1 Customer Support Summarizer (Instructor Demo — used in all 4 module demos)**  {#sp.1-customer-support-summarizer-(instructor-demo-—-used-in-all-4-module-demos)}

* **Business outcome:**   
  Faster, more accurate support ticket handoffs between agents — reducing handoff preparation time from \~12 minutes to under 3 minutes.   
* **Roles:** Support Agent (Tier 1), Support Agent (Tier 2), Support Team Lead, Compliance Officer   
* **Inputs:** Support ticket threads from Salesforce Service Cloud containing customer messages, agent responses, internal notes, and system-generated events.   
* **Risk notes:** GLBA compliance — PII in tickets (SSN, account numbers, full addresses, date of birth). Regulated financial services company. Any PII leakage is a compliance violation. Audit trail is mandatory. 800 handoffs/day means cost per summary matters at scale.

**Enterprise context:**

- Regulated financial services company  
- GLBA compliance requirements  
- PII present in nearly every ticket: SSN, account numbers, addresses, dates of birth  
- SLA: handoff must be completed within 30 minutes  
- Existing Salesforce Service Cloud workflow — agents work entirely within Salesforce  
- 800 handoffs per day across 120 agents in 3 time zones  
- Company-approved LLM gateway (internal, not direct model API calls)  
- Current handoff prep takes \~12 minutes per ticket (reading thread, writing handoff notes)

**"Messy" starting point for exercise:**

*"We need AI to summarize customer support tickets so agents can handle handoffs faster."*

**Constraint goal:** Produce a structured specification, EARS requirements, user stories with Given/When/Then acceptance criteria, and an ADR that an AI coding agent can implement from without asking clarifying questions — while maintaining GLBA compliance and integrating with the existing Salesforce workflow.

**Key complications for spec writing:**

- **PII everywhere** — privacy constraints are real and non-negotiable; partial redaction is not acceptable  
- **Existing Salesforce workflow** — cannot introduce a new UI; must appear within the existing agent workspace  
- **Contradictory information** common in tickets — customer says X, records show Y; AI must flag, not resolve  
- **Variable ticket lengths** — from 1 message to 50+ messages; summarization approach may need to vary  
- **Multi-language support** — global team across 3 time zones; tickets may arrive in languages other than English  
- **Cost at scale** — 800 handoffs/day; cost per summary must be sustainable  
- **Model failure** — what happens when the LLM is unavailable; fallback behavior must be specified

#### **SP.2 Invoice Data Extraction (Student Exercise — used in all 4 module exercises)** {#sp.2-invoice-data-extraction-(student-exercise-—-used-in-all-4-module-exercises)}

* **Business outcome:** Eliminate manual data entry for invoice processing, reducing errors and processing time — from 8-12 minutes per invoice at \~3% error rate to automated extraction with human verification only when confidence is low.   
* **Roles:** Accounts Payable Clerk, AP Manager, Financial Controller, External Auditor   
* **Inputs:** PDF invoices (digital and scanned) from 400+ vendors in varying formats, currencies, and languages.   
* **Risk notes:** SOX compliance — every extracted value must be traceable back to its source document with bounding box coordinates. External auditors require complete traceability. Any data quality issue in financial records is a SOX finding.

**Enterprise context:**

- SOX-compliant manufacturing company  
- \~3,000 invoices per month from 400+ vendors  
- Multi-currency: USD, EUR, GBP, JPY  
- Mix of digital PDFs and scanned paper invoices (some with handwritten annotations)  
- Legacy Oracle ERP system with batch import API (strict JSON field formatting)  
- Current manual entry takes 8-12 minutes per invoice with \~3% error rate  
- External auditors require complete traceability of every extracted value back to source document  
- AP team of 12 clerks processing invoices daily  
- Month-end close creates processing spikes (40% of volume in last 5 business days)

**"Messy" starting point for exercise:**

*"We need AI to pull data from invoices so the finance team doesn't have to type everything in manually."*

**Constraint goal:** Produce a structured specification, EARS requirements, user stories with Given/When/Then acceptance criteria, and an ADR that an AI coding agent can implement from without asking clarifying questions — while maintaining SOX compliance and integrating with the legacy Oracle ERP.

**Key complications for spec writing:**

- **Scanned/handwritten invoices** — OCR quality varies wildly; handwritten line items may be illegible; AI confidence will be low on these  
- **SOX compliance** — audit trail is non-negotiable; every extracted value must link back to source coordinates in the PDF  
- **Multi-currency** — extraction must detect and preserve currency; currency conversion is NOT in scope (the ERP handles that)  
- **Legacy ERP integration** — Oracle batch import API with strict field formatting (JSON); field names and types are fixed; validation errors reject the entire batch  
- **Vendor-specific formats** — no two vendors send invoices that look the same; headers, field positions, and terminology vary widely  
- **Partial extraction** — what happens when AI can extract some fields but not others? Does it submit partial data or queue for human review?  
- **Confidence scoring** — when should a human verify vs. auto-accept? What threshold separates auto-accept from human review?  
- **Cost at scale** — 3,000 invoices/month; cost per extraction matters; scanned invoices may require OCR \+ extraction (two model calls)  
- **Month-end spikes** — 40% of volume in the last 5 business days; system must handle bursts without degrading

### 

### **3\. Compiled Weak vs. Strong Examples** {#3.-compiled-weak-vs.-strong-examples}

#### **Module 1: Specs — Goals and Non-Goals** {#module-1:-specs-—-goals-and-non-goals}

**Weak spec goal:** 

| *"Build AI to process invoices."* |
| :---- |

**What's wrong:** 

* Completely unbounded.   
* "Process" could mean extract, validate, approve, route, archive, or all of the above.   
* No success criteria, no measurable target, no specification of which data fields matter.   
* An AI agent receiving this would build whatever it thinks "process invoices" means, and its guess would be plausible but wrong.

**Strong spec goal:** 

| *"Extract vendor name, invoice number, line items (description, quantity, unit price, total), tax amount, and grand total from PDF invoices with \>=95% field-level accuracy, processing each invoice in under 10 seconds."* |
| :---- |

**What makes it strong:** 

* Every element is specific and measurable.   
* The exact fields are listed (an AI agent knows what to extract). The accuracy threshold is numeric (\>=95% field-level).   
* The latency constraint is explicit (under 10 seconds).   
* A human or AI agent can implement this without asking, *"What do you mean by process?"*

**Weak non-goal:** 

| *(Missing entirely)* |
| :---- |

**What's wrong:** 

* Without non-goals, an AI agent will eagerly build anything adjacent to the stated goals.  
* It might add invoice approval, PO matching, vendor management, payment scheduling, all reasonable extensions that were never requested and are not in scope.   
* Missing non-goals is the most common spec failure in AI-assisted development.

**Strong non-goal:** 

| *"The system does not approve invoices for payment. Approval workflow remains manual in Oracle ERP. The system does not match invoices to purchase orders (future phase)."* |
| :---- |

**What makes it strong:** 

* Explicitly names two things an AI agent might reasonably build (approval and PO matching) and excludes them.   
* Explains where the excluded functionality lives (Oracle ERP) and when it might be revisited (future phase).   
* An AI agent reading this knows exactly where its scope ends.

#### 

#### **Module 2: Requirements — EARS Notation**  {#module-2:-requirements-—-ears-notation}

**Weak requirement:** 

| *"The system should extract data accurately from invoices."* |
| :---- |

**What's wrong:** 

* "Data" is undefined — which fields? "Accurately" is undefined — what percentage?   
* What counts as accurate for a line item total vs. a vendor name?   
* "Should" is ambiguous in requirements engineering; does it mean "must" or "ideally"?   
* An AI agent would guess at every one of these dimensions.

**Strong EARS requirement:** 

| *"When a PDF invoice is uploaded to the extraction queue, the Invoice Extractor shall identify and extract: vendor name, invoice number, invoice date, line items (description, quantity, unit price, line total), subtotal, tax amount, currency, and grand total. For each extracted field, the system shall assign a confidence score (0.0-1.0). Example: {vendor: 'Acme Corp', confidence: 0.98}. Counter-example: extracting 'Total: $1,234.56' from a footer disclaimer that says 'Total assets exceed $1,234.56'. This is not an invoice total."* |
| :---- |

**What makes it strong:** 

* Uses EARS event-driven pattern (When... shall...).   
* Lists every field explicitly.  
* Specifies confidence scoring for each field.   
* Includes a concrete example showing the output format.   
* Includes a counter-example preventing a specific, realistic misinterpretation (extracting dollar amounts from non-invoice-total contexts).   
* An AI agent can implement this directly and knows what to avoid.

#### 

#### **Module 3: User Stories \+ Acceptance Criteria** {#module-3:-user-stories-+-acceptance-criteria}

**Weak AC:** 

| *"The system extracts invoice data correctly."* |
| :---- |

**What's wrong:** 

* Not testable.   
* "Correctly" is undefined.   
* No input conditions specified (Given).   
* No trigger specified (When).   
* No measurable output specified (Then).   
* An AI agent cannot generate a test from this, as it would have to guess what "correctly" means for every field, every input format, and every edge case.

**Strong AC:** 

| *"Given a digital PDF invoice with clearly printed text, When the invoice is submitted for extraction, Then all required fields are extracted with confidence \>= 0.90, the extracted data is returned in the Oracle ERP batch import format (JSON), and a source-mapping is generated linking each extracted value to its bounding box coordinates in the source PDF."* |
| :---- |

**What makes it strong:** 

* Specifies the input condition (digital PDF with clearly printed text — distinguishing from scanned/handwritten).   
* Specifies the trigger (submitted for extraction).   
* Specifies three measurable outputs: confidence threshold (\>=0.90), output format (Oracle ERP batch import JSON), and traceability (bounding box source-mapping).   
* An AI agent can generate a test directly from this: create a digital PDF, submit it, assert confidence \>= 0.90 on all fields, validate JSON format against Oracle schema, verify source-mapping coordinates exist.

#### 

#### **Module 4: Process — Quality Gates**  {#module-4:-process-—-quality-gates}

**Weak quality gate:** 

| *"Review the spec before starting."* |
| :---- |

**What's wrong:** 

* "Review" is undefined. Review for what? By whom? Using what criteria? How do you know when the review is done?   
* This is not a quality gate. It is a vague aspiration. Teams will either skip it or conduct a cursory glance that catches nothing.

**Strong quality gate:** 

| *"Before a story enters the sprint: (1) AI Implementability Test passed — AI agent can generate function signatures \+ test outline from AC alone, (2) all \[NEEDS CLARIFICATION\] markers resolved, (3) every AC has Given/When/Then format, (4) at least one fallback/error AC per story, (5) NFR metadata attached (latency, privacy, auditability, rollback, cost)."* |
| :---- |

**What makes it strong:** 

* Five specific, binary checks, each one passes or fails.   
* The AI Implementability Test is a concrete, repeatable procedure (paste AC into AI tool, observe whether it asks questions).   
* \[NEEDS CLARIFICATION\] resolution ensures no gaps are left for guessing. Given/When/Then format ensures testability.   
* Fallback AC ensures AI failure modes are specified.   
* NFR metadata ensures operational concerns are addressed before development, not after.   
* A team can run this checklist in 10 minutes and know definitively whether a story is ready for the iteration.

