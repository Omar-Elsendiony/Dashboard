import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSpaceById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str) -> str:
        spaces = data.get("spaces", {})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": f"Space {space_id} not found"})
        
        space = spaces[str(space_id)]
        return json.dumps(space)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_space_by_id",
                "description": "Get a space record by space ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space to retrieve"}
                    },
                    "required": ["space_id"]
                }
            }
        }
