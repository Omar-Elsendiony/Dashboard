import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ManageClients(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, client_data: Dict[str, Any] = None, client_id: str = None) -> str:
        """
        Create or update client records.

        Actions:
        - create: Create new client (requires client_data with client_name, client_type, country)
        - update: Update existing client (requires client_id and client_data with fields to change)
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
                "error": "Invalid data format for clients"
            })

        clients = data.get("clients", {})

        valid_client_types = ["enterprise", "mid_market", "small_business", "startup"]
        valid_statuses = ["active", "inactive", "suspended"]

        if action == "create":
            if not client_data:
                return json.dumps({
                    "success": False,
                    "error": "client_data is required for create action"
                })

            # Required fields
            required_fields = ["client_name", "client_type", "country"]
            missing = [f for f in required_fields if f not in client_data or not client_data.get(f)]
            if missing:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for client creation: {', '.join(missing)}"
                })

            client_name = client_data["client_name"]
            client_type = client_data["client_type"]
            country = client_data["country"]
            registration_number = client_data.get("registration_number")
            contact_email = client_data.get("contact_email")
            industry = client_data.get("industry")
            status = client_data.get("status", "active")

            # Validate client_type
            if client_type not in valid_client_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid client_type. Must be one of: {', '.join(valid_client_types)}"
                })

            # Validate status
            if status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })

            # Check uniqueness of client_name
            for existing_client in clients.values():
                if existing_client.get("client_name") == client_name:
                    return json.dumps({
                        "success": False,
                        "error": f"Client name '{client_name}' already exists"
                    })

            # Check uniqueness of registration_number if provided
            if registration_number:
                for existing_client in clients.values():
                    if existing_client.get("registration_number") == registration_number:
                        return json.dumps({
                            "success": False,
                            "error": f"Registration number '{registration_number}' already exists"
                        })

            # Create client
            new_id = generate_id(clients)
            new_client = {
                "client_id": str(new_id),
                "client_name": client_name,
                "client_type": client_type,
                "country": country,
                "status": status,
                "created_at": "2025-10-04T12:00:00",
                "updated_at": "2025-10-04T12:00:00"
            }

            if registration_number:
                new_client["registration_number"] = registration_number
            if contact_email:
                new_client["contact_email"] = contact_email
            if industry:
                new_client["industry"] = industry

            clients[str(new_id)] = new_client

            return json.dumps({
                "success": True,
                "action": "create",
                "client_id": str(new_id),
                "message": f"Client {new_id} created successfully",
                "client_data": new_client
            })

        elif action == "update":
            if not client_id:
                return json.dumps({
                    "success": False,
                    "error": "client_id is required for update action"
                })

            if client_id not in clients:
                return json.dumps({
                    "success": False,
                    "error": f"Client {client_id} not found"
                })

            if not client_data:
                return json.dumps({
                    "success": False,
                    "error": "client_data is required for update action"
                })

            current_client = clients[client_id].copy()

            # Validate and update client_type
            if "client_type" in client_data:
                ct = client_data["client_type"]
                if ct not in valid_client_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid client_type. Must be one of: {', '.join(valid_client_types)}"
                    })
                current_client["client_type"] = ct

            # Validate and update status
            if "status" in client_data:
                st = client_data["status"]
                if st not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
                current_client["status"] = st

            # Check uniqueness of client_name if updating
            if "client_name" in client_data:
                new_name = client_data["client_name"]
                for cid, existing_client in clients.items():
                    if cid != client_id and existing_client.get("client_name") == new_name:
                        return json.dumps({
                            "success": False,
                            "error": f"Client name '{new_name}' already exists"
                        })
                current_client["client_name"] = new_name

            # Check uniqueness of registration_number if updating
            if "registration_number" in client_data:
                new_reg = client_data["registration_number"]
                for cid, existing_client in clients.items():
                    if cid != client_id and existing_client.get("registration_number") == new_reg:
                        return json.dumps({
                            "success": False,
                            "error": f"Registration number '{new_reg}' already exists"
                        })
                current_client["registration_number"] = new_reg

            # Update other fields
            for field in ["contact_email", "industry", "country"]:
                if field in client_data:
                    current_client[field] = client_data[field]

            current_client["updated_at"] = "2025-10-04T12:00:00"
            clients[client_id] = current_client

            return json.dumps({
                "success": True,
                "action": "update",
                "client_id": client_id,
                "message": f"Client {client_id} updated successfully",
                "client_data": current_client
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_clients",
                "description": "Create or update client records in the incident management system. Validates uniqueness of client names and registration numbers. Supports enterprise, mid-market, small business, and startup client types.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' or 'update'",
                            "enum": ["create", "update"]
                        },
                        "client_data": {
                            "type": "object",
                            "description": "Client data object. For create: requires client_name, client_type, country. For update: include fields to modify. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "client_name": {"type": "string", "description": "Name of the client (required for create)"},
                                "client_type": {
                                    "type": "string",
                                    "description": "Type of client (required for create)",
                                    "enum": ["enterprise", "mid_market", "small_business", "startup"]
                                },
                                "country": {"type": "string", "description": "Client's country (required for create)"},
                                "registration_number": {"type": "string", "description": "Registration number (optional)"},
                                "contact_email": {"type": "string", "description": "Contact email (optional)"},
                                "industry": {"type": "string", "description": "Industry (optional)"},
                                "status": {
                                    "type": "string",
                                    "description": "Client status (optional)",
                                    "enum": ["active", "inactive", "suspended"]
                                }
                            }
                        },
                        "client_id": {"type": "string", "description": "Unique identifier of the client (required for update action only)"}
                    },
                    "required": ["action"]
                }
            }
        }
