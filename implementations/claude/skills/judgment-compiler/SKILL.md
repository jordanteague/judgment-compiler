---
name: judgment-compiler
description: Build or update structured legal playbooks (the format read by full-stack-reviewer and similar review tools) by interviewing the user in plain language (client, matter, guardrails, task, practice-area, or industry playbooks), including capturing lessons from a matter. Use when someone wants to create, set up, or update a playbook, onboard a new client or matter, or record what they learned on a matter.
---

# Judgment compiler

Interview the user in plain language and write the playbook file for them. They answer questions, approve the complete playbook in plain English, and get a finished file in the playbook format (`spec/playbook-format.md`), ready for a review tool such as full-stack-reviewer.

## Principles

- **YAML is for the reviewer; plain English is for the human.** The user never writes or inspects YAML. Before creating or updating a playbook, show its complete operative contents in plain English for approval.
- **Ask; never invent.** Every position comes from something the user said. Mark anything you infer *(inferred — please confirm)*, and keep it out of the file until it's confirmed. Confirm a draft of your own (a check question, an instruction) explicitly only if it could change what the reviewer does. If it just puts something the user already confirmed into operational form, showing it in the approval view, labeled as drafted, is enough.
- **Make answers operational.** The goal is enough judgment for the reviewer to act consistently. Before moving on from an important answer, ask yourself: *could the reviewer act on what I have?* If the user gives shorthand ("aggressive", "conservative", "we fight this", "we usually accept it"), or says an issue is important without saying what the firm does about it, ask one short follow-up about what that means in practice. Don't follow up just to make an entry exhaustive.
- **Separate what is true from what to do.** Facts, preferences, acceptable fallbacks, red lines, reviewer instructions, and history are different things. Never turn one into another unless the user does. A past outcome doesn't become a position or an instruction on its own.
- **Capture judgment, not current law.** Playbooks are durable. They record what to look for, why it matters, what to check, how the firm approaches it, and what the reviewer should do. They don't record current deadlines, thresholds, statutory text or case-law formulations. Write "Check whether removal is available and the deadline that applies," not the deadline itself. The reviewer researches current law at review time. Don't draft black-letter law from your own knowledge, and don't spend the lawyer's time asking them to recite it. Include a durable legal principle only when the user wants it captured and it materially helps the reviewer. This applies to **every** field, including `why`, `firm_view`, `instruction` and notes. Moving law into another field doesn't make it durable, so turn time-sensitive legal conclusions into `check` questions. Playbooks store durable questions and judgment, not ephemeral legal answers.
- **Separate market practice, firm judgment, and client preference.** Never record a firm recommendation as market practice, or a client preference as a general rule. When it isn't clear which kind of statement the user is making, ask.
- **Respect the layers.** Matter instructions override client defaults. Client instructions override practice-area and industry defaults. Never move knowledge up a layer without the user's explicit say-so.
- **Keep turns short.** One topic at a time, and no more than three questions per turn. Offer choices wherever the answer is one of a few options. Use the multiple-choice question tool if you have one.
- **"Don't know" and "skip" are fine.** Record them as gaps.
- **Line up with existing playbooks.** Read the relevant playbooks before interviewing. Calibration items must use the issue `key`s that the practice and industry playbooks define.

## Where each kind of statement goes

Use the playbook format in this repo (`spec/playbook-format.md`):

| What the user tells you | Field |
|---|---|
| Something true about the client or matter | `facts` (with its source) |
| What the client prefers | `position` |
| Not preferred, but routinely accepted | `acceptable` |
| Never acceptable | `never` (or `red_line: true` when any departure from `position` is unacceptable) |
| A risk the client has decided to take | `accepts` |
| What the reviewer should flag, escalate, or do (client and matter playbooks) | `instruction` |
| What happened before | `history` |
| Legal or factual questions to check at review time (practice and industry playbooks) | `check` (current law is always verified at review time) |
| What the reviewer should flag, verify, recommend, or escalate on an issue (practice and industry playbooks) | `instruction` |
| A durable legal principle the user wants captured (rare) | `rule` |
| Market practice (practice and industry playbooks) | `market_position` or `approaches` |
| Firm judgment on legal strategy (practice and industry playbooks) | `firm_view` (`default`, `unless`). Legal issues only. |

Record where each substantive position came from in `source`:
- `stated`: stated by the user in this interview;
- `client-instruction`: a confirmed client instruction;
- `prior-matter`: an outcome observed on a past matter;
- `firm-default`: the firm's default;
- `matter-specific`: a departure for one matter.

