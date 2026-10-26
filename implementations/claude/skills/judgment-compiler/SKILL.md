---
name: judgment-compiler
description: Turn an expert's tacit judgment into a structured, reusable playbook an AI can apply, by interviewing them in plain language (with example clauses to react to) or by converting a playbook they've already drafted (Word, Markdown, notes) and asking only about its gaps and ambiguities, then testing it on a sample document. Covers any class of problems, such as contract review, a practice area, a sector, or the firm's baseline guardrails. Also updates playbooks and captures lessons from experience. Use when someone wants to create, set up, or update a playbook, or record what they learned on a matter.
---

# Judgment compiler

Interview the user in plain language, or start from a playbook they've already drafted, and write the playbook file for them. They answer questions, approve the complete playbook in plain English, and get a finished file in the playbook format (`spec/playbook-format.md`, schema version 2).

A playbook is reusable expert judgment about a class of problems: what to look for, what to check, the expert's views and their exceptions, preferred positions, acceptable alternatives, red lines, instructions, and guardrails. It isn't the facts of one matter, and it isn't a procedure.

## Principles

- **YAML is for the AI; plain English is for the human.** The user never writes or inspects YAML. Before creating or updating a playbook, show its complete operative contents in plain English for approval.
- **Ask; never invent.** Every position comes from something the user said. Mark anything you infer *(inferred — please confirm)*, and keep it out of the file until it's confirmed. Confirm a draft of your own (a check question, an instruction) explicitly only if it could change what the AI does. If it just puts something the user already confirmed into operational form, showing it in the approval view, labeled as drafted, is enough.
- **Make answers operational.** The goal is enough judgment for an AI to act consistently. Before moving on from an important answer, ask yourself: *could the AI act on what I have?* If the user gives shorthand ("aggressive", "conservative", "we fight this", "we usually accept it"), or says an issue is important without saying what to do about it, ask one short follow-up about what that means in practice. Ask for the exceptions too ("When wouldn't you?"). Don't follow up just to make an entry exhaustive.
- **Use examples, not just recall.** Experts recognize far more than they can list, and they rarely state exceptions in the abstract. Ask for language they've actually seen, show them example clauses to react to, and test the draft on a real document (section 7). Anything you write as an example is a prompt, not content: only their confirmed reaction goes in the playbook.
- **Keep kinds of judgment apart.** Firm views, preferred positions, acceptable alternatives, red lines, accepted risks, instructions, guardrails, market practice and history are different things. Never turn one into another unless the user does. A past outcome doesn't become a position or an instruction on its own.
- **Capture judgment, not current law.** Playbooks are durable. They record what to look for, why it matters, what to check, how the expert approaches it, and what the AI should do. They don't record current deadlines, thresholds, statutory text or case-law formulations. Write "Check whether removal is available and the deadline that applies," not the deadline itself. The AI researches current law at the time of the work. Don't draft black-letter law from your own knowledge, and don't spend the expert's time asking them to recite it. Include a durable legal principle only when the user wants it captured and it materially helps. This applies to **every** field, including `why`, `firm_view`, `instruction`, `guardrail` and notes. Moving law into another field doesn't make it durable, so turn time-sensitive legal conclusions into `check` questions. Playbooks store durable questions and judgment, not ephemeral legal answers.
- **Separate market practice, firm judgment, and client preference.** Never record a firm recommendation as market practice, or a client preference as a general rule. When it isn't clear which kind of statement the user is making, ask. Record whose statement it is in `source`.
- **Don't generalize beyond what was said.** If the user describes what they did on one matter, ask whether it's their general view before recording it as one. Leave out facts about a particular matter or client, and say that you have.
- **Judgment, not procedure.** "If the owner is a public entity, treat broad-form indemnity as non-negotiable" is judgment and belongs in the playbook (`triggers`, `firm_view.unless`, `guardrail.when`). "First read the whole document, then..." is procedure. Say it's outside the playbook, and don't record it.
- **Reuse existing keys.** If the user has other playbooks, read them first. When an issue is already covered there, use the same `key` (for example `indemnification`, not a new `indemnity`).
- **Keep turns short.** One topic at a time, and no more than three questions per turn. Offer choices wherever the answer is one of a few options. Use the multiple-choice question tool if you have one.
- **"Don't know" and "skip" are fine.** Record them as gaps.

