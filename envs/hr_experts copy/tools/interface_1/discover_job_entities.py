import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class DiscoverJobEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover job entities.
        
        Supported entities:
        - job_positions: Job position records by position_id, title, department_id, job_level, employment_type, hourly_rate_min, hourly_rate_max, status, created_at, updated_at
        - skills: Skill records by skill_id, skill_name, status
        - job_position_skills: Job position skill relationships by position_id, skill_id
        """
        if entity_type not in ["job_positions", "skills", "job_position_skills"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be one of: 'job_positions', 'skills', 'job_position_skills'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        if entity_type == "job_position_skills":
            # Special handling for many-to-many relationship table
            for relationship in entities.values():
                if filters:
                    match = True
                    for filter_key, filter_value in filters.items():
                        entity_value = relationship.get(filter_key)
                        if entity_value != filter_value:
                            match = False
                            break
                    if match:
                        results.append(relationship)
                else:
                    results.append(relationship)
        else:
            # Handle regular entities with primary keys
            id_field = "position_id" if entity_type == "job_positions" else "skill_id"
            
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
                "name": "discover_job_entities",
                "description": "Discover job entities. Entity types: 'job_positions' (job position records; filterable by position_id (string), title (string), department_id (string), job_level (enum: 'entry', 'junior', 'mid', 'senior', 'lead', 'manager', 'director', 'executive'), employment_type (enum: 'full_time', 'part_time', 'contract', 'intern', 'temporary'), hourly_rate_min (decimal), hourly_rate_max (decimal), status (enum: 'open', 'closed', 'draft'), created_at (timestamp), updated_at (timestamp)), 'skills' (skill records; filterable by skill_id (string), skill_name (string), status (enum: 'active', 'inactive')), 'job_position_skills' (job position skill relationships; filterable by position_id (string), skill_id (string)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'job_positions', 'skills', or 'job_position_skills'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For job_positions: position_id (string), title (string), department_id (string), job_level (enum: 'entry', 'junior', 'mid', 'senior', 'lead', 'manager', 'director', 'executive'), employment_type (enum: 'full_time', 'part_time', 'contract', 'intern', 'temporary'), hourly_rate_min (decimal), hourly_rate_max (decimal), status (enum: 'open', 'closed', 'draft'), created_at (timestamp), updated_at (timestamp). For skills: skill_id (string), skill_name (string), status (enum: 'active', 'inactive'). For job_position_skills: position_id (string), skill_id (string)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
