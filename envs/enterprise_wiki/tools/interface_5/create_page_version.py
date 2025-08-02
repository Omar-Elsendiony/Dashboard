import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreatePageVersion(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str, title: str, content: str, 
               content_format: str, change_comment: str, change_type: str, created_by: str) -> str:
        page_versions = data.get("page_versions", {})
        pages = data.get("pages", {})
        users = data.get("users", {})
        
        if page_id not in pages:
            raise ValueError("Page not found")
        
        if created_by not in users:
            raise ValueError("User not found")
                
        page_versions_number = 0
        page_version_new_id = 1
        
        for pv_key, pv_value in page_versions.items():
            if pv_value.get("page_id") == page_id:
                page_versions_number += 1
            if pv_value.get("id") >= page_version_new_id:
                page_version_new_id = pv_value.get("id") + 1
            
                
        new_version = {
            "id": page_version_new_id,
            "page_id": page_id,
            "title": title,
            "content": content,
            "content_format": content_format,
            "change_comment": change_comment,
            "change_type": change_type,
            "created_by": created_by,
            # "created_at": 
        }
        
        page_versions[str(page_version_new_id)] = new_version
        
        return json.dumps(page_versions[str(page_version_new_id)])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_page_version",
                "description": "Create a new page version",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The ID of the page"
                        },
                        "title": {
                            "type": "string",
                            "description": "The title of the page version"
                        },
                        "content": {
                            "type": "string",
                            "description": "The content of the page version"
                        },
                        "content_format": {
                            "type": "string",
                            "description": "The format of the content"
                        },
                        "change_comment": {
                            "type": "string",
                            "description": "Comment describing the changes"
                        },
                        "change_type": {
                            "type": "string",
                            "description": "Type of change made"
                        },
                        "created_by": {
                            "type": "string",
                            "description": "The ID of the user creating the version"
                        }
                    },
                    "required": ["page_id", "title", "content", "content_format", "change_comment", "change_type", "created_by"]
                }
            }
        }
