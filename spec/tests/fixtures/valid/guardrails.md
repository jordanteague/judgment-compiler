---
id: test-firm-baseline
name: Test firm baseline
schema_version: 2
version: 1
last_reviewed: 2026-10-25
owner: Test risk partner
---

```yaml
issues:
  - key: unverified-fact
    title: Conclusions resting on unconfirmed facts
    guardrail:
      when: A conclusion depends on an unconfirmed fact.
      action: flag
  - key: engagement-scope
    title: Work outside the engagement
    guardrail:
      when: Advice falls outside the engagement scope.
      action: escalate
      escalate_to: Supervising partner
```
