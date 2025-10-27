import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool
import re


class GetPage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: Optional[str] = None, page_name: Optional[str] = None, space_id: Optional[str] = None) -> str:
        """
        Retrieve single page details by ID or search pages by page name.
        Optionally filter by space_id.
        """

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        pages = data.get("pages", {})
        if not isinstance(pages, dict):
            return json.dumps({"success": False, "error": "Invalid pages container: expected dict at data['pages']"})
        
        # search by page id
        if page_id:
            if page_id in pages:
                page_data = pages[page_id].copy()
                # Filter by space_id if provided
                if space_id and page_data.get("space_id") != space_id:
                    return json.dumps({"success": False, "error": f"Page with id '{page_id}' not found in space '{space_id}'"})
                return json.dumps({
                    "success": True,
                    "page_data": page_data
                })
            if not page_name:
                return json.dumps({"success": False, "error": f"Page with id '{page_id}' not found"})
        
        # search by page name
        if page_name:
            pattern = re.compile(re.escape(page_name), re.IGNORECASE)
            matching_pages = [page.copy() for page in pages.values() if isinstance(page, dict) and pattern.search(page.get("title", ""))]
            
            # Filter by space_id if provided
            if space_id:
                matching_pages = [page for page in matching_pages if page.get("space_id") == space_id]
            
            return json.dumps({"success": True, "pages": matching_pages})

        return json.dumps({"success": False, "error": "Neither 'page_id' nor 'page_name' provided"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page",
                "description": "Retrieve page details by ID or search pages by title in the Confluence system. This tool returns a single page on ID match or a list of pages on title match. Can optionally filter results by space_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "Unique identifier of the page"
                        },
                        "page_name": {
                            "type": "string",
                            "description": "Page title to search for (supports partial matching, case-insensitive)"
                        },
                        "space_id": {
                            "type": "string",
                            "description": "Optional space ID to filter results by a specific space"
                        }
                    },
                    "required": []
                }
            }
        }
