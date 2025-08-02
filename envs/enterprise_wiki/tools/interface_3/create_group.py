import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateGroup(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        name: str,
        description: str = None,
        group_type: str = "custom",
        created_by: int = None
    ) -> str:
        groups = data.get("groups", {})

        created_at = "2025-07-01T00:00:00Z"

        group_id = max([int(gid) for gid in groups.keys()], default=0) + 1
        group = {
            "id": int(group_id),
            "name": name,
            "description": description,
            "type": group_type,
            "created_at": created_at,
            "created_by": created_by
        }

        groups[str(group_id)] = group
        return json.dumps(group)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_group",
                "description": "Create a new user group",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Group name"},
                        "description": {"type": "string", "description": "Group description", "nullable": True},
                        "group_type": {"type": "string", "description": "Group type (e.g., system, custom)", "default": "custom"},
                        "created_by": {"type": "integer", "description": "User ID of group creator", "nullable": True}
                    },
                    "required": ["name"]
                }
            }
        }
