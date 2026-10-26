#!/usr/bin/env python3
"""Run the validator against the fixtures. Valid fixtures must pass; each invalid fixture must fail with the expected error."""
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VALIDATE = HERE.parent / "tools" / "validate.py"
FIX = HERE / "fixtures"

EXPECT = {
    "missing-version.md": "'version' is a required property",
    "escalate-without-role.md": "'escalate_to' is a required property",
    "firm-view-on-commercial.md": "should not be valid",
    "bad-source.md": "is not one of",
    "duplicate-key.md": "appears more than once",
    "firm-default-position-on-commercial.md": "firm-default preference",
    "legacy-type.md": "schema version 1 field",
}

def run(paths):
    r = subprocess.run([sys.executable, str(VALIDATE), *paths], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr

failures = 0
code, out = run([str(FIX / "valid")])
ok = code == 0 and "WARNING" not in out
print(f"{'PASS' if ok else 'FAIL'}  valid fixtures pass with no warnings")
if not ok:
    failures += 1; print(out)

for name, needle in EXPECT.items():
    code, out = run([str(FIX / "invalid" / name)])
    ok = code == 1 and needle in out
    print(f"{'PASS' if ok else 'FAIL'}  {name} is rejected ({needle})")
    if not ok:
        failures += 1; print(out)

total = len(EXPECT) + 1
print(f"\n{total - failures}/{total} passed")
sys.exit(1 if failures else 0)
