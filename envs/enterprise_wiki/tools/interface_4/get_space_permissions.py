import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSpacePermissions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: int) -> str:
        space_permissions = data.get("space_permissions", {})
        return json.dumps([perm for perm in space_permissions.values() if str(perm.get("space_id")) == str(space_id)])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_space_permissions",
                "description": "Get all permissions assigned in a space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "integer", "description": "Space ID"}
                    },
                    "required": ["space_id"]
                }
            }
        }
