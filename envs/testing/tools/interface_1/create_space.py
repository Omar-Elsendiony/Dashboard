import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateSpace(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_name: str, requesting_user_id: str,
               space_type: Optional[str] = None, default_template_id: Optional[str] = None,
               permission_set: Optional[Dict[str, Any]] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        spaces = data.get("spaces", {})
        users = data.get("users", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        user = users[str(requesting_user_id)]
        user_role = user.get("role", "User")
        
        # Authority verification - only certain roles can create spaces
        if user_role not in ["PlatformOwner", "WikiProgramManager"]:
            return json.dumps({"error": "Insufficient authority to create space"})
        
        # Check if space name already exists
        for space in spaces.values():
            if space.get("name") == space_name:
                return json.dumps({"error": "Space name already exists"})
        
        # Validate space type
        if space_type and space_type not in ["global", "personal", "private"]:
            return json.dumps({"error": "Invalid space type"})
        
        space_id = generate_id(spaces)
        timestamp = "2025-10-01T00:00:00"
        
        # Generate space key from name (simplified)
        space_key = space_name.lower().replace(" ", "_")[:50]
        
        new_space = {
            "space_id": space_id,
            "space_key": space_key,
            "name": space_name,
            "description": None,
            "type": space_type or "global",
            "status": "current",
            "homepage_id": None,
            "theme": None,
            "logo_url": None,
            "anonymous_access": False,
            "public_signup": False,
            "created_at": timestamp,
            "updated_at": timestamp,
            "created_by_user_id": requesting_user_id
        }
        
        spaces[space_id] = new_space
        
        # Create space administrator permission
        # admin_permission_id = generate_id(space_permissions)
        # admin_permission = {
        #     "space_permission_id": admin_permission_id,
        #     "space_id": space_id,
        #     "user_id": requesting_user_id,
        #     "group_id": None,
        #     "permission_type": "moderate",
        #     "granted_at": timestamp,
        #     "granted_by_user_id": requesting_user_id
        # }
        
        # space_permissions[admin_permission_id] = admin_permission
        
        return json.dumps({
            "space_id": space_id,
            "success": True,
            # "space_administrator_id": requesting_user_id
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_space",
                "description": "Create a new wiki space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_name": {"type": "string", "description": "Unique name for the space"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user requesting space creation"},
                        "space_type": {"type": "string", "description": "Type of space (global, personal, private)"},
                        "default_template_id": {"type": "string", "description": "Template to apply to the space"},
                    },
                    "required": ["space_name", "requesting_user_id"]
                }
            }
        }
