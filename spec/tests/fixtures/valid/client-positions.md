---
id: test-client-positions
name: Test client positions
schema_version: 2
version: 1
last_reviewed: 2026-10-25
owner: Test relationship partner
---

```yaml
issues:
  - key: indemnity
    position: Mutual, capped at fees paid.
    acceptable: [Cap at twice fees paid.]
    never: [Uncapped indemnity for the counterparty's own negligence.]
    accepts: Indemnity for its own employees' injuries, uncapped.
    history: Something that happened on an earlier deal.
    source: client-instruction
  - key: price
    kind: commercial
    position: Fixed price only.
    source: client-instruction
```
