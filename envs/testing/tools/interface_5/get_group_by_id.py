import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetGroupById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], group_id: str) -> str:
        
        groups = data.get("groups", {})
        
        # Validate group exists
        if str(group_id) not in groups:
            return json.dumps({"error": f"Group {group_id} not found"})
        
        group = groups[str(group_id)]
        
        return json.dumps(group)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_group_by_id",
                "description": "Get a group by its ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "group_id": {"type": "string", "description": "ID of the group to retrieve"}
                    },
                    "required": ["group_id"]
                }
            }
        }
