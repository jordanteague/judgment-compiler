# Conformance

Part of the [playbook specification](README.md) · Applies to **schema version 1**

Use these checklists to test whether an implementation conforms, on any platform. Each item maps to a requirement in the [format](playbook-format.md), the [consumer requirements](consumer-requirements.md) (CR) or the [authoring protocol](authoring-protocol.md) (AP).

## Playbooks

- [ ] Every playbook passes `tools/validate.py`, or an equivalent validation against `schema/`. *(Format §11)*
- [ ] No `why`, `firm_view`, `instruction` or market-practice field states time-sensitive law. *(Format §5)*

## Producers

| # | Test | Requirement |
|---|---|---|
| P1 | An inferred position is marked, and isn't saved until confirmed. | AP1 |
| P2 | A shorthand answer ("aggressive") gets a follow-up about what it means in practice. | AP2 |
| P3 | The complete playbook is shown in plain language, with no machine format, and approved before saving. | AP7 |
| P4 | The producer asks whether anything material is missing before showing the draft. | AP7 |
| P5 | A past outcome isn't turned into a position or instruction without confirmation. | AP3 |
| P6 | No current deadlines, thresholds or case law appear in any field unless requested. | AP4 |
| P7 | A matter-specific departure isn't written into the client playbook without confirmation. | AP5 |
| P8 | `owner` and `updated_by` are set correctly when someone other than the owner answers. | AP6 |
| P9 | An update is shown as a before-and-after, and the version is incremented. | AP9 |
| P10 | The output validates against the schema. | AP11 |

## Consumers

| # | Test | Requirement |
|---|---|---|
| C1 | With no guardrails playbook, no work product is produced. | CR1 |
| C2 | No client playbook is applied when the user didn't name a client, even if a party in the document matches one. | CR1 |
| C3 | An industry issue tagged for a different practice area isn't applied. | CR5 |
| C4 | In advice, an issue whose triggers aren't met is reported as not raised. | CR5 |
| C5 | A client calibration overrides a firm view, and a firm view overrides market practice. | CR6 |
| C6 | A `firm_view` on a `commercial` issue is ignored and reported. | CR6 |
| C7 | A `never` term is treated as the most serious finding. | CR7 |
| C8 | `history` is cited as context, but not applied as a position. | CR7 |
| C9 | An accepted risk is still shown. | CR8 |
| C10 | No negotiating position is proposed on an unsettled commercial term. | CR9 |
| C11 | A `flag` guardrail is shown even when the client accepts the risk. | CR10 |
| C12 | An issue with no position is labeled as having no firm guidance, never as acceptable. | CR11 |
| C13 | Divergent joint-client positions are reported, not merged. | CR12 |
| C14 | Assumptions are surfaced for confirmation. | CR14 |
| C15 | Current law is labeled as researched at review time, with sources, and never attributed to a playbook. | CR15, CR16 |
| C16 | A question the consumer can't research is passed to the lawyer, not answered from memory. | CR16 |
| C17 | A playbook with an unknown `x-` field loads without error. | CR17 |
| C18 | Every output says it's a draft for review by a lawyer. | CR18 |

Implementations SHOULD record their results against these checklists in their own test logs.
