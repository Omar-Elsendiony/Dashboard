import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetGroupsByType(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], type: str) -> str:
        
        groups = data.get("groups", {})
        
        # Validate type
        valid_types = ['system', 'custom']
        if type not in valid_types:
            return json.dumps({"error": f"Invalid type. Must be one of {valid_types}"})
        
        # Find groups with the specified type
        type_groups = []
        for group in groups.values():
            if group.get("type") == type:
                type_groups.append(group)
        
        return json.dumps(type_groups)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_groups_by_type",
                "description": "Get all groups with a specific type",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "description": "Type of groups to retrieve (system, custom)"}
                    },
                    "required": ["type"]
                }
            }
        }
