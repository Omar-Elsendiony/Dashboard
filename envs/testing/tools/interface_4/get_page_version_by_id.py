import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPageVersionById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_version_id: str) -> str:
        
        page_versions = data.get("page_versions", {})
        
        # Validate page version exists
        if str(page_version_id) not in page_versions:
            return json.dumps({"error": f"Page version {page_version_id} not found"})
        
        page_version = page_versions[str(page_version_id)]
        
        return json.dumps(page_version)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_version_by_id",
                "description": "Get a single page version record by ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_version_id": {"type": "string", "description": "ID of the page version to retrieve"}
                    },
                    "required": ["page_version_id"]
                }
            }
        }
