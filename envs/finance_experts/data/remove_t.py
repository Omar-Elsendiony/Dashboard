import json
from pathlib import Path

# Input/output file paths
input_file = Path("payments.json")
output_file = Path("payments_clean.json")

# Load JSON
with input_file.open("r", encoding="utf-8") as f:
    data = json.load(f)

# Clean payment_date
for record in data.values():
    if "payment_date" in record and record["payment_date"]:
        # keep only the date (before "T")
        record["payment_date"] = record["payment_date"].split("T")[0]

# Save cleaned JSON
with output_file.open("w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Cleaned file written to {output_file}")