## Where each kind of statement goes

Everything about one issue goes in one entry under `issues`, keyed by `key`:

| What the user tells you | Field |
|---|---|
| Why the issue matters in practice | `why` (no legal requirements or consequences) |
| Facts that should make the AI consider it | `triggers` |
| Document language to look for | `look_for` |
| Situations that look like the issue but shouldn't be flagged | `not_when` |
| Legal or factual questions to check at the time of the work | `check` (current law is always verified then) |
| Market practice | `market_position` (by role) or `approaches` (by risk appetite) |
| Firm judgment on legal strategy | `firm_view` (`default`, `unless`). Not on commercial issues. |
| The preferred position | `position` |
| Not preferred, but routinely accepted | `acceptable` |
| Never acceptable | `never` (or `red_line: true` when any departure from `position` is unacceptable) |
| A risk deliberately taken | `accepts` |
| What the AI should flag, verify, recommend, or escalate | `instruction` |
| A professional non-negotiable that applies whatever the client wants | `guardrail` (`when`, `action`: flag / escalate / stop, `escalate_to`) |
| What happened before | `history` |
| A durable legal principle the user wants captured (rare) | `rule` |

Record where each substantive position came from in `source`:
- `stated`: stated by the user in this interview;
- `client-instruction`: a confirmed client instruction;
- `prior-matter`: an outcome observed on a past matter;
- `firm-default`: the firm's default (never on a commercial issue: business decisions belong to the client).

Never guess a source. If something the user tells you has no field in the schema, say so in the approval view rather than squeezing it into the nearest field.

**Guardrail or red line?** Ask: would this still apply if the client said they were fine with it? If yes, it's a guardrail. If it's the client's own limit, it's `never` or `red_line`.

## 1. Set up

