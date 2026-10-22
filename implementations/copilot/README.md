# Implementing the playbook specification in Microsoft 365 Copilot

**Status: implementation guide, not yet built or tested.** This maps the [playbook specification](../../spec/) onto Microsoft 365 components, so a firm on Copilot can produce and consume the same playbooks as the Claude reference implementations. Copilot's capabilities and limits change often, and vary by tenant and license. Check each assumption against your own environment.

## Component map

| Spec concept | Microsoft 365 component | Notes |
|---|---|---|
| Playbook files | SharePoint document libraries | Firm-level playbooks (guardrails, task, practice, industry) in a central library. Client and matter playbooks in each client hub or matter site, for example a "Context" library, so they inherit that site's permissions. |
| Canonical object (format §3.3) | Optional: Dataverse table or JSON files alongside the Markdown | Structured storage makes validation and retrieval more reliable than parsing Markdown at run time. |
| Validation (format §11, AP11) | A Power Automate flow on file create or modify, calling the validator through an Azure Function or custom connector | Power Automate can't parse YAML natively, so run `spec/tools/validate.py` (or a port of it) as a service. Alternatively, have the builder agent write the canonical JSON as well, and validate that against `schema/playbook.schema.json`. |
| Consumer (consumer requirements) | A Copilot Studio agent with the playbook libraries as knowledge sources | The agent's instructions implement CR1–CR18. See "Consumer agent" below. |
| Producer (authoring protocol) | A Copilot Studio agent (or topic) that interviews the lawyer | It writes the approved playbook to SharePoint through a Power Automate action. The lawyer only sees plain English. |
| Current law at review time (CR16) | Web grounding, or a licensed legal research connector, if enabled | If neither is available, every `check` question goes to the lawyer on the To confirm list. That's conformant behavior, not a failure. |

## Consumer agent

**Instructions.** Condense the consumer requirements into the agent's instructions, in this priority order:
1. guardrails first;
2. never guess the client;
3. the precedence order (CR6);
4. accepted risk stays visible;
5. business decisions stay with the client;
6. current law researched, not taken from playbooks;
7. state assumptions;
8. "draft for lawyer review."

Instruction length is limited, so keep the requirements terse and put detail in a knowledge document the agent can consult.

**Retrieval risk.** Knowledge sources are retrieved in chunks, so the agent may see part of a playbook rather than the whole thing. This is the biggest threat to conformance. Mitigations:
- keep playbooks small (one practice area or one client per file);
- tell the agent to load every playbook named in the matter in full before analyzing;
- for higher reliability, retrieve canonical JSON through a Power Automate action instead of relying on search.

**Orchestration.** For complex matters, consider one orchestrator agent that gathers the matter's playbooks and facts into a single bundle, with specialist agents (contract review, marketing review) that work from that bundle. This mirrors the context-bundle pattern from the original Copilot pilot.

## Producer agent

- Implement the interview as topics: setup, the interview guide for the playbook type, "anything material we haven't discussed?", the plain-English approval view, then save.
- The approval view must show the complete playbook in plain language (AP7). Generate the Markdown file only after approval.
- Save through a Power Automate action that runs validation before writing, and returns any errors to the conversation.
- Update mode and "learn from a matter" follow AP9 and AP10: show a before-and-after, ask which layer the change belongs to, then save.

## Testing

Run the [conformance checklists](../../spec/conformance.md) against both agents. The consumer tests most likely to fail on a retrieval-based platform are:
- **C2:** not inferring the client from the document;
- **C5:** precedence;
- **C9:** showing accepted risk.

Test those first.
