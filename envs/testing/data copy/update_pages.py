import json

with open('pages.json', 'r') as f:
    pages = json.load(f)
    
    
with open('updated_pages.json', 'r') as f:
    updated = json.load(f)

for k, v in pages.items():
    if k in updated:
        v.update(updated[k])

with open('pages.json', 'w') as f:
    json.dump(pages, f, indent=2)
