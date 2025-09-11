import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSpacesByStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], status: str) -> str:
        spaces = data.get("spaces", {})
        
        # Validate status
        valid_statuses = ["current", "archived"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}"})
        
        # Find spaces by status
        matching_spaces = []
        for space_id, space in spaces.items():
            if space.get("status") == status:
                matching_spaces.append(space)
        
        return json.dumps(matching_spaces)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_spaces_by_status",
                "description": "Get all spaces with a specific status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "description": "Status to filter by (current, archived)"}
                    },
                    "required": ["status"]
                }
            }
        }
