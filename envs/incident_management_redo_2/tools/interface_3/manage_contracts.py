import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageContracts(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        entity_type: str,
        entity_data: Optional[Dict[str, Any]] = None,
        entity_id: Optional[str] = None
    ) -> str:
        """
        Create or update subscription and SLA agreement records.
        
        Actions:
        - create: Create new subscription or SLA agreement record (requires entity_data)
        - update: Update existing subscription or SLA agreement record (requires entity_id and entity_data)
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
        
        if entity_type not in ["subscriptions", "sla_agreements"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'subscriptions' or 'sla_agreements'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        # ========== SUBSCRIPTIONS ==========
        if entity_type == "subscriptions":
            subscriptions = data.get("subscriptions", {})
            clients = data.get("clients", {})
            
            if action == "create":
                if not entity_data:
                    return json.dumps({
                        "success": False,
                        "error": "entity_data is required for create action"
                    })
                
                # Validate required fields
                required_fields = ["client_id", "tier", "start_date"]
                missing_fields = [field for field in required_fields if field not in entity_data]
                if missing_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Missing required fields: {', '.join(missing_fields)}"
                    })
                
                # Validate allowed fields
                allowed_fields = ["client_id", "tier", "start_date", "end_date", "status"]
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
                
                # Validate status enum if provided
                if "status" in entity_data:
                    valid_status = ["active", "expired", "cancelled"]
                    if entity_data["status"] not in valid_status:
                        return json.dumps({
                            "success": False,
                            "error": f"Invalid status '{entity_data['status']}'. Must be one of: {', '.join(valid_status)}"
                        })
                
                # Validate client_id exists
                if entity_data["client_id"] not in clients:
                    return json.dumps({
                        "success": False,
                        "error": "Client not found"
                    })
                
                # Create new subscription
                new_id = str(generate_id(subscriptions))
                new_subscription = {
                    "subscription_id": new_id,
                    "client_id": entity_data["client_id"],
                    "tier": entity_data["tier"],
                    "start_date": entity_data["start_date"],
                    "end_date": entity_data.get("end_date"),
                    "status": entity_data.get("status", "active"),
                    "created_at": timestamp,
                    "updated_at": timestamp
                }
                subscriptions[new_id] = new_subscription
                
                return json.dumps({
                    "success": True,
                    "action": "create",
                    "entity_type": "subscriptions",
                    "subscription_id": new_id,
                    "subscription_data": new_subscription
                })
            
            elif action == "update":
                if not entity_id:
                    return json.dumps({
                        "success": False,
                        "error": "entity_id is required for update action"
                    })
                
                if entity_id not in subscriptions:
                    return json.dumps({
                        "success": False,
                        "error": f"Subscription {entity_id} not found"
                    })
                
                if not entity_data:
                    return json.dumps({
                        "success": False,
                        "error": "entity_data is required for update action"
                    })
                
                # Validate allowed fields
                allowed_fields = ["client_id", "tier", "start_date", "end_date", "status"]
                invalid_fields = [field for field in entity_data.keys() if field not in allowed_fields]
                if invalid_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid fields: {', '.join(invalid_fields)}"
                    })
                
                # Validate tier enum if provided
                if "tier" in entity_data:
                    valid_tiers = ["premium", "standard", "basic"]
                    if entity_data["tier"] not in valid_tiers:
                        return json.dumps({
                            "success": False,
                            "error": f"Invalid tier. Must be one of: {', '.join(valid_tiers)}"
                        })
                
                # Validate status enum if provided
                if "status" in entity_data:
                    valid_status = ["active", "expired", "cancelled"]
                    if entity_data["status"] not in valid_status:
                        return json.dumps({
                            "success": False,
                            "error": f"Invalid status. Must be one of: {', '.join(valid_status)}"
                        })
                
                # Validate client_id if being updated
                if "client_id" in entity_data:
                    if entity_data["client_id"] not in clients:
                        return json.dumps({
                            "success": False,
                            "error": "Client not found"
                        })
                
                # Update subscription
                updated_subscription = subscriptions[entity_id].copy()
                for key, value in entity_data.items():
                    updated_subscription[key] = value
                updated_subscription["updated_at"] = timestamp
                subscriptions[entity_id] = updated_subscription
                
                return json.dumps({
                    "success": True,
                    "action": "update",
                    "entity_type": "subscriptions",
                    "subscription_id": entity_id,
                    "subscription_data": updated_subscription
                })
        
        # ========== SLA AGREEMENTS ==========
        elif entity_type == "sla_agreements":
            sla_agreements = data.get("sla_agreements", {})
            subscriptions = data.get("subscriptions", {})
            users = data.get("users", {})
            
            if action == "create":
                if not entity_data:
                    return json.dumps({
                        "success": False,
                        "error": "entity_data is required for create action"
                    })
                
                # Validate required fields
                required_fields = ["subscription_id", "severity_level", "response_time_minutes", "resolution_time_minutes", "created_by"]
                missing_fields = [field for field in required_fields if field not in entity_data]
                if missing_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Missing required fields: {', '.join(missing_fields)}"
                    })
                
                # Validate allowed fields
                allowed_fields = ["subscription_id", "severity_level", "response_time_minutes", "resolution_time_minutes", "availability_guarantee", "created_by"]
                invalid_fields = [field for field in entity_data.keys() if field not in allowed_fields]
                if invalid_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid fields: {', '.join(invalid_fields)}"
                    })
                
                # Validate severity_level enum
                valid_severity_levels = ["P1", "P2", "P3", "P4"]
                if entity_data["severity_level"] not in valid_severity_levels:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid severity_level '{entity_data['severity_level']}'. Must be one of: {', '.join(valid_severity_levels)}"
                    })
                
                # Validate subscription_id exists
                if entity_data["subscription_id"] not in subscriptions:
                    return json.dumps({
                        "success": False,
                        "error": "Subscription not found"
                    })
                
                # Validate created_by exists
                if entity_data["created_by"] not in users:
                    return json.dumps({
                        "success": False,
                        "error": "User not found"
                    })
                
                # Check uniqueness: one SLA per subscription per severity level
                for sla in sla_agreements.values():
                    if sla.get("subscription_id") == entity_data["subscription_id"] and sla.get("severity_level") == entity_data["severity_level"]:
                        return json.dumps({
                            "success": False,
                            "error": "SLA agreement already exists for this subscription and severity level"
                        })
                
                # Create new SLA agreement
                new_id = str(generate_id(sla_agreements))
                new_sla = {
                    "sla_id": new_id,
                    "subscription_id": entity_data["subscription_id"],
                    "severity_level": entity_data["severity_level"],
                    "response_time_minutes": entity_data["response_time_minutes"],
                    "resolution_time_minutes": entity_data["resolution_time_minutes"],
                    "availability_guarantee": entity_data.get("availability_guarantee"),
                    "created_by": entity_data["created_by"],
                    "created_at": timestamp
                }
                sla_agreements[new_id] = new_sla
                
                return json.dumps({
                    "success": True,
                    "action": "create",
                    "entity_type": "sla_agreements",
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
                
                if not entity_data:
                    return json.dumps({
                        "success": False,
                        "error": "entity_data is required for update action"
                    })
                
                # Validate allowed fields
                allowed_fields = ["subscription_id", "severity_level", "response_time_minutes", "resolution_time_minutes", "availability_guarantee", "created_by"]
                invalid_fields = [field for field in entity_data.keys() if field not in allowed_fields]
                if invalid_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid fields: {', '.join(invalid_fields)}"
                    })
                
                # Validate severity_level enum if provided
                if "severity_level" in entity_data:
                    valid_severity_levels = ["P1", "P2", "P3", "P4"]
                    if entity_data["severity_level"] not in valid_severity_levels:
                        return json.dumps({
                            "success": False,
                            "error": f"Invalid severity_level. Must be one of: {', '.join(valid_severity_levels)}"
                        })
                
                # Validate subscription_id if being updated
                if "subscription_id" in entity_data:
                    if entity_data["subscription_id"] not in subscriptions:
                        return json.dumps({
                            "success": False,
                            "error": "Subscription not found"
                        })
                
                # Validate created_by if being updated
                if "created_by" in entity_data:
                    if entity_data["created_by"] not in users:
                        return json.dumps({
                            "success": False,
                            "error": "User not found"
                        })
                
                # Check uniqueness if subscription_id or severity_level is being updated
                current_sla = sla_agreements[entity_id]
                new_subscription_id = entity_data.get("subscription_id", current_sla.get("subscription_id"))
                new_severity_level = entity_data.get("severity_level", current_sla.get("severity_level"))
                
                if "subscription_id" in entity_data or "severity_level" in entity_data:
                    for sla_id, sla in sla_agreements.items():
                        if sla_id != entity_id and sla.get("subscription_id") == new_subscription_id and sla.get("severity_level") == new_severity_level:
                            return json.dumps({
                                "success": False,
                                "error": "New SLA agreement combination already exists for this subscription and severity level"
                            })
                
                # Update SLA agreement
                updated_sla = sla_agreements[entity_id].copy()
                for key, value in entity_data.items():
                    updated_sla[key] = value
                sla_agreements[entity_id] = updated_sla
                
                return json.dumps({
                    "success": True,
                    "action": "update",
                    "entity_type": "sla_agreements",
                    "sla_id": entity_id,
                    "sla_data": updated_sla
                })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_contracts",
                "description": "Create or update subscription and SLA agreement records in the incident management system. For creation, establishes new subscription or SLA agreement records with comprehensive validation. For updates, modifies existing records while maintaining data integrity. Validates subscription tiers, SLA severity levels, and ensures unique SLA agreements per subscription and severity level combination.",
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
                            "description": "Type of entity to manage: 'subscriptions' or 'sla_agreements'",
                            "enum": ["subscriptions", "sla_agreements"]
                        },
                        "entity_data": {
                            "type": "object",
                            "description": "Entity data object. For subscriptions create: requires client_id, tier ('premium', 'standard', 'basic'), start_date (YYYY-MM-DD), with optional end_date (YYYY-MM-DD), status ('active', 'expired', 'cancelled'). For sla_agreements create: requires subscription_id, severity_level ('P1', 'P2', 'P3', 'P4'), response_time_minutes, resolution_time_minutes, created_by, with optional availability_guarantee. For update: includes fields to change. SYNTAX: {\"key\": \"value\"}"
                        },
                        "entity_id": {
                            "type": "string",
                            "description": "Unique identifier of the entity record (subscription_id for subscriptions, sla_id for sla_agreements). Required for update action only."
                        }
                    },
                    "required": ["action", "entity_type"]
                }
            }
        }
