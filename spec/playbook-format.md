# Playbook format

**Schema version 2** · Part of the [playbook specification](README.md)

This document defines what a playbook is and how it's written. It doesn't depend on any AI platform: any tool that can read Markdown and YAML can produce or use playbooks.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** are used as described in RFC 2119.

---

## 1. Purpose

A playbook is reusable expert judgment about a class of problems, in a form an AI system can apply consistently.

**Playbooks store durable questions and judgment, not ephemeral legal answers.** A playbook says what to look for, why it matters, what needs checking, how the expert approaches it, and what the AI should do. It doesn't restate current deadlines, thresholds, statutory text or case law. Those change, and would need constant maintenance. The system using the playbook works out the current law at the time of the work.

| In the playbook (durable) | At the time of the work (current) |
|---|---|
| What should we look for? | What are the relevant facts? |
| Why does it matter? | What does the current law say? |
| How do we think about it? | How does the playbook's judgment apply? |
| What should the AI do? | What does the lawyer need to verify or decide? |

**What a playbook isn't.**
- **Not task context.** It holds no facts about a particular matter, client or transaction.
- **Not a procedure.** It says how to evaluate what the AI encounters, not what job to do or in what order.
- **Not self-selecting.** It doesn't declare where it applies or how it relates to other playbooks.

---

## 2. Kinds of judgment

A playbook is a list of **issues**. Each issue keeps different kinds of judgment in different fields, because they behave differently: a firm's view can be overridden by a client's position, market practice is not a recommendation, and a past outcome is not a rule. Producers MUST NOT record one kind in another kind's field.

| Kind | Field |
|---|---|
| When the issue arises | `triggers`, `look_for` |
| When it doesn't apply | `not_when` |
| Why it matters | `why` |
| Questions to check at the time of the work | `check`, `jurisdiction_note` |
| Market practice | `market_position`, `approaches` |
| Expert or firm view, with its exceptions | `firm_view` (`default`, `unless`) |
| Preferred position | `position` |
| Acceptable alternatives and fallbacks | `acceptable` |
| Red lines | `never`, `red_line` |
| Risks deliberately accepted | `accepts` |
| Instructions for the AI | `instruction` |
| Non-negotiable rules and escalation conditions | `guardrail` |
| Past outcomes | `history` |
| Whose judgment it is | `source`, plus `owner` and `updated_by` |
| Durable legal principle (optional, rare) | `rule` |

**Stable keys.** Each issue has a `key`. Producers SHOULD reuse the keys already used in the user's other playbooks for the same issue, so related guidance is recognizable as such. A shared key means the guidance is related, not that one replaces the other.

---

## 3. File structure

### 3.1 Container

A playbook is a UTF-8 Markdown file (`.md`) made of:

1. **Front matter:** a YAML mapping between two lines containing only `---`, at the very start of the file.
2. **Body:** one or more fenced code blocks with the info string `yaml`, each holding an `issues:` list.

Lists from several blocks are concatenated in file order, so issues can be grouped under Markdown headings. Other Markdown in the file (headings, prose) is commentary. Tools MUST NOT give it meaning. They MAY show it to people.

### 3.2 Canonical object

For validation and storage, a playbook corresponds to a **canonical object**: the front matter fields, plus a `content` field holding the combined body.

```yaml
id: contract-review
schema_version: 2
version: 1
last_reviewed: 2026-10-25
content:
  issues:
    - key: indemnity
      ...
```

Systems that prefer structured storage (a database, a document store, JSON files) MAY store the canonical object directly. Producers that do SHOULD still be able to render the Markdown form for people. The JSON Schema in [`schema/playbook.schema.json`](schema/playbook.schema.json) validates the canonical object.

### 3.3 Identity

A playbook is identified by its `id`, which MUST be unique among the playbooks a firm uses. Tools MUST find playbooks by their front matter, not by file name or folder.

---

