import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FindBrokenLinks(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: Optional[str] = None) -> str:
        
        page_links = data.get("page_links", {})
        spaces = data.get("spaces", {})
        pages = data.get("pages", {})
        
        # Validate space if provided
        if space_id and str(space_id) not in spaces:
            return json.dumps({"error": f"Space {space_id} not found"})
        
        # Find broken links
        broken_links = []
        
        for link in page_links.values():
            # Check if link is marked as broken
            if link.get("is_broken", False):
                # If space_id is specified, filter by space
                if space_id:
                    source_page_id = link.get("source_page_id")
                    if str(source_page_id) in pages:
                        source_page = pages[str(source_page_id)]
                        if source_page.get("space_id") == space_id:
                            broken_links.append(link)
                else:
                    broken_links.append(link)
        
        return json.dumps(broken_links)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_broken_links",
                "description": "Find all broken links, optionally filtered by space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space to filter broken links (optional)"}
                    },
                    "required": []
                }
            }
        }
