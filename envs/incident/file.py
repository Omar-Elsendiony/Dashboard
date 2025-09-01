#!/usr/bin/env python3
"""
Rename incident tools to ensure globally-unique API names across interfaces
and keep imports working.

- Scans: tools/interface_{1..5}
- Renames filenames and updates get_info()["function"]["name"]
- Updates __init__.py imports to the new module names
- No .bak backups created — changes are in-place

Usage:
    python rename_incident_tools.py
"""

from pathlib import Path
import re
import sys
from collections import defaultdict

ROOT = Path(".")
INTERFACES = [1, 2, 3, 4, 5]
BASE_DIR = ROOT / "tools"

GET_PREFIX = {1: "get", 2: "fetch", 3: "retrieve", 4: "query", 5: "list"}
SET_PREFIX = {
    1: {"create": "create",  "update": "update",  "delete": "delete"},
    2: {"create": "add",     "update": "modify",  "delete": "remove"},
    3: {"create": "register","update": "amend",   "delete": "purge"},
    4: {"create": "record",  "update": "edit",    "delete": "drop"},
    5: {"create": "log",     "update": "revise",  "delete": "delete"},
}

SPECIAL_RENAMES = {}

NAME_JSON_DQ = lambda old: re.compile(r'("name"\s*:\s*")' + re.escape(old) + r'(")')
NAME_JSON_SQ = lambda old: re.compile(r"('name'\s*:\s*')" + re.escape(old) + r"(')")

INIT_IMPORT_LINE = re.compile(
    r'^\s*from\s+\.(?P<mod>[A-Za-z0-9_]+)\s+import\s+(?P<cls>[A-Za-z0-9_]+)\s*$'
)

def split_prefix(stem: str):
    for p in ("list_", "get_", "create_", "update_", "delete_"):
        if stem.startswith(p):
            return p[:-1], stem[len(p):]
    return None, stem

def map_get_prefix(prefix: str, iface: int) -> str:
    return GET_PREFIX[iface]

def map_set_prefix(prefix: str, iface: int) -> str:
    return SET_PREFIX[iface][prefix]

def compute_new_stem(stem: str, iface: int) -> str:
    if stem in SPECIAL_RENAMES.get(iface, {}):
        return SPECIAL_RENAMES[iface][stem]

    prefix, rest = split_prefix(stem)
    if prefix in ("list", "get"):
        return f"{map_get_prefix(prefix, iface)}_{rest}"
    if prefix in ("create", "update", "delete"):
        return f"{map_set_prefix(prefix, iface)}_{rest}"
    return stem

def update_tool_name_inside_file(text: str, old: str, new: str) -> str:
    if old == new:
        return text
    t = NAME_JSON_DQ(old).sub(r'\1' + new + r'\2', text)
    t = NAME_JSON_SQ(old).sub(r"\1" + new + r"\2", t)
    return t

def update_init_imports(init_path: Path, rename_map: dict):
    if not init_path.exists():
        return
    lines = init_path.read_text(encoding="utf-8").splitlines()
    new_lines, changed = [], False
    for line in lines:
        m = INIT_IMPORT_LINE.match(line)
        if not m:
            new_lines.append(line)
            continue
        old_mod, cls = m.group("mod"), m.group("cls")
        new_mod = rename_map.get(old_mod, old_mod)
        if new_mod != old_mod:
            changed = True
            new_lines.append(f"from .{new_mod} import {cls}")
        else:
            new_lines.append(line)
    if changed:
        init_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

def main():
    if not BASE_DIR.exists():
        print(f"[error] {BASE_DIR} not found.")
        sys.exit(1)

    global_targets = {}
    reverse_index = defaultdict(list)
    file_records = []

    for iface in INTERFACES:
        idir = BASE_DIR / f"interface_{iface}"
        if not idir.exists():
            continue
        for py in sorted(idir.glob("*.py")):
            if py.stem == "__init__":
                continue
            old_stem = py.stem
            new_stem = compute_new_stem(old_stem, iface)
            global_targets[(iface, old_stem)] = new_stem
            reverse_index[new_stem].append((iface, old_stem, py))
            file_records.append((iface, py, old_stem))

    # Resolve global collisions
    for new_stem, entries in reverse_index.items():
        if len(entries) > 1:
            for iface, old_stem, _ in entries:
                global_targets[(iface, old_stem)] = f"{new_stem}_{iface}"

    per_iface_rename_map = {iface: {} for iface in INTERFACES}
    all_changes, collisions = [], []

    for iface, py, old_stem in file_records:
        new_stem = global_targets[(iface, old_stem)]
        if new_stem == old_stem:
            continue
        new_path = py.with_name(new_stem + ".py")
        if new_path.exists():
            collisions.append((str(py), str(new_path)))
            continue
        txt = py.read_text(encoding="utf-8")
        new_txt = update_tool_name_inside_file(txt, old_stem, new_stem)
        py.write_text(new_txt, encoding="utf-8")
        py.rename(new_path)
        per_iface_rename_map[iface][old_stem] = new_stem
        all_changes.append((str(py), str(new_path)))

    for iface in INTERFACES:
        update_init_imports(BASE_DIR / f"interface_{iface}" / "__init__.py",
                            per_iface_rename_map.get(iface, {}))

    print("\n=== Rename Summary ===")
    if all_changes:
        print("Updated:")
        for a, b in all_changes:
            print(f"  {a} -> {b}")
    if collisions:
        print("\n[ATTENTION] Conflicts:")
        for a, b in collisions:
            print(f"  {a} -> {b}")
    if not all_changes and not collisions:
        print("No changes needed.")

if __name__ == "__main__":
    main()