## 4. Front matter

| Field | Required | Meaning |
|---|---|---|
| `id` | MUST | Unique identifier. Lowercase kebab-case. |
| `version` | MUST | Integer, starting at 1. Incremented on every substantive change. |
| `last_reviewed` | MUST | ISO date of the last substantive review. |
| `schema_version` | SHOULD | The version of this format the playbook follows. Currently `2`. |
| `name` | SHOULD | Human-readable name. |
| `owner` | SHOULD | The person or group substantively responsible, not necessarily whoever answered the questions. |
| `updated_by` | MAY | Who made the latest change, if not the owner. |
| `expires` | MAY | ISO date after which the playbook MUST NOT be used. |
| `description` | MAY | One or two sentences on what the playbook covers. |
| `tags` | MAY | Free-form labels for finding playbooks. They carry no meaning for tools that apply the playbook. |

---

## 5. Issues

Only `key` is required, so an entry can be as small as one red line, or as full as a complete treatment of the issue.

```yaml
issues:
  - key: indemnity
    title: Indemnification
    kind: legal
    severity: high
    why: Can shift the largest losses in the deal, often outside the cap.
    look_for: indemnify, defend and hold harmless
    check:
      - Whether the indemnity reaches the indemnified party's own negligence, and whether that is enforceable as drafted.
    firm_view:
      default: Recommend mutual indemnities.
      unless: Only one party performs work under the contract.
      source: stated
    instruction: Flag any indemnity outside the liability cap.
    guardrail:
      when: Our client's indemnity is uncapped.
      action: flag
```

**Identity and recognition**

| Field | Required | Meaning |
|---|---|---|
| `key` | MUST | Stable identifier, kebab-case. Firm-specific keys SHOULD start with `x-`. Unique within the playbook. |
| `title` | SHOULD | Human-readable name. |
| `kind` | SHOULD | `legal`, `commercial` (a business decision) or `hybrid` (a business decision with legal consequences). |
| `severity` | SHOULD | `low`, `medium` or `high`. |
| `why` | SHOULD | Practical significance. It MUST NOT state legal requirements, deadlines, thresholds or legal consequences. |
| `triggers` | MAY | Facts or circumstances that should make the AI consider the issue. |
| `look_for` | MAY | Language or terms to look for in a document. |
| `not_when` | MAY | Situations that look like the issue but shouldn't be flagged (for example, where the counterparty, not the client, holds the role). |

**Current law (asked, not answered)**

| Field | Required | Meaning |
|---|---|---|
| `check` | SHOULD | Legal and factual questions to investigate at the time of the work, phrased as questions, not answers. |
| `jurisdiction_note` | MAY | Jurisdiction questions to check, phrased as questions. |
| `rule` | MAY | A durable legal principle. Use it rarely, only where the owner wants it recorded. Tools MUST treat it as unverified background. |

**Judgment**

| Field | Required | Meaning |
|---|---|---|
| `market_position` | MAY | Market practice for documents, keyed by role label (`buyer`, `subcontractor`, ...). |
| `approaches` | MAY | Market practice for advice, keyed by risk appetite: `low`, `moderate`, `high`. |
| `firm_view` | MAY | Judgment on legal strategy: `default`, `unless`, optional `source`. It MUST NOT appear on `commercial` issues. |
| `position` | MAY | The preferred position. |
| `acceptable` | MAY | Alternatives that are not preferred but routinely accepted. |
| `never` | MAY | Terms that are never acceptable. |
| `red_line` | MAY | `true` makes any departure from `position` unacceptable. |
| `accepts` | MAY | A risk that has been deliberately accepted. It never hides the issue. |
| `instruction` | MAY | What the AI should flag, verify, recommend or escalate. |
| `history` | MAY | Past outcomes. Context only, never a position or instruction. |
| `note` | MAY | Context that fits no other field. |
| `source` | SHOULD, when any preference is set | `stated` (by the person interviewed), `client-instruction`, `prior-matter` or `firm-default`. |

