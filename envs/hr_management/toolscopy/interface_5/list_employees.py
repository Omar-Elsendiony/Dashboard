#!/usr/bin/env python3
from pathlib import Path
import shutil
from typing import Dict, List

# ---- CONFIG ----
SOURCE_ROOT = Path("tools")
DEST_DIR = Path("tools_v2/interface_4")  # <-- target directory
INTERFACE_DIRS = [SOURCE_ROOT / f"interface_{i}" for i in range(1, 6)]

TOOL_NAMES = [
    # GET
    "get_performance_reviews", "get_training_programs", "get_employee_training",
    "get_employees", "get_users", "get_departments", "get_audit_logs",
    "get_documents", "get_job_positions", "get_skills",
    "get_training_completion_report",
    # CREATE / UPDATE
    "create_performance_review", "update_performance_review",
    "create_training_program", "update_training_program",
    "enroll_employee_training", "complete_employee_training",
    "assign_skill_to_position", "upload_document", "update_document",
    "create_audit_log", "update_employee_profile",
]
# ---------------

def main() -> None:
    DEST_DIR.mkdir(parents=True, exist_ok=True)

    targets: Dict[str, List[Path]] = {name: [] for name in TOOL_NAMES}
    for idir in INTERFACE_DIRS:
        if not idir.exists():
            continue
        for py in idir.glob("*.py"):
            if py.stem in targets:
                targets[py.stem].append(py)

    copied: List[str] = []
    missing: List[str] = []
    duplicates: Dict[str, List[Path]] = {}

    for name, paths in targets.items():
        if not paths:
            missing.append(f"{name}.py")
            continue

        # Choose the newest version if found in multiple places
        chosen = max(paths, key=lambda p: p.stat().st_mtime)
        if len(paths) > 1:
            duplicates[name] = paths

        dest_path = DEST_DIR / f"{name}.py"
        shutil.copy2(chosen, dest_path)
        copied.append(f"{name}.py")

    # Summary
    print("\n=== Copy Summary ===")
    print(f"Destination: {DEST_DIR.resolve()}")
    if copied:
        print("\nCopied:")
        for c in copied:
            print(f"  - {c}")
    if duplicates:
        print("\nDuplicates found (picked newest):")
        for n, paths in duplicates.items():
            print(f"  - {n}.py:")
            for p in sorted(paths):
                print(f"      {p} (mtime={p.stat().st_mtime})")
    if missing:
        print("\nMissing (not found in interface_1..5):")
        for m in missing:
            print(f"  - {m}")

if __name__ == "__main__":
    main()
