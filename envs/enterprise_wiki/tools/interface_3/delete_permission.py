import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeletePermission(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], permission_id: int) -> str:
        permissions = data.get("permissions", {})
        removed = permissions.pop(str(permission_id), None)
        if not removed:
            raise ValueError("Permission not found.")
        
        return json.dumps(removed)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_permission",
                "description": "Delete a permission by ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "permission_id": {"type": "integer"}
                    },
                    "required": ["permission_id"]
                }
            }
        }
