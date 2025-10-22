import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SetWatchers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, watcher_type: str,
               watcher_id: str, entity_type: str, entity_id: str) -> str:
        """
        Add or remove watchers for spaces or pages.
        
        Actions:
        - add: Add watcher (requires watcher_type, watcher_id, entity_type, entity_id)
        - remove: Remove watcher (requires watcher_type, watcher_id, entity_type, entity_id)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["add", "remove"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'add' or 'remove'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        watchers = data.get("watchers", {})
        users = data.get("users", {})
        groups = data.get("groups", {})
        spaces = data.get("spaces", {})
        pages = data.get("pages", {})
        
        # Validate entity_type
        if entity_type not in ["space", "page"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'space' or 'page'"
            })
        
        # Validate watcher_type
        if watcher_type not in ["user", "group"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid watcher_type '{watcher_type}'. Must be 'user' or 'group'"
            })
        
        # Validate entity exists
        if entity_type == "space":
            if entity_id not in spaces:
                return json.dumps({
                    "success": False,
                    "error": f"Space {entity_id} not found"
                })
        elif entity_type == "page":
            if entity_id not in pages:
                return json.dumps({
                    "success": False,
                    "error": f"Page {entity_id} not found"
                })
        
        # Validate watcher exists
        if watcher_type == "user":
            if watcher_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User {watcher_id} not found"
                })
        elif watcher_type == "group":
            if watcher_id not in groups:
                return json.dumps({
                    "success": False,
                    "error": f"Group {watcher_id} not found"
                })
        
        if action == "add":
            # Check if already watching
            for watch_id, watch in watchers.items():
                matches_watcher = (
                    (watcher_type == "user" and watch.get("user_id") == watcher_id) or
                    (watcher_type == "group" and watch.get("group_id") == watcher_id)
                )
                matches_entity = (
                    (entity_type == "space" and watch.get("space_id") == entity_id) or
                    (entity_type == "page" and watch.get("page_id") == entity_id)
                )
                if matches_watcher and matches_entity:
                    return json.dumps({
                        "success": False,
                        "error": f"{watcher_type.capitalize()} {watcher_id} is already watching {entity_type} {entity_id}"
                    })
            
            # Generate new watcher ID
            new_watcher_id = generate_id(watchers)
            timestamp = "2025-10-01T12:00:00"
            
            new_watcher = {
                "watcher_id": str(new_watcher_id),
                "user_id": watcher_id if watcher_type == "user" else None,
                "group_id": watcher_id if watcher_type == "group" else None,
                "space_id": entity_id if entity_type == "space" else None,
                "page_id": entity_id if entity_type == "page" else None,
                "watched_at": timestamp
            }
            
            watchers[str(new_watcher_id)] = new_watcher
            
            return json.dumps({
                "success": True,
                "action": "add",
                "watcher_id": str(new_watcher_id),
                "message": f"{watcher_type.capitalize()} {watcher_id} is now watching {entity_type} {entity_id}",
                "watcher_data": new_watcher
            })
        
        elif action == "remove":
            # Find and remove the watcher
            watcher_to_remove = None
            key_to_remove = None
            
            for watch_id, watch in watchers.items():
                matches_watcher = (
                    (watcher_type == "user" and watch.get("user_id") == watcher_id) or
                    (watcher_type == "group" and watch.get("group_id") == watcher_id)
                )
                matches_entity = (
                    (entity_type == "space" and watch.get("space_id") == entity_id) or
                    (entity_type == "page" and watch.get("page_id") == entity_id)
                )
                if matches_watcher and matches_entity:
                    watcher_to_remove = watch.copy()
                    key_to_remove = watch_id
                    break
            
            if not watcher_to_remove:
                return json.dumps({
                    "success": False,
                    "error": f"{watcher_type.capitalize()} {watcher_id} is not watching {entity_type} {entity_id}"
                })
            
            del watchers[key_to_remove]
            
            return json.dumps({
                "success": True,
                "action": "remove",
                "message": f"{watcher_type.capitalize()} {watcher_id} removed from watching {entity_type} {entity_id}",
                "watcher_data": watcher_to_remove
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "set_watchers",
                "description": "Add or remove watchers for spaces or pages in the Confluence system. This tool manages notification subscriptions by adding users or groups as watchers to receive notifications about changes, or removing existing watch subscriptions. Validates entity and watcher existence, prevents duplicate watch subscriptions, and ensures clean removal of existing watches. Essential for notification management, keeping stakeholders informed of content changes, and facilitating collaborative awareness.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'add' to subscribe to notifications, 'remove' to unsubscribe",
                            "enum": ["add", "remove"]
                        },
                        "watcher_type": {
                            "type": "string",
                            "description": "Type of watcher (required)",
                            "enum": ["user", "group"]
                        },
                        "watcher_id": {
                            "type": "string",
                            "description": "ID of the user or group to watch (required)"
                        },
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to watch (required)",
                            "enum": ["space", "page"]
                        },
                        "entity_id": {
                            "type": "string",
                            "description": "ID of the space or page to watch (required)"
                        }
                    },
                    "required": ["action", "watcher_type", "watcher_id", "entity_type", "entity_id"]
                }
            }
        }
