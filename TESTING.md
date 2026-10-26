# Testing log

What has been tested, what it found, and what changed as a result. Findings are numbered from T13 because T1–T12 were logged when the project was part of an earlier repo.

## Live interviews

The skill has been run in live interviews, starting with a federal court litigation playbook. Findings:

| # | Finding | Change made |
|---|---|---|
| T13 | **Shorthand was accepted without follow-up.** "Aggressive, always playing offense" was recorded for the discovery approach, but an AI can't act consistently on "aggressive". "Usually remove" and "Rule 68 routinely" had no stated exceptions. External review raised the same point. | Added the "make answers operational" principle, and `firm_view.unless` for exceptions. |
| T14 | **Early samples stated current law** (lookback periods, statutory tests) in `rule` fields. | Playbooks now record questions to check (`check`), not current law. The interview no longer asks lawyers to recite law. The early samples were retired. |
| T15 | **Law crept back in through other fields.** "Why it matters" lines stated legal consequences ("defenses are waived if left out"), and one firm view stated a legal requirement. | `why` is defined as practical significance only. Every field is audited for time-sensitive law, which moves into `check`. |
| T16 | **Gaps included fields that don't apply.** "Market practice: none captured" made a procedural playbook look incomplete when it wasn't. | Gaps list only knowledge relevant to the playbook. |
| T17 | **Too much confirmation.** Every drafted instruction was marked for a yes or no. | Explicit confirmation only where a draft could change what the AI does. Faithful restatements just appear in the approval view. |
| T18 | **No open-ended question at the end** (user feedback). | The skill asks "anything material we haven't discussed?" before the approval view, and the approval step says plainly that the user can still add or change things. |

## Schema version 2 (2026-10-25)

A simplification, not new functionality:
- **One kind of playbook.** The six version 1 types (`guardrails`, `task`, `practice`, `industry`, `client`, `matter`), `applies_to` and the layer order are gone.
- **One issue shape.** The old issue and client "calibration item" merged, with the kinds of judgment still in separate fields. Guardrails became a field on an issue.
- **Out of scope.** Task context (client profile, matter facts, term sheets, engagement details) and procedure (task playbooks) were removed from the format and the skill.
- **Examples and testing.** The interview uses near-miss example clauses to draw out exclusions (new `not_when` field), and a draft can be tested on a sample document, with each false alarm or miss turned into a proposed update (AP15).
- **Drafts as input.** The skill can start from a human-drafted playbook and interview only on its gaps and ambiguities (AP14).
- **Validator:** `spec/tests/run_tests.py` passes 8 of 8. The valid fixtures pass with no warnings, including an `x-` field. Seven invalid fixtures are each rejected for the intended reason: missing version, escalation guardrail without a role, firm view on a commercial issue, invalid source, duplicate key, firm-default preference on a commercial issue, and a version 1 `type`.

Version 1 interview output, including the general contract review sample, needs to be re-run under version 2 before it's published here.

## Next

- Re-run a live interview under version 2, and record the producer checklist (`spec/conformance.md`, P1–P13).
- Try "start from a draft" on an existing firm playbook, then test it on a sample contract.
- Try the method with an expert outside law.
