---
id: test-construction
name: Test construction
schema_version: 2
version: 1
last_reviewed: 2026-10-25
---

```yaml
issues:
  - key: indemnity
    look_for: claims arising out of the work
    check:
      - Whether an anti-indemnity rule limits the clause in the project's state.
    instruction: Flag any indemnity reaching the indemnified party's sole negligence.
  - key: pay-when-paid
    kind: hybrid
    triggers: Payment to a subcontractor depends on payment by the owner.
    market_position:
      subcontractor: Pay-when-paid, not pay-if-paid.
```
