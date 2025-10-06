import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class SearchDocumentEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Uretrieve document entities.
        
        Supported entities:
        - document_storage: Document storage records by document_id, document_name, document_type, employee_id, file_path, upload_date, uploaded_by, confidentiality_level, retention_period_years, expiry_date, status, created_at
        """
        if entity_type not in ["document_storage"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'document_storage'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("document_storage", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "document_id": entity_id})
            else:
                results.append({**entity_data, "document_id": entity_id})
        
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
                "name": "search_document_entities",
                "description": "Uretrieve document entities. Entity types: 'document_storage' (document storage records; filterable by document_id (string), document_name (string), document_type (enum: 'contract', 'policy', 'handbook', 'form', 'certificate', 'report', 'resume', 'offer_letter'), employee_id (string), file_path (string), upload_date (timestamp), uploaded_by (string), confidentiality_level (enum: 'public', 'internal', 'confidential', 'restricted'), retention_period_years (integer), expiry_date (date), status (enum: 'active', 'archived', 'deleted'), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'document_storage'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For document_storage, filters are: document_id (string), document_name (string), document_type (enum: 'contract', 'policy', 'handbook', 'form', 'certificate', 'report', 'resume', 'offer_letter'), employee_id (string), file_path (string), upload_date (timestamp), uploaded_by (string), confidentiality_level (enum: 'public', 'internal', 'confidential', 'restricted'), retention_period_years (integer), expiry_date (date), status (enum: 'active', 'archived', 'deleted'), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
