import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class LookupReportingEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover reporting entities: reports and documents.
        
        Supported entities:
        - reports: Report records by report_id, fund_id, investor_id, report_date, report_type, generated_by, status, export_period_end
        - documents: Document records by document_id, name, format, uploaded_by, upload_date, report_id, size_bytes, confidentiality_level, status
        """
        if entity_type not in ["reports", "documents"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'reports' or 'documents'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        id_field = {
            "reports": "report_id",
            "documents": "document_id"
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
                "name": "lookup_reporting_entities",
                "description": "Discover reporting entities including reports and documents. Entity types: 'reports' (report records; filterable by report_id (string), fund_id (string), investor_id (string), report_date (date), report_type (enum: 'performance', 'holding', 'financial'), generated_by (string), status (enum: 'pending', 'completed', 'failed'), created_at (timestamp), export_period_end (date)), 'documents' (document records; filterable by document_id (string), name (string), format (enum: 'pdf', 'xlsx', 'docx', 'csv', 'other'), uploaded_by (string), upload_date (timestamp), report_id (string), size_bytes (bigint), confidentiality_level (enum: 'public', 'internal', 'confidential', 'restricted'), status (enum: 'available', 'archived', 'deleted')).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'reports' or 'documents'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For reports, filters are: report_id (string), fund_id (string), investor_id (string), report_date (date), report_type (enum: 'performance', 'holding', 'financial'), generated_by (string), status (enum: 'pending', 'completed', 'failed'), created_at (timestamp), export_period_end (date). For documents, filters are: document_id (string), name (string), format (enum: 'pdf', 'xlsx', 'docx', 'csv', 'other'), uploaded_by (string), upload_date (timestamp), report_id (string), size_bytes (bigint), confidentiality_level (enum: 'public', 'internal', 'confidential', 'restricted'), status (enum: 'available', 'archived', 'deleted')"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
