import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool
import uuid

class AddPageLabel(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str, label_id: str, added_by: str) -> str:
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        page_labels = data.get("page_labels", {})
        pages = data.get("pages", {})
        labels = data.get("labels", {})
        users = data.get("users", {})
        
        if page_id not in pages:
            raise ValueError("Page not found")
        
        if label_id not in labels:
            raise ValueError("Label not found")
        
        if added_by not in users:
            raise ValueError("User not found")
        
        # Check if label is already added to page
        for page_label_id, page_label in page_labels.items():
            if page_label.get("page_id") == page_id and page_label.get("label_id") == label_id:
                raise ValueError("Label already exists on this page")
        
        page_label_id = generate_id(page_labels)
        
        new_page_label = {
            "id": page_label_id,
            "page_id": page_id,
            "label_id": label_id,
            "added_by": added_by,
            "added_at": "2025-07-01T00:00:00Z" 
        }
        
        page_labels[str(page_label_id)] = new_page_label
        
        return json.dumps(new_page_label)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_page_label",
                "description": "Add label to a page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The ID of the page"
                        },
                        "label_id": {
                            "type": "string",
                            "description": "The ID of the label"
                        },
                        "added_by": {
                            "type": "string",
                            "description": "The ID of the user adding the label"
                        }
                    },
                    "required": ["page_id", "label_id", "added_by"]
                }
            }
        }
