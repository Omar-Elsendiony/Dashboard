import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSpaceStatistics(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: int) -> str:
        pages = data.get("pages", {})
        permissions = data.get("space_permissions", {})
        user_ids = set()

        page_count = sum(1 for p in pages.values() if str(p.get("space_id")) == str(space_id))
        # for p in pages.values():
        #     if str(p.get("space_id")) == str(space_id):
        #         user_ids.add(p.get("created_by"))
        
        for perm in permissions.values():
            if str(perm.get("space_id")) == str(space_id):
                if perm.get("subject_type") == "user":
                    user_ids.add(perm.get("subject_id"))
                # elif perm.get("subject_type") == "group":
                #     # Assuming groups have a way to resolve user IDs
                #     group_users = data.get("group_users", {}).get(str(perm.get("subject_id")), [])
                #     user_ids.update(group_users)

        stats = {
            "space_id": space_id,
            "page_count": page_count,
            "user_count": len(user_ids)
        }

        return json.dumps(stats)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_space_statistics",
                "description": "Get statistics about a space (page count, user count, etc.)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "integer", "description": "Space ID"}
                    },
                    "required": ["space_id"]
                }
            }
        }
