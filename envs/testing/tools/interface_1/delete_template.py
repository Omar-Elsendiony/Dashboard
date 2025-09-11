import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteTemplate(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], template_id: str, requesting_user_id: str) -> str:
        
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
            # For global templates, only Platform Owner can delete
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
            return json.dumps({"success": False, "error": "Insufficient permissions to delete template"})
        
        # Delete template directly
        del templates[str(template_id)]
        
        return json.dumps({
            "success": True,
            "message": "Template deleted"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_template",
                "description": "Delete a template",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "template_id": {"type": "string", "description": "ID of the template to delete"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user deleting the template"}
                    },
                    "required": ["template_id", "requesting_user_id"]
                }
            }
        }