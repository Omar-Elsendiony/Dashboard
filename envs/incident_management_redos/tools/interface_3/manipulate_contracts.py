import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManipulateContracts(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        entity_data: Optional[Dict[str, Any]] = None,
        entity_id: Optional[str] = None
    ) -> str:
        """
        Create or update SLA agreement records.
        
        Actions:
        - create: Create new SLA agreement record (requires entity_data)
        - update: Update existing SLA agreement record (requires entity_id and entity_data)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        timestamp = "2025-10-07T12:00:00"
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        sla_agreements = data.get("sla_agreements", {})
        clients = data.get("clients", {})
        users = data.get("users", {})
        
        if action == "create":
            if not entity_data:
                return json.dumps({
                    "success": False,
                    "error": "entity_data is required for create action"
                })
            
            # Validate required fields (based on DB schema)
            required_fields = ["client_id", "tier", "support_coverage", "effective_date", "created_by"]
            missing_fields = [field for field in required_fields if field not in entity_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                })
            
            # Validate non-empty required fields
            for field in required_fields:
                if not entity_data[field] or str(entity_data[field]).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })
            
            # Validate allowed fields
            allowed_fields = ["client_id", "tier", "support_coverage", "effective_date", "expiration_date", "created_by", "status"]
            invalid_fields = [field for field in entity_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields: {', '.join(invalid_fields)}"
                })
            
            # Validate tier enum
            valid_tiers = ["premium", "standard", "basic"]
            if entity_data["tier"] not in valid_tiers:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid tier '{entity_data['tier']}'. Must be one of: {', '.join(valid_tiers)}"
                })
            
            # Validate support_coverage enum
            valid_support_coverage = ["24x7", "business_hours", "on_call"]
            if entity_data["support_coverage"] not in valid_support_coverage:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid support_coverage '{entity_data['support_coverage']}'. Must be one of: {', '.join(valid_support_coverage)}"
                })
            
            # Validate status enum if provided
            if "status" in entity_data:
                valid_status = ["active", "inactive", "expired"]
                if entity_data["status"] not in valid_status:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status '{entity_data['status']}'. Must be one of: {', '.join(valid_status)}"
                    })
            
            # Validate optional fields are not empty if provided
            optional_fields = ["expiration_date"]
            for field in optional_fields:
                if field in entity_data and entity_data[field] is not None:
                    if str(entity_data[field]).strip() == "":
                        return json.dumps({
                            "success": False,
                            "error": f"Field '{field}' cannot be empty if provided"
                        })
            
            # Validate client_id exists
            if str(entity_data["client_id"]) not in clients:
                return json.dumps({
                    "success": False,
                    "error": "Client not found"
                })
            
            # Validate created_by exists
            if str(entity_data["created_by"]) not in users:
                return json.dumps({
                    "success": False,
                    "error": "User not found"
                })
            
            # Create new SLA agreement
            new_id = str(generate_id(sla_agreements))
            new_sla = {
                "sla_id": new_id,
                "client_id": str(entity_data["client_id"]),
                "tier": entity_data["tier"],
                "support_coverage": entity_data["support_coverage"],
                "effective_date": entity_data["effective_date"],
                "expiration_date": entity_data.get("expiration_date"),
                "created_by": str(entity_data["created_by"]),
                "created_at": timestamp,
                "updated_at": timestamp,
                "status": entity_data.get("status", "active")
            }
            sla_agreements[new_id] = new_sla
            
            return json.dumps({
                "success": True,
                "action": "create",
                "sla_id": new_id,
                "sla_data": new_sla
            })
        
        elif action == "update":
            if not entity_id:
                return json.dumps({
                    "success": False,
                    "error": "entity_id is required for update action"
                })
            
            if entity_id not in sla_agreements:
                return json.dumps({
                    "success": False,
                    "error": f"SLA agreement {entity_id} not found"
                })
            
            # Check if SLA is inactive or expired
            current_sla = sla_agreements[entity_id]
            if current_sla.get("status") in ["inactive", "expired"]:
                return json.dumps({
                    "success": False,
                    "error": f"Cannot update SLA agreement {entity_id} with status '{current_sla.get('status')}'. Please reactivate the SLA first."
                })
            
            if not entity_data:
                return json.dumps({
                    "success": False,
                    "error": "entity_data is required for update action"
                })
            
            # Validate allowed fields
            allowed_fields = ["client_id", "tier", "support_coverage", "effective_date", "expiration_date", "created_by", "status"]
            invalid_fields = [field for field in entity_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields: {', '.join(invalid_fields)}"
                })
            
            # Validate non-empty fields
            for field, value in entity_data.items():
                if field != "expiration_date" and value is not None and str(value).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })
                elif field == "expiration_date" and value is not None and str(value).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty if provided"
                    })
            
            # Validate tier enum if provided
            if "tier" in entity_data:
                valid_tiers = ["premium", "standard", "basic"]
                if entity_data["tier"] not in valid_tiers:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid tier. Must be one of: {', '.join(valid_tiers)}"
                    })
            
            # Validate support_coverage enum if provided
            if "support_coverage" in entity_data:
                valid_support_coverage = ["24x7", "business_hours", "on_call"]
                if entity_data["support_coverage"] not in valid_support_coverage:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid support_coverage. Must be one of: {', '.join(valid_support_coverage)}"
                    })
            
            # Validate status enum if provided
            if "status" in entity_data:
                valid_status = ["active", "inactive", "expired"]
                if entity_data["status"] not in valid_status:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_status)}"
                    })
            
            # Validate client_id if being updated
            if "client_id" in entity_data:
                if str(entity_data["client_id"]) not in clients:
                    return json.dumps({
                        "success": False,
                        "error": "Client not found"
                    })
            
            # Validate created_by if being updated
            if "created_by" in entity_data:
                if str(entity_data["created_by"]) not in users:
                    return json.dumps({
                        "success": False,
                        "error": "User not found"
                    })
            
            # Update SLA agreement
            updated_sla = sla_agreements[entity_id].copy()
            for key, value in entity_data.items():
                if key in ["client_id", "created_by"]:
                    updated_sla[key] = str(value)
                else:
                    updated_sla[key] = value
            updated_sla["updated_at"] = timestamp
            sla_agreements[entity_id] = updated_sla
            
            return json.dumps({
                "success": True,
                "action": "update",
                "sla_id": entity_id,
                "sla_data": updated_sla
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manipulate_contracts",
                "description": "Create or update SLA agreement records in the incident management system. For creation, establishes new SLA agreement records with comprehensive validation. For updates, modifies existing records while maintaining data integrity. Validates SLA tiers, support coverage, and status values according to system requirements.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new record, 'update' to modify existing record"
                        },
                        "entity_data": {
                            "type": "object",
                            "description": "SLA agreement data object containing fields for creating or updating SLA agreements",
                            "properties": {
                                "client_id": {
                                    "type": "string",
                                    "description": "Client identifier (required for create, cannot be empty, must exist in system)"
                                },
                                "tier": {
                                    "type": "string",
                                    "description": "SLA tier level (required for create). Must be one of: premium, standard, basic"
                                },
                                "support_coverage": {
                                    "type": "string",
                                    "description": "Support coverage level (required for create). Must be one of: 24x7, business_hours, on_call"
                                },
                                "effective_date": {
                                    "type": "string",
                                    "description": "Date when SLA becomes effective (required for create, cannot be empty)"
                                },
                                "expiration_date": {
                                    "type": "string",
                                    "description": "Date when SLA expires (optional, cannot be empty if provided)"
                                },
                                "created_by": {
                                    "type": "string",
                                    "description": "User identifier who created the SLA (required for create, cannot be empty, must exist in system)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status of the SLA agreement (optional, defaults to 'active'). Must be one of: active, inactive, expired"
                                }
                            }
                        },
                        "entity_id": {
                            "type": "string",
                            "description": "Unique identifier of the SLA agreement record. Required for update action only."
                        }
                    },
                    "required": ["action"]
                }
            }
        }