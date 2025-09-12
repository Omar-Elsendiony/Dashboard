import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPageLinks(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], link_id: Optional[str] = None, source_page_id: Optional[str] = None,
               target_url: Optional[str] = None, link_type: Optional[str] = None, is_broken: Optional[bool] = None) -> str:
        
        page_links = data.get("page_links", {})
        result = []
        
        for plid, link in page_links.items():
            # Apply filters
            if link_id and str(link_id) != plid:
                continue
            if source_page_id and link.get("source_page_id") != source_page_id:
                continue
            if target_url and link.get("target_url") != target_url:
                continue
            if link_type and link.get("link_type") != link_type:
                continue
            if is_broken is not None and link.get("is_broken") != is_broken:
                continue
            
            result.append({
                "link_id": plid,
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
                "name": "get_page_links",
                "description": "Get page links matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "link_id": {"type": "string", "description": "ID of the link"},
                        "source_page_id": {"type": "string", "description": "ID of the page containing the link"},
                        "target_url": {"type": "string", "description": "URL that the link points to"},
                        "link_type": {"type": "string", "description": "Type of link (internal, external)"},
                        "is_broken": {"type": "boolean", "description": "Whether the link is broken (True/False)"}
                    },
                    "required": []
                }
            }
        }
