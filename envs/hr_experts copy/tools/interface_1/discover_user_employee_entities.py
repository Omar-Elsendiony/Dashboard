import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverUserEmployeeEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover user and employee entities. The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - employees: Employee records by employee_id, user_id, position_id, hire_date, employment_status, manager_id, date_of_birth, address, hourly_rate, created_at, updated_at
        - users: User records by user_id, first_name, last_name, email, phone_number, role, status, mfa_enabled, created_at, updated_at
        """
        if entity_type not in ["employees", "users"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'employees' or 'users'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
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
                    # Add appropriate ID field based on entity type
                    id_field = "employee_id" if entity_type == "employees" else "user_id"
                    results.append({**entity_data, id_field: entity_id})
            else:
                id_field = "employee_id" if entity_type == "employees" else "user_id"
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
                "name": "discover_user_employee_entities",
                "description": "Discover user and employee entities. The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results. Entity types: 'employees' (employee records; filterable by employee_id (string), user_id (string), position_id (string), hire_date (date), employment_status (enum: 'active', 'terminated', 'on_leave', 'suspended'), manager_id (string), date_of_birth (date), address (string), hourly_rate (integer), created_at (timestamp), updated_at (timestamp)), 'users' (user records; filterable by user_id (string), first_name (string), last_name (string), email (string), phone_number (string), role (enum: 'hr_director', 'hr_manager', 'recruiter', 'payroll_administrator', 'hiring_manager', 'finance_officer', 'it_administrator', 'compliance_officer', 'employee'), status (enum: 'active', 'inactive', 'suspended'), mfa_enabled (boolean), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'employees' or 'users'",
                            "enum": ["employees", "users"]
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For employees: employee_id, user_id, position_id, hire_date, employment_status, manager_id, date_of_birth, address, hourly_rate, created_at, updated_at. For users: user_id, first_name, last_name, email, phone_number, role, status, mfa_enabled, created_at, updated_at"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }