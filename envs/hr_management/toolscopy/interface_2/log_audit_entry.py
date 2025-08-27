import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class LogAuditEntry(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, action: str, reference_type: str,
               reference_id: str, field_name: Optional[str] = None,
               old_value: Optional[str] = None, new_value: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        users = data.get("users", {})
        audit_logs = data.get("audit_logs", {})
        
        # Validate user exists
        if user_id not in users:
            return json.dumps({"success": False, "error": f"User {user_id} not found", "halt": True})
        
        # Validate action
        valid_actions = ['create', 'read', 'update', 'delete', 'approve', 'reject']
        if action not in valid_actions:
            return json.dumps({"success": False, "error": f"Invalid action. Must be one of {valid_actions}", "halt": True})
        
        log_id = generate_id(audit_logs)
        timestamp = "2025-10-01T00:00:00"
        
        new_audit_log = {
            "log_id": log_id,
            "user_id": user_id,
            "action": action,
            "reference_type": reference_type,
            "reference_id": reference_id,
            "field_name": field_name,
            "old_value": old_value,
            "new_value": new_value,
            "timestamp": timestamp
        }
        
        audit_logs[log_id] = new_audit_log
        return json.dumps({"log_id": log_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "log_audit_entry",
                "description": "Create a new audit log entry",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User ID performing the action"},
                        "action": {"type": "string", "description": "Action performed (create, read, update, delete, approve, reject)"},
                        "reference_type": {"type": "string", "description": "Type of record being acted upon"},
                        "reference_id": {"type": "string", "description": "ID of the record being acted upon"},
                        "field_name": {"type": "string", "description": "Specific field name if applicable"},
                        "old_value": {"type": "string", "description": "Previous value"},
                        "new_value": {"type": "string", "description": "New value"}
                    },
                    "required": ["user_id", "action", "reference_type", "reference_id"]
                }
            }
        }
