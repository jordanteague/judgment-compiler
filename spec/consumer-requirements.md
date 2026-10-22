# Consumer requirements

Part of the [playbook specification](README.md) · Applies to **schema version 1**

A **consumer** is any tool that uses playbooks to do legal work: review a document, draft one, or advise on facts. These requirements define how a consumer must combine playbooks, whatever platform it runs on. They say nothing about output formatting, which each consumer decides for itself.

The key words **MUST**, **MUST NOT**, **SHOULD** and **MAY** are used as described in RFC 2119.

---

## Selection

**CR1. Selecting playbooks.**
- The `guardrails` playbook MUST be loaded. Without it, the consumer MUST NOT produce work product.
- Exactly one `task` playbook applies per run, chosen from the request. If the task is unclear, the consumer SHOULD ask.
- The practice area SHOULD come from the matter's `practice_area`. Otherwise the consumer MAY infer it, and MUST state what it inferred.
- The industry SHOULD come from the client's `industry`. It MUST NOT be inferred from a counterparty.
- Client and matter playbooks MUST be used only when the user names them, or when a named matter refers to a client. A consumer MUST NOT guess a client from names in a document.

**CR2. Side.** A `market_position` MUST be used only when its role label matches one of the matter's `represents` labels. If the side is unknown, the consumer SHOULD ask.

**CR3. Currency.** Playbooks past their `expires` date MUST NOT be used. Playbooks not reviewed recently SHOULD be flagged as stale; 180 days is a reasonable default.

## Assembly

**CR4. The task is the backbone.** The task's steps run in order. Other playbooks only fill the slots that steps name. They MUST NOT add steps or change deliverables.

**CR5. Collecting issues.**
- Candidate issues are the practice issues whose `applies_to.tasks` includes the task, plus the industry issues whose `applies_to.tasks` includes the task **and** whose `applies_to.practice_areas` includes the matter's practice area.
- For `review` tasks, every candidate with a `look_for` is checked. For `draft` tasks, every candidate is covered. For `advise` tasks, only candidates whose `triggers` the facts meet are analyzed; the rest SHOULD be reported as considered but not raised.
- Issues sharing a `key` MUST be merged into one. The practice entry is the base, the industry entry's text is added alongside it, and both are cited.

## Calibration

**CR6. Precedence.** For each issue, the position comes from the first of these that applies:
1. a matter settled term or settled decision;
2. matter `calibration`;
3. client `calibration`;
4. for issues that aren't `commercial`, a `firm_view` (industry, then practice), applying `default` unless `unless` is met;
5. the industry playbook's `market_position` for our side (documents), or its `approaches` entry for the client's `risk_tolerance` (advice);
6. the same from the practice playbook;
7. otherwise, **no firm guidance**.

A `firm_view` on a `commercial` issue MUST be ignored and reported.

**CR7. Severity and calibration items.**
- Severity follows the same precedence.
- A term listed in `never`, or any departure from a `position` marked `red_line`, MUST be treated as the most serious category of finding.
- A term in `acceptable` MUST be identified as an acceptable fallback, not as the preferred position.
- An `instruction` MUST be followed.
- `history` MAY be cited to explain why something matters. It MUST NOT be treated as a position or instruction.

**CR8. Accepted risk stays visible.** An issue the client `accepts` MUST still be shown, identified as an accepted risk.

**CR9. Business decisions belong to the client.**
- For `commercial` issues in documents: settled terms are checked for conformity, and unsettled ones are presented as open decisions. The consumer MUST NOT propose negotiating positions on them.
- In advice: the consumer presents options with legal risk and business impact. It MAY advise against an option on legal grounds. It MUST NOT make the business call.
- `hybrid` issues: the business decision is handled as above, and the legal side is analyzed normally.

## Guardrails

**CR10. Guardrails can't be calibrated away.**
- `flag`: MUST be shown, even when the client accepts the risk.
- `escalate`: MUST be shown, and the output marked as needing sign-off.
- `stop`: no work product.
- Preconditions (`conflicts_cleared`, `engagement_scope`) MUST be checked against the matter. With no matter playbook, the consumer SHOULD ask the user to confirm them rather than assume.

## Special cases

**CR11. No firm guidance.** An issue with no position MUST be labeled as such. The consumer MAY comment from general practice, labeled as its own suggestion. It MUST NOT present such an issue as acceptable.

**CR12. Joint clients.** When a matter has several clients, each client playbook MUST be applied separately. Where their calibrations differ, the consumer MUST NOT merge them or pick one; it MUST report the divergence for the lawyer.

**CR13. Provenance.** Every finding SHOULD be traceable to the playbook type, `id` and `version` it relies on.

## Facts and law

**CR14. Facts.**
- Conclusions MUST rest on facts from the document, the matter's `facts`, or the user.
- Anything else is an assumption, and MUST be stated as one.
- Assumptions and missing facts that would change the answer SHOULD be collected in a list for the lawyer or client to confirm.

**CR15. Kinds of statement stay apart.** Current law, market practice, firm view and client preference MUST NOT be presented as one another. In particular, playbook content MUST NOT be presented as current law.

**CR16. Current law is determined at review time.**
- The consumer answers each issue's `check` questions as of the time of review, using whatever authoritative research it has.
- Current law MUST be presented as the consumer's own research, with sources, for the lawyer to verify. It MUST NOT be attributed to a playbook.
- Questions the consumer can't answer reliably MUST be passed to the lawyer, not answered from general knowledge as if settled.
- Any current-law text found in a playbook (for example, in `rule`) MUST be treated as unverified background.

## Format handling

**CR17. Versions and extensions.**
- The consumer MUST report playbooks with a `schema_version` higher than it supports.
- It MUST ignore unrecognized `x-` fields without failing.
- It SHOULD warn about other unrecognized fields.

**CR18. Professional responsibility.** Every output MUST state that it's a draft for review by a lawyer, and not legal advice.
