---
type: practice
id: test-practice
schema_version: 1
version: 1
last_reviewed: 2026-10-22
x-firm-code: P-01
---

```yaml
- key: example-issue
  kind: legal
  applies_to: { tasks: [test-advice] }
  why: Can materially affect the outcome.
  triggers: The facts involve the example situation.
  check:
    - Whether the example rule currently applies.
  firm_view:
    default: Recommend the cautious course.
    unless: The client has documented a reason not to.
    source: stated
  default_severity: high
- key: example-business-term
  kind: commercial
  applies_to: { tasks: [test-advice] }
  why: Affects cost.
```
