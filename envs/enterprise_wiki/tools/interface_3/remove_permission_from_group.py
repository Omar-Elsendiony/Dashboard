import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RemovePermissionFromGroup(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: int, group_id: int, permission_id: int) -> str:
        space_permissions = data.get("space_permissions", {})
        # print(f"Initial space permissions: {space_permissions}")
        # Find the key (ID) of the matching permission
        to_remove_key = None
        for key, perm in space_permissions.items():
            if (
                str(perm["space_id"]) == str(space_id) and
                perm["subject_type"] == "group" and
                str(perm["subject_id"]) == str(group_id) and
                str(perm["permission_id"]) == str(permission_id)
            ):
                to_remove_key = key
                break

        if to_remove_key is None:
            return json.dumps({
                "status": "not_found",
                "space_id": space_id,
                "group_id": group_id,
                "permission_id": permission_id
            })

        before = len(space_permissions)
        del space_permissions[to_remove_key]
        after = len(space_permissions)

        return json.dumps({
            "status": "removed" if before != after else "not_found",
            "space_id": space_id,
            "group_id": group_id,
            "permission_id": permission_id
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_permission_from_group",
                "description": "Remove a permission from a group in a space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "integer"},
                        "group_id": {"type": "integer"},
                        "permission_id": {"type": "integer"}
                    },
                    "required": ["space_id", "group_id", "permission_id"]
                }
            }
        }
