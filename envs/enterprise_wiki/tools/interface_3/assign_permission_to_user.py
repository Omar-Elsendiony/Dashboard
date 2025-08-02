import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AssignPermissionToUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: int, user_id: int, permission_id: int) -> str:
        space_permissions = data.setdefault("space_permissions", {})

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        # Check for duplicate assignment manually
        already_assigned = any(
            str(p.get("space_id")) == str(space_id) and
            p.get("subject_type") == "user" and
            str(p.get("subject_id")) == str(user_id) and
            str(p.get("permission_id")) == str(permission_id)
            for p in space_permissions.values()
        )

        if already_assigned:
            return json.dumps({"status": "already_assigned"})


        assignment_id = generate_id(space_permissions)
        assignment = {
            "space_id": space_id,
            "subject_type": "user",
            "subject_id": user_id,
            "permission_id": permission_id
        }
        space_permissions[str(assignment_id)] = assignment

        return json.dumps(assignment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "assign_permission_to_user",
                "description": "Assign a permission to a user in a space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "integer"},
                        "user_id": {"type": "integer"},
                        "permission_id": {"type": "integer"}
                    },
                    "required": ["space_id", "user_id", "permission_id"]
                }
            }
        }
