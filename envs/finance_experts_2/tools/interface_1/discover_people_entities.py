import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class DiscoverPeopleEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover users and investors based on specified filters.
        
        Supported entities:
        - users: Find system users by role, status, email, timezone
        - investors: Find investors by name, country, status, accreditation_status, email
        """
        if entity_type not in ["users", "investors"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'users' or 'investors'"
            })
        
        # Access the entity data directly from the JSON structure (data is the specific entity file content)
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        # Apply filters if provided
        if entity_type == "users":
            entities = data.get("users", {})
        elif entity_type == "investors":
            entities = data.get("investors", {})

        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, f"{entity_type[:-1]}_id": entity_id})
            else:
                results.append({**entity_data, f"{entity_type[:-1]}_id": entity_id})
        
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
                "name": "discover_people_entities",
                "description": "Discover users and investors in the fund management system. Supports filtering by various criteria. Entity types: 'users' (system users with roles: system_administrator, fund_manager, compliance_officer, finance_officer, trader; filterable by role, status, email, timezone), 'investors' (investment entities; filterable by name, country, status, accreditation_status, email, registration_number).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'users' or 'investors'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to apply. For users: role, status, email, timezone. For investors: name, country, status, accreditation_status, email, registration_number",
                            "additionalProperties": True
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
