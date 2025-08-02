import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteSpace(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: int) -> str:
        spaces = data.get("spaces", {})
        if str(space_id) not in spaces:
            raise ValueError("Space not found")

        deleted = spaces.pop(str(space_id))
        return json.dumps(deleted)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_space",
                "description": "Delete a space by ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "integer", "description": "ID of the space to delete"}
                    },
                    "required": ["space_id"]
                }
            }
        }
