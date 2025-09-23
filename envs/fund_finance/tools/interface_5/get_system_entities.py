import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class GetSystemEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover system entities: notifications and audit trails.
        
        Supported entities:
        - notifications: Notification records by notification_id, email, type, class, reference_id, status, sent_at
        - audit_trails: Audit trail records by audit_trail_id, reference_id, reference_type, action, user_id, field_name, old_value, new_value
        """
        if entity_type not in ["notifications", "audit_trails"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'notifications' or 'audit_trails'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        id_field = {
            "notifications": "notification_id",
            "audit_trails": "audit_trail_id"
        }[entity_type]
        
        entities = data.get(entity_type, {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_system_entities",
                "description": "Discover system entities including notifications and audit trails. Entity types: 'notifications' (notification records; filterable by notification_id (string), email (string), type (enum: 'alert', 'report', 'reminder', 'subscription_update'), class (enum: 'funds', 'investors', 'portfolios', 'trades', 'invoices', 'reports', 'documents', 'subscriptions', 'commitments'), reference_id (string), status (enum: 'pending', 'sent', 'failed'), sent_at (timestamp), created_at (timestamp)), 'audit_trails' (audit trail records; filterable by audit_trail_id (string), reference_id (string), reference_type (enum: 'user', 'fund', 'investor', 'subscription', 'commitment', 'redemption', 'trade', 'portfolio', 'holding', 'instrument', 'invoice', 'payment', 'document', 'report', 'nav', 'notification'), action (enum: 'create', 'update', 'delete', 'approve', 'cancel', 'process'), user_id (string), field_name (string), old_value (text), new_value (text), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'notifications' or 'audit_trails'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For notifications, filters are: notification_id (string), email (string), type (enum: 'alert', 'report', 'reminder', 'subscription_update'), class (enum: 'funds', 'investors', 'portfolios', 'trades', 'invoices', 'reports', 'documents', 'subscriptions', 'commitments'), reference_id (string), status (enum: 'pending', 'sent', 'failed'), sent_at (timestamp), created_at (timestamp). For audit_trails, filters are: audit_trail_id (string), reference_id (string), reference_type (enum: 'user', 'fund', 'investor', 'subscription', 'commitment', 'redemption', 'trade', 'portfolio', 'holding', 'instrument', 'invoice', 'payment', 'document', 'report', 'nav', 'notification'), action (enum: 'create', 'update', 'delete', 'approve', 'cancel', 'process'), user_id (string), field_name (string), old_value (text), new_value (text), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
