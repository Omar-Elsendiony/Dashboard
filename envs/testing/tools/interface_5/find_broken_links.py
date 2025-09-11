import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FindBrokenLinks(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: Optional[str] = None) -> str:
        
        page_links = data.get("page_links", {})
        pages = data.get("pages", {})
        result = []
        
        for link_id, link in page_links.items():
            # Only return broken links
            if not link.get("is_broken", False):
                continue
            
            # If space_id filter is provided, check if source page is in that space
            if space_id:
                source_page_id = link.get("source_page_id")
                if source_page_id and str(source_page_id) in pages:
                    page = pages[str(source_page_id)]
                    if page.get("space_id") != space_id:
                        continue
                else:
                    continue
            
            result.append({
                "link_id": link_id,
                "source_page_id": link.get("source_page_id"),
                "target_url": link.get("target_url"),
                "link_text": link.get("link_text"),
                "link_type": link.get("link_type"),
                "is_broken": link.get("is_broken"),
                "last_checked_at": link.get("last_checked_at"),
                "created_at": link.get("created_at")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_broken_links",
                "description": "Find broken links, optionally filtered by space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space to search for broken links (optional)"}
                    },
                    "required": []
                }
            }
        }
