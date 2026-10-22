# Playbook format

**Schema version 1** · Part of the [playbook specification](README.md)

This document defines what a playbook is and how it's written. It doesn't depend on any AI platform: any tool that can read Markdown and YAML can produce or consume playbooks.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** are used as described in RFC 2119.

---

## 1. Purpose

A playbook records a firm's professional judgment in a form an AI reviewer can apply consistently.

**Playbooks store durable questions and judgment, not ephemeral legal answers.** A playbook says what to look for, why it matters, what needs checking, how the firm approaches it, and what the reviewer should do. It doesn't restate current deadlines, thresholds, statutory text or case law. Those change, and would need constant maintenance. A consuming tool works out the current law at review time ([consumer requirements](consumer-requirements.md), CR16).

| In the playbook (durable) | At review time (current) |
|---|---|
| What should we look for? | What are the relevant facts? |
| Why does it matter? | What does the current law say? |
| How does our firm think about it? | How does the playbook's judgment apply? |
| What should the reviewer do? | What does the lawyer need to verify or decide? |

---

## 2. Playbook types

Each playbook type does a different job. Consumers combine them for each piece of work.

| Type | Job | Required for a consumer to run |
|---|---|---|
| `guardrails` | The firm's professional non-negotiables: what must always be flagged, escalated, or stopped | Yes |
| `task` | How a kind of work is done: steps and deliverables | Yes |
| `practice` | A practice area: issues, triggers, what to check, the firm's approach | No |
| `industry` | Sector issues that general playbooks miss, tagged by practice area | No |
| `client` | Calibration for one client: risk tolerance, positions, red lines, who decides | No |
| `matter` | One piece of work: question, facts, assumptions, decisions, term sheet | No |

There is no firm "house position" on business decisions, because those belong to clients. On legal strategy, a firm MAY record a labeled `firm_view`, which client and matter playbooks override.

### Kinds of statement

Playbooks keep these kinds of statement apart. Producers MUST NOT record one kind in another kind's field.

| Kind | Field |
|---|---|
| Questions to check at review time | `check` |
| Market practice | `market_position`, `approaches` |
| Firm judgment on legal strategy | `firm_view` |
| Reviewer instruction | `instruction` |
| Client or matter preference | `calibration` (`position`, `acceptable`, `never`, `red_line`, `accepts`) |
| Facts | `facts` |
| History | `history` |
| Durable legal principle (optional, rare) | `rule` |

---

## 3. File structure

### 3.1 Container

A playbook is a UTF-8 Markdown file (`.md`) made of:

1. **Front matter:** a YAML mapping between two lines containing only `---`, at the very start of the file.
2. **Body:** one or more fenced code blocks with the info string `yaml`.

Other Markdown in the file (headings, prose) is commentary. Consumers MUST NOT give it meaning. They MAY show it to people.

### 3.2 Body content

| Type | Body |
|---|---|
| `guardrails`, `practice`, `industry` | One or more `yaml` blocks, each a **list**. The content is the concatenation of all the lists in file order. |
| `task`, `client`, `matter` | Exactly one `yaml` block, holding a **mapping**. |

### 3.3 Canonical object

For validation and storage, a playbook corresponds to a **canonical object**: the front matter fields, plus a `content` field holding the body content.

```yaml
type: practice
id: federal-litigation
schema_version: 1
version: 1
last_reviewed: 2026-10-22
content:
  - key: removal
    ...
```

Systems that prefer structured storage (a database, a document store, JSON files) MAY store the canonical object directly. Producers that do SHOULD still be able to render the Markdown form for people. The JSON Schema in [`schema/playbook.schema.json`](schema/playbook.schema.json) validates the canonical object.

### 3.4 Identity and layout

- A playbook is identified by its `type` and `id`.
- Consumers MUST find playbooks by their front matter, not by file name or folder.
- A suggested layout is `playbooks/<type>/<id>.md`, with guardrails at `playbooks/guardrails.md`. It isn't required.

---

## 4. Front matter

