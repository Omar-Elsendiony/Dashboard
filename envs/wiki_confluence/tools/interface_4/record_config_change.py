import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RecordConfigChange(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str, changed_by_user_id: str,
               old_config: str, new_config: str) -> str:
        """
        Record configuration changes for traceability.
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        space_config_history = data.get("space_config_history", {})
        spaces = data.get("spaces", {})
        users = data.get("users", {})
        
        # Validate space exists
        if space_id not in spaces:
            return json.dumps({
                "success": False,
                "error": f"Space {space_id} not found"
            })
        
        # Validate user exists
        if changed_by_user_id not in users:
            return json.dumps({
                "success": False,
                "error": f"User {changed_by_user_id} not found"
            })
        
        # Get next config version
        max_version = 0
        for history in space_config_history.values():
            if history.get("space_id") == space_id:
                version = history.get("config_version", 0)
                if version > max_version:
                    max_version = version
        
        next_version = max_version + 1
        
        # Generate new history ID
        new_history_id = generate_id(space_config_history)
        timestamp = "2025-10-01T12:00:00"
        
        new_history = {
            "history_id": str(new_history_id),
            "space_id": space_id,
            "changed_by_user_id": changed_by_user_id,
            "changed_at": timestamp,
            "config_version": next_version,
            "old_config": old_config,
            "new_config": new_config
        }
        
        space_config_history[str(new_history_id)] = new_history
        
        return json.dumps({
            "success": True,
            "history_id": str(new_history_id),
            "config_version": next_version,
            "message": f"Configuration change recorded for space {space_id}, version {next_version}",
            "history_data": new_history
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "record_config_change",
                "description": "Record configuration changes for traceability in the Confluence system. This tool creates version-tracked records of space configuration modifications, capturing both old and new configuration states with user attribution and timestamps. Automatically increments version numbers to maintain chronological configuration history. Essential for configuration management, change tracking, rollback capabilities, audit compliance, and troubleshooting configuration issues.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {
                            "type": "string",
                            "description": "Unique identifier of the space (required)"
                        },
                        "changed_by_user_id": {
                            "type": "string",
                            "description": "User ID of the person making the configuration change (required)"
                        },
                        "old_config": {
                            "type": "string",
                            "description": "Previous configuration state as JSON string (required)"
                        },
                        "new_config": {
                            "type": "string",
                            "description": "New configuration state as JSON string (required)"
                        }
                    },
                    "required": ["space_id", "changed_by_user_id", "old_config", "new_config"]
                }
            }
        }
