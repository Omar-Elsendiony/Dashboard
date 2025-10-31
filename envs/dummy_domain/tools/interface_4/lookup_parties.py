import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class LookupParties(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover party entities (clients, users). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - clients: Client records
        - users: User records
        """
        if entity_type not in ["clients", "users"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'clients' or 'users'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        for entity_id, entity_data in entities.items():
            # Create a copy of the entity data to avoid modifying the original
            result_data = entity_data.copy()
            
            # Remove the 'role' field from users if it exists
            if entity_type == "users" and "role" in result_data:
                del result_data["role"]
            
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    # Check against original entity_data for filtering (including role)
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    if entity_type == "clients":
                        id_field = "client_id"
                    else:  # users
                        id_field = "user_id"
                    results.append({**result_data, id_field: entity_id})
            else:
                if entity_type == "clients":
                    id_field = "client_id"
                else:  # users
                    id_field = "user_id"
                results.append({**result_data, id_field: entity_id})
        
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
                "name": "lookup_parties",
                "description": "Discover party entities (clients, users). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results. Note: The 'role' field is excluded from user results but can still be used for filtering.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'clients' or 'users'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "client_id": {
                                    "type": "string",
                                    "description": "Client ID (for clients)"
                                },
                                "client_name": {
                                    "type": "string",
                                    "description": "Client name (for clients)"
                                },
                                "registration_number": {
                                    "type": "string",
                                    "description": "Registration number (for clients)"
                                },
                                "company_type": {
                                    "type": "string",
                                    "description": "Company type: 'enterprise', 'mid_market', 'smb', 'startup' (for clients)"
                                },
                                "primary_address": {
                                    "type": "string",
                                    "description": "Primary address (for clients)"
                                },
                                "support_coverage": {
                                    "type": "string",
                                    "description": "Support coverage: '24x7', 'business_hours', 'on_call' (for clients)"
                                },
                                "preferred_communication": {
                                    "type": "string",
                                    "description": "Preferred communication: 'email', 'portal', 'phone', 'slack' (for clients)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status: 'active', 'inactive'"
                                },
                                "user_id": {
                                    "type": "string",
                                    "description": "User ID (for users)"
                                },
                                "first_name": {
                                    "type": "string",
                                    "description": "First name (for users)"
                                },
                                "last_name": {
                                    "type": "string",
                                    "description": "Last name (for users)"
                                },
                                "email": {
                                    "type": "string",
                                    "description": "Email address (for users)"
                                },
                                "role": {
                                    "type": "string",
                                    "description": "User role: 'incident_manager', 'technical_support', 'account_manager', 'executive', 'system_administrator', 'client_contact' (for users - can be used for filtering but won't appear in results)"
                                },
                                "timezone": {
                                    "type": "string",
                                    "description": "Timezone (for users)"
                                },
                                "created_at": {
                                    "type": "string",
                                    "description": "Creation timestamp in YYYY-MM-DD format"
                                },
                                "updated_at": {
                                    "type": "string",
                                    "description": "Update timestamp in YYYY-MM-DD format"
                                }
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
