import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str, target_type: str, 
               target_id: str, notification_preferences: Optional[Dict[str, Any]] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        pages = data.get("pages", {})
        watchers = data.get("watchers", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": f"Requesting user {requesting_user_id} not found"})
        
        # Validate target_type
        valid_target_types = ["space", "page", "user"]
        if target_type not in valid_target_types:
            return json.dumps({"error": f"Invalid target_type. Must be one of {valid_target_types}"})
        
        # Validate target exists based on type
        if target_type == "space" and str(target_id) not in spaces:
            return json.dumps({"error": f"Space {target_id} not found"})
        elif target_type == "page" and str(target_id) not in pages:
            return json.dumps({"error": f"Page {target_id} not found"})
        elif target_type == "user" and str(target_id) not in users:
            return json.dumps({"error": f"User {target_id} not found"})
        
        # Check if subscription already exists
        for watcher in watchers.values():
            if (watcher.get("user_id") == requesting_user_id and 
                watcher.get("target_type") == target_type and
                str(watcher.get("target_id")) == str(target_id) and
                watcher.get("watch_type") == "watching"):
                return json.dumps({"error": "Subscription already exists"})
        
        subscription_id = generate_id(watchers)
        timestamp = "2025-10-01T00:00:00"
        
        notifications_enabled = True
        if notification_preferences:
            notifications_enabled = notification_preferences.get("notifications_enabled", True)
        
        new_subscription = {
            "watcher_id": subscription_id,
            "user_id": requesting_user_id,
            "target_type": target_type,
            "target_id": target_id,
            "watch_type": "watching",
            "notifications_enabled": notifications_enabled,
            "created_at": timestamp
        }
        
        watchers[str(subscription_id)] = new_subscription
        return json.dumps({"subscription_id": str(subscription_id), "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_subscription",
                "description": "Create a subscription for a user to watch a space, page, or user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user creating the subscription"},
                        "target_type": {"type": "string", "description": "Type of target (space, page, user)"},
                        "target_id": {"type": "string", "description": "ID of the space, page, or user to watch"},
                        "notification_preferences": {"type": "object", "description": "Notification settings with notifications_enabled (True/False)"}
                    },
                    "required": ["requesting_user_id", "target_type", "target_id"]
                }
            }
        }
