# change_name.py
from pathlib import Path
import re

# Prefer toolscopy/, fall back to tools/
ROOT = Path("tools")
if not ROOT.exists():
    ROOT = Path("tools")

INTERFACE_DIRS = [ROOT / f"interface_{i}" for i in range(1, 6)]

# Match the class line that subclasses Tool, keep indentation/suffix intact
CLASS_PATTERN = re.compile(
    r'^(\s*class\s+)([A-Za-z_]\w*)(\s*\(\s*Tool\s*\)\s*:\s*)$',
    re.MULTILINE
)

def snake_to_pascal(stem: str) -> str:
    # fetch_users -> FetchUsers, retrieve_employee_timesheets -> RetrieveEmployeeTimesheets
    return ''.join(part.capitalize() for part in re.split(r'[^0-9A-Za-z]+', stem) if part)

changed = 0
skipped = 0

for idir in INTERFACE_DIRS:
    if not idir.exists():
        continue

    # Flatten then sort files for stable output
    files = sorted(idir.glob("*.py"), key=lambda p: p.name.lower())

    for path in files:
        text = path.read_text(encoding="utf-8")
        expected = snake_to_pascal(path.stem)

        def repl(m: re.Match) -> str:
            return f"{m.group(1)}{expected}{m.group(3)}"

        new_text, n = CLASS_PATTERN.subn(repl, text, count=1)

        if n and new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
            print(f"updated: {path} -> class {expected}(Tool):")
        else:
            skipped += 1

print(f"\nDone. Files updated: {changed}, skipped: {skipped}")
