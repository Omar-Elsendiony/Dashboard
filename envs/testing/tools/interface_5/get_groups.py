import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetGroups(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], group_id: Optional[str] = None, name: Optional[str] = None,
               type: Optional[str] = None, creator_id: Optional[str] = None) -> str:
        
        groups = data.get("groups", {})
        result = []
        
        for gid, group in groups.items():
            # Apply filters
            if group_id and str(group_id) != gid:
                continue
            if name and group.get("name").lower() != name.lower():
                continue
            if type and group.get("type") != type:
                continue
            if creator_id and group.get("created_by_user_id") != creator_id:
                continue
            
            result.append({
                "group_id": gid,
                "name": group.get("name"),
                "description": group.get("description"),
                "type": group.get("type"),
                "created_at": group.get("created_at"),
                "created_by_user_id": group.get("created_by_user_id")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_groups",
                "description": "Get groups matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "group_id": {"type": "string", "description": "ID of the group"},
                        "name": {"type": "string", "description": "Name of the group"},
                        "type": {"type": "string", "description": "Type of group (system, custom)"},
                        "creator_id": {"type": "string", "description": "ID of the user who created the group"}
                    },
                    "required": []
                }
            }
        }
