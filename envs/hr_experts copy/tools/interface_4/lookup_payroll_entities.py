import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class LookupPayrollEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Uretrieve payroll entities.
        
        Supported entities:
        - payroll_records: Payroll records by payroll_id, employee_id, pay_period_start, pay_period_end, hours_worked, hourly_rate, payment_date, status, approved_by, created_at, updated_at
        - payroll_deductions: Payroll deductions by deduction_id, payroll_id, deduction_type, amount, created_by, created_at
        """
        if entity_type not in ["payroll_records", "payroll_deductions"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'payroll_records' or 'payroll_deductions'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        id_field = "payroll_id" if entity_type == "payroll_records" else "deduction_id"
        
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
                "name": "lookup_payroll_entities",
                "description": "Uretrieve payroll entities. Entity types: 'payroll_records' (payroll records; filterable by payroll_id (string), employee_id (string), pay_period_start (date), pay_period_end (date), hours_worked (decimal), hourly_rate (decimal), payment_date (date), status (enum: 'draft', 'approved', 'paid', 'cancelled'), approved_by (string), created_at (timestamp), updated_at (timestamp)), 'payroll_deductions' (payroll deductions; filterable by deduction_id (string), payroll_id (string), deduction_type (enum: 'tax', 'insurance', 'retirement', 'garnishment', 'equipment', 'other'), amount (decimal), created_by (string), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'payroll_records' or 'payroll_deductions'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For payroll_records, filters are: payroll_id (string), employee_id (string), pay_period_start (date), pay_period_end (date), hours_worked (decimal), hourly_rate (decimal), payment_date (date), status (enum: 'draft', 'approved', 'paid', 'cancelled'), approved_by (string), created_at (timestamp), updated_at (timestamp). For payroll_deductions, filters are: deduction_id (string), payroll_id (string), deduction_type (enum: 'tax', 'insurance', 'retirement', 'garnishment', 'equipment', 'other'), amount (decimal), created_by (string), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
