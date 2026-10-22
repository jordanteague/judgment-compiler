# Testing log: judgment-compiler

> **Name:** this project was called *playbook-builder* until 2026-10-22. Entries before that date use the new name throughout, for consistency.

The builder started life inside the full-stack-reviewer repo and moved to its own repo on 2026-10-22. Earlier reviewer findings (T1–T12) stay in that repo's log. The numbering continues from there, so T13 is the first builder finding.

## Status

`skills/judgment-compiler` (interview mode) was added on 2026-10-22. The worked example, `examples/worked-example-playbook-interview.md`, is a **simulated** interview: the answers were written for the demo. It shows the intended flow, but it isn't a test.

What was checked: the resulting `cascade-mechanical.md` parses, and every calibration key matches an issue in the construction or commercial-contracts playbooks.

**Next**
- Run a live interview with a lawyer playing the relationship partner, and log time taken, questions that confused, and corrections at the summary step.
- Review a subcontract for Cascade with full-stack-reviewer, to confirm the `subcontractor` market positions and Cascade's red lines are applied.
- Test update mode: change one position after a matter and check that the version bump and change list are right.

### Builder v2 (2026-10-22), after review feedback

Changes:
- Every playbook is now approved as a **complete plain-English view** before anything is written. Updates are approved as before-and-after diffs.
- New principles: make answers operational; separate what is true from what to do; separate law, market practice, firm judgment and client preference; never move knowledge up a layer without explicit confirmation.
- New "learn from a matter" workflow.
- Owner is asked, not assumed.
- Time estimates removed.

Schema additions (all optional, so existing playbooks still work):
- on calibration items: `acceptable`, `never`, `instruction`, `history`, `source`;
- on client playbooks: top-level `facts`;
- on practice and industry issues: `firm_view` (legal issues only), with the "no house positions" rule refined accordingly (C15);
- on front matter: `updated_by`.

**First live interview (federal court litigation practice playbook): in progress.** It has already produced one finding:

| # | Finding | Change made |
|---|---|---|
| T13 | **Shorthand was accepted without follow-up.** "Aggressive, always playing offense" was recorded for the discovery approach, but a reviewer can't act consistently on "aggressive". "Usually remove" and "Rule 68 routinely" had no stated exceptions. External review raised the same point. | Added the "make answers operational" principle and `firm_view.unless`. The interview resumes with follow-ups. |

### Builder v3 (2026-10-22): judgment, not current law

Playbooks now record the questions to check (`check`), not current law. The reviewer researches current law at review time (rule C16) and presents it, with sources, for the lawyer to verify. The builder no longer drafts black-letter law or asks lawyers to recite it. Interview time goes on defaults, exceptions and what to watch for.

| # | Finding | Status |
|---|---|---|
| T14 | **The sample playbooks predate this change.** Several `rule` fields state current law: FLSA lookback periods, the Davis-Bacon 20% test, FTC substantiation, OSHA outreach cards. The reviewer now treats such text as unverified background, so the worked examples still hold. But the samples don't yet show the recommended style. | Open. Convert the sample `rule` fields to `check` questions in the next revision. |

### Builder v4 (2026-10-22): second review round, from the live interview

| # | Finding | Change made |
|---|---|---|
| T15 | **Law crept back in through other fields.** After `rule` was retired, "why it matters" lines still stated legal consequences ("defenses are waived if left out"), and one firm view stated a legal requirement (Rule 26(g) certification). | `why` is now defined as practical significance only. Every field is audited for time-sensitive law, which moves into `check`. |
| T16 | **Gaps included fields that don't apply.** "Market practice: none captured" made a procedural playbook look incomplete when it wasn't. | Gaps list only knowledge relevant to the playbook. |
| T17 | **Too much confirmation.** Every drafted reviewer instruction was marked for a yes or no. | Explicit confirmation only where a draft could change what the reviewer does. Faithful operationalizations just appear in the approval view. |
| T18 | **No open-ended question at the end** (user feedback). | The builder now asks "anything material we haven't discussed?" before the approval view, and the approval step says plainly that it's a chance to add or change things, not just approve or reject. |

---

## Specification extracted (2026-10-22)

The format, consumer rules and authoring rules were pulled out of the Claude skills into a platform-neutral specification (`spec/`), with the Claude skills kept as reference implementations.

**Effect on the Claude skill:** none. The only change to `SKILL.md` was the path of the format document, in two places (verified by diff). Its instructions are otherwise unchanged, word for word, and it doesn't read repo files once installed.

**Validator:** `spec/tests/run_tests.py` passed 8 of 8:
- the valid fixtures pass, including an `x-` extension field, with no warnings;
- seven invalid fixtures are each rejected for the intended reason: missing required field, escalation without a role, firm view on a commercial issue, industry issue without practice areas, unknown calibration key, extra body block, invalid source value.

**Next**
- Run the producer conformance checklist (P1–P10) against the next live interview.
- Validate the first real sample playbook with `spec/tools/validate.py` before committing it.
