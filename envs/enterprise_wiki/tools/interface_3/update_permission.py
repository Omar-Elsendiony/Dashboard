import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdatePermission(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], permission_id: int, name: str = None, description: str = None, category: str = None) -> str:
        permissions = data.get("permissions", {})
        perm = permissions.get(str(permission_id))
        if not perm:
            raise ValueError("Permission not found.")

        if name is None and description is None and category is None:
            raise ValueError("At least one field (name, description, category) must be provided for update.")

        if name is not None:
            perm["name"] = name
        if description is not None:
            perm["description"] = description
        if category is not None:
            perm["category"] = category

        return json.dumps(perm)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_permission",
                "description": "Update fields of a permission (name, description, category)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "permission_id": {"type": "integer", "description": "Permission ID to update"},
                        "name": {"type": "string", "description": "New permission name"},
                        "description": {"type": "string", "description": "New permission description"},
                        "category": {"type": "string", "description": "New permission category"}
                    },
                    "required": ["permission_id"]
                }
            }
        }
