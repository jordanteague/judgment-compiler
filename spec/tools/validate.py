#!/usr/bin/env python3
"""Validate playbooks against the playbook specification (schema version 2).

Usage:
    python validate.py PATH [PATH ...]      # files or folders of .md playbooks

What it does:
  1. Reads each Markdown playbook and builds its canonical object (format §3.2).
  2. Validates the object against schema/playbook.schema.json.
  3. Runs the checks in format §7 that JSON Schema can't express:
       - a version 1 `type` field, or schema_version 1 (format §8);
       - duplicate playbook id, and duplicate issue key within a playbook;
       - a firm-default preference on a commercial issue;
       - warnings for unrecognized fields that don't start with "x-" (format §6.3);
       - warnings for schema_version above the supported version (format §6.2).

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

SUPPORTED_SCHEMA_VERSION = 2
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema" / "playbook.schema.json"
PREFERENCE_FIELDS = ("position", "acceptable", "never", "red_line", "accepts")

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


def merge_blocks(blocks):
    """Combine body blocks (format §3.1): lists under the same section concatenate,
    mappings merge, and a scalar section may appear only once. Returns (content, errors)."""
    content, errors = {}, []
    for b in blocks:
        if not isinstance(b, dict):
            errors.append("every body block must be a mapping of sections (for example `issues:`)")
            continue
        for section, value in b.items():
            if section not in content:
                content[section] = value
            elif isinstance(content[section], list) and isinstance(value, list):
                content[section] = content[section] + value
            elif isinstance(content[section], dict) and isinstance(value, dict):
                for k, v in value.items():
                    if k in content[section]:
                        errors.append(f"'{section}.{k}' is set in more than one body block")
                    content[section][k] = v
            else:
                errors.append(f"section '{section}' appears in more than one body block with values that can't be combined")
    return content, errors


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
    content, errors = merge_blocks(blocks)
    return _iso(dict(front, content=content)), errors


def known_fields(schema):
    """Collect recognised field names per object kind, for unknown-field warnings."""
    d = schema["$defs"]
    return {
        "front": set(schema["properties"]),
        "content": set(d["content"]["properties"]),
        "issue": set(d["issue_base"]["properties"]) | {"source"},
    }


def unknown(keys, allowed):
    return sorted(k for k in keys if k not in allowed and not str(k).startswith("x-"))


def issues_of(obj):
    content = obj.get("content")
    issues = content.get("issues") if isinstance(content, dict) else None
    return [i for i in issues if isinstance(i, dict)] if isinstance(issues, list) else []


def check_playbook(f, obj, fields):
    """Checks on one playbook that JSON Schema can't express. Returns (errors, warnings)."""
    errors, warnings = [], []
    if "type" in obj:
        errors.append(f"{f}: 'type: {obj['type']}' is a schema version 1 field. Playbooks have no type in version 2 (format §8)")
    sv = obj.get("schema_version")
    if isinstance(sv, int) and sv < SUPPORTED_SCHEMA_VERSION:
        errors.append(f"{f}: schema_version {sv} is no longer supported; migrate to version 2 (format §8)")
    if isinstance(sv, int) and sv > SUPPORTED_SCHEMA_VERSION:
        warnings.append(f"{f}: schema_version {sv} is newer than this validator supports ({SUPPORTED_SCHEMA_VERSION})")

    for k in unknown(obj.keys(), fields["front"] | {"type"}):
        warnings.append(f"{f}: unrecognized front matter field '{k}'")
    content = obj.get("content")
    if isinstance(content, dict):
        for k in unknown(content.keys(), fields["content"]):
            warnings.append(f"{f}: unrecognized section '{k}'")

    seen = set()
    for issue in issues_of(obj):
        key = issue.get("key")
        if key in seen:
            errors.append(f"{f}: issue key '{key}' appears more than once")
        seen.add(key)
        for k in unknown(issue.keys(), fields["issue"]):
            warnings.append(f"{f}: issue '{key}': unrecognized field '{k}'")
        if issue.get("kind") == "commercial" and issue.get("source") == "firm-default":
            set_prefs = [p for p in PREFERENCE_FIELDS if p in issue]
            if set_prefs:
                errors.append(f"{f}: issue '{key}': a firm-default preference ({', '.join(set_prefs)}) on a commercial issue. "
                              "Business decisions belong to the client (format §5)")
    return errors, warnings


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
        ident = obj.get("id")
        if ident in loaded:
            errors.append(f"{f}: duplicate playbook id '{ident}' (also in {loaded[ident][0]})")
        loaded[ident] = (f, obj)
        errs, warns = check_playbook(f, obj, fields)
        errors += errs
        warnings += warns

    for w in warnings:
        print(f"WARNING  {w}")
    for e in errors:
        print(f"ERROR    {e}")
    print(f"\n{len(loaded)} playbook(s) checked: {len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
