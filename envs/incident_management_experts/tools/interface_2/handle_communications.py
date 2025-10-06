import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class HandleCommunications(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, communication_data: Dict[str, Any] = None, communication_id: str = None) -> str:
        """
        Create or update communication records.

        Actions:
        - create: Create new communication (requires communication_data with incident_id, sender_id, recipient_type, communication_type)
        - update: Update existing communication (requires communication_id and communication_data with fields to change)
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

        communications = data.get("communications", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})

        # Allowed/enums
        valid_recipient_types = ["client", "internal_team", "executive", "vendor", "regulatory"]
        valid_communication_types = ["email", "sms", "phone_call", "status_page", "portal_update"]
        valid_delivery_statuses = ["sent", "delivered", "failed", "pending"]

        if action == "create":
            if not communication_data:
                return json.dumps({
                    "success": False,
                    "error": "communication_data is required for create action"
                })

            # Validate required fields for creation
            required_fields = ["incident_id", "sender_id", "recipient_type", "communication_type"]
            missing = [f for f in required_fields if f not in communication_data]
            if missing:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for communication creation: {', '.join(missing)}"
                })

            # # Approval: require at least one of the roles
            # if not (communication_data.get("incident_manager") or communication_data.get("technical_support") or communication_data.get("system_administrator") or communication_data.get("account_manager")):
            #     return json.dumps({
            #         "success": False,
            #         "error": "Missing approval for creating communication record. Required: incident_manager OR technical_support OR system_administrator OR account_manager"
            #     })
            
            # Only allow known fields to be supplied
            allowed_fields = [
                "incident_id", "sender_id", "recipient_id", "recipient_type",
                "communication_type", "delivery_status", "sent_at"
            ]
            invalid_fields = [k for k in communication_data.keys() if k not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for communication creation: {', '.join(invalid_fields)}"
                })

            incident_id = str(communication_data["incident_id"])
            sender_id = str(communication_data["sender_id"])
            recipient_id = communication_data.get("recipient_id")
            recipient_type = communication_data["recipient_type"]
            communication_type = communication_data["communication_type"]
            delivery_status = communication_data.get("delivery_status")
            sent_at = communication_data.get("sent_at")

            # Validate incident exists
            if incident_id not in incidents:
                return json.dumps({
                    "success": False,
                    "error": f"Incident {incident_id} not found"
                })

            # Validate sender exists and is active
            if sender_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"Sender {sender_id} not found"
                })
            if users[sender_id].get("status") != "active":
                return json.dumps({
                    "success": False,
                    "error": f"Sender {sender_id} is not active"
                })

            # Validate recipient if specified
            if recipient_id and str(recipient_id) not in users:
                return json.dumps({
                    "success": False,
                    "error": f"Recipient {recipient_id} not found"
                })

            # Validate enums
            if recipient_type not in valid_recipient_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid recipient_type. Must be one of: {', '.join(valid_recipient_types)}"
                })

            if communication_type not in valid_communication_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid communication_type. Must be one of: {', '.join(valid_communication_types)}"
                })

            if delivery_status and delivery_status not in valid_delivery_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid delivery_status. Must be one of: {', '.join(valid_delivery_statuses)}"
                })

            # Generate ID and create record
            new_id = generate_id(communications)
            new_comm = {
                "communication_id": str(new_id),
                "incident_id": incident_id,
                "sender_id": sender_id,
                "recipient_id": str(recipient_id) if recipient_id is not None else None,
                "recipient_type": recipient_type,
                "communication_type": communication_type,
                "sent_at": sent_at if sent_at else "2025-10-02T12:00:00",
                "delivery_status": delivery_status if delivery_status else "pending",
                "created_at": "2025-10-02T12:00:00",
                "updated_at": "2025-10-02T12:00:00"
            }

            communications[str(new_id)] = new_comm

            return json.dumps({
                "success": True,
                "action": "create",
                "communication_id": str(new_id),
                "message": f"Communication {new_id} created successfully",
                "communication_data": new_comm
            })

        elif action == "update":
            if not communication_id:
                return json.dumps({
                    "success": False,
                    "error": "communication_id is required for update action"
                })

            if communication_id not in communications:
                return json.dumps({
                    "success": False,
                    "error": f"Communication {communication_id} not found"
                })

            if not communication_data:
                return json.dumps({
                    "success": False,
                    "error": "communication_data is required for update action"
                })

            # # Approval required for updates as well
            # if not (communication_data.get("incident_manager") or communication_data.get("technical_support") or communication_data.get("system_administrator") or communication_data.get("account_manager")):
            #     return json.dumps({
            #         "success": False,
            #         "error": "Missing approval for creating communication record. Required: incident_manager OR technical_support OR system_administrator OR account_manager"
            #     })

            # Only allow known update fields
            allowed_update_fields = [
                "incident_id", "sender_id", "recipient_id", "recipient_type",
                "communication_type", "delivery_status", "sent_at"
            ]
            invalid_fields = [k for k in communication_data.keys() if k not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for communication update: {', '.join(invalid_fields)}"
                })

            # At least one valid field must be present
            if not any(field in communication_data for field in allowed_update_fields):
                return json.dumps({
                    "success": False,
                    "error": "At least one updatable field must be provided in communication_data"
                })

            current_comm = communications[communication_id].copy()

            # Validate fields when present
            if "incident_id" in communication_data:
                incident_id = str(communication_data["incident_id"])
                if incident_id not in incidents:
                    return json.dumps({
                        "success": False,
                        "error": f"Incident {incident_id} not found"
                    })
                current_comm["incident_id"] = incident_id

            if "sender_id" in communication_data:
                sender_id = str(communication_data["sender_id"])
                if sender_id not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"Sender {sender_id} not found"
                    })
                if users[sender_id].get("status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": f"Sender {sender_id} is not active"
                    })
                current_comm["sender_id"] = sender_id

            if "recipient_id" in communication_data:
                recipient_id = communication_data["recipient_id"]
                if recipient_id and str(recipient_id) not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"Recipient {recipient_id} not found"
                    })
                current_comm["recipient_id"] = str(recipient_id) if recipient_id is not None else None

            if "recipient_type" in communication_data:
                recipient_type = communication_data["recipient_type"]
                if recipient_type not in valid_recipient_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid recipient_type. Must be one of: {', '.join(valid_recipient_types)}"
                    })
                current_comm["recipient_type"] = recipient_type

            if "communication_type" in communication_data:
                communication_type = communication_data["communication_type"]
                if communication_type not in valid_communication_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid communication_type. Must be one of: {', '.join(valid_communication_types)}"
                    })
                current_comm["communication_type"] = communication_type

            if "delivery_status" in communication_data:
                delivery_status = communication_data["delivery_status"]
                if delivery_status not in valid_delivery_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid delivery_status. Must be one of: {', '.join(valid_delivery_statuses)}"
                    })
                current_comm["delivery_status"] = delivery_status

            if "sent_at" in communication_data:
                current_comm["sent_at"] = communication_data["sent_at"]

            current_comm["updated_at"] = "2025-10-02T12:00:00"
            communications[communication_id] = current_comm

            return json.dumps({
                "success": True,
                "action": "update",
                "communication_id": str(communication_id),
                "message": f"Communication {communication_id} updated successfully",
                "communication_data": current_comm
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_communications",
                "description": "Create or update communication records in the incident management system. Tracks emails, SMS, phone calls, status page updates, and portal updates sent to stakeholders. Requires approval from incident managers, technical support, system administrators, or account managers.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new communication record, 'update' to modify existing record",
                            "enum": ["create", "update"]
                        },
                        "communication_data": {
                            "type": "object",
                            "description": "Communication data object. requires incident_id (incident ID), sender_id (sender ID), recipient_type (client/internal_team/executive/vendor/regulatory), communication_type (email/sms/phone_call/status_page/portal_update). For update: include communication fields to change. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "incident_id": {"type": "string", "description": "ID of associated incident (required for create)"},
                                "sender_id": {"type": "string", "description": "ID of user sending the communication (required for create)"},
                                "recipient_id": {"type": "string", "description": "ID of the recipient user (optional)"},
                                "recipient_type": {
                                    "type": "string",
                                    "description": "Type of recipient (required for create)",
                                    "enum": ["client", "internal_team", "executive", "vendor", "regulatory"]
                                },
                                "communication_type": {
                                    "type": "string",
                                    "description": "Channel used for communication (required for create)",
                                    "enum": ["email", "sms", "phone_call", "status_page", "portal_update"]
                                },
                                "delivery_status": {
                                    "type": "string",
                                    "description": "Delivery status (optional)",
                                    "enum": ["sent", "delivered", "failed", "pending"]
                                },
                                "sent_at": {
                                    "type": "string",
                                    "description": "Timestamp when communication was sent (optional) in YYYY-MM-DDTHH:MM:SS"
                                }
                            }
                        },
                        "communication_id": {
                            "type": "string",
                            "description": "Unique identifier of the communication record (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
