import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class FindTrainingEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Uretrieve training entities.
        
        Supported entities:
        - training_programs: Training programs by program_id, program_name, program_type, duration_hours, delivery_method, mandatory, status, created_at, updated_at
        - employee_training: Employee training records by training_record_id, employee_id, program_id, enrollment_date, completion_date, status, score, certificate_issued, expiry_date, created_at, updated_at
        """
        if entity_type not in ["training_programs", "employee_training"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'training_programs' or 'employee_training'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        id_field = "program_id" if entity_type == "training_programs" else "training_record_id"
        
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
                "name": "find_training_entities",
                "description": "Uretrieve training entities. Entity types: 'training_programs' (training programs; filterable by program_id (string), program_name (string), program_type (enum: 'onboarding', 'compliance', 'technical', 'leadership', 'safety', 'diversity', 'ai_ethics'), duration_hours (integer), delivery_method (enum: 'in_person', 'online', 'hybrid', 'self_paced'), mandatory (boolean), status (enum: 'active', 'inactive', 'draft'), created_at (timestamp), updated_at (timestamp)), 'employee_training' (employee training records; filterable by training_record_id (string), employee_id (string), program_id (string), enrollment_date (date), completion_date (date), status (enum: 'enrolled', 'in_progress', 'completed', 'failed', 'cancelled'), score (decimal), certificate_issued (boolean), expiry_date (date), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'training_programs' or 'employee_training'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For training_programs, filters are: program_id (string), program_name (string), program_type (enum: 'onboarding', 'compliance', 'technical', 'leadership', 'safety', 'diversity', 'ai_ethics'), duration_hours (integer), delivery_method (enum: 'in_person', 'online', 'hybrid', 'self_paced'), mandatory (boolean), status (enum: 'active', 'inactive', 'draft'), created_at (timestamp), updated_at (timestamp). For employee_training, filters are: training_record_id (string), employee_id (string), program_id (string), enrollment_date (date), completion_date (date), status (enum: 'enrolled', 'in_progress', 'completed', 'failed', 'cancelled'), score (decimal), certificate_issued (boolean), expiry_date (date), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
