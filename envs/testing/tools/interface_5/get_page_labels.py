import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPageLabels(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_label_id: Optional[str] = None, page_id: Optional[str] = None,
               label_id: Optional[str] = None, added_by_user_id: Optional[str] = None) -> str:
        
        page_labels = data.get("page_labels", {})
        result = []
        
        for plid, page_label in page_labels.items():
            # Apply filters
            if page_label_id and str(page_label_id) != plid:
                continue
            if page_id and page_label.get("page_id") != page_id:
                continue
            if label_id and page_label.get("label_id") != label_id:
                continue
            if added_by_user_id and page_label.get("added_by_user_id") != added_by_user_id:
                continue
            
            result.append({
                "page_label_id": plid,
                "page_id": page_label.get("page_id"),
                "label_id": page_label.get("label_id"),
                "added_at": page_label.get("added_at"),
                "added_by_user_id": page_label.get("added_by_user_id")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_labels",
                "description": "Get page-label relationships matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_label_id": {"type": "string", "description": "ID of the page-label relationship"},
                        "page_id": {"type": "string", "description": "ID of the page"},
                        "label_id": {"type": "string", "description": "ID of the label"},
                        "added_by_user_id": {"type": "string", "description": "ID of the user who added the label to the page"}
                    },
                    "required": []
                }
            }
        }
