import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateTemplatesByFilter(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str,
               filter_space_id: Optional[str] = None, filter_is_global: Optional[bool] = None,
               filter_category: Optional[str] = None, update_category: Optional[str] = None,
               update_description: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        templates = data.get("page_templates", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        updated_templates = []
        timestamp = "2025-10-01T00:00:00"
        
        for template_id, template in templates.items():
            # Apply filters
            if filter_space_id and template.get("space_id") != filter_space_id:
                continue
            if filter_is_global is not None and template.get("is_global") != filter_is_global:
                continue
            if filter_category and template.get("category") != filter_category:
                continue
            
            # Check permissions for this template
            has_permission = False
            
            # Platform Owner can update any template
            if requesting_user.get("role") == "PlatformOwner":
                has_permission = True
            # Template creator can update their own template
            elif template.get("created_by_user_id") == requesting_user_id:
                has_permission = True
            # Space admin can update space-specific templates
            elif not template.get("is_global") and template.get("space_id"):
                for perm in space_permissions.values():
                    if (perm.get("space_id") == template.get("space_id") and 
                        perm.get("user_id") == requesting_user_id and 
                        perm.get("permission_type") == "moderate"):
                        has_permission = True
                        break
            
            if not has_permission:
                continue
            
            # Apply updates
            if update_category is not None:
                template["category"] = update_category
            if update_description is not None:
                template["description"] = update_description
            
            template["updated_at"] = timestamp
            updated_templates.append(template)
        
        return json.dumps(updated_templates)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_templates_by_filter",
                "description": "Update templates based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "filter_space_id": {"type": "string", "description": "Filter by space ID"},
                        "filter_is_global": {"type": "boolean", "description": "Filter by global status (True/False)"},
                        "filter_category": {"type": "string", "description": "Filter by category"},
                        "update_category": {"type": "string", "description": "New category to set"},
                        "update_description": {"type": "string", "description": "New description to set"}
                    },
                    "required": ["requesting_user_id"]
                }
            }
        }