import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class GetUserActivityLog(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: int) -> str:
        activity_log: List[Dict[str, Any]] = []

        # Pages created
        for page in data.get("pages", {}).values():
            if str(page.get("created_by")) == str(user_id):
                activity_log.append({
                    "type": "page_created",
                    "page_id": page["id"],
                    "title": page.get("title"),
                    "timestamp": page.get("created_at")
                })

        # Comments made
        for comment in data.get("comments", {}).values():
            if str(comment.get("user_id")) == str(user_id):
                activity_log.append({
                    "type": "comment_added",
                    "comment_id": comment["id"],
                    "page_id": comment.get("page_id"),
                    "content": comment.get("content"),
                    "timestamp": comment.get("created_at")
                })

        # Spaces created
        for space in data.get("spaces", {}).values():
            if str(space.get("created_by")) == str(user_id):
                activity_log.append({
                    "type": "space_created",
                    "space_id": space["id"],
                    "name": space.get("name"),
                    "timestamp": space.get("created_at")
                })

        # Page versions
        for version in data.get("page_versions", {}).values():
            if version.get("updated_by") == user_id:
                activity_log.append({
                    "type": "page_edited",
                    "page_id": version.get("page_id"),
                    "version_id": version.get("id"),
                    "timestamp": version.get("updated_at")
                })

        # Attachments uploaded
        for attachment in data.get("attachments", {}).values():
            if str(attachment.get("uploaded_by")) == str(user_id):
                activity_log.append({
                    "type": "attachment_uploaded",
                    "attachment_id": attachment["id"],
                    "page_id": attachment.get("page_id"),
                    "filename": attachment.get("file_name"),
                    "timestamp": attachment.get("created_at")
                })

        # Notifications received
        for notif in data.get("notifications", {}).values():
            if str(notif.get("user_id")) == str(user_id):
                activity_log.append({
                    "type": "notification_received",
                    "notification_id": notif["id"],
                    "content": notif.get("content"),
                    "timestamp": notif.get("created_at")
                })

        # Optional: Sort by timestamp
        activity_log.sort(key=lambda x: x.get("timestamp") or "", reverse=True)

        return json.dumps(activity_log)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_activity_log",
                "description": "Aggregate user activity from pages, comments, spaces, versions, attachments, and notifications.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "User ID to retrieve activity log for"
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }
