import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPermissionInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], permission_id: int) -> str:
        permissions = data.get("permissions", {})
        return json.dumps(permissions.get(str(permission_id), {}))

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_permission_info",
                "description": "Get permission information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "permission_id": {"type": "integer", "description": "Permission ID"}
                    }
                }
            }
        }
                    
