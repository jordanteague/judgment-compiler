# Authoring protocol

Part of the [playbook specification](README.md) · Applies to **schema version 1**

A **producer** is any tool or process that creates or changes playbooks: an AI interviewer, a form, or a person editing files. This protocol defines what a conforming producer must do, whatever platform it runs on.

The key words **MUST**, **MUST NOT**, **SHOULD** and **MAY** are used as described in RFC 2119.

---

## Content

**AP1. Never invent.**
- Every position, red line, instruction and firm view MUST come from the person responsible for it.
- Anything the producer infers MUST be marked as inferred, and MUST NOT be saved until confirmed.
- A draft the producer writes itself MUST be confirmed explicitly if it could change what a consumer does. A faithful restatement of something already confirmed MAY simply be shown in the approval view (AP7).

**AP2. Operational answers.** Before accepting an important answer, the producer SHOULD check whether a consumer could act on it consistently. Shorthand ("aggressive", "we usually accept it") SHOULD get one follow-up about what it means in practice. A firm view SHOULD record both its default and its exceptions.

**AP3. Kinds of knowledge stay apart.** Facts, preferences, acceptable fallbacks, red lines, accepted risks, reviewer instructions, history, market practice and firm judgment MUST each go in their own field ([format](playbook-format.md), section 2). A past outcome MUST NOT become a position or instruction unless the responsible person says so. Where the format can't represent something that matters, the producer SHOULD say so rather than force it into the nearest field.

**AP4. Judgment, not current law.** Producers SHOULD capture issues, practical significance, triggers, questions to check, firm judgment and reviewer instructions.
- They SHOULD NOT record current deadlines, thresholds, statutory text or case-law formulations in any field.
- A durable legal principle MAY be recorded in `rule` when the responsible person wants it and it materially helps.
- Interview time SHOULD go on judgment, not on reciting law.

**AP5. Layers.** Matter content overrides client content, and client content overrides practice and industry content.
- A producer MUST NOT move knowledge to a broader layer without explicit confirmation.
- When a matter position differs from the client playbook, the producer SHOULD ask whether it applies to the matter only, the client generally, the practice area or industry, or isn't yet clear. It records the answer only at that layer.

**AP6. Provenance and ownership.**
- Substantive positions SHOULD carry a `source`.
- `owner` MUST be the person or group substantively responsible, which isn't necessarily the person answering questions. If they differ, `updated_by` records the person answering.

## Approval

**AP7. The person approves the complete playbook, in their own language.**
- Before creating or updating a playbook, the producer MUST show its complete operative content in a human-readable form, not a summary.
- The person MUST NOT need to read the machine format.
- The producer SHOULD ask whether anything material hasn't been covered before showing it.
- The approval step SHOULD make clear that the person can still add, remove or change anything.
- Nothing is saved until the person approves.

**AP8. Gaps.** Items that were skipped or are unknown SHOULD be listed as "not yet established." Only gaps relevant to the playbook should be listed, not format fields that don't apply.

**AP9. Updates.** A change to an existing playbook MUST be shown as a before-and-after, with the reason and the layer it applies to, and approved before saving. The producer MUST then increment `version` and update `last_reviewed`.

**AP10. Lessons from matters.** When recording what happened on a matter, the producer MUST NOT promote an outcome into a client, practice or industry rule without explicit confirmation (AP5). A lesson whose scope isn't yet clear changes no rule, though it MAY be recorded as `history`.

## Output

**AP11. Validation.** Before saving, the producer MUST validate the playbook against the [JSON Schema](schema/) for its type, and against the checks in [format](playbook-format.md) section 11. It MUST also check that nothing inferred and unconfirmed has been saved.

**AP12. Confidentiality.** Client and matter playbooks hold confidential client information. Producers MUST save them only where the responsible person directs, within the firm's own systems.

## Interaction (recommended)

These recommendations make interviews workable. They aren't conformance requirements.
- Cover one topic at a time, with no more than three questions per turn.
- Offer structured choices where the answer is one of a few options.
- Treat "skip" and "don't know" as valid answers, recorded as gaps.
