import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSpacePermissionsBySpace(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str) -> str:
        
        space_permissions = data.get("space_permissions", {})
        spaces = data.get("spaces", {})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": f"Space {space_id} not found"})
        
        # Find permissions for the space
        space_permission_records = []
        for permission in space_permissions.values():
            if permission.get("space_id") == space_id:
                space_permission_records.append(permission)
        
        return json.dumps(space_permission_records)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_space_permissions_by_space",
                "description": "Get all space permission records for a specific space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space to get permissions for"}
                    },
                    "required": ["space_id"]
                }
            }
        }
