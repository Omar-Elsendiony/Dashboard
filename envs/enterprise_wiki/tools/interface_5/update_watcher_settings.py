import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateWatcherSettings(Tool):
    @staticmethod
    def invoke(
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
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_watcher_settings",
                "description": "Update watcher settings",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "watcher_id": {"type": "integer", "description": "ID of the watcher"},
                        "watch_type": {"type": "string", "description": "Watch type (watching/not_watching)"},
                        "notifications_enabled": {"type": "boolean", "description": "Whether notifications are enabled"}
                    },
                    "required": ["watcher_id"]
                }
            }
        }