| Field | Required | Meaning |
|---|---|---|
| `type` | MUST | `guardrails`, `task`, `practice`, `industry`, `client` or `matter` |
| `id` | MUST | Unique within its type. Lowercase kebab-case. |
| `version` | MUST | Integer, starting at 1. Incremented on every substantive change. |
| `last_reviewed` | MUST | ISO date of the last substantive review. |
| `schema_version` | SHOULD | The version of this format the playbook follows. Currently `1`. |
| `name` | SHOULD | Human-readable name. |
| `owner` | SHOULD | The person or group substantively responsible, not necessarily whoever answered the questions. |
| `updated_by` | MAY | Who made the latest change, if not the owner. |
| `expires` | MAY | ISO date after which consumers MUST NOT use the playbook. |

---

## 5. Issues (practice and industry playbooks)

An issue is the shared unit. Practice and industry playbooks define issues; client and matter playbooks calibrate them by `key`.

```yaml
- key: classification
  title: Exempt / non-exempt classification
  kind: legal
  applies_to:
    tasks: [contract-review, advice-memo]
    practice_areas: [employment]        # industry playbooks only
  why: Misclassification can create significant back-pay and benefits exposure.
  triggers: The client is setting or changing a role's pay basis or overtime status.
  look_for: Whether the duties and pay structure support the classification used.
  check:
    - Whether the role meets the current salary and duties tests, federal and state.
  firm_view:
    default: Recommend restructuring a role before reclassifying it.
    unless: The duties are already primarily managerial and documented.
    source: firm-default
  instruction: Flag any exempt classification resting on job title alone.
  default_severity: high
```

| Field | Required | Meaning |
|---|---|---|
| `key` | MUST | Stable identifier, kebab-case. Firm-specific keys SHOULD start with `x-`. |
| `applies_to.tasks` | MUST | Task ids this issue applies to. |
| `applies_to.practice_areas` | MUST in industry playbooks | Practice-area ids the issue applies to. Not used in practice playbooks. |
| `title` | SHOULD | Human-readable name. |
| `kind` | SHOULD | `legal`, `commercial` (a business decision) or `hybrid` (a business decision with legal consequences). |
| `why` | SHOULD | Practical significance. It MUST NOT state legal requirements, deadlines, thresholds or legal consequences. |
| `triggers` | SHOULD, for advice tasks | Facts or circumstances that should make the reviewer consider the issue. |
| `look_for` | SHOULD, for review tasks | Language or terms to look for in a document. |
| `check` | SHOULD | Legal and factual questions to investigate at review time, phrased as questions, not answers. |
| `firm_view` | MAY | The firm's judgment on legal strategy: `default`, `unless`, optional `source`. It MUST NOT appear on `commercial` issues. |
| `instruction` | MAY | What the reviewer should flag, verify, recommend or escalate. |
| `market_position` | MAY | Market practice for documents, keyed by role label (`buyer`, `subcontractor`, ...). |
| `approaches` | MAY | Market practice for advice, keyed by risk tolerance: `low`, `moderate`, `high`. |
| `default_severity` | SHOULD | `low`, `medium` or `high`. |
| `jurisdiction_note` | MAY | Jurisdiction questions to check, phrased as questions. |
| `rule` | MAY | A durable legal principle. Use it rarely, only where the firm wants it recorded. Consumers MUST treat it as unverified background (CR16). |

When an industry issue and a practice issue share a `key`, consumers merge them (CR5). The industry entry MAY omit fields it inherits.

**Durability rule:** time-sensitive legal propositions MUST NOT appear in `why`, `firm_view`, `instruction`, `market_position`, `approaches` or notes. They belong in `check`, as questions.

---

## 6. Guardrails

The body is a list of guardrail items.

| Field | Required | Meaning |
|---|---|---|
| `id` | MUST | Identifier. |
| `trigger` | MUST | The condition that applies the guardrail. |
| `action` | MUST | `flag` (always shown), `escalate` (shown, and needs sign-off), or `stop` (no work product). |
| `escalate_to` | MUST when `action` is `escalate` | The role that must sign off. |
| `rationale` | SHOULD | Why the guardrail exists. |

---

## 7. Task playbooks

| Field | Required | Meaning |
|---|---|---|
| `task` | MUST | Task id, matching `applies_to.tasks` in issues. |
| `task_type` | MUST | `review` (a document), `draft` (from instructions or a term sheet) or `advise` (a question and facts). |
| `steps` | MUST | An ordered list. Each step has `id` (MUST), `do` (MUST) and `uses` (MAY: slots from `issues`, `calibration`, `guardrails`, `facts`, `term-sheet`). |
| `deliverable` | SHOULD | `outputs` (what the task produces) and `sections` (their order). |
| `redline_style`, `term_sheet_rule` | MAY | Style rules for review and draft tasks. |

