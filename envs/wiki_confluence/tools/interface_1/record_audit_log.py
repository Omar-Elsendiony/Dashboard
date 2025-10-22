import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RecordAuditLog(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], actor_user_id: str, action_type: str,
               target_entity_type: str, target_entity_id: str,
               details: Optional[str] = None) -> str:
        """
        Record audit trail events in the system.
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
        
        audit_logs = data.get("audit_logs", {})
        users = data.get("users", {})
        
        # Validate user exists
        if actor_user_id not in users:
            return json.dumps({
                "success": False,
                "error": f"User {actor_user_id} not found"
            })
        
        # Validate action_type enum
        valid_actions = [
            "create_space", "update_space", "delete_space", "manage_permissions",
            "grant_admin_rights", "configure_settings", "export_space", "import_space",
            "create_page", "update_page", "delete_page", "move_page", "rename_page",
            "restore_version", "clone_page", "publish_page", "unpublish_page",
            "archive_content", "watch_content", "unwatch_content"
        ]
        if action_type not in valid_actions:
            return json.dumps({
                "success": False,
                "error": f"Invalid action_type. Must be one of: {', '.join(valid_actions)}"
            })
        
        # Generate new log ID
        new_log_id = generate_id(audit_logs)
        timestamp = "2025-10-01T12:00:00"
        
        new_log = {
            "log_id": str(new_log_id),
            "actor_user_id": actor_user_id,
            "action_type": action_type,
            "target_entity_type": target_entity_type,
            "target_entity_id": target_entity_id,
            "occurred_at": timestamp,
            "details": details
        }
        
        audit_logs[str(new_log_id)] = new_log
        
        return json.dumps({
            "success": True,
            "log_id": str(new_log_id),
            "message": f"Audit log created for action '{action_type}' by user {actor_user_id}",
            "log_data": new_log
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "record_audit_log",
                "description": "Record audit trail events in the Confluence system. This tool creates comprehensive audit log entries tracking user actions across the system including space operations, page management, permission changes, and content lifecycle events. Captures actor attribution, action types, target entities, timestamps, and optional contextual details. Essential for security auditing, compliance reporting, change tracking, troubleshooting, and maintaining complete system activity history.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "actor_user_id": {
                            "type": "string",
                            "description": "User ID of the actor performing the action (required)"
                        },
                        "action_type": {
                            "type": "string",
                            "description": "Type of action performed (required)",
                            "enum": ["create_space", "update_space", "delete_space", "manage_permissions", "grant_admin_rights", "configure_settings", "export_space", "import_space", "create_page", "update_page", "delete_page", "move_page", "rename_page", "restore_version", "clone_page", "publish_page", "unpublish_page", "archive_content", "watch_content", "unwatch_content"]
                        },
                        "target_entity_type": {
                            "type": "string",
                            "description": "Type of entity affected by the action (required, e.g., 'space', 'page', 'user', 'group')"
                        },
                        "target_entity_id": {
                            "type": "string",
                            "description": "ID of the entity affected by the action (required)"
                        },
                        "details": {
                            "type": "string",
                            "description": "Additional context or description of the action (optional) in JSON format"
                        }
                    },
                    "required": ["actor_user_id", "action_type", "target_entity_type", "target_entity_id"]
                }
            }
        }
