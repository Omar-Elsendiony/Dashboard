import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ModifyTemplate(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], template_id: str, requesting_user_id: str,
               updated_content: str, template_name: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        templates = data.get("page_templates", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate template exists
        if str(template_id) not in templates:
            return json.dumps({"success": False, "error": f"Template {template_id} not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"success": False, "error": f"User {requesting_user_id} not found"})
        
        template = templates[str(template_id)]
        user = users[str(requesting_user_id)]
        
        # Check permissions
        has_permission = False
        
        if template.get("is_global"):
            # For global templates, only Platform Owner can modify
            if user.get("role") == "PlatformOwner":
                has_permission = True
        else:
            # For space-specific templates
            space_id = template.get("space_id")
            
            # Check if user is Platform Owner or WikiProgramManager
            if user.get("role") in ["PlatformOwner", "WikiProgramManager"]:
                has_permission = True
            
            # Check if user is template creator
            elif template.get("created_by_user_id") == requesting_user_id:
                has_permission = True
            
            # Check if user is Space Administrator
            elif space_id:
                for perm in space_permissions.values():
                    if (perm.get("space_id") == space_id and 
                        perm.get("user_id") == requesting_user_id and 
                        perm.get("permission_type") == "moderate"):
                        has_permission = True
                        break
        
        if not has_permission:
            return json.dumps({"success": False, "error": "Insufficient permissions to modify template"})
        
        # Update template
        timestamp = "2025-10-01T00:00:00"
        template["content"] = updated_content
        template["updated_at"] = timestamp
        
        if template_name:
            template["name"] = template_name
        
        return json.dumps({
            "success": True,
            "message": "Template modified"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_template",
                "description": "Modify an existing template",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "template_id": {"type": "string", "description": "ID of the template to modify"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user modifying the template"},
                        "updated_content": {"type": "string", "description": "New template content"},
                        "template_name": {"type": "string", "description": "New template name (optional)"}
                    },
                    "required": ["template_id", "requesting_user_id", "updated_content"]
                }
            }
        }