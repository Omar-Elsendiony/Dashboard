import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverParties(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover party entities (clients, vendors, users). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - clients: Client records
        - vendors: Vendor records
        - users: User records
        """
        if entity_type not in ["clients", "vendors", "users"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'clients', 'vendors', or 'users'"
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
                    if entity_type == "clients":
                        id_field = "client_id"
                    elif entity_type == "vendors":
                        id_field = "vendor_id"
                    else:  # users
                        id_field = "user_id"
                        # Remove role field from user data
                        entity_data = {k: v for k, v in entity_data.items() if k != "role"}
                    results.append({**entity_data, id_field: entity_id})
            else:
                if entity_type == "clients":
                    id_field = "client_id"
                elif entity_type == "vendors":
                    id_field = "vendor_id"
                else:  # users
                    id_field = "user_id"
                    # Remove role field from user data
                    entity_data = {k: v for k, v in entity_data.items() if k != "role"}
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
                "name": "discover_parties",
                "description": "Discover party entities (clients, vendors, users). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'clients', 'vendors', or 'users'"
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
                                "address": {
                                    "type": "string",
                                    "description": "Client address (for clients)"
                                },
                                "contact_phone": {
                                    "type": "string",
                                    "description": "Contact phone number"
                                },
                                "contact_email": {
                                    "type": "string",
                                    "description": "Contact email address"
                                },
                                "support_coverage": {
                                    "type": "string",
                                    "description": "Support coverage: '24x7', 'business_hours', 'on_call' (for clients)"
                                },
                                "preferred_communication": {
                                    "type": "string",
                                    "description": "Preferred communication method: 'email', 'portal', 'phone', 'slack' (for clients)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status of the entity"
                                },
                                "vendor_id": {
                                    "type": "string",
                                    "description": "Vendor ID (for vendors)"
                                },
                                "vendor_name": {
                                    "type": "string",
                                    "description": "Vendor name (for vendors)"
                                },
                                "user_id": {
                                    "type": "string",
                                    "description": "User ID (for users)"
                                },
                                "first_name": {
                                    "type": "string",
                                    "description": "User first name (for users)"
                                },
                                "last_name": {
                                    "type": "string",
                                    "description": "User last name (for users)"
                                },
                                "email": {
                                    "type": "string",
                                    "description": "User email address (for users)"
                                },
                                "timezone": {
                                    "type": "string",
                                    "description": "User timezone (for users)"
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
