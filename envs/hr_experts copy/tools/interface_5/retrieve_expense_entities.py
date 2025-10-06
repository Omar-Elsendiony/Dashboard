import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class RetrieveExpenseEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Uretrieve expense entities.
        
        Supported entities:
        - expense_reimbursements: Expense reimbursements by reimbursement_id, employee_id, expense_date, amount, expense_type, receipt_file_path, status, approved_by, payment_date, created_at, updated_at
        """
        if entity_type not in ["expense_reimbursements"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'expense_reimbursements'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("expense_reimbursements", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "reimbursement_id": entity_id})
            else:
                results.append({**entity_data, "reimbursement_id": entity_id})
        
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
                "name": "retrieve_expense_entities",
                "description": "Uretrieve expense entities. Entity types: 'expense_reimbursements' (expense reimbursements; filterable by reimbursement_id (string), employee_id (string), expense_date (date), amount (decimal), expense_type (enum: 'travel', 'meals', 'equipment', 'training', 'other'), receipt_file_path (string), status (enum: 'submitted', 'approved', 'rejected', 'paid'), approved_by (string), payment_date (date), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'expense_reimbursements'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For expense_reimbursements, filters are: reimbursement_id (string), employee_id (string), expense_date (date), amount (decimal), expense_type (enum: 'travel', 'meals', 'equipment', 'training', 'other'), receipt_file_path (string), status (enum: 'submitted', 'approved', 'rejected', 'paid'), approved_by (string), payment_date (date), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
