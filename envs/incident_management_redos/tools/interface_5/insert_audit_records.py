import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class InsertAuditRecords(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reference_id: str,
        reference_type: str,
        action: str,
        user_id: str,
        field_name: Optional[str] = None,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None
    ) -> str:
        """
        Create audit trail records to track changes made to database records.
        
        Parameters:
        - reference_id: ID of the record that was changed
        - reference_type: Type of record being audited
        - action: Action performed (create, update)
        - user_id: ID of the user who performed the action
        - field_name: Name of the field that was changed (required for update)
        - old_value: Previous value of the field (nullable)
        - new_value: New value of the field (required for update)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        timestamp = "2025-10-07T12:00:00"
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        audit_trails = data.get("audit_trails", {})
        users = data.get("users", {})
        
        # Validate reference_type based on DBML schema
        valid_reference_types = [
            "user", "client", "sla", "ci", "incident", "escalation", "bridge", 
            "change", "rollback", "work_order", "problem", "incident_ci", 
            "problem_ci", "client_ci"
        ]
        if reference_type not in valid_reference_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid reference_type '{reference_type}'. Must be one of: {', '.join(valid_reference_types)}"
            })
        
        # Validate action enum based on DBML schema
        valid_actions = ["create", "update"]
        if action not in valid_actions:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be one of: {', '.join(valid_actions)}"
            })
        
        # Business rule validation
        if action == "create" and field_name is not None:
            return json.dumps({
                "success": False,
                "error": "field_name should be null for create actions"
            })
        
        if action == "create" and old_value is not None:
            return json.dumps({
                "success": False,
                "error": "old_value should be null for create actions"
            })
        
        if action == "update":
            if field_name is None or str(field_name).strip() == "":
                return json.dumps({
                    "success": False,
                    "error": "field_name is required for update actions"
                })
            if new_value is None or str(new_value).strip() == "":
                return json.dumps({
                    "success": False,
                    "error": "new_value is required for update actions"
                })
        
        # Validate user_id FK
        user_id_str = str(user_id).strip().strip('"')
        if user_id_str not in users:
            return json.dumps({
                "success": False,
                "error": f"User '{user_id_str}' not found"
            })
        if users[user_id_str]["status"] != "active":
            return json.dumps({
                "success": False,
                "error": f"User '{user_id_str}' is not active"
            })
        
        # Validate that the referenced entity exists based on reference_type
        reference_tables = {
            "user": "users",
            "client": "clients",
            "sla": "sla_agreements",
            "ci": "configuration_items",
            "incident": "incidents",
            "escalation": "escalations",
            "bridge": "bridges",
            "change": "change_requests",
            "rollback": "rollback_requests",
            "work_order": "work_orders",
            "problem": "problem_tickets",
            "incident_ci": "incident_configuration_items",
            "problem_ci": "problem_configuration_items",
            "client_ci": "ci_client_assignments",
            "communication": "communications",
            "attachment": "attachments",
            "root_cause_analysis": "root_cause_analyses"
        }
        
        reference_table = reference_tables.get(reference_type)
        if reference_table and reference_table in data:
            reference_id_str = str(reference_id).strip().strip('"')
            if reference_id_str not in data[reference_table]:
                return json.dumps({
                    "success": False,
                    "error": f"{reference_type.title()} '{reference_id_str}' not found"
                })
        
        audit_trail_id = generate_id(audit_trails)
        
        new_audit_trail = {
            "audit_id": str(audit_trail_id),
            "reference_id": str(reference_id),
            "reference_type": reference_type,
            "action": action,
            "user_id": user_id_str,
            "field_name": field_name if field_name else None,
            "old_value": old_value if old_value else None,
            "new_value": new_value if new_value else None,
            "created_at": timestamp
        }
        
        audit_trails[str(audit_trail_id)] = new_audit_trail
        return json.dumps({
            "success": True,
            "audit_id": str(audit_trail_id),
            "audit_data": new_audit_trail
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "insert_audit_records",
                "description": "Create audit trail records to track changes made to database records. Validates user activity, reference types, and enforces business rules for create vs update actions.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reference_id": {
                            "type": "string",
                            "description": "ID of the record that was changed (required, cannot be empty)"
                        },
                        "reference_type": {
                            "type": "string",
                            "description": "Type of record being audited. Must be one of: user, client, sla, ci, incident, escalation, bridge, change, rollback, work_order, problem, incident_ci, problem_ci, client_ci",
                            "enum": ["user", "client", "sla", "ci", "incident", "escalation", "bridge", "change", "rollback", "work_order", "problem", "incident_ci", "problem_ci", "client_ci", "communication", "attachment", "root_cause_analysis"]
                        },
                        "action": {
                            "type": "string",
                            "description": "Action performed. Must be one of: create, update. Note: field_name must be null for create actions, old_value must be null for create actions",
                            "enum": ["create", "update"]
                        },
                        "user_id": {
                            "type": "string",
                            "description": "ID of the user who performed the action (required, must be an active user)"
                        },
                        "field_name": {
                            "type": "string",
                            "description": "Name of the field that was changed (required for update actions, must be null for create actions)"
                        },
                        "old_value": {
                            "type": "string",
                            "description": "Previous value of the field (nullable, must be null for create actions)"
                        },
                        "new_value": {
                            "type": "string",
                            "description": "New value of the field (required for update actions, nullable for create actions)"
                        }
                    },
                    "required": ["reference_id", "reference_type", "action", "user_id"]
                }
            }
        }