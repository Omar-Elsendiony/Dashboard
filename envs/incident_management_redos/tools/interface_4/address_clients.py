import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddressClients(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        client_data: Optional[Dict[str, Any]] = None,
        client_id: Optional[str] = None
    ) -> str:
        """
        Create or update client records.

        Actions:
        - create: Create a new client record (requires client_data)
        - update: Update an existing client record (requires client_id and client_data)
        """

        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "CLI1"
            max_id = 0
            for k in table.keys():
                try:
                    num = int(k[3:]) # Assuming format 'CLIX'
                    if num > max_id:
                        max_id = num
                except ValueError:
                    continue
            return f"CLI{max_id + 1}"

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

        clients = data.get("clients", {})
        # No 'users' needed for primary_contact_id validation as per this schema for clients table

        # Define valid enums based on DBML schema
        valid_company_types = ["enterprise", "mid_market", "smb", "startup"]
        valid_support_coverages = ["24x7", "business_hours", "on_call"]
        valid_preferred_communications = ["email", "portal", "phone", "slack"]
        valid_statuses = ["active", "inactive"]

        if action == "create":
            if not client_data:
                return json.dumps({
                    "success": False,
                    "error": "client_data is required for create action"
                })

            # Validate required fields as per DBML
            # client_name, company_type, support_coverage, preferred_communication are NOT NULL
            required_fields = ["client_name", "company_type", "support_coverage", "preferred_communication"]
            missing_fields = [field for field in required_fields if field not in client_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                })
            
            # Validate non-empty required fields
            for field in required_fields:
                if not client_data[field] or (isinstance(client_data[field], str) and str(client_data[field]).strip() == ""):
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })

            # Validate client_name uniqueness
            client_name = str(client_data["client_name"]).strip()
            for client in clients.values():
                if client["client_name"].lower() == client_name.lower():
                    return json.dumps({
                        "success": False,
                        "error": f"Client with name '{client_name}' already exists."
                    })

            # Validate registration_number uniqueness if provided
            registration_number = client_data.get("registration_number")
            if registration_number:
                registration_number = str(registration_number).strip()
                for client in clients.values():
                    if client.get("registration_number") and client["registration_number"].lower() == registration_number.lower():
                        return json.dumps({
                            "success": False,
                            "error": f"Client with registration number '{registration_number}' already exists."
                        })
            
            # Validate enums
            if client_data["company_type"] not in valid_company_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid company_type '{client_data['company_type']}'. Must be one of: {', '.join(valid_company_types)}"
                })
            if client_data["support_coverage"] not in valid_support_coverages:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid support_coverage '{client_data['support_coverage']}'. Must be one of: {', '.join(valid_support_coverages)}"
                })
            if client_data["preferred_communication"] not in valid_preferred_communications:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid preferred_communication '{client_data['preferred_communication']}'. Must be one of: {', '.join(valid_preferred_communications)}"
                })
            
            # Status is 'active' by default, if provided, must be valid
            status = client_data.get("status", "active")
            if status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}"
                })

            new_id = generate_id(clients)
            new_client = {
                "client_id": new_id,
                "client_name": client_name,
                "registration_number": registration_number if registration_number else None, # Nullable
                "company_type": client_data["company_type"],
                "primary_address": client_data.get("primary_address"), # Nullable
                "support_coverage": client_data["support_coverage"],
                "preferred_communication": client_data["preferred_communication"],
                "status": status,
                "created_at": timestamp,
                "updated_at": timestamp
            }
            clients[new_id] = new_client
            return json.dumps({
                "success": True,
                "action": "create",
                "client_id": new_id,
                "client_data": new_client
            })

        elif action == "update":
            if not client_id:
                return json.dumps({
                    "success": False,
                    "error": "client_id is required for update action"
                })
            client_id = str(client_id).strip().strip('"')
            if client_id not in clients:
                return json.dumps({
                    "success": False,
                    "error": f"Client '{client_id}' not found"
                })

            if not client_data:
                return json.dumps({
                    "success": False,
                    "error": "client_data is required for update action"
                })

            # Allowed fields for update
            allowed_fields = [
                "client_name", "registration_number", "company_type", "primary_address",
                "support_coverage", "preferred_communication", "status"
            ]
            invalid_fields = [field for field in client_data if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for update: {', '.join(invalid_fields)}"
                })
            
            # Validate non-empty fields (if provided, they shouldn't be empty strings, but nullable fields can be None)
            # Note: company_type, support_coverage, preferred_communication, status are NOT NULL, so cannot be empty string/None if provided for update
            nullable_fields = ["registration_number", "primary_address"]
            for field, value in client_data.items():
                if field not in nullable_fields and (value is None or (isinstance(value, str) and value.strip() == "")):
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })
                elif field in nullable_fields and (isinstance(value, str) and value.strip() == ""):
                    client_data[field] = None # Treat empty string as null for nullable fields

            # Validate client_name uniqueness if updated
            if "client_name" in client_data:
                updated_client_name = str(client_data["client_name"]).strip()
                for existing_client_id, client in clients.items():
                    if existing_client_id != client_id and client["client_name"].lower() == updated_client_name.lower():
                        return json.dumps({
                            "success": False,
                            "error": f"Client with name '{updated_client_name}' already exists."
                        })
                client_data["client_name"] = updated_client_name

            # Validate registration_number uniqueness if updated
            if "registration_number" in client_data and client_data["registration_number"] is not None:
                updated_reg_num = str(client_data["registration_number"]).strip()
                for existing_client_id, client in clients.items():
                    if existing_client_id != client_id and client.get("registration_number") and client["registration_number"].lower() == updated_reg_num.lower():
                        return json.dumps({
                            "success": False,
                            "error": f"Client with registration number '{updated_reg_num}' already exists."
                        })
                client_data["registration_number"] = updated_reg_num
            elif "registration_number" in client_data and client_data["registration_number"] is None:
                client_data["registration_number"] = None # Allow setting to null

            # Validate enums if provided
            if "company_type" in client_data and client_data["company_type"] not in valid_company_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid company_type '{client_data['company_type']}'. Must be one of: {', '.join(valid_company_types)}"
                })
            if "support_coverage" in client_data and client_data["support_coverage"] not in valid_support_coverages:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid support_coverage '{client_data['support_coverage']}'. Must be one of: {', '.join(valid_support_coverages)}"
                })
            if "preferred_communication" in client_data and client_data["preferred_communication"] not in valid_preferred_communications:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid preferred_communication '{client_data['preferred_communication']}'. Must be one of: {', '.join(valid_preferred_communications)}"
                })
            if "status" in client_data and client_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status '{client_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                })

            updated_client = clients[client_id].copy()
            for key, value in client_data.items():
                updated_client[key] = value
            updated_client["updated_at"] = timestamp
            clients[client_id] = updated_client
            return json.dumps({
                "success": True,
                "action": "update",
                "client_id": client_id,
                "client_data": updated_client
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "address_clients",
                "description": "Create or update client records in the system. This tool allows for managing client details, including their company type, support coverage, and communication preferences.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to add a new client, 'update' to modify an existing client."
                        },
                        "client_data": {
                            "type": "object",
                            "description": "Data object containing fields for creating or updating a client.",
                            "properties": {
                                "client_name": {
                                    "type": "string",
                                    "description": "The unique name of the client (required for create, must be unique, cannot be empty). Updatable."
                                },
                                "registration_number": {
                                    "type": "string",
                                    "description": "The client's unique registration number (optional, must be unique if provided). Updatable, can be set to null."
                                },
                                "company_type": {
                                    "type": "string",
                                    "description": "The type of company (required for create). Must be one of: enterprise, mid_market, smb, startup. Updatable.",
                                    "enum": ["enterprise", "mid_market", "smb", "startup"]
                                },
                                "primary_address": {
                                    "type": "string",
                                    "description": "The client's primary physical address (optional). Updatable, can be set to null."
                                },
                                "support_coverage": {
                                    "type": "string",
                                    "description": "The level of support coverage for the client (required for create). Must be one of: 24x7, business_hours, on_call. Updatable.",
                                    "enum": ["24x7", "business_hours", "on_call"]
                                },
                                "preferred_communication": {
                                    "type": "string",
                                    "description": "The client's preferred method of communication (required for create). Must be one of: email, portal, phone, slack. Updatable.",
                                    "enum": ["email", "portal", "phone", "slack"]
                                },
                                "status": {
                                    "type": "string",
                                    "description": "The operational status of the client (optional for create, defaults to 'active'). Must be one of: active, inactive. Updatable.",
                                    "enum": ["active", "inactive"]
                                }
                            }
                        },
                        "client_id": {
                            "type": "string",
                            "description": "The unique identifier of the client to update. Required for 'update' action only."
                        }
                    },
                    "required": ["action"]
                }
            }
        }