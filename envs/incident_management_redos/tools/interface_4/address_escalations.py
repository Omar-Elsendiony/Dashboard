import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddressEscalations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, escalation_data: Dict[str, Any] = None, escalation_id: str = None) -> str:
        """
        Create or update escalation records.
        
        Actions:
        - create: Create new escalation (requires incident_id, escalated_from, escalated_to, escalation_reason, approver)
        - update: Update existing escalation (requires escalation_id and fields to update)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for escalations"
            })
        
        # get existing data tables
        escalations = data.get("escalations", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})

        # allowed enums
        valid_statuses = ["pending", "approved", "denied", "cancelled"]

        # allowed values
        required_user_status = ["active"]

        # for create action
        if action == "create":
            if not escalation_data:
                return json.dumps({
                    "success": False,
                    "error": "escalation_data is required for create action"
                })

            # Validate required fields for create (approver is optional as it's set during approval)
            required_fields = ["incident_id", "escalated_to", "escalation_reason", "escalated_from"]
            
            missing_fields = [field for field in required_fields if field not in escalation_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Missing required fields for create action: {', '.join(missing_fields)}"
                })
            
            # Validate non-empty required fields
            for field in required_fields:
                if not escalation_data[field] or str(escalation_data[field]).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })
            
            # Allowed fields
            allowed_fields = ["incident_id", "escalated_to", "escalation_reason", "escalated_from", "approver", "status"]

            escalation_fields = [field for field in escalation_data if field not in allowed_fields]
            if escalation_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Unrecognized fields in escalation_data: {', '.join(escalation_fields)}"
                })
            
            # Validate that incident exists
            if str(escalation_data["incident_id"]) not in incidents:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Incident not found"
                })
            
            # Validate that escalated_from user exists
            if str(escalation_data["escalated_from"]) not in users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: User escalated_from not found"
                })
            
            # Validate that escalated_to user exists
            if str(escalation_data["escalated_to"]) not in users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: User escalated_to not found"
                })
            
            # Validate that escalated_to and escalated_from users are active
            for key in ["escalated_to", "escalated_from"]:
                user_id = str(escalation_data[key])
                if users[user_id]["status"] not in required_user_status:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: User {key} must be active"
                    })
            
            # Validate optional approver if provided
            if escalation_data.get("approver"):
                if not str(escalation_data["approver"]).strip():
                    return json.dumps({
                        "success": False,
                        "error": "Field 'approver' cannot be empty if provided"
                    })
                
                if str(escalation_data["approver"]) not in users:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Approver user not found"
                    })
                
                # Validate that approver user is active
                if users[str(escalation_data["approver"])]["status"] not in required_user_status:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: User 'approver' must be active"
                    })
            
            # Validate status
            status = escalation_data.get("status", "pending")
            if status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid status - must be one of: {', '.join(valid_statuses)}"
                })
            
            # Generate new escalation ID
            new_escalation_id = generate_id(escalations)
            
            # Create new escalation record
            new_escalation = {
                "escalation_id": str(new_escalation_id),
                "incident_id": str(escalation_data["incident_id"]),
                "escalated_to": str(escalation_data["escalated_to"]),
                "escalation_reason": escalation_data["escalation_reason"],
                "approver": str(escalation_data["approver"]) if escalation_data.get("approver") not in (None, "") else None,
                "status": status,
                "escalated_from": str(escalation_data["escalated_from"]),
                "requested_at": "2025-10-07T12:00:00",
                "responded_at": None
            }
            
            escalations[str(new_escalation_id)] = new_escalation
            
            return json.dumps({
                "success": True,
                "action": "create",
                "escalation_id": str(new_escalation_id),
                "message": f"Escalation {new_escalation_id} created successfully",
                "escalation_data": new_escalation
            })
        
        # for update action
        elif action == "update":
            if not escalation_id:
                return json.dumps({
                    "success": False,
                    "error": "escalation_id is required for update action"
                })
            
            if str(escalation_id) not in escalations:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Escalation not found"
                })
            
            if not escalation_data:
                return json.dumps({
                    "success": False,
                    "error": "escalation_data is required for update action"
                })
            
            # Validate at least one optional field is provided (added escalation_reason and approver)
            update_fields = ["status", "escalated_to", "escalation_reason", "approver", "responded_at"]
            provided_fields = [field for field in update_fields if field in escalation_data]
            if not provided_fields:
                return json.dumps({
                    "success": False,
                    "error": f"At least one optional field must be provided for updates {', '.join(update_fields)}"
                })
            
            # Validate only allowed fields for updates
            invalid_fields = [field for field in escalation_data.keys() if field not in update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for escalation updating: {', '.join(invalid_fields)}"
                })

            # Validate non-empty fields
            for field, value in escalation_data.items():
                if field not in ["responded_at", "approver"] and value is not None and str(value).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })

            # Validate user to reassign the escalation to exists if provided
            if "escalated_to" in escalation_data: 
                if str(escalation_data["escalated_to"]) not in users:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: User escalated_to not found"
                    })
            
                # Validate that reassign escalated_to user is active
                if users[str(escalation_data["escalated_to"])]["status"] not in required_user_status: 
                    return json.dumps({ 
                        "success": False, 
                        "error": "Halt: User escalated_to must be active" 
                    })
            
            # Validate approver if provided
            if "approver" in escalation_data:
                if escalation_data["approver"] is not None and str(escalation_data["approver"]).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": "Field 'approver' cannot be empty if provided"
                    })
                
                if escalation_data["approver"] is not None:
                    if str(escalation_data["approver"]) not in users:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: Approver user not found"
                        })
                    
                    # Validate that approver user is active
                    if users[str(escalation_data["approver"])]["status"] not in required_user_status:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: User 'approver' must be active"
                        })
            
            # Validate status if provided
            if "status" in escalation_data and escalation_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })
            
            # Validate responded_at is not empty if provided
            if "responded_at" in escalation_data:
                if escalation_data["responded_at"] is not None and str(escalation_data["responded_at"]).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": "Field 'responded_at' cannot be empty if provided"
                    })

            # Get current escalation record
            current_escalation = escalations[str(escalation_id)]
            # Update escalation record with modified information
            updated_escalation = current_escalation.copy()
            for key, value in escalation_data.items():
                if key in ["responded_at", "approver"]:
                    updated_escalation[key] = str(value) if value not in (None, "") else None
                elif key == "escalated_to":
                    updated_escalation[key] = str(value)
                else:
                    updated_escalation[key] = value
            
            escalations[str(escalation_id)] = updated_escalation
            
            return json.dumps({
                "success": True,
                "action": "update",
                "escalation_id": str(escalation_id),
                "message": f"Escalation {escalation_id} updated successfully",
                "escalation_data": updated_escalation
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "address_escalations",
                "description": "Create or update escalation records in the incident management system. This tool manages escalation workflows with comprehensive validation of users, incidents, and status transitions. For creation, establishes new escalations with proper validation of incident existence, user roles, and escalation paths. For updates, modifies existing escalation records including status changes, escalation reason updates, and response timestamps.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to create new escalation, 'update' to modify existing escalation"
                        },
                        "escalation_data": {
                            "type": "object",
                            "description": "Escalation data object containing fields for creating or updating escalations",
                            "properties": {
                                "incident_id": {
                                    "type": "string",
                                    "description": "Related incident identifier (required for create, cannot be empty, must exist in system)"
                                },
                                "escalated_from": {
                                    "type": "string",
                                    "description": "User identifier who requested the escalation (required for create, cannot be empty, must be active user)"
                                },
                                "escalated_to": {
                                    "type": "string",
                                    "description": "User identifier receiving the escalation (required for create, cannot be empty, must be active user). Updatable."
                                },
                                "escalation_reason": {
                                    "type": "string",
                                    "description": "Reason for escalation (required for create, cannot be empty). Updatable."
                                },
                                "approver": {
                                    "type": "string",
                                    "description": "User identifier who approved/denied the escalation (optional, typically set during approval process, cannot be empty if provided, must be active user). Updatable."
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Escalation status (optional for create, defaults to 'pending'). Must be one of: pending, approved, denied, cancelled. Updatable."
                                },
                                "responded_at": {
                                    "type": "string",
                                    "description": "Response timestamp in YYYY-MM-DDTHH:MM:SS format (optional, cannot be empty if provided). Updatable."
                                }
                            }
                        },
                        "escalation_id": {
                            "type": "string",
                            "description": "Unique identifier of the escalation. Required for update action only."
                        }
                    },
                    "required": ["action"]
                }
            }
        }