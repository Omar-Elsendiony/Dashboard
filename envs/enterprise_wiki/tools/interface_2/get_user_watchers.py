import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserWatchers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: int) -> str:
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
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_watchers",
                "description": "Get users who are watching the same pages or spaces as the given user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "ID of the user to check shared watchers with"}
                    },
                    "required": ["user_id"]
                }
            }
        }
