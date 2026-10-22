# The playbook specification

**Schema version 1**

A platform-neutral specification for legal playbooks: structured records of a firm's professional judgment that AI tools can apply consistently. It doesn't depend on any AI platform. A playbook works the same whether the tool reading it is a Claude skill, a Microsoft Copilot agent, or anything else.

**Playbooks store durable questions and judgment, not ephemeral legal answers.**

## Three parts

| Part | Defines | For |
|---|---|---|
| [Playbook format](playbook-format.md) + [JSON Schema](schema/) | What a playbook is: types, fields, file structure, versioning | Everyone |
| [Consumer requirements](consumer-requirements.md) | How a tool must combine playbooks to do legal work (CR1–CR18) | Review tools |
| [Authoring protocol](authoring-protocol.md) | How playbooks must be created and changed (AP1–AP12) | Builders, interviewers, editors |

[Conformance](conformance.md) turns all three into testable checklists.

## Implementations

| Implementation | Role | Platform |
|---|---|---|
| judgment-compiler ([`implementations/claude/`](../implementations/claude/)) | Producer (reference) | Claude |
| [full-stack-reviewer](https://github.com/jordanteague/full-stack-reviewer) | Consumer (reference) | Claude |
| [Copilot implementation guide](../implementations/copilot/) | Producer and consumer (guide only) | Microsoft 365 Copilot |

## Validating playbooks

```bash
pip install -r spec/requirements.txt
python spec/tools/validate.py path/to/playbooks/
```

The validator reads Markdown playbooks, builds the canonical object (format §3.3), validates it against `schema/playbook.schema.json`, and runs the cross-playbook checks in format §11. Its own tests are in `tests/` (`python spec/tests/run_tests.py`).

## Status

Version 1 is a working draft, developed alongside the Claude reference implementations and tested in live interviews. Changes follow the versioning rules in format §10.
