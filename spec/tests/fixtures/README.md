# Test fixtures

Minimal playbooks for testing the schema and validator. These are **test fixtures, not sample playbooks**. The content is deliberately generic.

- `valid/`: four playbooks that must pass with no warnings. Between them they use every field, including an `x-` extension.
- `invalid/`: each must fail for the reason its file name gives.