**No house positions on business decisions.** On a `commercial` issue, a `position`, `acceptable`, `never`, `red_line` or `accepts` MUST NOT have `source: firm-default`. Business decisions belong to clients. On legal strategy, a firm MAY record a `firm_view`.

**Durability rule:** time-sensitive legal propositions MUST NOT appear in `why`, `firm_view`, `instruction`, `market_position`, `approaches`, `guardrail` or notes. They belong in `check`, as questions.

### 5.1 Guardrails

A guardrail is a professional rule that applies whatever else the playbook or the client says. It decides what must be **shown**, escalated or stopped, never what is acceptable.

| Field | Required | Meaning |
|---|---|---|
| `when` | MUST | The condition that applies the guardrail. It MAY be narrower than the issue (only an *uncapped* indemnity, not every indemnity). |
| `action` | MUST | `flag` (always shown), `escalate` (shown, and needs sign-off), or `stop` (no work product). |
| `escalate_to` | MUST when `action` is `escalate` | The role that must sign off. |
| `rationale` | SHOULD | Why the guardrail exists. |

`guardrail` MAY be a single item or a list. Rules that aren't about one issue are issues of their own, for example `key: conflicts-cleared` with a `stop` guardrail. A firm's firm-wide guardrails SHOULD live in one baseline playbook.

A guardrail is not an `instruction`. An instruction is judgment that can be weighed against other guidance. A guardrail is non-negotiable.

---

## 6. Versioning and extensions

### 6.1 Playbook versions
A producer MUST increment `version` and update `last_reviewed` on every substantive change.

### 6.2 Schema versions
- **Within a schema version,** changes are additive only: new optional fields, or new allowed values that don't change existing meanings.
- **A new schema version** is required for any change that removes a field, makes a field required, or changes what a field means.
- **Tools** MUST report any playbook that declares a `schema_version` higher than they support. They SHOULD then use the fields they recognize.

### 6.3 Extensions
- Producers MAY add fields whose names start with `x-`, at any level. Tools that don't recognize an `x-` field MUST ignore it, and MUST NOT fail.
- Tools SHOULD warn about unrecognized fields that don't start with `x-`.

---

## 7. Validation

[`schema/playbook.schema.json`](schema/playbook.schema.json) is a JSON Schema (draft 2020-12) for the canonical object. [`tools/validate.py`](tools/validate.py) reads Markdown playbooks, builds the canonical object, and validates it.

JSON Schema can't check every rule. The validator also checks:
- playbook ids are unique, and issue keys are unique within a playbook;
- no `type` field or `schema_version: 1` (§8);
- no firm-default preference on a `commercial` issue (§5).

The **durability rule** (no time-sensitive law in narrative fields) needs judgment. It's a producer obligation ([authoring protocol](authoring-protocol.md), AP4), not something the schema can enforce.

---

## 8. Changes from schema version 1

Version 1 classified playbooks into six types (`guardrails`, `task`, `practice`, `industry`, `client`, `matter`) and gave them a fixed layer order. Version 2 has one kind of playbook, and leaves task context, procedure and selection out of scope.

| Version 1 | Version 2 |
|---|---|
| `type` | Removed. Describe the playbook in `name`, `description` and `tags`. |
| Practice and industry issues (a list body) | `issues:` section. `default_severity` becomes `severity`. |
| `applies_to` | Removed. A playbook doesn't declare where it applies. |
| Client `calibration` items (positions, fallbacks, red lines, accepted risks) | Issue entries with the same `key`. |
| Guardrails playbook items (`id`, `trigger`, `action`) | Issues with a `guardrail` field (`when`, `action`). |
| Client profile, matter facts, term sheets, engagement details | Removed: task context, out of scope. |
| Task playbooks | Removed: procedure, out of scope. |
