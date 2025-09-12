import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetWatchers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], watcher_id: Optional[str] = None, user_id: Optional[str] = None,
               target_type: Optional[str] = None, target_id: Optional[str] = None, watch_type: Optional[str] = None) -> str:
        
        watchers = data.get("watchers", {})
        result = []
        
        for wid, watcher in watchers.items():
            # Apply filters
            if watcher_id and str(watcher_id) != wid:
                continue
            if user_id and watcher.get("user_id") != user_id:
                continue
            if target_type and watcher.get("target_type") != target_type:
                continue
            if target_id and watcher.get("target_id") != target_id:
                continue
            if watch_type and watcher.get("watch_type") != watch_type:
                continue
            
            result.append({
                "watcher_id": wid,
                "user_id": watcher.get("user_id"),
                "target_type": watcher.get("target_type"),
                "target_id": watcher.get("target_id"),
                "watch_type": watcher.get("watch_type"),
                "notifications_enabled": watcher.get("notifications_enabled"),
                "created_at": watcher.get("created_at")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_watchers",
                "description": "Get watchers matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "watcher_id": {"type": "string", "description": "ID of the watcher"},
                        "user_id": {"type": "string", "description": "ID of the user who is watching"},
                        "target_type": {"type": "string", "description": "Type of target being watched (space, page, user)"},
                        "target_id": {"type": "string", "description": "ID of the target being watched"},
                        "watch_type": {"type": "string", "description": "Type of watch (watching, not_watching)"}
                    },
                    "required": []
                }
            }
        }
