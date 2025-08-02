import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteWatcher(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], watcher_id: int) -> str:
        watchers = data.get("watchers", {})
        if str(watcher_id) not in watchers:
            raise ValueError("Watcher not found")
        
        del watchers[str(watcher_id)]
        return json.dumps({"success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_watcher",
                "description": "Remove a watcher",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "watcher_id": {"type": "integer", "description": "ID of the watcher"}
                    },
                    "required": ["watcher_id"]
                }
            }
        }
