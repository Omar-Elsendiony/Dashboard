import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManageEscalations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, escalation_data: Dict[str, Any] = None, escalation_id: str = None) -> str:
        """
        Create or update escalation records.
        
        Actions:
        - create: Create new escalation (requires incident_id, escalated_from, escalated_to, escalation_level, escalation_reason)
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
        valid_levels = ["L1_to_L2", "L2_to_L3", "L3_to_management", "management_to_executive"]
        valid_statuses = ["pending", "approved", "denied", "cancelled"]

        # allowed values
        required_incident_statuses = ["open", "in_progress"]
        required_user_status = ["active"]


        # for create action
        if action == "create":
            if not escalation_data:
                return json.dumps({
                    "success": False,
                    "error": "escalation_data is required for create action"
                })

            # Validate required fields for create
            required_fields = ["incident_id", "escalated_from", "escalated_to", "escalation_level", "escalation_reason"]
            
            missing_fields = [field for field in required_fields if field not in escalation_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Missing required fields for create action: {', '.join(missing_fields)}"
                })
            
            # Validate that incident exists
            if str(escalation_data["incident_id"]) not in incidents:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Incident not found"
                })
            
            # Validate that incident is open or in_progress
            incident_status = incidents[str(escalation_data["incident_id"])]["status"]
            if incident_status not in required_incident_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Incident status must be one of: {', '.join(required_incident_statuses)}"
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
            
            # Validate that both escalated_to and escalated_from users are active
            for key in ["escalated_to", "escalated_from"]:
                user_id = str(escalation_data[key])
                if users[user_id]["status"] not in required_user_status:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: User {key} must be active"
                    })
            
            # Validate escalation_level enum
            if escalation_data["escalation_level"] not in valid_levels:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid escalation_level. Must be one of: {', '.join(valid_levels)}"
                })
            
            # Validate escalation_reason is not empty
            if not escalation_data.get("escalation_reason") or not escalation_data.get("escalation_reason", "").strip():
                return json.dumps({
                    "success": False,
                    "error": "Halt: escalation_reason cannot be empty"
                })
            
            # Validate status
            status = escalation_data.get("delivery_status", "pending")
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
                "escalated_from": str(escalation_data["escalated_from"]),
                "escalated_to": str(escalation_data["escalated_to"]),
                "escalation_level": escalation_data["escalation_level"],
                "escalation_reason": escalation_data["escalation_reason"],
                "status": status,
                "requested_at": "2025-10-07T00:00:00",
                "responded_at": escalation_data["responded_at"] if "responded_at" in escalation_data else None
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
                    "error": "Halt: escalation_id is required for update action"
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
            
            # Validate at least one optional field is provided
            update_fields = ["status", "escalated_to", "responded_at"]
            provided_fields = [field for field in update_fields if field in escalation_data]
            if not provided_fields:
                return json.dumps({
                    "success": False,
                    "error": f"At least one optional field must be provided for updates {', '.join(update_fields)}"
                })

            # Validate user to reassign the escalation to exists if provided
            if "escalated_to" in escalation_data and str(escalation_data["escalated_to"]) not in users:
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
            
            # Validate status if provided
            if "status" in escalation_data and escalation_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })
            

            # Get current escalation record
            current_escalation = escalations[str(escalation_id)]
            # Update escalation record with modified information
            updated_escalation = current_escalation.copy()
            for key, value in escalation_data.items():
                if key == "responded_at":
                    updated_escalation[key] = str(value) if value not in (None, "") else None
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
                "name": "manage_escalations",
                "description": "Create or update escalation records in the incident management system. This tool manages escalation workflows with comprehensive validation of users, incidents, escalation levels, and status transitions. For creation, establishes new escalations with proper validation of incident existence, user roles, and escalation paths. For updates, modifies existing escalation records including status changes and response timestamps. Validates escalation levels (L1_to_L2, L2_to_L3, L3_to_management, management_to_executive), ensures proper user assignments, and maintains escalation audit trail. Essential for incident escalation management, workflow tracking, and maintaining proper escalation procedures.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to create new escalation, 'update' to modify existing escalation",
                            "enum": ["create", "update"]
                        },
                        "escalation_data": {
                            "type": "object",
                            "description": "Details for creating or updating an escalation record",
                            "properties": {
                                "incident_id": {
                                    "type": "string",
                                    "description": "Related incident identifier (required for create, must exist in system)"
                                },
                                "escalated_from": {
                                    "type": "string",
                                    "description": "User identifier who requested the escalation (required for create, must exist in system)"
                                },
                                "escalated_to": {
                                    "type": "string",
                                    "description": "User identifier receiving the escalation (required for create, must exist in system)"
                                },
                                "escalation_level": {
                                    "type": "string",
                                    "description": "Escalation level (required for create). Must be one of: L1_to_L2, L2_to_L3, L3_to_management, management_to_executive",
                                    "enum": ["L1_to_L2", "L2_to_L3", "L3_to_management", "management_to_executive"]
                                },
                                "escalation_reason": {
                                    "type": "string",
                                    "description": "Reason for escalation (required for create, cannot be empty)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Escalation status (required for create). Must be one of: pending, approved, denied, cancelled",
                                    "enum": ["pending", "approved", "denied", "cancelled"]
                                },
                                "responded_at": {
                                    "type": "string",
                                    "description": "Response timestamp in YYYY-MM-DDTHH:MM:SS format"
                                }
                            }
                        },
                        "escalation_id": {
                            "type": "string",
                            "description": "Unique identifier of the escalation (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
