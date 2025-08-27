#!/usr/bin/env python3
"""
Rename tool files and their tool 'name' in get_info() across tools/interface_1..5
to enforce globally-unique names with minimal changes.

Rules:
- GET prefix by interface:
    1: get_      (unchanged)
    2: fetch_
    3: retrieve_
    4: query_
    5: list_
- Resolve common duplicates for SET-style names with small interface-specific tweaks.

What is changed:
- Filename: <old>.py -> <new>.py
- In-file tool name (get_info()["function"]["name"]) from <old> to <new>

Usage:
    python rename_hr_tools.py
"""

from pathlib import Path
import re
import shutil
import sys

ROOT = Path(".")
INTERFACES = [1, 2, 3, 4, 5]

GET_PREFIX = {
    1: "get",
    2: "fetch",
    3: "retrieve",
    4: "query",
    5: "lookup",
}

# Minimal targeted duplicate-resolvers for common SET names
SPECIAL_RENAMES = {
    2: {
        "upload_document": "submit_document",
        "update_document": "modify_document",
        "create_audit_log": "log_audit_entry",
    },
    3: {
        "upload_document": "attach_document",
        "update_document": "amend_document",
        "create_audit_log": "record_audit_entry",
        "add_payroll_deduction": "insert_payroll_deduction",
    },
    4: {
        "upload_document": "add_document",
        "update_document": "edit_document",
        "create_audit_log": "register_audit_entry",
        "assign_skill_to_position": "map_skill_to_position",
    },
    5: {
        "upload_document": "insert_document",
        "update_document": "adjust_document",
        "create_audit_log": "log_audit_event",
    },
}

# Regex helpers to update get_info()["function"]["name"] safely
NAME_JSON_DQ = lambda old: re.compile(r'("name"\s*:\s*")' + re.escape(old) + r'(")')
NAME_JSON_SQ = lambda old: re.compile(r"('name'\s*:\s*')" + re.escape(old) + r"(')")

def compute_new_name(stem: str, iface: int) -> str:
    """Return the new tool name for this file stem within given interface, or the original if no change."""
    # GET mapping (only for names starting with 'get_')
    if stem.startswith("get_"):
        # Interface 1 stays 'get_'
        if iface == 1:
            return stem
        rest = stem[len("get_"):]
        return f"{GET_PREFIX[iface]}_{rest}"

    # Common duplicates (SET-side) with interface-specific synonyms
    sp = SPECIAL_RENAMES.get(iface, {})
    if stem in sp:
        return sp[stem]

    # Otherwise, leave as-is (minimal change)
    return stem

def update_tool_name_inside_file(text: str, old: str, new: str) -> str:
    """Update the function name returned in get_info()['function']['name'] from old to new."""
    if old == new:
        return text
    text2 = NAME_JSON_DQ(old).sub(r'\1' + new + r'\2', text)
    text2 = NAME_JSON_SQ(old).sub(r"\1" + new + r"\2", text2)
    return text2

def main():
    all_changes = []
    collisions = set()

    for iface in INTERFACES:
        idir = ROOT / "tools" / f"interface_{iface}"
        if not idir.exists():
            print(f"[warn] {idir} does not exist; skipping.")
            continue

        for py in sorted(idir.glob("*.py")):
            old_stem = py.stem
            new_stem = compute_new_name(old_stem, iface)

            if new_stem == old_stem:
                continue

            new_path = py.with_name(new_stem + ".py")
            if new_path.exists():
                # If this happens, it means mapping produced an already-existing filename in same dir.
                collisions.add((str(py), str(new_path)))
                continue

            # Read file
            try:
                txt = py.read_text(encoding="utf-8")
            except Exception as e:
                print(f"[error] Could not read {py}: {e}")
                continue

            # Update internal tool name in get_info()
            new_txt = update_tool_name_inside_file(txt, old_stem, new_stem)

            # Write to temp, then move to target filename; keep a backup of original
            backup = py.with_suffix(".py.bak")
            try:
                if not backup.exists():
                    shutil.copy2(py, backup)
                py.write_text(new_txt, encoding="utf-8")
                py.rename(new_path)
                all_changes.append((str(backup), str(new_path)))
            except Exception as e:
                print(f"[error] Could not rename/update {py}: {e}")
                # attempt rollback if we changed content
                try:
                    if backup.exists():
                        shutil.copy2(backup, py)
                except Exception:
                    pass

    # Summary
    print("\n=== Rename Summary ===")
    if not all_changes and not collisions:
        print("No changes performed (either already unique or directories missing).")
        return

    if all_changes:
        print("\nUpdated files (backup created as *.py.bak):")
        for b, n in all_changes:
            print(f"  -> {n}")

    if collisions:
        print("\n[ATTENTION] Filename collisions blocked some renames:")
        for a, b in collisions:
            print(f"  - Desired rename conflict: {a} -> {b}")
        print("You may manually resolve these (or tweak SPECIAL_RENAMES).")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
