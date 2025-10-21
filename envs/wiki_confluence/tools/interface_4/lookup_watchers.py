import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class LookupWatchers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, entity_id: str) -> str:
        """
        Retrieve all watchers for a space or page.
        """
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        watchers = data.get("watchers", {})
        spaces = data.get("spaces", {})
        pages = data.get("pages", {})
        
        # Validate entity_type
        if entity_type not in ["space", "page"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'space' or 'page'"
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
        
        # Find all watchers for the entity
        matching_watchers = []
        for watcher_id, watcher in watchers.items():
            if entity_type == "space" and watcher.get("space_id") == entity_id:
                matching_watchers.append(watcher.copy())
            elif entity_type == "page" and watcher.get("page_id") == entity_id:
                matching_watchers.append(watcher.copy())
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "count": len(matching_watchers),
            "watchers": matching_watchers
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "lookup_watchers",
                "description": "Retrieve all watchers for a space or page in the Confluence system. This tool fetches the complete list of users and groups subscribed to receive notifications about changes to a specific space or page. Returns watcher details including watcher IDs, types (user or group), and subscription timestamps. Essential for notification management, understanding content subscribers, and managing watch lists.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to get watchers for (required)",
                            "enum": ["space", "page"]
                        },
                        "entity_id": {
                            "type": "string",
                            "description": "ID of the space or page (required)"
                        }
                    },
                    "required": ["entity_type", "entity_id"]
                }
            }
        }
