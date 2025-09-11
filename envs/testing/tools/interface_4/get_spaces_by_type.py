import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSpacesByType(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], type: str) -> str:
        spaces = data.get("spaces", {})
        
        # Validate type
        valid_types = ["global", "personal", "private"]
        if type not in valid_types:
            return json.dumps({"error": f"Invalid type. Must be one of {valid_types}"})
        
        # Find spaces by type
        matching_spaces = []
        for space_id, space in spaces.items():
            if space.get("type") == type:
                matching_spaces.append(space)
        
        return json.dumps(matching_spaces)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_spaces_by_type",
                "description": "Get all spaces with a specific type",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "description": "Type to filter by (global, personal, private)"}
                    },
                    "required": ["type"]
                }
            }
        }
