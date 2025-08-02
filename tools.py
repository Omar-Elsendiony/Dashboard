from typing import Any, Dict
from typing import Any, Dict, Optional
import json

class Tools:
    @staticmethod
    def get_user_groups_invoke(data: Dict[str, Any], user_id: int) -> str:
        
        user_groups = data.get("user_groups", {})
        groups = data.get("groups", {})
        group_ids = [ug["group_id"] for ug in user_groups.values() if str(ug["user_id"]) == str(user_id)]
        print(f"User ID: {user_id}, Group IDs: {group_ids}")
        return json.dumps([groups[str(gid)] for gid in group_ids if str(gid) in groups])

    @staticmethod
    def update_notification_read_status_invoke(data: Dict[str, Any], notification_id: int, is_read: bool) -> str:
        notifications = data.get("notifications", {})
        notification = notifications.get(str(notification_id))

        if not notification:
            raise ValueError("Notification not found")

        notification["is_read"] = is_read

        return json.dumps({
            "status": "updated",
            "notification_id": notification_id,
            "is_read": is_read
        })

    @staticmethod
    def get_spaces_by_filters_invoke(data: Dict[str, Any],  **criteria: Any) -> str:
        """
        Return all spaces that match *all* supplied non-None criteria.
        Example call:
            GetSpacesByFilters.get_spaces_by_filters_invoke(data, name="General Documentation", status="current")
        """
        spaces = data.get("spaces", {})
        filtered_spaces = []
        # print("Criteria received:", criteria)
        
        # Remove params that aren't actual filters (defensive) and drop None values
        criteria = {
            k: v for k, v in criteria.items()
            if k not in ("data",) and v is not None  # 'data' shouldn't be passed, but guard anyway
        }
        
        # Check for empty criteria after filtering
        if not criteria:
            raise ValueError("At least one filter criterion must be provided.")

        for space in spaces.values():
            # require all provided criteria to match exactly
            if all(str(space.get(k)) == str(v) for k, v in criteria.items()):
                filtered_spaces.append(space)

        return json.dumps(filtered_spaces)

    @staticmethod
    def get_user_notifications_invoke(data: Dict[str, Any], user_id: int) -> str:
        notifications = data.get("notifications", {})
        user_notifications = [
            notif for notif in notifications.values()
            if str(notif["user_id"]) == str(user_id)
        ]
        return json.dumps(user_notifications)

    @staticmethod
    def update_comment_status_invoke(data: Dict[str, Any], comment_id: int, status: str) -> str:
        comments = data.get("comments", {})
        comment = comments.get(str(comment_id))
        if not comment:
            raise ValueError("Comment not found")
        
        valid_statuses = ["active", "deleted", "resolved"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        comment["status"] = status
        # set_updated_at("comments", comment_id, data)
        comment["updated_at"] = None
        return json.dumps(comment)

    @staticmethod
    def get_users_by_filters_invoke(
        data: Dict[str, Any],
        status: Optional[str] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
        locale: Optional[str] = None,
        timezone: Optional[str] = None,
    ) -> str:
        users = data.get("users", {})
        filtered_users = []
        
        if (status is None and username is None and email is None and locale is None and timezone is None):
            raise ValueError("At least one filter criterion must be provided.")

        for user in users.values():
            if status and user.get("status") != status:
                continue
            if username and user.get("username") != username:
                continue
            if email and user.get("email") != email:
                continue
            if locale and user.get("locale") != locale:
                continue
            if timezone and user.get("timezone") != timezone:
                continue
            filtered_users.append(user)

        return json.dumps(filtered_users)

    @staticmethod
    def update_watcher_settings_invoke(
        data: Dict[str, Any],
        watcher_id: int,
        watch_type: Optional[str] = None,
        notifications_enabled: Optional[bool] = None
    ) -> str:
        watchers = data.get("watchers", {})
        watcher = watchers.get(str(watcher_id))
        if not watcher:
            raise ValueError("Watcher not found")
        
        if watch_type is None and notifications_enabled is None:
            raise ValueError("At least one of watch_type or notifications_enabled must be provided")
        
        if watch_type:
            valid_types = ["watching", "not_watching"]
            if watch_type not in valid_types:
                raise ValueError(f"Invalid watch type. Must be one of {valid_types}")
            watcher["watch_type"] = watch_type
        
        if notifications_enabled is not None:
            watcher["notifications_enabled"] = notifications_enabled
        
        return json.dumps(watcher)

    @staticmethod
    def update_user_status_invoke(data: Dict[str, Any], user_id: int, status: str) -> str:
        users = data.get("users", {})
        user = users.get(str(user_id))
        if not user:
            raise ValueError("User not found")
        
        valid_statuses = ["active", "inactive", "suspended"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        user["status"] = status
        # set_updated_at("users", user_id, data)
        user["updated_at"] = None
        return json.dumps(user)

    @staticmethod
    def update_comment_content_invoke(
        data: Dict[str, Any],
        comment_id: int,
        content: str,
        content_format: str = "markdown"
    ) -> str:
        comments = data.get("comments", {})
        comment = comments.get(str(comment_id))
        if not comment:
            raise ValueError("Comment not found")
        
        comment["content"] = content
        comment["content_format"] = content_format
        comment["updated_at"] = None
        
        return json.dumps(comment)

    @staticmethod
    def get_comment_info_invoke(data: Dict[str, Any], comment_id: int) -> str:
        comments = data.get("comments", {})
        comment = comments.get(str(comment_id))
        if not comment:
            raise ValueError("Comment not found")
        return json.dumps(comment)

    @staticmethod
    def get_space_pages_invoke(data: Dict[str, Any], space_id: str) -> str:
        pages = data.get("pages", {})
        spaces = data.get("spaces", {})
        
        if space_id not in spaces:
            raise ValueError("Space not found")
        
        space_pages = []
        for page_id, page in pages.items():
            if str(page.get("space_id")) == str(space_id):
                space_pages.append(page)
        
        return json.dumps(space_pages)

    @staticmethod
    def delete_watcher_invoke(data: Dict[str, Any], watcher_id: int) -> str:
        watchers = data.get("watchers", {})
        if str(watcher_id) not in watchers:
            raise ValueError("Watcher not found")
        
        del watchers[str(watcher_id)]
        return json.dumps({"success": True})

    @staticmethod
    def create_attachment_invoke(data: Dict[str, Any], filename: str, original_filename: str, 
               mime_type: str, file_size: int, storage_path: str, uploaded_by: str,
               storage_type: str = None, version: str = None, page_id: Optional[str] = None, 
               comment_id: Optional[str] = None) -> str:
        attachments = data.get("attachments", {})
        users = data.get("users", {})
        
        if uploaded_by not in users:
            raise ValueError("User not found")
        
        if page_id:
            pages = data.get("pages", {})
            if page_id not in pages:
                raise ValueError("Page not found")
        
        if comment_id:
            comments = data.get("comments", {})
            if comment_id not in comments:
                raise ValueError("Comment not found")
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return 1
            return (max(int(k) for k in table.keys()) + 1)
        
        attachment_id = generate_id(attachments)
        
        new_attachment = {
            "id": attachment_id,
            "page_id": page_id,
            "comment_id": comment_id,
            "filename": filename,
            "original_filename": original_filename,
            "mime_type": mime_type,
            "file_size": file_size,
            "storage_path": storage_path,
            "storage_type": storage_type,
            "version": version,
            "uploaded_by": uploaded_by,
            "created_at": "2025-07-01T00:00:00Z",
        }
        
        attachments[str(attachment_id)] = new_attachment
        
        return json.dumps({"attachment_id": attachment_id})

    @staticmethod
    def create_comment_invoke(
        data: Dict[str, Any],
        page_id: int,
        content: str,
        created_by: int,
        content_format: str = "markdown",
        parent_id: Optional[int] = None
    ) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        # Validate page
        pages = data.get("pages", {})
        if str(page_id) not in pages:
            raise ValueError("Page not found")
        
        # Validate user
        users = data.get("users", {})
        if str(created_by) not in users:
            raise ValueError("User not found")
        
        # Validate parent comment if exists
        if parent_id:
            comments = data.get("comments", {})
            if str(parent_id) not in comments:
                raise ValueError("Parent comment not found")
        
        # Create new comment
        comments = data.setdefault("comments", {})
        new_id = generate_id(comments)
        
        thread_level = 0
        if parent_id:
            # Calculate thread level based on parent
            parent = comments[str(parent_id)]
            thread_level = parent.get("thread_level", 0) + 1

        created_at = updated_at = "2025-07-01T00:00:00Z"


        new_comment = {
            "id": new_id,
            "page_id": page_id,
            "parent_id": parent_id,
            "content": content,
            "content_format": content_format,
            "status": "active",
            "thread_level": thread_level,
            "created_at": created_at,
            "updated_at": updated_at,
            "created_by": created_by
        }
        
        comments[str(new_id)] = new_comment
        return json.dumps(new_comment)

    @staticmethod
    def create_watcher_invoke(
        data: Dict[str, Any],
        user_id: int,
        target_type: str,
        target_id: int,
        watch_type: str = "watching",
        notifications_enabled: bool = True
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        # Validate user
        users = data.get("users", {})
        if str(user_id) not in users:
            raise ValueError("User not found")
        
        # Validate target type
        valid_targets = ["space", "page", "user"]
        if target_type not in valid_targets:
            raise ValueError(f"Invalid target type. Must be one of {valid_targets}")
        
        # Create watcher
        watchers = data.setdefault("watchers", {})
        new_id = generate_id(watchers)
        
        
        created_at = "2025-07-01T00:00:00Z"

        
        new_watcher = {
            "id": new_id,
            "user_id": user_id,
            "target_type": target_type,
            "target_id": target_id,
            "watch_type": watch_type,
            "notifications_enabled": notifications_enabled,
            "created_at": created_at
        }
        
        watchers[str(new_id)] = new_watcher
        return json.dumps(new_watcher)

    @staticmethod
    def update_notification_delivery_method_invoke(data: Dict[str, Any], notification_id: int, delivery_method: str) -> str:
        notifications = data.get("notifications", {})
        notification = notifications.get(str(notification_id))
        if not notification:
            raise ValueError("Notification not found")
        
        valid_methods = ["web", "email", "both"]
        if delivery_method not in valid_methods:
            raise ValueError(f"Invalid delivery method. Must be one of {valid_methods}")
        
        notification["delivery_method"] = delivery_method
        return json.dumps({"success": True})

    @staticmethod
    def create_notification_invoke(
        data: Dict[str, Any],
        user_id: int,
        notification_type: str,
        title: str,
        message: str,
        created_by: int,
        target_type: str,
        target_id: int,
        delivery_method: str = "web"  # <-- add this
    ) -> str:

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        # Validate user
        users = data.get("users", {})
        if str(user_id) not in users:
            raise ValueError("User not found")
        
        # Validate created_by
        if str(created_by) not in users:
            raise ValueError("Created_by user not found")
        
        # Create notification
        notifications = data.setdefault("notifications", {})
        new_id = generate_id(notifications)
        
        
        created_at = "2025-07-01T00:00:00Z"

        
        new_notification = {
            "id": new_id,
            "user_id": user_id,
            "type": notification_type,
            "title": title,
            "message": message,
            "target_type": target_type,
            "target_id": target_id,
            "is_read": False,
            "read_at": None,
            "delivery_method": "web",
            "email_sent": False,
            "created_at": created_at,
            "created_by": created_by
        }
        
        notifications[str(new_id)] = new_notification
        return json.dumps(new_notification)

    @staticmethod
    def get_user_watchers_invoke(data: Dict[str, Any], user_id: int) -> str:
        watchers = data.get("watchers", {})  # watcher_id -> {"target_type", "target_id", "user_id"}
        user_watch_targets = set()

        # Step 1: collect all targets the user is watching
        for w in watchers.values():
            if str(w["user_id"]) == str(user_id):
                user_watch_targets.add((w["target_type"], str(w["target_id"])))

        if not user_watch_targets:
            return json.dumps([])

        # Step 2: find other users watching the same targets
        result = list()
        for w in watchers.values():
            target = (w["target_type"], str(w["target_id"]))
            if target in user_watch_targets and str(w["user_id"]) != str(user_id):
                result.append(w)

        return json.dumps(result)

    @staticmethod
    def get_user_by_email_invoke(data: Dict[str, Any], email: str) -> str:
        users = data.get("users", {})
        
        for user_id, user in users.items():
            if user.get("email") == email:
                return json.dumps(user)
        
        raise ValueError("User not found")

    @staticmethod
    def get_page_comments_invoke(data: Dict[str, Any], page_id: int) -> str:
        comments = data.get("comments", {})
        print(type(comments))
        return json.dumps([c["id"] for c in comments.values() if c["page_id"] == int(page_id)])

