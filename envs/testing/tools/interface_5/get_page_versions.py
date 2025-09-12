import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPageVersions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_version_id: Optional[str] = None, page_id: Optional[str] = None,
               creator_id: Optional[str] = None, change_type: Optional[str] = None) -> str:
        
        page_versions = data.get("page_versions", {})
        result = []
        
        for pvid, version in page_versions.items():
            # Apply filters
            if page_version_id and str(page_version_id) != pvid:
                continue
            if page_id and version.get("page_id") != page_id:
                continue
            if creator_id and version.get("created_by_user_id") != creator_id:
                continue
            if change_type and version.get("change_type") != change_type:
                continue
            
            result.append({
                "page_version_id": pvid,
                "page_id": version.get("page_id"),
                "version_number": version.get("version_number"),
                "title": version.get("title"),
                "content": version.get("content"),
                "content_format": version.get("content_format"),
                "change_type": version.get("change_type"),
                "created_at": version.get("created_at"),
                "created_by_user_id": version.get("created_by_user_id")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_versions",
                "description": "Get page versions matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_version_id": {"type": "string", "description": "ID of the page version"},
                        "page_id": {"type": "string", "description": "ID of the page"},
                        "creator_id": {"type": "string", "description": "ID of the user who created the version"},
                        "change_type": {"type": "string", "description": "Type of change (major, minor)"}
                    },
                    "required": []
                }
            }
        }
