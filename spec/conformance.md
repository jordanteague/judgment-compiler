# Conformance

Part of the [playbook specification](README.md) · Applies to **schema version 2**

Use these checklists to test whether a playbook or a producer conforms, on any platform. Each item maps to a requirement in the [format](playbook-format.md) or the [authoring protocol](authoring-protocol.md) (AP).

## Playbooks

- [ ] Every playbook passes `tools/validate.py`, or an equivalent validation against `schema/`. *(Format §7)*
- [ ] No `why`, `firm_view`, `instruction`, `guardrail` or market-practice field states time-sensitive law. *(Format §5)*
- [ ] No playbook contains merge or precedence instructions about other playbooks. *(AP5)*

## Producers

| # | Test | Requirement |
|---|---|---|
| P1 | An inferred position is marked, and isn't saved until confirmed. | AP1 |
| P2 | A shorthand answer ("aggressive") gets a follow-up about what it means in practice. | AP2 |
| P3 | The complete playbook is shown in plain language, with no machine format, and approved before saving. | AP7 |
| P4 | The producer asks whether anything material is missing before showing the draft. | AP7 |
| P5 | A past outcome isn't turned into a position or instruction without confirmation. | AP3 |
| P6 | No current deadlines, thresholds or case law appear in any field unless requested. | AP4 |
| P7 | A view stated about one situation isn't recorded as a general rule without confirmation, and matter facts are left out. | AP5 |
| P8 | `owner` and `updated_by` are set correctly when someone other than the owner answers. | AP6 |
| P9 | An update is shown as a before-and-after, and the version is incremented. | AP9 |
| P10 | The output validates against the schema. | AP11 |
| P11 | An issue the user's other playbooks already cover reuses their `key`. | AP5 |
| P12 | A guardrail is confirmed explicitly, and a client red line isn't recorded as a guardrail. | AP13 |
| P13 | From a human draft, uncertain classifications are confirmed, gaps aren't filled from general knowledge, and anything left out is reported. | AP14 |
| P14 | Exclusions drawn from example clauses or a test document are confirmed by the person, and no facts from the test document end up in the playbook. | AP15 |

Implementations SHOULD record their results against these checklists in their own test logs.
