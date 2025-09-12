import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetLabels(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], label_id: Optional[str] = None, name: Optional[str] = None,
               space_id: Optional[str] = None, creator_id: Optional[str] = None, color: Optional[str] = None) -> str:
        
        labels = data.get("labels", {})
        result = []
        
        for lid, label in labels.items():
            # Apply filters
            if label_id and str(label_id) != lid:
                continue
            if name and label.get("name").lower() != name.lower():
                continue
            if space_id and label.get("space_id") != space_id:
                continue
            if creator_id and label.get("created_by_user_id") != creator_id:
                continue
            if color and label.get("color") != color:
                continue
            
            result.append({
                "label_id": lid,
                "name": label.get("name"),
                "color": label.get("color"),
                "description": label.get("description"),
                "space_id": label.get("space_id"),
                "created_by_user_id": label.get("created_by_user_id"),
                "usage_count": label.get("usage_count"),
                "created_at": label.get("created_at")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_labels",
                "description": "Get labels matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "label_id": {"type": "string", "description": "ID of the label"},
                        "name": {"type": "string", "description": "Name of the label"},
                        "space_id": {"type": "string", "description": "ID of the space containing the label"},
                        "creator_id": {"type": "string", "description": "ID of the user who created the label"},
                        "color": {"type": "string", "description": "Color of the label"}
                    },
                    "required": []
                }
            }
        }
