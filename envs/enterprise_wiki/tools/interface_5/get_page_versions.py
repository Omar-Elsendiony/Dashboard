import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPageVersions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        page_versions = data.get("page_versions", {})
        pages = data.get("pages", {})
        
        if page_id not in pages:
            raise ValueError("Page not found")
        
        versions = []
        for version_id, version in page_versions.items():
            if str(version.get("page_id")) == str(page_id):
                versions.append(version)
        
        return json.dumps(versions)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_versions",
                "description": "Get all versions of a page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The ID of the page"
                        }
                    },
                    "required": ["page_id"]
                }
            }
        }
