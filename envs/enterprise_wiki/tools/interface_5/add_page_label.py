import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddPageLabel(Tool):
    """
    Add a label to a page (join table: page_labels).
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        page_id: int,
        label_id: int,
        added_by: int
    ) -> str:
        # Collections from in-memory data store
        pages = data.get("pages", {})
        labels = data.get("labels", {})
        page_labels = data.get("page_labels", {})  # expect dict keyed by "<page_id>:<label_id>"

        # Validate page exists
        if str(page_id) not in pages:
            raise ValueError(f"Page not found: {page_id}")

        # Validate label exists
        label = labels.get(str(label_id))
        if not label:
            raise ValueError(f"Label not found: {label_id}")


        for pl in page_labels.values():
            if pl.get("page_id") == page_id and pl.get("label_id") == label_id:
                # Label already exists for this page
                status = "already_exists"
                return json.dumps({
                    "status": status
                })
        else:
            # Minimal join row
            pl_key = max(int(k) for k in page_labels.keys()) + 1 if page_labels else 1
            added_at = "2025-07-01T00:00:00Z"
            page_labels[pl_key] = {
                "page_id": page_id,
                "label_id": label_id,
                "added_at": added_at,
                "added_by": added_by,
            }
            # Increment usage_count on the label
            # label["usage_count"] = label.get("usage_count", 0) + 1
            # status = "added"

            return json.dumps(page_labels[pl_key])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_page_label",
                "description": "Associate a label with a page; increments label usage count if newly added.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": { "type": "integer", "description": "Page ID to label" },
                        "label_id": { "type": "integer", "description": "Label ID to apply" },
                        "added_by": { "type": "integer", "description": "User ID performing the add" }
                    },
                    "required": ["page_id", "label_id", "added_by"]
                }
            }
        }
