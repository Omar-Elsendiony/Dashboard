import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class SearchBenefitsEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Uretrieve benefits entities.
        
        Supported entities:
        - benefits_plans: Benefits plans by plan_id, plan_name, plan_type, provider, employee_cost, employer_cost, status, effective_date, expiration_date, created_at, updated_at
        - employee_benefits: Employee benefits by enrollment_id, employee_id, plan_id, enrollment_date, status, coverage_level, beneficiary_name, beneficiary_relationship, created_at, updated_at
        """
        if entity_type not in ["benefits_plans", "employee_benefits"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'benefits_plans' or 'employee_benefits'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        id_field = "plan_id" if entity_type == "benefits_plans" else "enrollment_id"
        
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
                "name": "search_benefits_entities",
                "description": "Uretrieve benefits entities. Entity types: 'benefits_plans' (benefits plans; filterable by plan_id (string), plan_name (string), plan_type (enum: 'health_insurance', 'dental', 'vision', 'life_insurance', 'disability', 'retirement_401k', 'pto', 'flexible_spending'), provider (string), employee_cost (decimal), employer_cost (decimal), status (enum: 'active', 'inactive'), effective_date (date), expiration_date (date), created_at (timestamp), updated_at (timestamp)), 'employee_benefits' (employee benefits; filterable by enrollment_id (string), employee_id (string), plan_id (string), enrollment_date (date), status (enum: 'active', 'terminated', 'pending'), coverage_level (enum: 'employee_only', 'employee_spouse', 'employee_children', 'family'), beneficiary_name (string), beneficiary_relationship (string), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'benefits_plans' or 'employee_benefits'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For benefits_plans, filters are: plan_id (string), plan_name (string), plan_type (enum: 'health_insurance', 'dental', 'vision', 'life_insurance', 'disability', 'retirement_401k', 'pto', 'flexible_spending'), provider (string), employee_cost (decimal), employer_cost (decimal), status (enum: 'active', 'inactive'), effective_date (date), expiration_date (date), created_at (timestamp), updated_at (timestamp). For employee_benefits, filters are: enrollment_id (string), employee_id (string), plan_id (string), enrollment_date (date), status (enum: 'active', 'terminated', 'pending'), coverage_level (enum: 'employee_only', 'employee_spouse', 'employee_children', 'family'), beneficiary_name (string), beneficiary_relationship (string), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
