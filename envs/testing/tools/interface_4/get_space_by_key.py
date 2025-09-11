import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSpaceByKey(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_key: str) -> str:
        spaces = data.get("spaces", {})
        
        # Find space by key
        for space_id, space in spaces.items():
            if space.get("space_key") == space_key:
                return json.dumps(space)
        
        return json.dumps({"error": f"Space with key '{space_key}' not found"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_space_by_key",
                "description": "Get a space record by space key",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_key": {"type": "string", "description": "Key of the space to retrieve"}
                    },
                    "required": ["space_key"]
                }
            }
        }
