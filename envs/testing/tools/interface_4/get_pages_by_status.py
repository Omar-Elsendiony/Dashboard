import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPagesByStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], status: str) -> str:
        
        pages = data.get("pages", {})
        
        # Validate status
        valid_statuses = ["current", "draft", "deleted", "historical"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}"})
        
        # Find all pages with the specified status
        status_pages = []
        for page in pages.values():
            if page.get("status") == status:
                status_pages.append(page)
        
        return json.dumps(status_pages)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_pages_by_status",
                "description": "Get all pages with a specific status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "description": "Page status (current, draft, deleted, historical)"}
                    },
                    "required": ["status"]
                }
            }
        }
