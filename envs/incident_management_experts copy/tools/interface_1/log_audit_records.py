import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class LogAuditRecords(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], audit_data: Dict[str, Any]) -> str:
        """
        Create audit log records for tracking changes to system entities.
        
        This tool only supports creation of audit records - no updates are allowed
        as audit logs are immutable for compliance purposes.
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        # Access audit_log data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for audit_log"
            })
        
        audit_log = data.get("audit_log", {})
        
        if not audit_data:
            return json.dumps({
                "success": False,
                "error": "audit_data is required for audit log creation"
            })
        
        # Validate required fields for creation
        required_fields = ["entity_type", "entity_id", "operation_type", "changed_by_id"]
        missing_fields = [field for field in required_fields if field not in audit_data]
        if missing_fields:
            return json.dumps({
                "success": False,
                "error": f"Missing required fields for audit log creation: {', '.join(missing_fields)}"
            })
        
        # Validate only allowed fields are present
        allowed_fields = ["entity_type", "entity_id", "operation_type", "changed_by_id", "field_name", "old_value", "new_value"]
        invalid_fields = [field for field in audit_data.keys() if field not in allowed_fields]
        if invalid_fields:
            return json.dumps({
                "success": False,
                "error": f"Invalid fields for audit log creation: {', '.join(invalid_fields)}"
            })
        
        # Validate enum fields
        valid_operation_types = ["INSERT", "UPDATE", "DELETE"]
        if audit_data["operation_type"] not in valid_operation_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation_type '{audit_data['operation_type']}'. Must be one of: {', '.join(valid_operation_types)}"
            })
        
        # Validate entity_type (should be a valid table name)
        valid_entity_types = ["clients", "vendors", "users", "products", "infrastructure_components", 
                             "client_subscriptions", "sla_agreements", "incidents", "workarounds", 
                             "root_cause_analysis", "communications", "escalations", "change_requests", 
                             "rollback_requests", "metrics", "incident_reports", "knowledge_base_articles", 
                             "post_incident_reviews"]
        if audit_data["entity_type"] not in valid_entity_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{audit_data['entity_type']}'. Must be one of: {', '.join(valid_entity_types)}"
            })
        
        # For UPDATE operations, field_name should be provided
        if audit_data["operation_type"] == "UPDATE" and not audit_data.get("field_name"):
            return json.dumps({
                "success": False,
                "error": "field_name is required for UPDATE operations"
            })
        
        # Generate new audit ID
        new_audit_id = generate_id(audit_log)
        
        # Create new audit log record
        new_audit_record = {
            "audit_id": str(new_audit_id),
            "entity_type": audit_data["entity_type"],
            "entity_id": str(audit_data["entity_id"]),
            "operation_type": audit_data["operation_type"],
            "changed_by_id": str(audit_data["changed_by_id"]),
            "field_name": audit_data.get("field_name"),
            "old_value": str(audit_data.get("old_value")) if audit_data.get("old_value") is not None else None,
            "new_value": str(audit_data.get("new_value")) if audit_data.get("new_value") is not None else None,
            "created_at": "2025-10-01T00:00:00"
        }
        
        audit_log[str(new_audit_id)] = new_audit_record
        
        return json.dumps({
            "success": True,
            "action": "create",
            "audit_id": str(new_audit_id),
            "audit_data": new_audit_record
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "log_audit_records",
                "description": "Create audit log records in the incident management system for tracking all changes to system entities. This tool maintains an immutable audit trail for compliance and security purposes by logging all INSERT, UPDATE, and DELETE operations across all system tables. Records include the entity type, entity ID, operation type, user who made the change, and specific field changes for UPDATE operations. Essential for regulatory compliance, security monitoring, change tracking, and forensic analysis. Audit records cannot be modified or deleted once created to maintain data integrity.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "audit_data": {
                            "type": "object",
                            "description": "Audit log data object. Requires entity_type (table name), entity_id (record ID), operation_type, changed_by_id (user ID), with optional field_name (required for UPDATE), old_value, new_value. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "entity_type": {
                                    "type": "string",
                                    "description": "Name of the database table that was modified: 'clients', 'vendors', 'users', 'products', 'infrastructure_components', 'client_subscriptions', 'sla_agreements', 'incidents', 'workarounds', 'root_cause_analysis', 'communications', 'escalations', 'change_requests', 'rollback_requests', 'metrics', 'incident_reports', 'knowledge_base_articles', 'post_incident_reviews'",
                                    "enum": ["clients", "vendors", "users", "products", "infrastructure_components", "client_subscriptions", "sla_agreements", "incidents", "workarounds", "root_cause_analysis", "communications", "escalations", "change_requests", "rollback_requests", "metrics", "incident_reports", "knowledge_base_articles", "post_incident_reviews"]
                                },
                                "entity_id": {
                                    "type": "string",
                                    "description": "Unique identifier of the record that was changed"
                                },
                                "operation_type": {
                                    "type": "string",
                                    "description": "Type of database operation performed: 'INSERT', 'UPDATE', 'DELETE'",
                                    "enum": ["INSERT", "UPDATE", "DELETE"]
                                },
                                "changed_by_id": {
                                    "type": "string",
                                    "description": "User ID of the person who made the change"
                                },
                                "field_name": {
                                    "type": "string",
                                    "description": "Name of the specific field that was changed (required for UPDATE operations, optional for others)"
                                },
                                "old_value": {
                                    "type": "string",
                                    "description": "Previous value of the field before the change (optional, for UPDATE operations)"
                                },
                                "new_value": {
                                    "type": "string",
                                    "description": "New value of the field after the change (optional, for INSERT and UPDATE operations)"
                                }
                            },
                            "required": ["entity_type", "entity_id", "operation_type", "changed_by_id"]
                        }
                    },
                    "required": ["audit_data"]
                }
            }
        }
