# judgment-compiler

**Turns an expert's tacit judgment into structured, reusable playbooks an AI can apply.**

Expert judgment often exists only in experienced practitioners' heads. judgment-compiler is a structured method for eliciting that judgment, by interviewing the expert in plain language or by working from a playbook they've already drafted, and turning it into instructions an AI system can follow and a person can inspect. Nobody writes YAML.

It was developed for legal work, and law is the only domain it has been tried in.

## Why

Law firms have had playbooks forever: checklists, position papers, a partner's markup notes. They're written for other lawyers, so they lean on shared context. "Push back on the cap." "Use judgment on indemnity." "Standard market terms." A junior associate fills the gaps by asking down the hall. An AI can't.

For an AI to apply a lawyer's judgment consistently, that judgment has to be explicit and operational:
- **When does the issue arise?**
- **What needs checking?**
- **What's the default, and what changes it?**
- **What should the AI do?**

The judgment also has to be separated from things that look similar but behave differently: current law, market practice, a client's preference, a lesson from one past deal.

That isn't a skill lawyers are trained in, or naturally inclined to practice. Expert judgment is mostly tacit. Lawyers know what they'd do in a given case far better than they can state the rule they follow. Asking them to write prompts or structured files mostly produces the same shorthand as a traditional playbook, in a new format.

**judgment-compiler bridges that gap.** The lawyer talks, the way they'd brief a colleague, reacts to examples, and corrects the result. The compiler does the translation:
- it asks the follow-up a good associate would ask ("aggressive how?", "when wouldn't you?");
- it shows near-miss example clauses ("flag or not, and why?") to draw out when an issue doesn't apply;
- it keeps views, positions, red lines, instructions, guardrails and history apart;
- it leaves time-sensitive law out, as questions to check at the time of the work;
- it shows the lawyer the complete result in plain English to approve;
- it validates the output before anything is saved.

## What a playbook holds

A playbook is reusable expert judgment about a class of problems, such as contract review, federal litigation, or a sector's issues. It's a list of issues, and each issue can record:

| | |
|---|---|
| **When it arises** | triggers, language to look for, and when it doesn't apply |
| **What to check** | questions to research at the time of the work, never the answers |
| **The expert's view** | a default, and the exceptions that change it |
| **Positions** | preferred, acceptable alternatives, red lines, risks deliberately accepted |
| **What the AI should do** | instructions to flag, verify, recommend or escalate |
| **Guardrails** | non-negotiable rules: always flag, escalate to a named role, or stop |
| **Context** | why it matters, market practice, past outcomes (never treated as rules) |
| **Provenance** | whose judgment each position is: the firm's, a client's standing instruction, or learned from a past matter |

**Playbooks store durable questions and judgment, not ephemeral legal answers,** so they don't go stale when a rule changes. A playbook is also not the facts of a particular matter, and not a step-by-step procedure.

## Why "compiler"

| Compiler stage | judgment-compiler |
|---|---|
| **Source** | The expert's tacit judgment: defaults, exceptions, priorities, what to watch for. It's drawn out by interview, with follow-ups until an AI could act on each answer. |
| **Intermediate representation** | The canonical object ([format §3.2](spec/playbook-format.md)): typed fields that keep each kind of judgment apart |
| **Type checking** | Validation against [JSON Schema](spec/schema/playbook.schema.json), plus checks the schema can't express ([validator](spec/tools/validate.py)) |
| **Semantic rules** | The [authoring protocol](spec/authoring-protocol.md): nothing inferred is saved unconfirmed, no time-sensitive law, no silent generalization, approval of the complete playbook in plain language |
| **Target** | A Markdown playbook with YAML blocks: readable by people, parseable by any AI system |

## How an interview works

1. **One topic at a time**, no more than three questions per turn, with multiple choice wherever it fits. "Skip" and "don't know" are fine.
2. **Judgment, not law.** It spends the lawyer's time on defaults, exceptions, priorities and what to watch for. It doesn't ask them to recite rules.
3. **Answers made operational.** Shorthand like "aggressive" or "we usually accept it" gets one follow-up, so an AI could actually act on it.
4. **Examples, not just recall.** It asks for language the lawyer has actually seen, and shows near-miss clauses to find when an issue shouldn't be flagged.
5. **Kinds of judgment kept apart.** Views, positions, red lines, instructions, guardrails, market practice and history each go in their own field. A past outcome never quietly becomes a rule.
6. **"Anything material we haven't discussed?"** is always asked before the draft.
7. **The complete playbook in plain English.** That's the approval step, and the lawyer can still add, remove or change anything. Nothing is saved before approval.
8. **Validated and saved.** Every playbook is checked before it's saved, including for time-sensitive law that has crept in.

