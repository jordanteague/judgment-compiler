---
type: task
id: test-advice
schema_version: 1
version: 1
last_reviewed: 2026-10-22
---

```yaml
task: test-advice
task_type: advise
steps:
  - id: facts
    do: List the facts relied on.
    uses: [facts]
  - id: analysis
    do: Analyze each triggered issue.
    uses: [issues, calibration, guardrails]
```
