# The playbook specification

**Schema version 2**

A platform-neutral specification for playbooks: reusable, human-approved expert judgment that AI systems can apply consistently. It was developed for legal work. It doesn't depend on any AI platform. A playbook works the same whether the tool reading it is a Claude skill, a Microsoft Copilot agent, or anything else.

**Playbooks store durable questions and judgment, not ephemeral legal answers.**

## Two parts

| Part | Defines | For |
|---|---|---|
| [Playbook format](playbook-format.md) + [JSON Schema](schema/) | What a playbook is: kinds of judgment, fields, file structure, versioning | Everyone |
| [Authoring protocol](authoring-protocol.md) | How playbooks must be created and changed (AP1–AP15) | Builders, interviewers, editors |

[Conformance](conformance.md) turns both into testable checklists.

## Implementations

The reference implementation is the Claude skill in [`implementations/claude/`](../implementations/claude/). Another platform can implement the authoring protocol and validate its output against the schema.

## Validating playbooks

```bash
pip install -r spec/requirements.txt
python spec/tools/validate.py path/to/playbooks/
```

The validator reads Markdown playbooks, builds the canonical object (format §3.2), validates it against `schema/playbook.schema.json`, and runs the checks in format §7. Its own tests are in `tests/` (`python spec/tests/run_tests.py`).

## Status

Version 2 is a working draft. It replaces version 1's six playbook types with a single kind of playbook (format §8). Changes follow the versioning rules in format §6.
