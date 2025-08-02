import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RemovePageLabel(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str, label_id: str) -> str:
        page_labels = data.get("page_labels", {})
        pages = data.get("pages", {})
        labels = data.get("labels", {})
        
        if page_id not in pages:
            raise ValueError("Page not found")
        
        if label_id not in labels:
            raise ValueError("Label not found")
        
        # Find and remove the page label
        page_label_to_remove = None
        for page_label_id, page_label in page_labels.items():
            if str(page_label.get("page_id")) == str(page_id) and str(page_label.get("label_id")) == str(label_id):
                page_label_to_remove = page_label_id
                break
        
        if not page_label_to_remove:
            raise ValueError("Label not found on this page")
        
        del page_labels[page_label_to_remove]
        
        return json.dumps({"success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_page_label",
                "description": "Remove label from a page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The ID of the page"
                        },
                        "label_id": {
                            "type": "string",
                            "description": "The ID of the label to remove"
                        }
                    },
                    "required": ["page_id", "label_id"]
                }
            }
        }   
