import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManageCommunications(Tool):
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
        users = data.get("users", {})

        # allowed enums
        valid_types = ["status_update", "resolution_notice", "escalation_notice", "bridge_invitation"]
        valid_recipient_types = ["client", "internal", "vendor", "executive"]
        valid_methods = ["email", "portal", "sms", "phone"]
        valid_statuses = ["pending", "sent", "delivered", "failed"]


        # for create action
        if action == "create":
            if not communication_data:
                return json.dumps({
                    "success": False,
                    "error": "communication_data is required for create action"
                })
            
            # Validate required fields
            required_fields = ["incident_id", "communication_type", "recipient_type", "sender", "delivery_method", "message_content"]
            
            missing_fields = [field for field in required_fields if field not in communication_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid communication details - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate incident exists
            if str(communication_data["incident_id"]) not in incidents:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Incident not found"
                })
            
            # Validate sender exists
            if str(communication_data["sender"]) not in users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Sender user not found"
                })
            
            # Validate recipient if provided
            if communication_data.get("recipient"):
                if str(communication_data["recipient"]) not in users:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Recipient user not found"
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
            
            # Validate delivery_method
            if communication_data["delivery_method"] not in valid_methods:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid delivery method - must be one of: {', '.join(valid_methods)}"
                })
            
            # Validate delivery_status
            delivery_status = communication_data.get("delivery_status", "pending")
            if delivery_status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid delivery status - must be one of: {', '.join(valid_statuses)}"
                })
            
            # Generate new communication ID
            new_comm_id = generate_id(communications)
            
            # Create new communication record
            new_comm = {
                "communication_id": str(new_comm_id),
                "incident_id": str(communication_data["incident_id"]),
                "communication_type": communication_data["communication_type"],
                "recipient_type": communication_data["recipient_type"],
                "sender": str(communication_data["sender"]),
                "recipient": str(communication_data["recipient"]) if communication_data.get("recipient") not in (None, "") else None,
                "delivery_method": communication_data["delivery_method"],
                "message_content": communication_data["message_content"],
                "delivery_status": delivery_status,
                "sent_at": communication_data.get("sent_at") or None,
                "created_at": "2025-10-07T00:00:00"
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
            update_fields = ["communication_type", "recipient_type", "recipient", "delivery_method", "message_content", "delivery_status"]
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
            
            # Validate recipient if provided
            if "recipient" in communication_data and str(communication_data["recipient"]) not in users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Recipient user not found"
                })
            
            # Get current communication record
            current_comm = communications[str(communication_id)]
            # Update communication record with modified information
            updated_comm = current_comm.copy()
            for key, value in communication_data.items():
                if key == "recipient":
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
                "name": "manage_communications",
                "description": "Create or update communication records for incident notifications in the incident management system. This tool manages all incident-related communications including status updates, resolution notices, escalation notifications, and bridge invitations. Handles multi-channel delivery (email, portal, SMS, phone) to various recipient types (client, internal, vendor, executive). Validates sender/recipient user existence, ensures proper communication types, tracks delivery status, and maintains communication audit trail. Essential for stakeholder management, SLA compliance, and maintaining transparency throughout incident lifecycle.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to record new communication or 'update' to modify existing communication",
                            "enum": ["create", "update"]
                        },
                        "communication_data": {
                            "type": "object",
                            "description": "Details of the communication to create or update",
                            "properties": {
                                "incident_id": {
                                    "type": "string",
                                    "description": "Related incident identifier (required for create)"
                                },
                                "communication_type": {
                                    "type": "string",
                                    "description": "Type of communication (required for create): status_update, resolution_notice, escalation_notice, bridge_invitation",
                                    "enum": ["status_update", "resolution_notice", "escalation_notice", "bridge_invitation"]
                                },
                                "recipient_type": {
                                    "type": "string",
                                    "description": "Type of recipient (required for create): client, internal, vendor, executive",
                                    "enum": ["client", "internal", "vendor", "executive"]
                                },
                                "sender": {
                                    "type": "string",
                                    "description": "User identifier sending the communication (required for create, must exist in system)"
                                },
                                "recipient": {
                                    "type": "string",
                                    "description": "Specific user identifier receiving the communication (optional, must exist if provided)"
                                },
                                "delivery_method": {
                                    "type": "string",
                                    "description": "Method of delivery (required for create): email, portal, sms, phone",
                                    "enum": ["email", "portal", "sms", "phone"]
                                },
                                "message_content": {
                                    "type": "string",
                                    "description": "Content of the communication message (required for create)"
                                },
                                "sent_at": {
                                    "type": "string",
                                    "description": "Timestamp when communication was sent in YYYY-MM-DDTHH:MM:SS format"
                                },
                                "delivery_status": {
                                    "type": "string",
                                    "description": "Delivery status (required for create): pending, sent, delivered, failed",
                                    "enum": ["pending", "sent", "delivered", "failed"]
                                }
                            }
                        },
                        "communication_id": {
                            "type": "string",
                            "description": "Unique identifier of the communication (provide this to update existing communication)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