Steps are the backbone. Other playbooks only fill the slots that steps name.

---

## 8. Client playbooks

| Field | Required | Meaning |
|---|---|---|
| `industry` | SHOULD | Industry playbook id. Selects the industry playbook. |
| `role` | MAY | The client's usual role. |
| `risk_tolerance` | SHOULD | `low`, `moderate` or `high`. Selects `approaches` in advice. |
| `negotiation_style` | MAY | What the client fights for and lets go, in operational terms. |
| `decision_makers` | SHOULD | A map of decision area to person or role. |
| `communication` | MAY | How the client wants advice delivered. |
| `facts` | MAY | Things true about the client, each with its source. |
| `calibration` | MAY | Calibration items (below). |

### Calibration items (client and matter playbooks)

| Field | Required | Meaning |
|---|---|---|
| `key` | MUST | An issue key from a practice or industry playbook. |
| `position` | MAY | The preferred position. |
| `acceptable` | MAY | A list of fallbacks that are not preferred but routinely accepted. |
| `never` | MAY | A list of terms that are never acceptable. |
| `red_line` | MAY | `true` makes any departure from `position` unacceptable. |
| `accepts` | MAY | A risk the client has decided to take. It never hides the issue (CR8). |
| `severity` | MAY | Overrides the issue's severity for this client. |
| `instruction` | MAY | What the reviewer should do for this client. |
| `history` | MAY | Past events. Context only, never a position or instruction. |
| `note` | MAY | Context that fits no other field. |
| `source` | SHOULD | `stated`, `client-instruction`, `prior-matter`, `firm-default` or `matter-specific`. |

---

## 9. Matter playbooks

| Field | Required | Meaning |
|---|---|---|
| `client` | MUST | Client playbook id, or a list of ids for joint clients. |
| `represents` | SHOULD | Every role label our client holds in this matter. |
| `practice_area` | SHOULD | Practice playbook id. |
| `engagement_scope` | SHOULD | What the firm is engaged to do, in one sentence. |
| `conflicts_cleared` | SHOULD | Adverse-party names, exactly as they appear in the documents. Empty if there's no adverse party. |
| `question` | MAY | The question, for advice matters. |
| `facts` | MAY | Facts relied on, each with its source. |
| `assumptions` | MAY | Facts relied on but not confirmed. |
| `decisions` | MAY | `settled` and `open` business decisions. |
| `term_sheet` | MAY | `settled` and `open` commercial terms, for deals. Each has a `key`, and a `value` or `note`. |
| `calibration` | MAY | Departures from the client playbook for this matter only. |
| `notes` | MAY | Other context. |

---

## 10. Versioning and extensions

### 10.1 Playbook versions
A producer MUST increment `version` and update `last_reviewed` on every substantive change.

### 10.2 Schema versions
- **Within a schema version,** changes are additive only: new optional fields, or new allowed values that don't change existing meanings.
- **A new schema version** is required for any change that removes a field, makes a field required, or changes what a field means.
- **Consumers** MUST report any playbook that declares a `schema_version` higher than they support. They SHOULD then use the fields they recognize.

### 10.3 Extensions
- Producers MAY add fields whose names start with `x-`, at any level. Consumers that don't recognize an `x-` field MUST ignore it, and MUST NOT fail.
- Consumers SHOULD warn about unrecognized fields that don't start with `x-`.
- Firm-specific issue keys SHOULD start with `x-`.

---

## 11. Validation

[`schema/playbook.schema.json`](schema/playbook.schema.json) is a JSON Schema (draft 2020-12) covering the canonical object of every playbook type. [`tools/validate.py`](tools/validate.py) reads Markdown playbooks, builds the canonical object, and validates it.

JSON Schema can't check every rule. The validator also checks:
- `firm_view` is absent from `commercial` issues;
- industry issues carry `practice_areas`;
- calibration keys exist in the loaded practice and industry playbooks.

The **durability rule** (no time-sensitive law in narrative fields) needs judgment. It's a producer obligation ([authoring protocol](authoring-protocol.md), AP4), not something the schema can enforce.
