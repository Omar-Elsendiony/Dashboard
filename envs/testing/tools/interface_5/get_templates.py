import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetTemplates(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], template_id: Optional[str] = None, space_id: Optional[str] = None,
               creator_id: Optional[str] = None, is_global: Optional[bool] = None, category: Optional[str] = None) -> str:
        
        templates = data.get("page_templates", {})
        result = []
        
        for tid, template in templates.items():
            # Apply filters
            if template_id and str(template_id) != tid:
                continue
            if space_id and template.get("space_id") != space_id:
                continue
            if creator_id and template.get("created_by_user_id") != creator_id:
                continue
            if is_global is not None and template.get("is_global") != is_global:
                continue
            if category and template.get("category") != category:
                continue
            
            result.append({
                "template_id": tid,
                "name": template.get("name"),
                "description": template.get("description"),
                "content": template.get("content"),
                "content_format": template.get("content_format"),
                "space_id": template.get("space_id"),
                "is_global": template.get("is_global"),
                "category": template.get("category"),
                "usage_count": template.get("usage_count"),
                "created_at": template.get("created_at"),
                "updated_at": template.get("updated_at"),
                "created_by_user_id": template.get("created_by_user_id")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_templates",
                "description": "Get templates matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "template_id": {"type": "string", "description": "ID of the template"},
                        "space_id": {"type": "string", "description": "ID of the space containing the template"},
                        "creator_id": {"type": "string", "description": "ID of the user who created the template"},
                        "is_global": {"type": "boolean", "description": "Whether template is global (True/False)"},
                        "category": {"type": "string", "description": "Category of the template"}
                    },
                    "required": []
                }
            }
        }