Never guess a source. If something the user tells you has no field in the schema, say so in the approval view rather than squeezing it into the nearest field.

## 1. Set up

1. **Which playbook?** If the user hasn't said, ask. Suggest a **client** playbook first. The types are client, matter, guardrails, task, practice area, and industry.
2. **New, update, or a lesson from a matter?** If a playbook with that id exists, use update mode (section 4). If the user is reporting what happened on a matter, use section 5.
3. **Read the context:**
   - for a client, the industry and practice playbooks it will draw on;
   - for a matter, the client playbook;
   - for a practice or industry playbook, the task playbooks that will use it.
4. **Who owns it?** Ask who is substantively responsible for the playbook. That person is the `owner`. If someone else is answering, record them as `updated_by`.
5. Say: "I'll take this one topic at a time. You can skip anything you don't know or don't want to answer."

## 2. Interview guides

Each line is a topic, not a script. Ask it naturally, apply the operational test to important answers, and move on when you have enough.

### Client
1. **Who and what:** the client's name, its industry, and its role in typical deals. The industry selects the industry playbook, and the role sets which side's market positions apply. Record other true things about the client under `facts`.
2. **Who decides:** who makes money and business decisions, who handles legal, and anyone else who signs off.
3. **Appetite for risk:**
   - *cautious*: "avoid risk even if it costs money";
   - *balanced*: "take sensible risks for a good reason";
   - *aggressive*: "accept risk for commercial advantage".
4. **How they negotiate:** what they fight for, what they let go, and relationships they protect. If the answer is shorthand, ask what it looks like in practice.
5. **How they want to hear from us:** format, length, and what comes first.
6. **Never accept:** each answer goes in `never` on the matching issue.
7. **Routinely accept:** separate risks the client has decided to take (`accepts`) from fallbacks it will agree to in negotiation (`acceptable`).
8. **Issue walk-through:** take the high-severity issues from the industry and practice playbooks (eight at most, the most common first). Ask for a preferred position, what they'd accept, and what they'd never accept. Use only the parts the user actually has a view on.
9. **History and sensitivities:** record past events as `history`. If the user wants a past event to change what the reviewer does, record that separately as an `instruction` or a `position`, and confirm it.

### Matter
1. **The work:** review, draft, or advice; which client; and the deadline.
2. **Other parties:** the exact names of adverse parties, as they'll appear in the documents. Ask whether conflicts are cleared for each one. If they aren't, say the reviewer will stop until they are.
3. **Scope:** what the firm has been engaged to do, in one sentence.
4. **Our side:** the client's role in this deal.
5. **For deals:** what's already agreed (term sheet) and what's still open.
6. **For advice:** the question in one sentence. The facts, and where each came from. What's assumed but not confirmed. Which decisions are open.
7. **Departures:** if a position here differs from the client playbook, ask whether it's (a) only for this matter, (b) generally true for this client, (c) a broader practice-area or industry lesson, or (d) not yet clear. Record (a) here with `source: matter-specific`. For (b) or (c), offer to update that playbook separately, through update mode.

### Guardrails
1. Offer a starter set to accept, edit, or reject:
   - flag uncapped indemnities;
   - flag deadlines under 10 days;
   - escalate advice outside the engagement scope;
   - stop if conflicts aren't cleared;
   - flag conclusions that rest on unverified facts.
2. **Insurer and risk requirements:** anything the malpractice carrier requires to be flagged.
3. **Escalation:** what needs a partner, and which role.
4. **Hard stops:** anything that must stop work entirely.

### Task
1. **The steps:** "Walk me through how your firm does this, start to finish."
2. **The deliverables:** what goes to the client, and what stays internal.
3. **Style:** how markups are written, and who reviews before anything goes out.
4. **The type:** confirm whether this is review, drafting, or advice.

### Practice area or industry
1. **Scope:** which work the playbook will be used for, which side the firm usually represents, and how broad it should be.
2. **Issues:** offer a starter list grouped by stage or topic, and let the user pick and add.
3. **For each issue, capture:**
   - *Why it matters* (`why`): the practical significance, without stating legal requirements, deadlines, thresholds, or consequences. Those go in `check`. For example, "can materially affect whether, where and how the case proceeds," not "can be waived if not raised." Then *how important* it is (`default_severity`).
   - *What should make the reviewer consider it:* facts (`triggers`), document language (`look_for`), or both.
   - *What needs checking* (`check`): the legal and factual questions a competent lawyer would investigate. Phrase them as questions or instructions, not answers. You may propose these as drafts for the lawyer to correct.
   - *The firm's approach:* its default, and the exceptions that change it (`firm_view`). Legal issues only. A default without exceptions usually fails the operational test, so ask "When wouldn't you?"
   - *What the reviewer should do:* flag, verify, recommend, or escalate (`instruction`).
   - *Market practice,* if the lawyer has a view (`market_position` or `approaches`).
   - *Industry playbooks only:* which practice areas the issue applies to (required).
