import json

# Input and output file paths
input_file = "incident_configuration_items.json"
output_file = "incident_configuration_items.json"

# Read the JSON file
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Remove specified keys if they exist
for key, value in data.items():
    if isinstance(value, dict):
        value.pop("relationship_type", None)
        value.pop("symptoms", None)

# Write the cleaned data to a new file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Cleaned JSON written to {output_file}")
