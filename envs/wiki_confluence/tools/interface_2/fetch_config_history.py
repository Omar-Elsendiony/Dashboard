import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FetchConfigHistory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str) -> str:
        """
        Retrieve configuration change history for a space.
        """
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        space_config_history = data.get("space_config_history", {})
        spaces = data.get("spaces", {})
        
        # Validate space exists
        if space_id not in spaces:
            return json.dumps({
                "success": False,
                "error": f"Space {space_id} not found"
            })
        
        # Find all config history entries for the space
        matching_history = []
        for history_id, history in space_config_history.items():
            if history.get("space_id") == space_id:
                matching_history.append(history.copy())
        
        # Sort by config_version descending
        matching_history.sort(key=lambda x: x.get("config_version", 0), reverse=True)
        
        return json.dumps({
            "success": True,
            "space_id": space_id,
            "count": len(matching_history),
            "history": matching_history
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_config_history",
                "description": "Retrieve configuration change history for a space in the Confluence system. This tool fetches the complete version history of space configuration changes, including config version numbers, change timestamps, user attribution, and old/new configuration states. Returns entries sorted by version number in descending order. Essential for configuration management, change tracking, audit trails, and troubleshooting configuration issues.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {
                            "type": "string",
                            "description": "Unique identifier of the space (required)"
                        }
                    },
                    "required": ["space_id"]
                }
            }
        }
