#!/usr/bin/env python3
from pathlib import Path

ROOT = Path("tools")
deleted = []
failed = []

for p in ROOT.rglob("*.bak"):
    try:
        p.unlink()
        deleted.append(p)
    except Exception as e:
        failed.append((p, e))

print("\n=== .bak Cleanup Summary ===")
print(f"Deleted: {len(deleted)} file(s)")
for d in deleted:
    print(f"  - {d}")

if failed:
    print(f"\nFailed: {len(failed)} file(s)")
    for p, e in failed:
        print(f"  - {p} :: {e}")
