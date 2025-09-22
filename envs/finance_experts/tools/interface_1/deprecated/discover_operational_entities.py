import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class DiscoverOperationalEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover operational entities: reports, documents, notifications, and audit trails.
        
        Supported entities:
        - reports: Generated reports by fund_id, report_type, status, report_date
        - documents: Uploaded documents by name, format, uploaded_by, confidentiality_level
        - notifications: System notifications by email, type, class, status
        - audit_trails: Audit records by reference_type, action, user_id, created_at
        """
        if entity_type not in ["reports", "documents", "notifications", "audit_trails"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'reports', 'documents', 'notifications', or 'audit_trails'"
            })
        
        # Access the entity data directly from the JSON structure (data is the specific entity file content)
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        # Determine ID field name
        id_field = {
            "reports": "report_id",
            "documents": "document_id",
            "notifications": "notification_id",
            "audit_trails": "audit_trail_id"
        }[entity_type]
        
        # Apply filters if provided
        if entity_type == "reports":
            entities = data.get("reports", {})
        elif entity_type == "documents":
            entities = data.get("documents", {})
        elif entity_type == "notifications":
            entities = data.get("notifications", {})
        elif entity_type == "audit_trails":
            entities = data.get("audit_trails", {})

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
                "name": "discover_operational_entities",
                "description": "Discover operational entities including reports, documents, notifications, and audit trails. Entity types: 'reports' (generated reports; filterable by fund_id, report_type, status, report_date, generated_by), 'documents' (uploaded documents; filterable by name, format, uploaded_by, confidentiality_level, status), 'notifications' (system notifications; filterable by email, type, class, status, reference_id), 'audit_trails' (audit records; filterable by reference_type, action, user_id, reference_id, created_at).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'reports', 'documents', 'notifications', or 'audit_trails'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For reports, filters are: fund_id, report_type, status, report_date, generated_by. For documents, filters are: name, format, uploaded_by, confidentiality_level, status. For notifications, filters are: email, type, class, status, reference_id. For audit_trails, filters are: reference_type, action, user_id, reference_id, created_at"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }