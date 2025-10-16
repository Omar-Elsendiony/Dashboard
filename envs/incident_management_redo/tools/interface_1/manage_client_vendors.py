import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageClientVendors(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        entity_type: str,
        entity_data: Optional[Dict[str, Any]] = None,
        entity_id: Optional[str] = None
    ) -> str:
        """
        Create or update client and vendor records.
        
        Actions:
        - create: Create new client or vendor record (requires entity_data)
        - update: Update existing client or vendor record (requires entity_id and entity_data)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        timestamp = "2025-10-01T00:00:00"
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if entity_type not in ["clients", "vendors"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'clients' or 'vendors'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        # ========== CLIENTS ==========
        if entity_type == "clients":
            clients = data.get("clients", {})
            
            if action == "create":
                if not entity_data:
                    return json.dumps({
                        "success": False,
                        "error": "entity_data is required for create action"
                    })
                
                # Validate required fields
                required_fields = ["client_name", "company_type", "contact_email", "support_coverage", "preferred_communication"]
                missing_fields = [field for field in required_fields if field not in entity_data]
                if missing_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Missing required fields: {', '.join(missing_fields)}"
                    })
                
                # Validate allowed fields
                allowed_fields = ["client_name", "registration_number", "company_type", "address", "contact_phone", "contact_email", "support_coverage", "preferred_communication", "status"]
                invalid_fields = [field for field in entity_data.keys() if field not in allowed_fields]
                if invalid_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid fields: {', '.join(invalid_fields)}"
                    })
                
                # Validate enums
                valid_company_types = ["enterprise", "mid_market", "smb", "startup"]
                if entity_data["company_type"] not in valid_company_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid company_type '{entity_data['company_type']}'. Must be one of: {', '.join(valid_company_types)}"
                    })
                
                valid_support_coverage = ["24x7", "business_hours", "on_call"]
                if entity_data["support_coverage"] not in valid_support_coverage:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid support_coverage '{entity_data['support_coverage']}'. Must be one of: {', '.join(valid_support_coverage)}"
                    })
                
                valid_preferred_communication = ["email", "portal", "phone", "slack"]
                if entity_data["preferred_communication"] not in valid_preferred_communication:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid preferred_communication '{entity_data['preferred_communication']}'. Must be one of: {', '.join(valid_preferred_communication)}"
                    })
                
                if "status" in entity_data:
                    valid_status = ["active", "inactive", "pending"]
                    if entity_data["status"] not in valid_status:
                        return json.dumps({
                            "success": False,
                            "error": f"Invalid status '{entity_data['status']}'. Must be one of: {', '.join(valid_status)}"
                        })
                
                # Check registration_number uniqueness
                if "registration_number" in entity_data and entity_data["registration_number"]:
                    for client in clients.values():
                        if client.get("registration_number") == entity_data["registration_number"]:
                            return json.dumps({
                                "success": False,
                                "error": "Registration number already exists"
                            })
                
                # Create new client
                new_id = str(generate_id(clients))
                new_client = {
                    "client_id": new_id,
                    "client_name": entity_data["client_name"],
                    "registration_number": entity_data.get("registration_number"),
                    "company_type": entity_data["company_type"],
                    "address": entity_data.get("address"),
                    "contact_phone": entity_data.get("contact_phone"),
                    "contact_email": entity_data["contact_email"],
                    "support_coverage": entity_data["support_coverage"],
                    "preferred_communication": entity_data["preferred_communication"],
                    "status": entity_data.get("status", "active"),
                    "created_at": timestamp,
                    "updated_at": timestamp
                }
                clients[new_id] = new_client
                
                return json.dumps({
                    "success": True,
                    "action": "create",
                    "entity_type": "clients",
                    "client_id": new_id,
                    "client_data": new_client
                })
            
            elif action == "update":
                if not entity_id:
                    return json.dumps({
                        "success": False,
                        "error": "entity_id is required for update action"
                    })
                
                if entity_id not in clients:
                    return json.dumps({
                        "success": False,
                        "error": f"Client {entity_id} not found"
                    })
                
                if not entity_data:
                    return json.dumps({
                        "success": False,
                        "error": "entity_data is required for update action"
                    })
                
                # Validate allowed fields
                allowed_fields = ["client_name", "registration_number", "company_type", "address", "contact_phone", "contact_email", "support_coverage", "preferred_communication", "status"]
                invalid_fields = [field for field in entity_data.keys() if field not in allowed_fields]
                if invalid_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid fields: {', '.join(invalid_fields)}"
                    })
                
                # Validate enums if provided
                if "company_type" in entity_data:
                    valid_company_types = ["enterprise", "mid_market", "smb", "startup"]
                    if entity_data["company_type"] not in valid_company_types:
                        return json.dumps({
                            "success": False,
                            "error": f"Invalid company_type. Must be one of: {', '.join(valid_company_types)}"
                        })
                
                if "support_coverage" in entity_data:
                    valid_support_coverage = ["24x7", "business_hours", "on_call"]
                    if entity_data["support_coverage"] not in valid_support_coverage:
                        return json.dumps({
                            "success": False,
                            "error": f"Invalid support_coverage. Must be one of: {', '.join(valid_support_coverage)}"
                        })
                
                if "preferred_communication" in entity_data:
                    valid_preferred_communication = ["email", "portal", "phone", "slack"]
                    if entity_data["preferred_communication"] not in valid_preferred_communication:
                        return json.dumps({
                            "success": False,
                            "error": f"Invalid preferred_communication. Must be one of: {', '.join(valid_preferred_communication)}"
                        })
                
                if "status" in entity_data:
                    valid_status = ["active", "inactive", "pending"]
                    if entity_data["status"] not in valid_status:
                        return json.dumps({
                            "success": False,
                            "error": f"Invalid status. Must be one of: {', '.join(valid_status)}"
                        })
                
                # Check registration_number uniqueness if being updated
                if "registration_number" in entity_data and entity_data["registration_number"]:
                    for cid, client in clients.items():
                        if cid != entity_id and client.get("registration_number") == entity_data["registration_number"]:
                            return json.dumps({
                                "success": False,
                                "error": "New registration_number already exists"
                            })
                
                # Update client
                updated_client = clients[entity_id].copy()
                for key, value in entity_data.items():
                    updated_client[key] = value
                updated_client["updated_at"] = timestamp
                clients[entity_id] = updated_client
                
                return json.dumps({
                    "success": True,
                    "action": "update",
                    "entity_type": "clients",
                    "client_id": entity_id,
                    "client_data": updated_client
                })
        
        # ========== VENDORS ==========
        elif entity_type == "vendors":
            vendors = data.get("vendors", {})
            
            if action == "create":
                if not entity_data:
                    return json.dumps({
                        "success": False,
                        "error": "entity_data is required for create action"
                    })
                
                # Validate required fields
                required_fields = ["vendor_name"]
                missing_fields = [field for field in required_fields if field not in entity_data]
                if missing_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Missing required fields: {', '.join(missing_fields)}"
                    })
                
                # Validate allowed fields
                allowed_fields = ["vendor_name", "contact_email", "contact_phone", "status"]
                invalid_fields = [field for field in entity_data.keys() if field not in allowed_fields]
                if invalid_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid fields: {', '.join(invalid_fields)}"
                    })
                
                # Validate status enum
                if "status" in entity_data:
                    valid_status = ["active", "inactive"]
                    if entity_data["status"] not in valid_status:
                        return json.dumps({
                            "success": False,
                            "error": f"Invalid status '{entity_data['status']}'. Must be one of: {', '.join(valid_status)}"
                        })
                
                # Create new vendor
                new_id = str(generate_id(vendors))
                new_vendor = {
                    "vendor_id": new_id,
                    "vendor_name": entity_data["vendor_name"],
                    "contact_email": entity_data.get("contact_email"),
                    "contact_phone": entity_data.get("contact_phone"),
                    "status": entity_data.get("status", "active"),
                    "created_at": timestamp
                }
                vendors[new_id] = new_vendor
                
                return json.dumps({
                    "success": True,
                    "action": "create",
                    "entity_type": "vendors",
                    "vendor_id": new_id,
                    "vendor_data": new_vendor
                })
            
            elif action == "update":
                if not entity_id:
                    return json.dumps({
                        "success": False,
                        "error": "entity_id is required for update action"
                    })
                
                if entity_id not in vendors:
                    return json.dumps({
                        "success": False,
                        "error": f"Vendor {entity_id} not found"
                    })
                
                if not entity_data:
                    return json.dumps({
                        "success": False,
                        "error": "entity_data is required for update action"
                    })
                
                # Validate allowed fields
                allowed_fields = ["vendor_name", "contact_email", "contact_phone", "status"]
                invalid_fields = [field for field in entity_data.keys() if field not in allowed_fields]
                if invalid_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid fields: {', '.join(invalid_fields)}"
                    })
                
                # Validate status enum if provided
                if "status" in entity_data:
                    valid_status = ["active", "inactive"]
                    if entity_data["status"] not in valid_status:
                        return json.dumps({
                            "success": False,
                            "error": f"Invalid status. Must be one of: {', '.join(valid_status)}"
                        })
                
                # Update vendor
                updated_vendor = vendors[entity_id].copy()
                for key, value in entity_data.items():
                    updated_vendor[key] = value
                vendors[entity_id] = updated_vendor
                
                return json.dumps({
                    "success": True,
                    "action": "update",
                    "entity_type": "vendors",
                    "vendor_id": entity_id,
                    "vendor_data": updated_vendor
                })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_client_vendors",
                "description": "Create or update client and vendor records in the incident management system. For creation, establishes new client or vendor records with comprehensive validation. For updates, modifies existing records while maintaining data integrity. Validates company types, support coverage, communication preferences, and status values according to system requirements.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new record, 'update' to modify existing record",
                            "enum": ["create", "update"]
                        },
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to manage: 'clients' or 'vendors'",
                            "enum": ["clients", "vendors"]
                        },
                        "entity_data": {
                            "type": "object",
                            "description": "Entity data object. For clients create: requires client_name, company_type ('enterprise', 'mid_market', 'smb', 'startup'), contact_email, support_coverage ('24x7', 'business_hours', 'on_call'), preferred_communication ('email', 'portal', 'phone', 'slack'), with optional registration_number, address, contact_phone, status ('active', 'inactive', 'pending'). For vendors create: requires vendor_name, with optional contact_email, contact_phone, status ('active', 'inactive'). For update: includes fields to change. SYNTAX: {\"key\": \"value\"}"
                        },
                        "entity_id": {
                            "type": "string",
                            "description": "Unique identifier of the entity record (client_id for clients, vendor_id for vendors). Required for update action only."
                        }
                    },
                    "required": ["action", "entity_type"]
                }
            }
        }
