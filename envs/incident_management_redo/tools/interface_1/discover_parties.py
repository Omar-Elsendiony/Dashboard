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
                    results.append({**entity_data, id_field: entity_id})
            else:
                if entity_type == "clients":
                    id_field = "client_id"
                elif entity_type == "vendors":
                    id_field = "vendor_id"
                else:  # users
                    id_field = "user_id"
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
                "description": "Discover party entities (clients, vendors, users). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results. Entity types: 'clients' (client records; filterable by client_id (string), client_name (string), registration_number (string), company_type (enum: 'enterprise', 'mid_market', 'smb', 'startup'), address (text), contact_phone (string), contact_email (string), support_coverage (enum: '24x7', 'business_hours', 'on_call'), preferred_communication (enum: 'email', 'portal', 'phone', 'slack'), status (enum: 'active', 'inactive', 'pending'), created_at (timestamp), updated_at (timestamp)), 'vendors' (vendor records; filterable by vendor_id (string), vendor_name (string), contact_email (string), contact_phone (string), status (enum: 'active', 'inactive'), created_at (timestamp)), 'users' (user records; filterable by user_id (string), first_name (string), last_name (string), email (string), role (enum: 'incident_manager', 'technical_support', 'account_manager', 'executive', 'vendor_contact', 'system_administrator', 'client_contact'), timezone (string), status (enum: 'active', 'inactive', 'suspended'), client_id (string), vendor_id (string), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'clients', 'vendors', or 'users'",
                            "enum": ["clients", "vendors", "users"]
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For clients: client_id, client_name, registration_number, company_type, address, contact_phone, contact_email, support_coverage, preferred_communication, status, created_at, updated_at. For vendors: vendor_id, vendor_name, contact_email, contact_phone, status, created_at. For users: user_id, first_name, last_name, email, role, timezone, status, client_id, vendor_id, created_at, updated_at"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }

