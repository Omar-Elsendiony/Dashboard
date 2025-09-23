import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class GetBillingEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover billing entities: invoices and payments.
        
        Supported entities:
        - invoices: Invoice records by invoice_id, commitment_id, invoice_date, due_date, amount, status
        - payments: Payment records by payment_id, invoice_id, subscription_id, payment_date, amount, payment_method, status
        """
        if entity_type not in ["invoices", "payments"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'invoices' or 'payments'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        id_field = {
            "invoices": "invoice_id",
            "payments": "payment_id"
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
                "name": "get_billing_entities",
                "description": "Discover billing entities including invoices and payments. Entity types: 'invoices' (invoice records; filterable by invoice_id (string), commitment_id (string), invoice_date (date), due_date (date), amount (decimal), status (enum: 'issued', 'paid'), updated_at (timestamp)), 'payments' (payment records; filterable by payment_id (string), invoice_id (string), subscription_id (string), payment_date (timestamp), amount (decimal), payment_method (enum: 'wire', 'cheque', 'credit_card', 'bank_transfer'), status (enum: 'draft', 'completed', 'failed'), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'invoices' or 'payments'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For invoices, filters are: invoice_id (string), commitment_id (string), invoice_date (date), due_date (date), amount (decimal), status (enum: 'issued', 'paid'), updated_at (timestamp). For payments, filters are: payment_id (string), invoice_id (string), subscription_id (string), payment_date (timestamp), amount (decimal), payment_method (enum: 'wire', 'cheque', 'credit_card', 'bank_transfer'), status (enum: 'draft', 'completed', 'failed'), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
