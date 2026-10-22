# judgment-compiler

**Compiles a lawyer's professional judgment into structured playbooks an AI can apply consistently.**

The compiler interviews the lawyer in plain language. Nobody writes YAML.

**Playbooks store durable questions and judgment, not ephemeral legal answers.** A playbook captures what to look for, why it matters, what needs checking, how the firm approaches it, and what an AI reviewer should do. Current law is left for the review tool to research at the time of review, so playbooks don't go stale when a rule changes.

## Why "compiler"

| Compiler stage | judgment-compiler |
|---|---|
| **Source** | The lawyer's tacit judgment: defaults, exceptions, priorities, what to watch for. It's drawn out by interview, with follow-ups until a reviewer could act on each answer. |
| **Intermediate representation** | The canonical object ([format §3.3](spec/playbook-format.md)): typed fields that keep facts, history, preferences, firm judgment and reviewer instructions apart |
| **Type checking** | Validation against [JSON Schema](spec/schema/playbook.schema.json), plus cross-playbook checks ([validator](spec/tools/validate.py)) |
| **Semantic rules** | The [authoring protocol](spec/authoring-protocol.md): nothing inferred is saved unconfirmed, no time-sensitive law in narrative fields, no silent promotion between layers, approval of the complete playbook in plain language |
| **Targets** | Markdown for Claude ([full-stack-reviewer](https://github.com/jordanteague/full-stack-reviewer)); structured data for platforms like Microsoft 365 Copilot ([guide](implementations/copilot/)) |

Everything is defined in a **platform-neutral specification** ([`spec/`](spec/)). This repo's Claude skill is the reference implementation for creating playbooks, and full-stack-reviewer is the reference implementation for using them.

**Beyond law.** Nothing in the method is specific to law: interviewing an expert, separating durable judgment from current facts, plain-language approval, and validation would carry over to other expert domains. Law is the first domain it's been applied to and tested in.

---

## What it builds

| Playbook | Captures |
|---|---|
| **Practice area** | Issues to watch for, what to check, the firm's defaults and exceptions, what the reviewer should do |
| **Industry** | Sector issues general playbooks miss, tagged by the practice areas they apply to |
| **Client** | Risk appetite, who decides, negotiating style, positions, red lines, accepted risks, history |
| **Matter** | The question or deal, facts and where they came from, assumptions, term sheet, departures from the client's usual approach |
| **Task** | How the firm does a kind of work: steps, deliverables, style |
| **Guardrails** | The firm's professional non-negotiables |

## How an interview works

1. **One topic at a time**, no more than three questions per turn, with multiple choice wherever it fits. "Skip" and "don't know" are fine.
2. **Judgment, not law.** It spends the lawyer's time on defaults, exceptions, priorities and what to watch for. It doesn't ask them to recite rules.
3. **Answers made operational.** Shorthand like "aggressive" or "we usually accept it" gets one follow-up, so a reviewer could actually act on it.
4. **Kinds of knowledge kept apart.** Facts, history, preferences, reviewer instructions, market practice and firm judgment each go in their own field. A past outcome never quietly becomes a rule.
5. **"Anything material we haven't discussed?"** is always asked before the draft.
6. **The complete playbook in plain English.** That's the approval step, and the lawyer can still add, remove or change anything. Nothing is saved before approval.
7. **Validated and saved.** Every playbook is checked before it's saved, including for time-sensitive law that has crept in.

It also runs **updates**, approved as a plain-English before-and-after, and **lessons from a matter**. Each lesson is classified as matter-only, client-wide, or practice-wide, so a one-off negotiation result never silently becomes a general client position.

## Install

**In Claude (web or desktop app):** add `implementations/claude/skills/judgment-compiler/SKILL.md` as a custom skill in Claude's settings.

**In Claude Code:**

```bash
cp -r implementations/claude/skills/judgment-compiler ~/.claude/skills/
```

**On other platforms:** implement the [authoring protocol](spec/authoring-protocol.md) and validate output against the [schema](spec/schema/playbook.schema.json). See the [Copilot guide](implementations/copilot/) for one mapping.

## Use

> Help me build a playbook for federal court litigation.
>
> We've taken on a new client. Set up their playbook.
>
> Here's what happened on the Voltline deal. Should any of it change our playbooks?

## Contents

| Path | What it is |
|---|---|
| `spec/` | The platform-neutral specification: [format](spec/playbook-format.md), [JSON Schema](spec/schema/playbook.schema.json), [consumer requirements](spec/consumer-requirements.md), [authoring protocol](spec/authoring-protocol.md), [conformance checklists](spec/conformance.md), and a [validator](spec/tools/validate.py) with tests |
| `implementations/claude/skills/judgment-compiler/SKILL.md` | The Claude skill (reference implementation) |
| `implementations/copilot/` | Guide to implementing the specification in Microsoft 365 Copilot |
| `examples/playbooks/` | Sample playbooks, each generated by this skill in a real interview |
| `TESTING.md` | Test log: findings from live interviews and the changes they led to |

## Status

Being tested in live interviews. The first sample, a federal court litigation practice playbook, is in review. Known issues and next steps are in `TESTING.md`.

Playbooks guide AI-assisted legal work. They're not legal advice, and everything a review tool produces from them is a draft for a lawyer to review.

## License

[MIT](LICENSE)
