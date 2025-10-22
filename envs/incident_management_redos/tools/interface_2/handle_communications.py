import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class HandleCommunications(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, communication_data: Dict[str, Any] = None, communication_id: str = None) -> str:
        """
        Create or update communication records for incident notifications.

        Actions:
        - create: Create new communication (requires incident_id, communication_type, recipient_type, sender, delivery_method, message_content)
        - update: Update existing communication (requires communication_id and fields to update)
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
                "error": "Invalid data format for communications"
            })
        
        # get existing data tables
        communications = data.get("communications", {})
        incidents = data.get("incidents", {})
        problem_tickets = data.get("problem_tickets", {}) # Added for problem_ticket_id validation
        users = data.get("users", {})

        # allowed enums
        valid_types = ["status_update", "resolution_notice", "escalation_notice", "bridge_invitation", "other"]
        valid_recipient_types = ["client", "internal", "executive"]
        valid_methods = ["email", "portal", "sms", "phone"]
        valid_statuses = ["pending", "sent", "delivered", "failed"]

        # valid values
        required_user_status = ["active"]

        # for create action
        if action == "create":
            if not communication_data:
                return json.dumps({
                    "success": False,
                    "error": "communication_data is required for create action"
                })
            
            # Validate required fields
            required_fields = ["communication_type", "recipient_type", "message_content", "sender", "delivery_method"]
            
            missing_fields = [field for field in required_fields if field not in communication_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid communication details - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate non-empty required fields
            for field in required_fields:
                if not communication_data[field] or str(communication_data[field]).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })
            
            # Validate incident_id OR problem_ticket_id
            incident_id = communication_data.get("incident_id")
            problem_ticket_id = communication_data.get("problem_ticket_id")

            if not incident_id and not problem_ticket_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Either 'incident_id' or 'problem_ticket_id' must be provided"
                })
            if incident_id and problem_ticket_id:
                 return json.dumps({
                    "success": False,
                    "error": "Halt: Only one of 'incident_id' or 'problem_ticket_id' can be provided, not both"
                })

            # Validate incident exists if provided
            if incident_id:
                if str(incident_id) not in incidents:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Incident not found"
                    })
            
            # Validate problem ticket exists if provided
            if problem_ticket_id:
                if str(problem_ticket_id) not in problem_tickets:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Problem ticket not found"
                    })

            # Allowed fields
            allowed_fields = ["incident_id", "problem_ticket_id", "communication_type", "recipient_type", "message_content", "sender", "recipient", "delivery_method", "delivery_status", "sent_at"]

            comm_fields = [field for field in communication_data if field not in allowed_fields]
            if comm_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Unrecognized fields in communication_data: {', '.join(comm_fields)}"
                })
            
            # Validate communication_type
            if communication_data["communication_type"] not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid communication type - must be one of: {', '.join(valid_types)}"
                })
            
            # Validate recipient_type
            if communication_data["recipient_type"] not in valid_recipient_types:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid recipient type - must be one of: {', '.join(valid_recipient_types)}"
                })
            
            # Validate sender exists
            if str(communication_data["sender"]) not in users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Sender user not found"
                })
            
            # Validate that sender user is active
            if users[str(communication_data["sender"])]["status"] not in required_user_status: 
                return json.dumps({ 
                    "success": False, 
                    "error": "Halt: User 'sender' must be active" 
                })
            
            # Validate delivery_method
            if communication_data["delivery_method"] not in valid_methods:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid delivery method - must be one of: {', '.join(valid_methods)}"
                })
            
            # Validate optional fields
            if communication_data.get("recipient"):
                if not str(communication_data["recipient"]).strip():
                    return json.dumps({
                        "success": False,
                        "error": "Field 'recipient' cannot be empty if provided"
                    })
                
                # Validate recipient if provided
                if str(communication_data["recipient"]) not in users:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Recipient user not found"
                    })
                
                # Validate that recipient user is active
                if users[str(communication_data["recipient"])]["status"] not in required_user_status: 
                    return json.dumps({ 
                        "success": False, 
                        "error": "Halt: User 'recipient' must be active" 
                    })
                
            # Validate delivery_status
            delivery_status = communication_data.get("delivery_status", "pending")
            if delivery_status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid delivery status - must be one of: {', '.join(valid_statuses)}"
                })
            
            # Validate sent_at is not empty if provided
            if "sent_at" in communication_data:
                if not str(communication_data["sent_at"]).strip():  
                    return json.dumps({
                        "success": False,
                        "error": "Halt: sent_at cannot be empty"
                    })
            
            # Generate new communication ID
            new_comm_id = generate_id(communications)
            
            # Create new communication record
            new_comm = {
                "communication_id": str(new_comm_id),
                "incident_id": str(incident_id) if incident_id else None,
                "problem_ticket_id": str(problem_ticket_id) if problem_ticket_id else None,
                "communication_type": communication_data["communication_type"],
                "recipient_type": communication_data["recipient_type"],
                "message_content": communication_data["message_content"],
                "sender": str(communication_data["sender"]),
                "recipient": str(communication_data["recipient"]) if communication_data.get("recipient") not in (None, "") else None,
                "delivery_method": communication_data["delivery_method"],
                "delivery_status": delivery_status,
                "sent_at": communication_data.get("sent_at") or None,
                "created_at": "2025-10-07T12:00:00"
            }
            
            communications[str(new_comm_id)] = new_comm
            
            return json.dumps({
                "success": True,
                "action": "create",
                "communication_id": str(new_comm_id),
                "message": f"Communication {new_comm_id} created successfully",
                "communication_data": new_comm
            })
        
        # for update action
        elif action == "update":
            if not communication_id:
                return json.dumps({
                    "success": False,
                    "error": "communication_id is required for update action"
                })

            if str(communication_id) not in communications:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Communication not found"
                })
            
            if not communication_data:
                return json.dumps({
                    "success": False,
                    "error": "communication_data is required for update action"
                })
            
            # Validate at least one optional field is provided
            update_fields = ["incident_id", "problem_ticket_id", "communication_type", "recipient_type", "message_content", "sender", "recipient", "delivery_method", "delivery_status", "sent_at"]

            provided_fields = [field for field in update_fields if field in communication_data]
            if not provided_fields:
                return json.dumps({
                    "success": False,
                    "error": f"At least one optional field must be provided for updates {', '.join(update_fields)}"
                })
            
            # Validate only allowed fields for updates
            invalid_fields = [field for field in communication_data.keys() if field not in update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for communication updating: {', '.join(invalid_fields)}"
                })

            # Validate non-empty fields
            for field, value in communication_data.items():
                if field not in ["incident_id", "problem_ticket_id", "recipient"] and value is not None and str(value).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })

            # Validate incident_id OR problem_ticket_id if either is provided
            incident_id_update = communication_data.get("incident_id")
            problem_ticket_id_update = communication_data.get("problem_ticket_id")

            if incident_id_update is not None and problem_ticket_id_update is not None:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Only one of 'incident_id' or 'problem_ticket_id' can be provided, not both"
                })
            
            # If both are provided as None, it means the user wants to clear both, which is not allowed.
            # If one is provided as None and the other as a value, it's a valid update.
            # If one is provided as None and the other is not in communication_data, use existing.
            current_incident_id = communications[str(communication_id)].get("incident_id")
            current_problem_ticket_id = communications[str(communication_id)].get("problem_ticket_id")

            final_incident_id = incident_id_update if "incident_id" in communication_data else current_incident_id
            final_problem_ticket_id = problem_ticket_id_update if "problem_ticket_id" in communication_data else current_problem_ticket_id

            if not final_incident_id and not final_problem_ticket_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Either 'incident_id' or 'problem_ticket_id' must be provided and not null"
                })

            # Validate incident exists if provided
            if incident_id_update:
                if str(incident_id_update) not in incidents:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Incident not found"
                    })
            
            # Validate problem ticket exists if provided
            if problem_ticket_id_update:
                if str(problem_ticket_id_update) not in problem_tickets:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Problem ticket not found"
                    })

            # Validate communication type if provided
            if "communication_type" in communication_data and communication_data["communication_type"] not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid communication type - must be one of: {', '.join(valid_types)}"
                })
            
            # Validate recipient type if provided
            if "recipient_type" in communication_data and communication_data["recipient_type"] not in valid_recipient_types:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid recipient type - must be one of: {', '.join(valid_recipient_types)}"
                })
            
            # Validate sender if provided
            if "sender" in communication_data:
                if str(communication_data["sender"]) not in users:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Sender user not found"
                    })
                
                # Validate that sender user is active
                if users[str(communication_data["sender"])]["status"] not in required_user_status: 
                    return json.dumps({ 
                        "success": False, 
                        "error": "Halt: User 'sender' must be active" 
                    })
            
            # Validate recipient if provided
            if "recipient" in communication_data:
                if communication_data["recipient"] is not None and str(communication_data["recipient"]).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": "Field 'recipient' cannot be empty if provided"
                    })
                
                if communication_data["recipient"] is not None:
                    if str(communication_data["recipient"]) not in users:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: Recipient user not found"
                        })
                    
                    # Validate that recipient user is active
                    if users[str(communication_data["recipient"])]["status"] not in required_user_status: 
                        return json.dumps({ 
                            "success": False, 
                            "error": "Halt: User 'recipient' must be active" 
                        })
            
            # Validate delivery method if provided
            if "delivery_method" in communication_data and communication_data["delivery_method"] not in valid_methods:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid delivery method - must be one of: {', '.join(valid_methods)}"
                })
            
            # Validate delivery_status if provided
            if "delivery_status" in communication_data and communication_data["delivery_status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid delivery status - must be one of: {', '.join(valid_statuses)}"
                })
            
            # Validate sent_at is not empty if provided
            if "sent_at" in communication_data:
                if communication_data["sent_at"] is not None and str(communication_data["sent_at"]).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": "Field 'sent_at' cannot be empty if provided"
                    })

            # Get current communication record
            current_comm = communications[str(communication_id)]
            # Update communication record with modified information
            updated_comm = current_comm.copy()
            for key, value in communication_data.items():
                if key in ["incident_id", "problem_ticket_id", "recipient", "delivery_method", "sent_at"]:
                    updated_comm[key] = str(value) if value not in (None, "") else None
                else:
                    updated_comm[key] = value

            communications[str(communication_id)] = updated_comm
            
            return json.dumps({
                "success": True,
                "action": "update",
                "communication_id": str(communication_id),
                "message": f"Communication {communication_id} updated successfully",
                "communication_data": updated_comm
            })
        
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_communications",
                "description": "Create or update communication records for incident notifications in the incident management system. This tool manages all incident-related communications including status updates, resolution notices, escalation notifications, and bridge invitations. Handles multi-channel delivery (email, portal, SMS, phone) to various recipient types (client, internal, executive). Validates sender/recipient user existence, ensures proper communication types, tracks delivery status, and maintains communication audit trail. Either incident_id or problem_ticket_id must be provided, but not both.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to record new communication or 'update' to modify existing communication"
                        },
                        "communication_data": {
                            "type": "object",
                            "description": "Communication data object containing fields for creating or updating communications",
                            "properties": {
                                "incident_id": {
                                    "type": "string",
                                    "description": "Related incident identifier (required for create if problem_ticket_id is not provided, cannot be empty, must exist in system). Can be set to null for update if problem_ticket_id is provided."
                                },
                                "problem_ticket_id": {
                                    "type": "string",
                                    "description": "Related problem ticket identifier (required for create if incident_id is not provided, cannot be empty, must exist in system). Can be set to null for update if incident_id is provided."
                                },
                                "communication_type": {
                                    "type": "string",
                                    "description": "Type of communication (required for create). Must be one of: status_update, resolution_notice, escalation_notice, bridge_invitation, other"
                                },
                                "recipient_type": {
                                    "type": "string",
                                    "description": "Type of recipient (required for create). Must be one of: client, internal, executive"
                                },
                                "sender": {
                                    "type": "string",
                                    "description": "User identifier sending the communication (required for create, must be active user)"
                                },
                                "recipient": {
                                    "type": "string",
                                    "description": "Specific user identifier receiving the communication (optional, must be active user if provided). Can be set to null."
                                },
                                "delivery_method": {
                                    "type": "string",
                                    "description": "Method of delivery (required for create). Must be one of: email, portal, sms, phone"
                                },
                                "message_content": {
                                    "type": "string",
                                    "description": "Content of the communication message (required for create, cannot be empty)"
                                },
                                "sent_at": {
                                    "type": "string",
                                    "description": "Timestamp when communication was sent in YYYY-MM-DDTHH:MM:SS format (optional, cannot be empty if provided). Can be set to null."
                                },
                                "delivery_status": {
                                    "type": "string",
                                    "description": "Delivery status (optional, defaults to 'pending'). Must be one of: pending, sent, delivered, failed"
                                }
                            }
                        },
                        "communication_id": {
                            "type": "string",
                            "description": "Unique identifier of the communication. Required for update action only."
                        }
                    },
                    "required": ["action"]
                }
            }
        }