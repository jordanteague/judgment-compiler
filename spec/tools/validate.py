#!/usr/bin/env python3
"""Validate playbooks against the playbook specification (schema version 1).

Usage:
    python validate.py PATH [PATH ...]      # files or folders of .md playbooks

What it does:
  1. Reads each Markdown playbook and builds its canonical object (format §3.3).
  2. Validates the object against schema/playbook.schema.json.
  3. Runs the cross-playbook checks in format §11:
       - duplicate type + id;
       - calibration keys exist in a loaded practice or industry playbook (or start with "x-");
       - warnings for unrecognized fields that don't start with "x-" (format §10.3);
       - warnings for schema_version above the supported version (format §10.2).

Exit status: 0 if there are no errors (warnings allowed), 1 otherwise.
Requires: pip install pyyaml jsonschema
"""
import datetime
import json
import re
import sys
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("validate.py needs PyYAML and jsonschema 4.0 or later: pip install -r spec/requirements.txt")

SUPPORTED_SCHEMA_VERSION = 1
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema" / "playbook.schema.json"
LIST_TYPES = {"guardrails", "practice", "industry"}
MAPPING_TYPES = {"task", "client", "matter"}

FRONT_MATTER = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*\n", re.DOTALL)
YAML_BLOCK = re.compile(r"^```yaml[ \t]*\n(.*?)^```[ \t]*$", re.DOTALL | re.MULTILINE)


def _iso(value):
    """YAML parses bare dates as date objects; the schema expects ISO strings."""
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()[:10]
    if isinstance(value, dict):
        return {k: _iso(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_iso(v) for v in value]
    return value


def canonical_object(path: Path):
    """Build the canonical object for one Markdown playbook. Returns (obj, errors)."""
    text = path.read_text(encoding="utf-8")
    m = FRONT_MATTER.match(text)
    if not m:
        return None, ["no front matter (the file must start with a --- block)"]
    try:
        front = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        return None, [f"front matter is not valid YAML: {e}"]
    if not isinstance(front, dict):
        return None, ["front matter must be a mapping"]

    blocks = []
    for raw in YAML_BLOCK.findall(text[m.end():]):
        try:
            blocks.append(yaml.safe_load(raw))
        except yaml.YAMLError as e:
            return None, [f"body block is not valid YAML: {e}"]

    ptype = front.get("type")
    errors = []
    if ptype in LIST_TYPES:
        content = []
        for b in blocks:
            if not isinstance(b, list):
                errors.append(f"every body block in a {ptype} playbook must be a list")
            else:
                content.extend(b)
    elif ptype in MAPPING_TYPES:
        if len(blocks) != 1 or not isinstance(blocks[0], dict):
            errors.append(f"a {ptype} playbook must have exactly one body block holding a mapping")
            content = blocks[0] if blocks else None
        else:
            content = blocks[0]
    else:
        content = blocks
    obj = _iso(dict(front, content=content))
    return obj, errors


def known_fields(schema):
    """Collect recognised field names per object kind, for unknown-field warnings."""
    d = schema["$defs"]
    props = lambda name: set(d[name]["properties"])
    return {
        "front": set(schema["properties"]),
        "guardrails": props("guardrail"),
        "task": props("task_content"),
        "issue": props("issue"),
        "client": props("client_content"),
        "matter": props("matter_content"),
        "calibration": props("calibration_item"),
    }


def unknown(keys, allowed):
    return sorted(k for k in keys if k not in allowed and not str(k).startswith("x-"))


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    files = []
    for arg in argv:
        p = Path(arg)
        files.extend(sorted(p.rglob("*.md")) if p.is_dir() else [p])
    files = [f for f in files if f.name.lower() != "readme.md"]

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    fields = known_fields(schema)

    loaded, errors, warnings = {}, [], []
    for f in files:
        obj, errs = canonical_object(f)
        errors += [f"{f}: {e}" for e in errs]
        if obj is None:
            continue
        for e in sorted(validator.iter_errors(obj), key=lambda e: list(e.path)):
            where = "/".join(str(p) for p in e.path) or "(root)"
            errors.append(f"{f}: {where}: {e.message}")
        ident = (obj.get("type"), obj.get("id"))
        if ident in loaded:
            errors.append(f"{f}: duplicate playbook {ident[0]}:{ident[1]} (also in {loaded[ident][0]})")
        loaded[ident] = (f, obj)

        sv = obj.get("schema_version")
        if isinstance(sv, int) and sv > SUPPORTED_SCHEMA_VERSION:
            warnings.append(f"{f}: schema_version {sv} is newer than this validator supports ({SUPPORTED_SCHEMA_VERSION})")
        for k in unknown(obj.keys(), fields["front"]):
            warnings.append(f"{f}: unrecognized front matter field '{k}'")
        content, ptype = obj.get("content"), obj.get("type")
        if ptype in ("practice", "industry") and isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    for k in unknown(item.keys(), fields["issue"]):
                        warnings.append(f"{f}: issue '{item.get('key')}': unrecognized field '{k}'")
        if ptype == "guardrails" and isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    for k in unknown(item.keys(), fields["guardrails"]):
                        warnings.append(f"{f}: guardrail '{item.get('id')}': unrecognized field '{k}'")
        if ptype in ("task", "client", "matter") and isinstance(content, dict):
            for k in unknown(content.keys(), fields[ptype]):
                warnings.append(f"{f}: unrecognized field '{k}'")
            for item in content.get("calibration") or []:
                if isinstance(item, dict):
                    for k in unknown(item.keys(), fields["calibration"]):
                        warnings.append(f"{f}: calibration '{item.get('key')}': unrecognized field '{k}'")

    # Cross-playbook: calibration keys must exist in a loaded practice or industry playbook.
    issue_keys = {
        item.get("key")
        for (ptype, _), (_, obj) in loaded.items()
        if ptype in ("practice", "industry") and isinstance(obj.get("content"), list)
        for item in obj["content"] if isinstance(item, dict)
    }
    for (ptype, _), (f, obj) in loaded.items():
        content = obj.get("content")
        if ptype in ("client", "matter") and isinstance(content, dict):
            for item in content.get("calibration") or []:
                key = item.get("key") if isinstance(item, dict) else None
                if key and not str(key).startswith("x-"):
                    if not issue_keys:
                        warnings.append(f"{f}: calibration key '{key}' not checked (no practice or industry playbooks loaded)")
                    elif key not in issue_keys:
                        errors.append(f"{f}: calibration key '{key}' matches no loaded practice or industry issue")

    for w in warnings:
        print(f"WARNING  {w}")
    for e in errors:
        print(f"ERROR    {e}")
    print(f"\n{len(loaded)} playbook(s) checked: {len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