1. **What is the playbook about?** If the user hasn't said, ask for a name and one sentence on the class of problems it covers.
2. **New, update, a draft, or a lesson?** If a playbook with that id exists, use update mode (section 4). If the user gives you an existing document (a firm playbook, a checklist, a partner's notes), use section 6. If the user is reporting what happened on a piece of work, use section 5.
3. **Read the user's other playbooks,** if any, so you can reuse their keys.
4. **Who owns it?** Ask who is substantively responsible for the playbook. That person is the `owner`. If someone else is answering, record them as `updated_by`.
5. Say: "I'll take this one topic at a time. You can skip anything you don't know or don't want to answer."

## 2. Interview guides

These are starting points. Each line is a topic, not a script. Ask it naturally, apply the operational test to important answers, and move on when you have enough.

### Issues
1. **Scope:** the class of problems the playbook covers, which side the user usually represents, and how broad it should be. Record this in `description`, not as a rule.
2. **Issues:** offer a starter list grouped by stage or topic, and let the user pick and add.
3. **For each issue, capture:**
   - *Why it matters* (`why`): the practical significance, without stating legal requirements, deadlines, thresholds, or consequences. Those go in `check`. For example, "can materially affect whether, where and how the case proceeds," not "can be waived if not raised." Then *how important* it is (`severity`).
   - *What should make the AI consider it:* facts (`triggers`), document language (`look_for`), or both. Ask for language they've actually seen: "What did the problem clause say?"
   - *When not to flag it* (`not_when`): write three or four short clauses that differ in one way (who holds the role, whose assets, which direction the obligation runs), and ask "Flag or not, and why?" for each. The reasons for "not" are the exclusions. Confirm the wording before recording it.
   - *What needs checking* (`check`): the legal and factual questions a competent expert would investigate. Phrase them as questions or instructions, not answers. You may propose these as drafts for the user to correct.
   - *The firm's approach:* its default, and the exceptions that change it (`firm_view`). Legal issues only. A default without exceptions usually fails the operational test, so ask "When wouldn't you?"
   - *Positions, if the user has them:* what they'd prefer (`position`), what they'd accept (`acceptable`), and what they'd never accept (`never`).
   - *What the AI should do:* flag, verify, recommend, or escalate (`instruction`).
   - *Anything non-negotiable:* "Is there anything here the firm always flags, escalates or stops on, whatever the client wants?" Record it as a `guardrail` with its own `when`.
   - *Market practice,* if the user has a view (`market_position` or `approaches`).
4. Spend the expert's time on judgment: defaults, exceptions, priorities, and what to watch for. Don't ask them to recite law.
5. When it's unclear whether an answer is market practice or firm judgment, ask.
6. For long playbooks, you may confirm issues a group at a time during the interview. The complete approval view in section 3 is still required.

Suggest that a senior expert in the area answers these questions.

### Firm baseline
A firm's baseline playbook holds the guardrails that apply to every piece of work. Keep it short: anything that only makes sense for one kind of work belongs in that work's playbook.
1. Offer a starter set to accept, edit, or reject, each as an issue with a `guardrail`:
   - stop if conflicts aren't cleared for every adverse party;
   - escalate advice outside the engagement scope;
   - flag conclusions that rest on unconfirmed facts.
2. **Insurer and risk requirements:** anything the malpractice carrier requires to be flagged or escalated.
3. **Escalation:** what needs a partner's sign-off, and which role.
4. **Hard stops:** anything that must stop work entirely.

Suggest that the firm's risk or general-counsel partner owns it.

## 3. Approve, then write

1. **Ask one last open question first:** "Is there anything material we haven't discussed?" Capture anything new the same way as the rest, then build the approval view.
2. **Show the complete playbook in plain English.** Not a summary: every substantive item that will go in the file, with one section per stage or topic. Show each issue as a short block, using only the lines that apply:

   > **Limitation of liability** · Importance: High
   > Why it matters: ... · Consider it when: ... · Don't flag when: ...
   > Check at the time of the work: ... (verify current law)
   > Market practice: ... · Our firm's view: ... (unless ...)
   > Preferred: ... · Will accept: ... · Never accept: ...
   > AI should: ... · Always (whatever the client wants): flag / escalate to ... / stop when ...
   > History: ... · Source: stated in this interview

   Mark inferences *(inferred — please confirm)*, and mark your own drafts that could change what the AI does. Mark every guardrail for explicit confirmation. List under **Not yet established** only the gaps that matter for this playbook: things the user skipped or didn't know. Don't list fields that don't apply. Note anything the schema can't represent, and anything you left out (matter facts, procedure).
3. **Ask for approval, and make clear this is another chance to add or change anything**, not just approve or reject. For example: "Approve as is, or tell me anything to add, remove or change." Don't write anything until they approve.
4. **Write the file** in the playbook format:
   - front matter: `id`, `name`, `description`, `schema_version` (currently 2), `owner`, optional `updated_by`, `version` (1, or the old version + 1), `last_reviewed` (today), and optional `tags` and `expires`;
   - the body in fenced YAML blocks, each holding an `issues:` list. You may split the issues across several blocks under Markdown headings;
   - a closing comment listing what's not yet established.
5. **Validate.** If `spec/tools/validate.py` is available, run it on the file and fix every error. Either way, check that:
   - the YAML parses, and each block holds an `issues:` list;
   - every issue has a `key`, keys are unique, and keys already used in the user's other playbooks are reused;
   - `firm_view` appears only on legal or hybrid issues, and no commercial preference has `source: firm-default`;
   - every `escalate` guardrail names `escalate_to`;
   - no time-sensitive law (deadlines, thresholds, statutory text, legal consequences) has crept into any field, including `why`, `firm_view`, `instruction` and `guardrail`, unless the user asked for it;
   - there are no matter facts, no procedure, and no instructions about other playbooks;
   - nothing inferred and unconfirmed made it in.
6. **Save** where the user's playbooks live (by default `playbooks/<id>.md`) and say where it went.

## 4. Update mode

1. Read the existing playbook and summarize what it says now in three plain-English lines.
2. Ask what's changed.
3. Apply the operational test to each change, and ask how general it is if that's unclear.
4. **Show a plain-English diff and get approval before saving:**

   > **Current:** ...
   > **Proposed:** ...
   > **Why this is changing:** ...

5. Change only what's approved. Bump `version`, set `last_reviewed` to today, and set `updated_by`. These metadata changes don't need separate approval.

## 5. Learn from experience

You can't see what happened on past work, so the user supplies the lesson.

1. Ask what happened, or what they learned.
2. Compare it with the relevant playbook, and say what, if anything, differs from what it currently says.
3. For each possible lesson, ask whether it should change the playbook, or whether it was specific to that situation or isn't yet clear. If it shouldn't change the playbook, you may record the event as `history` with `source: prior-matter`, if the user wants.
4. **Never turn an outcome into a position, instruction or general rule without explicit confirmation.**
5. Show each proposed change as a diff (section 4, step 4), including **What happened**, and get approval.
6. Update the playbook, validate it, and bump its version.

## 6. Start from a draft

The user may already have a playbook in some form: a Word document, a checklist, a position paper, markup notes. Treat it as the user's own statement of judgment, and do the translation rather than the whole interview.

1. **Read it all first.** Confirm who owns it, whether it's current, and whose judgment it states (the firm's, or a client's standing instructions). That sets `source`.
2. **Sort every statement** into its field, using the tables above. Keep the user's wording wherever it already works. Mark every classification you weren't sure of *(inferred — please confirm)*: for example, whether "we don't accept uncapped indemnities" is a firm view, a red line, or a guardrail.
3. **Apply the same tests as an interview,** on the draft's text:
   - **shorthand** ("push back", "market standard", "use judgment") gets one follow-up about what it means in practice;
   - **current law** in the draft (deadlines, thresholds, statutory text) becomes `check` questions. Tell the user you've done so;
   - **past outcomes** stay `history` unless the user says they're a rule;
   - **procedure** and **matter facts** are left out, and you say so.
4. **Interview only on what's missing or unclear.** Ask about ambiguities and the gaps that matter for this playbook, using section 2 as a checklist, not a script. Never fill a gap from your own knowledge.
5. **Report what didn't fit.** List anything in the draft you couldn't place, and anything you left out, so the user can decide.
6. Continue with section 3. The approval view marks what came from the draft, what you drafted, and what's inferred. Every guardrail is still confirmed explicitly.

## 7. Test it on a document

A playbook is only calibrated once it has been tried on real material. Offer this after approval, or whenever the user wants to check a playbook.

1. Ask for a sample document the playbook should handle, one the user is free to share with you here. Don't save it, and don't copy its facts into the playbook.
2. Apply the playbook **as written**, using nothing but its content: list what it would flag, citing the issue `key` and the passage, and the near-misses it would correctly leave alone. Don't add your own judgment. The point is to see what the playbook does by itself.
3. Ask the user to mark each item: right, false alarm, or miss.
4. For each **false alarm**, ask why it shouldn't be flagged. The answer is usually a `not_when` exclusion, or a narrower `look_for` or guardrail `when`. For each **miss**, ask what should have caught it: a missing signal, trigger or issue.
5. Write each change in general terms, with no names or facts from the document. Show the changes as an update (section 4, step 4) and get approval before saving.

## Confidentiality

A playbook may hold a firm's or a client's confidential judgment, and so may a draft the user gives you. Save playbooks only where the user says, inside the firm's own systems. Don't paste their contents anywhere else.
