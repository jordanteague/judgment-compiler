#!/usr/bin/env python3
"""Run the validator against the fixtures. Valid fixtures must pass; each invalid fixture must fail with the expected error."""
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VALIDATE = HERE.parent / "tools" / "validate.py"
FIX = HERE / "fixtures"
CONTEXT = [str(FIX / "valid" / "practice.md"), str(FIX / "valid" / "industry.md")]  # issue keys for cross-checks

EXPECT = {
    "missing-version.md": "'version' is a required property",
    "escalate-without-role.md": "'escalate_to' is a required property",
    "firm-view-on-commercial.md": "should not be valid",
    "industry-without-practice-areas.md": "'practice_areas' is a required property",
    "unknown-calibration-key.md": "matches no loaded practice or industry issue",
    "two-blocks-in-task.md": "exactly one body block",
    "bad-source.md": "is not one of",
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
    code, out = run([str(FIX / "invalid" / name), *CONTEXT])
    ok = code == 1 and needle in out
    print(f"{'PASS' if ok else 'FAIL'}  {name} is rejected ({needle})")
    if not ok:
        failures += 1; print(out)

print(f"\n{len(EXPECT) + 1 - failures}/{len(EXPECT) + 1} passed")
sys.exit(1 if failures else 0)
