import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreatePermission(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        name: str,
        description: str = None,
        category: str = None
    ) -> str:
        permissions = data.get("permissions", {})

        permission_id = max([int(gid) for gid in permissions.keys()], default=0) + 1

        permission = {
            "id": int(permission_id),
            "name": name,
            "description": description,
            "category": category
        }

        permissions[str(permission_id)] = permission
        return json.dumps(permission)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_permission",
                "description": "Create a new permission entry",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Permission name"},
                        "description": {"type": "string", "description": "Permission description", "nullable": True},
                        "category": {"type": "string", "description": "Permission category", "nullable": True}
                    },
                    "required": ["name"]
                }
            }
        }
