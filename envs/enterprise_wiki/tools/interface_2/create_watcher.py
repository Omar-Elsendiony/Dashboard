import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateWatcher(Tool):
    @staticmethod
    def invoke(
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
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_watcher",
                "description": "Create a new watcher",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "ID of the user"},
                        "target_type": {"type": "string", "description": "Type of target (space/page/user)"},
                        "target_id": {"type": "integer", "description": "ID of the target"},
                        "watch_type": {"type": "string", "description": "Watch type (watching/not_watching)"},
                        "notifications_enabled": {"type": "boolean", "description": "Whether notifications are enabled"}
                    },
                    "required": ["user_id", "target_type", "target_id"]
                }
            }
        }

