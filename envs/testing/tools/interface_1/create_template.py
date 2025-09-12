import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateTemplate(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], template_name: str, template_content: str,
               requesting_user_id: str, is_global: bool, space_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        templates = data.get("page_templates", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"success": False, "error": f"User {requesting_user_id} not found"})
        
        user = users[str(requesting_user_id)]
        
        # Check permissions based on template type
        has_permission = False
        
        if is_global:
            # Only Platform Owner can create global templates
            if user.get("role") == "PlatformOwner":
                has_permission = True
        else:
            # For space-specific templates, validate space exists
            if not space_id:
                return json.dumps({"success": False, "error": "Space ID required for space-specific templates"})
            
            if str(space_id) not in spaces:
                return json.dumps({"success": False, "error": f"Space {space_id} not found"})
            
            # Check if user is Platform Owner, WikiProgramManager, or Space Administrator
            if user.get("role") in ["PlatformOwner", "WikiProgramManager"]:
                has_permission = True
            else:
                # Check if user is Space Administrator
                for perm in space_permissions.values():
                    if (perm.get("space_id") == space_id and 
                        perm.get("user_id") == requesting_user_id and 
                        perm.get("permission_type") == "moderate"):
                        has_permission = True
                        break
        
        if not has_permission:
            return json.dumps({"success": False, "error": "Insufficient permissions to create template"})
        
        # Create template
        template_id = str(generate_id(templates))
        timestamp = "2025-10-01T00:00:00"
        
        new_template = {
            "template_id": int(template_id),
            "name": template_name,
            "description": None,
            "content": template_content,
            "content_format": "wiki",
            "space_id": space_id if not is_global else None,
            "is_global": is_global,
            "category": None,
            "usage_count": 0,
            "created_at": timestamp,
            "updated_at": timestamp,
            "created_by_user_id": requesting_user_id
        }
        
        templates[template_id] = new_template
        
        scope = "global" if is_global else "space-specific"
        
        return json.dumps({
            "template_id": template_id,
            "success": True,
            "scope": scope
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_template",
                "description": "Create a new page template",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "template_name": {"type": "string", "description": "Name of the template"},
                        "template_content": {"type": "string", "description": "Content of the template"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user creating the template"},
                        "is_global": {"type": "boolean", "description": "True for global template, False for space-specific (True/False)"},
                        "space_id": {"type": "string", "description": "Space ID if creating space-specific template (optional)"}
                    },
                    "required": ["template_name", "template_content", "requesting_user_id", "is_global"]
                }
            }
        }
