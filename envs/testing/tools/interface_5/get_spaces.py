import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetSpaces(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: Optional[str] = None, space_key: Optional[str] = None,
               creator_id: Optional[str] = None, type: Optional[str] = None, status: Optional[str] = None) -> str:
        
        spaces = data.get("spaces", {})
        result = []
        
        for sid, space in spaces.items():
            # Apply filters
            if space_id and str(space_id) != sid:
                continue
            if space_key and space.get("space_key") != space_key:
                continue
            if creator_id and space.get("created_by_user_id") != creator_id:
                continue
            if type and space.get("type") != type:
                continue
            if status and space.get("status") != status:
                continue
            
            result.append({
                "space_id": sid,
                "space_key": space.get("space_key"),
                "name": space.get("name"),
                "description": space.get("description"),
                "type": space.get("type"),
                "status": space.get("status"),
                "homepage_id": space.get("homepage_id"),
                "theme": space.get("theme"),
                "logo_url": space.get("logo_url"),
                "anonymous_access": space.get("anonymous_access"),
                "public_signup": space.get("public_signup"),
                "created_at": space.get("created_at"),
                "updated_at": space.get("updated_at"),
                "created_by_user_id": space.get("created_by_user_id")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_spaces",
                "description": "Get spaces matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space"},
                        "space_key": {"type": "string", "description": "Key of the space"},
                        "creator_id": {"type": "string", "description": "ID of the user who created the space"},
                        "type": {"type": "string", "description": "Type of space (global, personal, private)"},
                        "status": {"type": "string", "description": "Status of space (current, archived)"}
                    },
                    "required": []
                }
            }
        }
