import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool


class FetchSystemEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Optional[Dict[str, Any]] = None) -> str:
        """
        Discover system entities including employee exits, notifications, and audit trails with optional filtering.

        Args:
            data: Dictionary containing system entities data
            entity_type: Type of system entity to discover ("employee_exits", "notifications", "audit_trails")
            filters: Optional dictionary of filters to apply

        Returns:
            JSON string with discovered entities and metadata
        """
        if entity_type not in ["employee_exits", "notifications", "audit_trails"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be one of: employee_exits, notifications, audit_trails"
            })

        def matches_filter(entity: Dict[str, Any], filter_key: str, filter_value: Any) -> bool:
            """Check if entity matches a specific filter"""
            if filter_key.endswith("_from"):
                # Date range filter - from date
                field_name = filter_key.replace("_from", "")
                entity_value = entity.get(field_name)
                if not entity_value:
                    return False
                return entity_value >= filter_value
            elif filter_key.endswith("_to"):
                # Date range filter - to date
                field_name = filter_key.replace("_to", "")
                entity_value = entity.get(field_name)
                if not entity_value:
                    return False
                return entity_value <= filter_value
            else:
                # Exact match filter
                entity_value = entity.get(filter_key)
                if isinstance(filter_value, str) and isinstance(entity_value, str):
                    return entity_value.lower() == filter_value.lower()
                return entity_value == filter_value

        def apply_filters(entities: Dict[str, Any], valid_filters: List[str], filters: Dict[str, Any]) -> Dict[str, Any]:
            """Apply filters to entities and return matching results"""
            if not filters:
                return entities
            
            # Validate filter keys
            invalid_filters = [key for key in filters.keys() if key not in valid_filters]
            if invalid_filters:
                return {
                    "error": f"Invalid filter keys: {', '.join(invalid_filters)}. Valid filters are: {', '.join(valid_filters)}"
                }
            
            filtered_entities = {}
            for entity_id, entity in entities.items():
                matches = True
                for filter_key, filter_value in filters.items():
                    if not matches_filter(entity, filter_key, filter_value):
                        matches = False
                        break
                
                if matches:
                    filtered_entities[entity_id] = entity
            
            return filtered_entities

        if entity_type == "employee_exits":
            entities = data.get("employee_exits", {})
            valid_filters = [
                "exit_id", "employee_id", "exit_date_from", "exit_date_to", 
                "manager_clearance", "it_equipment_return", "finance_settlement_status", 
                "clearance_status", "approved_by", "approval_date_from", "approval_date_to", 
                "paid_date_from", "paid_date_to"
            ]
            
            if filters:
                filtered_entities = apply_filters(entities, valid_filters, filters)
                if "error" in filtered_entities:
                    return json.dumps({
                        "success": False,
                        "error": filtered_entities["error"]
                    })
                entities = filtered_entities
            
            return json.dumps({
                "success": True,
                "entity_type": "employee_exits",
                "count": len(entities),
                "employee_exits": entities,
                "filters_applied": filters or {}
            })
        
        elif entity_type == "notifications":
            entities = data.get("notifications", {})
            valid_filters = [
                "notification_id", "recipient_user_id", "recipient_email", 
                "notification_type", "reference_type", "reference_id", "notification_status"
            ]
            
            if filters:
                filtered_entities = apply_filters(entities, valid_filters, filters)
                if "error" in filtered_entities:
                    return json.dumps({
                        "success": False,
                        "error": filtered_entities["error"]
                    })
                entities = filtered_entities
            
            return json.dumps({
                "success": True,
                "entity_type": "notifications",
                "count": len(entities),
                "notifications": entities,
                "filters_applied": filters or {}
            })
        
        elif entity_type == "audit_trails":
            entities = data.get("audit_trails", {})
            valid_filters = [
                "audit_id", "reference_id", "reference_type", "action", "user_id", "field_name"
            ]
            
            if filters:
                filtered_entities = apply_filters(entities, valid_filters, filters)
                if "error" in filtered_entities:
                    return json.dumps({
                        "success": False,
                        "error": filtered_entities["error"]
                    })
                entities = filtered_entities
            
            return json.dumps({
                "success": True,
                "entity_type": "audit_trails",
                "count": len(entities),
                "audit_trails": entities,
                "filters_applied": filters or {}
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_system_entities",
                "description": "Discover system entities including employee exits, notifications, and audit trails with optional filtering. Entity types: 'employee_exits' (manager_clearance: pending, approved, rejected; it_equipment_return: pending, completed, not_applicable; finance_settlement_status: pending, completed, not_applicable; clearance_status: pending, in_progress, completed, rejected), 'notifications' (notification_type: email, sms, push, system; notification_status: pending, sent, delivered, failed, read), 'audit_trails' (action: create, update, delete, approve, reject, release, payment).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of system entity to discover",
                            "enum": ["employee_exits", "notifications", "audit_trails"]
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to apply. For employee_exits: exit_id, employee_id, exit_date_from, exit_date_to, manager_clearance, it_equipment_return, finance_settlement_status, clearance_status, approved_by, approval_date_from, approval_date_to, paid_date_from, paid_date_to. For notifications: notification_id, recipient_user_id, recipient_email, notification_type, reference_type, reference_id, notification_status. For audit_trails: audit_id, reference_id, reference_type, action, user_id, field_name. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                # Employee Exits filters
                                "exit_id": {"type": "string", "description": "Exact exit ID match"},
                                "employee_id": {"type": "string", "description": "Employee ID match"},
                                "exit_date_from": {"type": "string", "description": "Exit date from (YYYY-MM-DD)"},
                                "exit_date_to": {"type": "string", "description": "Exit date to (YYYY-MM-DD)"},
                                "manager_clearance": {"type": "string", "description": "Manager clearance status", "enum": ["pending", "approved", "rejected"]},
                                "it_equipment_return": {"type": "string", "description": "IT equipment return status", "enum": ["pending", "completed", "not_applicable"]},
                                "finance_settlement_status": {"type": "string", "description": "Finance settlement status", "enum": ["pending", "completed", "not_applicable"]},
                                "clearance_status": {"type": "string", "description": "Overall clearance status", "enum": ["pending", "in_progress", "completed", "rejected"]},
                                "approved_by": {"type": "string", "description": "User who approved the exit"},
                                "approval_date_from": {"type": "string", "description": "Approval date from (YYYY-MM-DD)"},
                                "approval_date_to": {"type": "string", "description": "Approval date to (YYYY-MM-DD)"},
                                "paid_date_from": {"type": "string", "description": "Paid date from (YYYY-MM-DD)"},
                                "paid_date_to": {"type": "string", "description": "Paid date to (YYYY-MM-DD)"},
                                
                                # Notifications filters
                                "notification_id": {"type": "string", "description": "Exact notification ID match"},
                                "recipient_user_id": {"type": "string", "description": "Recipient user ID match"},
                                "recipient_email": {"type": "string", "description": "Recipient email match"},
                                "notification_type": {"type": "string", "description": "Notification type", "enum": ["email", "sms", "push", "system"]},
                                "reference_type": {"type": "string", "description": "Reference entity type"},
                                "reference_id": {"type": "string", "description": "Reference entity ID"},
                                "notification_status": {"type": "string", "description": "Notification status", "enum": ["pending", "sent", "delivered", "failed", "read"]},
                                
                                # Audit Trails filters
                                "audit_id": {"type": "string", "description": "Exact audit ID match"},
                                "reference_id": {"type": "string", "description": "Reference entity ID"},
                                "reference_type": {"type": "string", "description": "Reference entity type"},
                                "action": {"type": "string", "description": "Action performed", "enum": ["create", "update", "delete", "approve", "reject", "release", "payment"]},
                                "user_id": {"type": "string", "description": "User who performed the action"},
                                "field_name": {"type": "string", "description": "Field that was modified"}
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }