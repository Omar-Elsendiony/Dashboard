import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPageDependencies(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        
        pages = data.get("pages", {})
        page_links = data.get("page_links", {})
        attachments = data.get("attachments", {})
        comments = data.get("comments", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"error": f"Page {page_id} not found"})
        
        page = pages[str(page_id)]
        dependencies = {
            "page_id": page_id,
            "page_title": page.get("title"),
            "child_pages": [],
            "parent_page": None,
            "linked_from": [],
            "links_to": [],
            "attachments": [],
            "comments_count": 0
        }
        
        # Get parent page
        if page.get("parent_page_id"):
            parent_page = pages.get(str(page.get("parent_page_id")))
            if parent_page:
                dependencies["parent_page"] = {
                    "page_id": page.get("parent_page_id"),
                    "title": parent_page.get("title")
                }
        
        # Get child pages
        for child_page in pages.values():
            if str(child_page.get("parent_page_id")) == str(page_id):
                dependencies["child_pages"].append({
                    "page_id": child_page.get("page_id"),
                    "title": child_page.get("title"),
                    "status": child_page.get("status")
                })
        
        # Get outgoing links from this page
        for link in page_links.values():
            if str(link.get("source_page_id")) == str(page_id):
                dependencies["links_to"].append({
                    "link_id": link.get("link_id"),
                    "target_url": link.get("target_url"),
                    "link_text": link.get("link_text"),
                    "link_type": link.get("link_type"),
                    "is_broken": link.get("is_broken")
                })
        
        # Get incoming links to this page (internal links only)
        for link in page_links.values():
            if (link.get("link_type") == "internal" and 
                str(page_id) in str(link.get("target_url"))):
                source_page = pages.get(str(link.get("source_page_id")))
                if source_page:
                    dependencies["linked_from"].append({
                        "link_id": link.get("link_id"),
                        "source_page_id": link.get("source_page_id"),
                        "source_page_title": source_page.get("title"),
                        "link_text": link.get("link_text")
                    })
        
        # Get attachments
        for attachment in attachments.values():
            if str(attachment.get("page_id")) == str(page_id):
                dependencies["attachments"].append({
                    "attachment_id": attachment.get("attachment_id"),
                    "filename": attachment.get("filename"),
                    "original_filename": attachment.get("original_filename"),
                    "mime_type": attachment.get("mime_type"),
                    "file_size": attachment.get("file_size"),
                    "created_at": attachment.get("created_at")
                })
        
        # Count comments
        comment_count = 0
        for comment in comments.values():
            if str(comment.get("page_id")) == str(page_id) and comment.get("status") == "active":
                comment_count += 1
        dependencies["comments_count"] = comment_count
        
        return json.dumps(dependencies)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_dependencies",
                "description": "Get page dependencies and their relationships",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page to check dependencies for"}
                    },
                    "required": ["page_id"]
                }
            }
        }
