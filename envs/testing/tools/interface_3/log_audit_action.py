import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class LogAuditAction(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action_type: str, user_id: str, 
               target_type: str, target_id: str, timestamp: str,
               old_values: Optional[Dict[str, Any]] = None, 
               new_values: Optional[Dict[str, Any]] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            max_id = max(int(k) for k in table.keys() if k.isdigit())
            return str(max_id + 1)
        
        users = data.get("users", {})
        audit_logs = data.get("audit_logs", {})
        
        # Validate user exists
        if str(user_id) not in users:
            return json.dumps({"error": f"User {user_id} not found"})
        
        # Validate action_type
        valid_actions = ["create", "update", "delete"]
        if action_type not in valid_actions:
            return json.dumps({"error": f"Invalid action_type. Must be one of {valid_actions}"})
        
        # Validate required fields
        if not target_type:
            return json.dumps({"error": "target_type is required"})
        
        if not target_id:
            return json.dumps({"error": "target_id is required"})
        
        if not timestamp:
            return json.dumps({"error": "timestamp is required"})
        
        log_id = generate_id(audit_logs)
        
        new_audit_log = {
            "log_id": log_id,
            "user_id": user_id,
            "action": action_type,
            "reference_type": target_type,
            "reference_id": target_id,
            "field_name": None,
            "old_value": json.dumps(old_values) if old_values else None,
            "new_value": json.dumps(new_values) if new_values else None,
            "timestamp": timestamp
        }
        
        audit_logs[log_id] = new_audit_log
        return json.dumps({"audit_log_id": log_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "log_audit_action",
                "description": "Log an audit action performed by a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action_type": {"type": "string", "description": "Type of action performed (create, update, delete)"},
                        "user_id": {"type": "string", "description": "ID of the user who performed the action"},
                        "target_type": {"type": "string", "description": "Type of target (space, page, comment, etc.)"},
                        "target_id": {"type": "string", "description": "ID of the target"},
                        "timestamp": {"type": "string", "description": "Timestamp of the action"},
                        "old_values": {"type": "object", "description": "Previous values before change"},
                        "new_values": {"type": "object", "description": "New values after change"}
                    },
                    "required": ["action_type", "user_id", "target_type", "target_id", "timestamp"]
                }
            }
        }
