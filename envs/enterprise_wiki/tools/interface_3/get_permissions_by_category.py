import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetPermissionsByCategory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], category: str) -> str:
        permissions = data.get("permissions", {})
        filtered = [perm for perm in permissions.values() if perm.get("category") == category]
        return json.dumps(filtered)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_permissions_by_category",
                "description": "Get permissions filtered by category",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "description": "Permission category"}
                    },
                    "required": ["category"]
                }
            }
        }
