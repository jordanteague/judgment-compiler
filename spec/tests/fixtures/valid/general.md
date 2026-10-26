---
id: test-contract-review
name: Test contract review
schema_version: 2
version: 1
last_reviewed: 2026-10-25
tags: [contracts]
x-firm-code: P-01
---

```yaml
issues:
  - key: indemnity
    title: Indemnification
    kind: legal
    severity: high
    why: Can shift the largest losses in the deal.
    look_for: indemnify, defend and hold harmless
    not_when: The indemnity runs only to our client.
    check:
      - Whether the indemnity is enforceable as drafted under the governing law.
    firm_view:
      default: Recommend mutual indemnities.
      unless: The client is the only party performing work.
      source: stated
    guardrail:
      when: Our client's indemnity is uncapped.
      action: flag
```

```yaml
issues:
  - key: price
    kind: commercial
    why: Affects cost.
```
