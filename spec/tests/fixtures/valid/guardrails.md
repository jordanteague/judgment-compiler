---
type: guardrails
id: test-firm
schema_version: 1
version: 1
last_reviewed: 2026-10-22
---

```yaml
- id: unverified-fact
  trigger: A conclusion depends on an unconfirmed fact.
  action: flag
- id: out-of-scope
  trigger: Advice falls outside the engagement scope.
  action: escalate
  escalate_to: Supervising partner
```
