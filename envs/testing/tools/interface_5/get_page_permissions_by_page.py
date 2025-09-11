import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPagePermissionsByPage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        
        page_permissions = data.get("page_permissions", {})
        pages = data.get("pages", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"error": f"Page {page_id} not found"})
        
        # Find permissions for the page
        page_permission_records = []
        for permission in page_permissions.values():
            if permission.get("page_id") == page_id:
                page_permission_records.append(permission)
        
        return json.dumps(page_permission_records)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_permissions_by_page",
                "description": "Get all page permission records for a specific page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page to get permissions for"}
                    },
                    "required": ["page_id"]
                }
            }
        }
