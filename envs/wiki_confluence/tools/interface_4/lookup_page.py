import json
from typing import Any, Dict,Optional
from tau_bench.envs.tool import Tool
import re
class LookupPage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: Optional[str] = None, page_name: Optional[str] = None) -> str:
        """
        Retrieve single page details by ID or search pages by page name.
        """

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        pages = data.get("pages", {})
        if not isinstance(pages, dict):
            return json.dumps({"success": False, "error": "Invalid pages container: expected dict at data['pages']"})
        # Search by page id
        if page_id:
            if page_id in pages:
                page_data = pages[page_id].copy()
                return json.dumps({
                    "success": True,
                    "page_data": page_data
                })
            if not page_name:

                return json.dumps({"success": False, "error": f"Page with id '{page_id}' not found"})
        # Seach by page name
        if page_name:
            pattern = re.compile(re.escape(page_name), re.IGNORECASE)
            return json.dumps({"success": True, "pages": [page.copy() for page in pages.values() if isinstance(page, dict) and pattern.search(page.get("title", ""))]})

        return json.dumps({"success": False, "error": "Neither 'page_id' nor 'page_name' provided"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "lookup_page",
                "description": "Retrieve page details by ID or list of pages by page name in the Confluence system. This tool returns page JSON on ID match or a list of pages on page name match.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "Unique identifier of the page"
                        },
                        "page_name": {
                            "type": "string",
                            "description": "Page title to search for"
                        }
                    },
                    "required": []
                }
            }
        }

