import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPageVersionsByPage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        
        page_versions = data.get("page_versions", {})
        pages = data.get("pages", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"error": f"Page {page_id} not found"})
        
        # Find all versions for the page
        page_version_list = []
        for version in page_versions.values():
            if version.get("page_id") == page_id:
                page_version_list.append(version)
        
        return json.dumps(page_version_list)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_versions_by_page",
                "description": "Get all versions for a specific page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page"}
                    },
                    "required": ["page_id"]
                }
            }
        }