4. Spend the lawyer's time on judgment: defaults, exceptions, priorities, and what to watch for. Don't ask them to recite law.
5. When it's unclear whether an answer is market practice or firm judgment, ask.
6. For long playbooks, you may confirm issues a group at a time during the interview. The complete approval view in section 3 is still required.

Suggest that a senior lawyer in the area answers practice and industry questions.

## 3. Approve, then write

1. **Ask one last open question first:** "Is there anything material we haven't discussed?" Capture anything new the same way as the rest, then build the approval view.
2. **Show the complete playbook in plain English.** Not a summary: every substantive item that will go in the file, under natural headings for its type.
   - For a client: About the client · Who decides · Risk approach · Negotiating approach · Never accept · Routinely accept · Positions on key issues · How to communicate · History and sensitivities · Not yet established.
   - For a practice area: one section per stage or topic.

   Show each issue as a short block, using only the lines that apply:

   > **Limitation of liability** · Importance: High
   > Why it matters: ... · Consider it when: ...
   > Check at review time: ... (verify current law)
   > Market practice: ... · Our firm's view: ... (unless ...)
   > Preferred: ... · Will accept: ... · Never accept: ...
   > Reviewer should: ... · History: ... · Source: stated in this interview

   Mark inferences *(inferred — please confirm)*, and mark your own drafts that could change what the reviewer does. List under **Not yet established** only the gaps that matter for this playbook: things the user skipped or didn't know. Don't list schema fields that don't apply (for example, market practice in a procedural playbook). Note anything the schema can't represent.
3. **Ask for approval, and make clear this is another chance to add or change anything**, not just approve or reject. For example: "Approve as is, or tell me anything to add, remove or change." Don't write anything until they approve.
4. **Write the file** in the playbook format:
   - front matter: `type`, `id`, `name`, `schema_version` (currently 1), `owner`, optional `updated_by`, `version` (1, or the old version + 1), and `last_reviewed` (today);
   - the body in fenced YAML blocks;
   - a closing comment listing what's not yet established.
5. **Validate:**
   - the YAML parses;
   - required fields are present;
   - every calibration `key` exists in a loaded practice or industry playbook (or starts with `x-`, which you flag);
   - `firm_view` appears only on legal issues;
   - no time-sensitive law (deadlines, thresholds, statutory text, legal consequences) has crept into any field, including `why`, `firm_view` and `instruction`, unless the user asked for it;
   - industry issues have `practice_areas`;
   - `conflicts_cleared` uses exact names;
   - nothing inferred and unconfirmed made it in.
6. **Save** where the user's playbooks live (by default `playbooks/<type>/<id>.md`), say where it went, and give one example request that uses it (for example, with full-stack-reviewer).

## 4. Update mode

1. Read the existing playbook and summarize what it says now in three plain-English lines.
2. Ask what's changed.
3. Apply the operational test and the layer question (section 2, Matter, item 7) to each change.
4. **Show a plain-English diff and get approval before saving:**

   > **Current:** ...
   > **Proposed:** ...
   > **Why this is changing:** ...
   > **Applies to:** Matter / Client / Practice area / Industry

5. Change only what's approved. Bump `version`, set `last_reviewed` to today, and set `updated_by`. These metadata changes don't need separate approval.

## 5. Learn from a matter

You can't see matter history, so the user supplies the lesson.

1. Ask what happened, or what they learned.
2. Compare it with the relevant playbooks: the matter, the client, and the practice area or industry.
3. Say what, if anything, differs from what the playbooks currently say.
4. For each possible lesson, ask whether it's: specific to this matter · generally true for this client · a broader practice-area or industry lesson · not yet clear. "Not yet clear" changes nothing, but you may record the event as `history` with `source: prior-matter` if the user wants.
5. **Never promote a matter outcome to a client, practice-area, or industry rule without explicit confirmation.**
6. Show each proposed change as a diff (section 4, step 4), including **What happened**, and get approval.
7. Update only the approved playbook, validate it, and bump its version.

## Confidentiality

Client and matter playbooks hold confidential client information. Save them only where the user says, inside the firm's own systems. Don't paste their contents anywhere else.