**Starting from a draft.** Given an existing playbook (a Word document, a checklist, a partner's notes), it sorts each statement into its field, asks only about ambiguities and gaps, and reports anything it couldn't place. The same safeguards and approval step apply.

**Testing on a document.** After approval, the playbook can be applied as written to a sample contract. The lawyer marks each flag right, false alarm, or miss, and each mistake becomes a follow-up question and a proposed update. Interviews capture what an expert can articulate. Examples and tests capture what they recognize but wouldn't think to say.

It also runs **updates**, approved as a plain-English before-and-after, and **lessons from experience**: an outcome from one deal becomes a rule only if the lawyer says so.

## Designed, demonstrated, and open

**Designed.** The interview method, the separation of kinds of judgment, the plain-language approval step, the authoring protocol, and validation are what the system is built to do. They're specified in [`spec/`](spec/) and implemented in the Claude skill.

**Demonstrated so far:**
- The skill has been run in live interviews. What those interviews exposed (shorthand accepted without follow-up, law creeping into narrative fields, too much confirmation) is logged in [`TESTING.md`](TESTING.md), along with the changes it led to.
- The validator's tests pass: valid playbooks are accepted, and each invalid case is rejected for the intended reason.
- Interviews haven't yet been re-run under the current format (schema version 2), so the repo has no sample playbook yet.

**Open questions:**
- Whether an AI applies a compiled playbook more consistently or more accurately than it applies a traditional playbook, or a well-written prompt. This repo contains no evaluation of that.
- How much interview time the method saves or costs, compared with lawyers writing playbooks themselves.
- How well the method carries over to experts outside law.

## The broader problem

Capturing expert judgment is only one part of using expert knowledge in AI systems. A working system also has to combine reusable playbooks with task-specific facts, client preferences, precedents and governing sources. That problem isn't addressed here.

## Install

**In Claude (web or desktop app):** add `implementations/claude/skills/judgment-compiler/SKILL.md` as a custom skill in Claude's settings.

**In Claude Code:**

```bash
cp -r implementations/claude/skills/judgment-compiler ~/.claude/skills/
```

**On other platforms:** implement the [authoring protocol](spec/authoring-protocol.md) and validate output against the [schema](spec/schema/playbook.schema.json).

## Use

> Help me build a playbook for federal court litigation.
>
> Let's write down the firm's baseline guardrails.
>
> Here's our existing construction checklist. Turn it into a playbook.
>
> Here's what happened on the Voltline deal. Should any of it change our contract review playbook?

Validate a playbook yourself:

```bash
pip install -r spec/requirements.txt
python spec/tools/validate.py path/to/playbooks/
python spec/tests/run_tests.py
```

## Trying it on another domain

The method isn't specific to law, but the skill's wording is. To try it with, say, clinical protocols or underwriting:
- Use the "Issues" interview guide as it stands. Triggers, checks, views with exceptions, positions, red lines and guardrails are general ideas.
- Read "current law" as whatever in that domain changes faster than the judgment: guidelines, rates, regulations. It still belongs in `check` questions.
- Ignore `kind` (legal, commercial, hybrid) and the business-decision rule if they don't fit, and use `x-` fields for anything the domain needs that the format lacks.

Start with: "Interview me to build a playbook for [your area]. I'm the expert."

## Contents

| Path | What it is |
|---|---|
| `spec/` | The platform-neutral specification: [format](spec/playbook-format.md), [JSON Schema](spec/schema/playbook.schema.json), [authoring protocol](spec/authoring-protocol.md), [conformance checklists](spec/conformance.md), and a [validator](spec/tools/validate.py) with tests |
| `implementations/claude/skills/judgment-compiler/SKILL.md` | The Claude skill (reference implementation) |
| `examples/playbooks/` | Sample playbooks, once interviews are re-run under schema version 2 |
| `TESTING.md` | Test log: findings from live interviews and the changes they led to |

Playbooks guide AI-assisted legal work. They're not legal advice, and everything an AI produces from them is a draft for a lawyer to review.

## License

[MIT](LICENSE)
