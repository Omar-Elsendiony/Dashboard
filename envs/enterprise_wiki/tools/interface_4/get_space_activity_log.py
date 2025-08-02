import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class GetSpaceActivityLog(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: int) -> str:
        logs = []

        for page in data.get("pages", {}).values():
            if str(page.get("space_id")) == str(space_id):
                logs.append({
                    "type": "page_created",
                    "page_id": page["id"],
                    "title": page["title"],
                    "created_by": page["created_by"],
                    "timestamp": page["created_at"]
                })

        for comment in data.get("comments", {}).values():
            if str(comment.get("space_id")) == str(space_id):
                logs.append({
                    "type": "comment_added",
                    "comment_id": comment["id"],
                    "page_id": comment["page_id"],
                    "user_id": comment["user_id"],
                    "timestamp": comment["created_at"]
                })

        for notif in data.get("notifications", {}).values():
            if notif.get("target_type") == "space" and str(notif.get("target_id")) == str(space_id):
                notif["type"] = notif.get("type", "unknown") + "_notification"
                logs.append(notif)

        logs.sort(key=lambda x: x.get("timestamp") or "", reverse=True)
        return json.dumps(logs)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_space_activity_log",
                "description": "Get the activity log of a specific space, including page creation and comments.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "integer", "description": "ID of the space"}
                    },
                    "required": ["space_id"]
                }
            }
        }
