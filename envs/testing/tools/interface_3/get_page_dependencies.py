import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPageDependencies(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        page_id = str(page_id)  # normalize once

        pages = data.get("pages", {})
        page_links = data.get("page_links", {})
        attachments = data.get("attachments", {})
        comments = data.get("comments", {})
        labels = data.get("page_labels", {})
        versions = data.get("page_versions", {})

        # Validate page exists
        if page_id not in pages:
            return json.dumps({"error": f"Page {page_id} not found"})

        page = pages[page_id]
        dependencies = {
            "page_id": page_id,
            "page_title": page.get("title"),
            "child_pages": [],
            "parent_page": None,
            "linked_from": [],
            "links_to": [],
            "attachments": [],
            "comments_count": 0,
            "labels": [],
            "versions": []
        }

        # Parent page
        parent_id = page.get("parent_page_id")
        if parent_id and (parent := pages.get(str(parent_id))):
            dependencies["parent_page"] = {
                "page_id": parent_id,
                "title": parent.get("title")
            }

        # Child pages
        dependencies["child_pages"] = [
            {"page_id": p.get("page_id"), "title": p.get("title"), "status": p.get("status")}
            for p in pages.values()
            if str(p.get("parent_page_id")) == page_id
        ]

        # Links (both directions handled in single pass)
        for link in page_links.values():
            source_id = str(link.get("source_page_id"))
            if source_id == page_id:
                dependencies["links_to"].append({
                    "link_id": link.get("link_id"),
                    "target_url": link.get("target_url"),
                    "link_text": link.get("link_text"),
                    "link_type": link.get("link_type"),
                    "is_broken": link.get("is_broken")
                })
            elif link.get("link_type") == "internal" and page_id in str(link.get("target_url")):
                if (source_page := pages.get(source_id)):
                    dependencies["linked_from"].append({
                        "link_id": link.get("link_id"),
                        "source_page_id": source_id,
                        "source_page_title": source_page.get("title"),
                        "link_text": link.get("link_text")
                    })

        # Attachments
        dependencies["attachments"] = [
            {
                "attachment_id": a.get("attachment_id"),
                "filename": a.get("filename"),
                "original_filename": a.get("original_filename"),
                "mime_type": a.get("mime_type"),
                "file_size": a.get("file_size"),
                "created_at": a.get("created_at")
            }
            for a in attachments.values()
            if str(a.get("page_id")) == page_id
        ]

        # Count comments (direct sum instead of loop)
        dependencies["comments_count"] = sum(
            1 for c in comments.values()
            if str(c.get("page_id")) == page_id and c.get("status") == "active"
        )

        # Labels
        dependencies["labels"] = [
            {
                "page_label_id": l.get("page_label_id"),
                "label_id": l.get("label_id"),
                "added_at": l.get("added_at"),
                "added_by_user_id": l.get("added_by_user_id")
            }
            for l in labels.values()
            if str(l.get("page_id")) == page_id
        ]

        # Versions
        dependencies["versions"] = sorted(
            [
                {
                    "page_version_id": v.get("page_version_id"),
                    "version_number": v.get("version_number"),
                    "title": v.get("title"),
                    "change_type": v.get("change_type"),
                    "created_at": v.get("created_at"),
                    "created_by_user_id": v.get("created_by_user_id")
                }
                for v in versions.values()
                if str(v.get("page_id")) == page_id
            ],
            key=lambda x: x["version_number"],
            reverse=True  # latest version first
        )

        return json.dumps(dependencies, ensure_ascii=False, indent=2)

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
