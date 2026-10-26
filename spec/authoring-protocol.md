# Authoring protocol

Part of the [playbook specification](README.md) · Applies to **schema version 2**

A **producer** is any tool or process that creates or changes playbooks: an AI interviewer, a form, or a person editing files. This protocol defines what a conforming producer must do, whatever platform it runs on.

The key words **MUST**, **MUST NOT**, **SHOULD** and **MAY** are used as described in RFC 2119.

---

## Content

**AP1. Never invent.**
- Every position, red line, instruction, guardrail and firm view MUST come from the person responsible for it.
- Anything the producer infers MUST be marked as inferred, and MUST NOT be saved until confirmed.
- A draft the producer writes itself MUST be confirmed explicitly if it could change what the AI does. A faithful restatement of something already confirmed MAY simply be shown in the approval view (AP7).

**AP2. Operational answers.** Before accepting an important answer, the producer SHOULD check whether an AI could act on it consistently. Shorthand ("aggressive", "we usually accept it") SHOULD get one follow-up about what it means in practice. A firm view SHOULD record both its default and its exceptions.

**AP3. Kinds of judgment stay apart.** Firm views, preferred positions, acceptable alternatives, red lines, accepted risks, instructions, guardrails, market practice and history MUST each go in their own field ([format](playbook-format.md), section 2). A past outcome MUST NOT become a position or instruction unless the responsible person says so. Where the format can't represent something that matters, the producer SHOULD say so rather than force it into the nearest field.

**AP4. Judgment, not current law.** Producers SHOULD capture issues, practical significance, triggers, questions to check, judgment and instructions.
- They SHOULD NOT record current deadlines, thresholds, statutory text or case-law formulations in any field.
- A durable legal principle MAY be recorded in `rule` when the responsible person wants it and it materially helps.
- Interview time SHOULD go on judgment, not on reciting law.

**AP5. Don't generalize beyond what was said.**
- A view stated about one situation MUST NOT be recorded as a general rule without the person's explicit confirmation. When it's unclear how general a statement is, the producer SHOULD ask.
- Facts about a particular matter or client aren't playbook content. The producer SHOULD leave them out, and say so.
- The producer SHOULD reuse the `key`s already used in the user's other playbooks for the same issue ([format](playbook-format.md), section 2).
- Playbooks MUST NOT contain instructions about how they relate to other playbooks.

**AP6. Provenance and ownership.**
- Substantive positions SHOULD carry a `source`. In particular, a preference on a `commercial` issue MUST NOT be recorded as `firm-default`.
- `owner` MUST be the person or group substantively responsible, which isn't necessarily the person answering questions. If they differ, `updated_by` records the person answering.

## Approval

**AP7. The person approves the complete playbook, in their own language.**
- Before creating or updating a playbook, the producer MUST show its complete operative content in a human-readable form, not a summary.
- The person MUST NOT need to read the machine format.
- The producer SHOULD ask whether anything material hasn't been covered before showing it.
- The approval step SHOULD make clear that the person can still add, remove or change anything.
- Nothing is saved until the person approves.

**AP8. Gaps.** Items that were skipped or are unknown SHOULD be listed as "not yet established." Only gaps relevant to the playbook should be listed, not format fields that don't apply.

**AP9. Updates.** A change to an existing playbook MUST be shown as a before-and-after, with the reason, and approved before saving. The producer MUST then increment `version` and update `last_reviewed`.

**AP10. Learning from experience.** When the person reports what happened on a piece of work, the producer MUST NOT turn the outcome into a position, instruction or general rule without explicit confirmation (AP5). A lesson whose scope isn't yet clear changes no rule, though it MAY be recorded as `history`.

**AP13. Guardrails are confirmed explicitly.** Adding, changing or removing a `guardrail` MUST be confirmed explicitly, even when it restates something already said, because it changes what must be shown on every piece of work that uses the playbook. A guardrail MUST be a professional rule that applies whatever the client wants. A client's own red line belongs in `never` or `red_line`, not in a guardrail.

**AP14. Starting from a draft.** A producer MAY start from an existing human-drafted playbook instead of an interview. The draft counts as the responsible person's statement, but only for what it actually says.
- Each statement MUST be classified into its field (AP3). A classification the producer isn't sure of MUST be marked as inferred and confirmed (AP1).
- Shorthand (AP2), current law (AP4) and past outcomes (AP3) in the draft MUST be handled as they would be in an interview.
- The producer MUST NOT fill gaps in the draft from its own knowledge. It SHOULD ask about the gaps that matter, and list the rest (AP8).
- Anything in the draft the producer couldn't represent, or left out, MUST be reported to the person.
- Approval (AP7) and validation (AP11) apply in full.

**AP15. Examples and tests.** A producer MAY show the person example clauses, or apply a draft playbook to a sample document, to draw out judgment that's hard to state in the abstract: signals, exclusions and calibration.
- Example clauses the producer writes are prompts, not content. Only the person's reaction, once confirmed, goes in the playbook.
- A change prompted by a test (a false alarm or a miss) is an update, shown and approved as in AP9.
- Facts from a sample document MUST NOT be recorded in the playbook, and the document MUST NOT be saved with it (AP12).

## Output

**AP11. Validation.** Before saving, the producer MUST validate the playbook against the [JSON Schema](schema/), and against the checks in [format](playbook-format.md) section 7. It MUST also check that nothing inferred and unconfirmed has been saved.

**AP12. Confidentiality.** A playbook may hold a firm's or a client's confidential judgment. Producers MUST save it only where the responsible person directs, within the firm's own systems.

## Interaction (recommended)

These recommendations make interviews workable. They aren't conformance requirements.
- Cover one topic at a time, with no more than three questions per turn.
- Offer structured choices where the answer is one of a few options.
- Treat "skip" and "don't know" as valid answers, recorded as gaps.
