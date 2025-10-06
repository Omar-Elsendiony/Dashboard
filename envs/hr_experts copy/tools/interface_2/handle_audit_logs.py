import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class HandleAuditLogs(Tool):
    """
    Execute the creation of immutable audit logs.
    """
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        operation: str,
        user_id: str,
        action: str,
        reference_type: str,
        reference_id: str,
        field_name: Optional[str] = None,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None,
    ) -> str:
        """
        Executes the create operation for audit logs.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        audit_logs = data.get("audit_logs", {})
        users = data.get("users", {})

        if operation != "create":
            return json.dumps({"error": "Invalid operation. Only 'create' is permitted for audit logs."})
        
        if not all([user_id, action, reference_type, reference_id]):
            return json.dumps({"error": "Missing required parameters for create operation."})
        
        if user_id not in users:
            return json.dumps({"error": f"User with ID {user_id} not found."})

        valid_actions = ["create", "update", "delete", "approve", "reject"]
        if action not in valid_actions:
            return json.dumps({"error": f"Invalid action. Must be one of {valid_actions}."})

        new_log_id = generate_id(audit_logs)
        new_log = {
            "log_id": new_log_id,
            "user_id": user_id,
            "action": action,
            "reference_type": reference_type,
            "reference_id": reference_id,
            "field_name": field_name,
            "old_value": old_value,
            "new_value": new_value,
            "timestamp": timestamp,
        }
        audit_logs[new_log_id] = new_log
        return json.dumps(new_log)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns the schema for the ManageAuditLogs tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "handle_audit_logs",
                "description": "Used to create immutable audit trail records for significant actions performed within the system.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {"type": "string", "description": "Must be 'create'."},
                        "user_id": {"type": "string", "description": "The ID of the user who performed the action."},
                        "action": {"type": "string", "description": "Type of action audited: 'create', 'update', 'delete', 'approve', 'reject'."},
                        "reference_type": {"type": "string", "description": "Type or table: (e.g., 'employees', 'payroll_records')."},
                        "reference_id": {"type": "string", "description": "The primary key or unique identifier of the affected record."},
                        "field_name": {"type": "string", "description": "The specific field that was changed. Used for 'update' actions."},
                        "old_value": {"type": "string", "description": "The value of the field before the change."},
                        "new_value": {"type": "string", "description": "The value of the field after the change."},
                    },
                    "required": ["operation", "user_id", "action", "reference_type", "reference_id"],
                },
            },
        }
