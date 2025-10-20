import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class HandleAssets(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        entity_type: str,
        entity_data: Optional[Dict[str, Any]] = None,
        entity_id: Optional[str] = None
    ) -> str:
        """
        Create or update asset records (configuration items or CI-client assignments).

        Actions:
        - create: Create a new record (requires entity_type and entity_data)
        - update: Update an existing record (requires entity_type, entity_id, and entity_data)

        Entity Types:
        - configuration_items: Manages individual configuration items.
        - ci_client_assignments: Manages the assignment of configuration items to clients.
        """

        def generate_id(table: Dict[str, Any], prefix: str = "") -> str:
            if not table:
                return f"{prefix}1"
            max_id_num = 0
            for k in table.keys():
                try:
                    # Extract numeric part, handling potential non-numeric keys gracefully
                    if k.startswith(prefix):
                        num_part = int(k[len(prefix):])
                        if num_part > max_id_num:
                            max_id_num = num_part
                except ValueError:
                    continue # Ignore keys that don't match the expected format
            return f"{prefix}{max_id_num + 1}"

        timestamp = "2025-10-07T12:00:00"

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

        if entity_type not in ["configuration_items", "ci_client_assignments"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'configuration_items' or 'ci_client_assignments'"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        config_items = data.get("configuration_items", {})
        ci_client_assignments = data.get("ci_client_assignments", {})
        users = data.get("users", {}) # For responsible_owner validation
        clients = data.get("clients", {}) # For client_id validation

        # Define valid enums based on DBML schema
        valid_ci_types = ["server", "application", "database", "network", "storage", "service"]
        valid_environments = ["production", "staging", "development", "testing"]
        valid_operational_statuses = ["operational", "degraded", "down"]

        if action == "create":
            if not entity_data:
                return json.dumps({
                    "success": False,
                    "error": "entity_data is required for create action"
                })

            if entity_type == "configuration_items":
                required_fields = ["ci_name", "ci_type", "environment", "operational_status", "responsible_owner"]
                for field in required_fields:
                    if field not in entity_data or not entity_data[field] or str(entity_data[field]).strip() == "":
                        return json.dumps({
                            "success": False,
                            "error": f"Missing or empty required field for configuration_items: '{field}'"
                        })

                # Validate enums
                if entity_data["ci_type"] not in valid_ci_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid ci_type '{entity_data['ci_type']}'. Must be one of: {', '.join(valid_ci_types)}"
                    })
                if entity_data["environment"] not in valid_environments:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid environment '{entity_data['environment']}'. Must be one of: {', '.join(valid_environments)}"
                    })
                if entity_data["operational_status"] not in valid_operational_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid operational_status '{entity_data['operational_status']}'. Must be one of: {', '.join(valid_operational_statuses)}"
                    })

                # Validate responsible_owner exists and is active
                responsible_owner = str(entity_data["responsible_owner"]).strip().strip('"')
                if responsible_owner not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"Responsible owner user '{responsible_owner}' not found"
                    })
                if users[responsible_owner]["status"] != "active":
                    return json.dumps({
                        "success": False,
                        "error": f"Responsible owner user '{responsible_owner}' is not active"
                    })

                # Check for unique ci_name
                for ci in config_items.values():
                    if ci["ci_name"] == entity_data["ci_name"]:
                        return json.dumps({
                            "success": False,
                            "error": f"Configuration item with name '{entity_data['ci_name']}' already exists."
                        })

                new_id = generate_id(config_items, "CI")
                new_ci = {
                    "ci_id": new_id,
                    "ci_name": entity_data["ci_name"],
                    "ci_type": entity_data["ci_type"],
                    "environment": entity_data["environment"],
                    "operational_status": entity_data["operational_status"],
                    "responsible_owner": responsible_owner,
                    "created_at": timestamp,
                    "updated_at": timestamp
                }
                config_items[new_id] = new_ci
                return json.dumps({
                    "success": True,
                    "action": "create",
                    "entity_type": entity_type,
                    "ci_id": new_id,
                    "ci_data": new_ci
                })

            elif entity_type == "ci_client_assignments":
                required_fields = ["ci_id", "client_id"]
                for field in required_fields:
                    if field not in entity_data or not entity_data[field] or str(entity_data[field]).strip() == "":
                        return json.dumps({
                            "success": False,
                            "error": f"Missing or empty required field for ci_client_assignments: '{field}'"
                        })

                # Validate ci_id and client_id exist
                ci_id = str(entity_data["ci_id"]).strip().strip('"')
                client_id = str(entity_data["client_id"]).strip().strip('"')

                if ci_id not in config_items:
                    return json.dumps({
                        "success": False,
                        "error": f"Configuration item '{ci_id}' not found."
                    })
                if client_id not in clients:
                    return json.dumps({
                        "success": False,
                        "error": f"Client '{client_id}' not found."
                    })

                # Check for unique assignment (ci_id, client_id)
                for assignment in ci_client_assignments.values():
                    if assignment["ci_id"] == ci_id and assignment["client_id"] == client_id:
                        return json.dumps({
                            "success": False,
                            "error": f"Assignment for CI '{ci_id}' to client '{client_id}' already exists."
                        })

                new_id = generate_id(ci_client_assignments, "ASSIGN")
                new_assignment = {
                    "assignment_id": new_id,
                    "ci_id": ci_id,
                    "client_id": client_id,
                    "created_at": timestamp
                }
                ci_client_assignments[new_id] = new_assignment
                return json.dumps({
                    "success": True,
                    "action": "create",
                    "entity_type": entity_type,
                    "assignment_id": new_id,
                    "assignment_data": new_assignment
                })

        elif action == "update":
            if not entity_id:
                return json.dumps({
                    "success": False,
                    "error": "entity_id is required for update action"
                })
            if not entity_data:
                return json.dumps({
                    "success": False,
                    "error": "entity_data is required for update action"
                })

            entity_id = str(entity_id).strip().strip('"')

            if entity_type == "configuration_items":
                if entity_id not in config_items:
                    return json.dumps({
                        "success": False,
                        "error": f"Configuration item '{entity_id}' not found."
                    })

                # Validate allowed fields for update
                allowed_fields = ["ci_name", "ci_type", "environment", "operational_status", "responsible_owner"]
                invalid_fields = [field for field in entity_data if field not in allowed_fields]
                if invalid_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid fields for configuration_items update: {', '.join(invalid_fields)}"
                    })

                # Validate non-empty fields
                for field, value in entity_data.items():
                    if value is None or (isinstance(value, str) and value.strip() == ""):
                        return json.dumps({
                            "success": False,
                            "error": f"Field '{field}' cannot be empty"
                        })

                # Validate enums if provided
                if "ci_type" in entity_data and entity_data["ci_type"] not in valid_ci_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid ci_type '{entity_data['ci_type']}'. Must be one of: {', '.join(valid_ci_types)}"
                    })
                if "environment" in entity_data and entity_data["environment"] not in valid_environments:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid environment '{entity_data['environment']}'. Must be one of: {', '.join(valid_environments)}"
                    })
                if "operational_status" in entity_data and entity_data["operational_status"] not in valid_operational_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid operational_status '{entity_data['operational_status']}'. Must be one of: {', '.join(valid_operational_statuses)}"
                    })

                # Validate responsible_owner if provided
                if "responsible_owner" in entity_data:
                    responsible_owner = str(entity_data["responsible_owner"]).strip().strip('"')
                    if responsible_owner not in users:
                        return json.dumps({
                            "success": False,
                            "error": f"Responsible owner user '{responsible_owner}' not found"
                        })
                    if users[responsible_owner]["status"] != "active":
                        return json.dumps({
                            "success": False,
                            "error": f"Responsible owner user '{responsible_owner}' is not active"
                        })
                    entity_data["responsible_owner"] = responsible_owner

                # Check for unique ci_name if updated
                if "ci_name" in entity_data:
                    for ci_id_key, ci in config_items.items():
                        if ci_id_key != entity_id and ci["ci_name"] == entity_data["ci_name"]:
                            return json.dumps({
                                "success": False,
                                "error": f"Configuration item with name '{entity_data['ci_name']}' already exists."
                            })

                updated_ci = config_items[entity_id].copy()
                for key, value in entity_data.items():
                    updated_ci[key] = value
                updated_ci["updated_at"] = timestamp
                config_items[entity_id] = updated_ci
                return json.dumps({
                    "success": True,
                    "action": "update",
                    "entity_type": entity_type,
                    "ci_id": entity_id,
                    "ci_data": updated_ci
                })

            elif entity_type == "ci_client_assignments":
                if entity_id not in ci_client_assignments:
                    return json.dumps({
                        "success": False,
                        "error": f"CI-Client assignment '{entity_id}' not found."
                    })

                # Based on the DBML schema, ci_id and client_id are not directly updatable via assignment_id.
                # Assignments are typically immutable; if changes are needed, the old assignment is deleted,
                # and a new one is created.
                return json.dumps({
                    "success": False,
                    "error": "CI-Client assignments are generally immutable. Please delete and re-create if changes are needed."
                })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_assets",
                "description": "Create or update asset records. This includes managing configuration items (CIs) and their assignments to clients. Use 'configuration_items' for individual asset details and 'ci_client_assignments' for linking CIs to clients.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new record, 'update' to modify existing record"
                        },
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to manage. Must be 'configuration_items' or 'ci_client_assignments'.",
                            "enum": ["configuration_items", "ci_client_assignments"]
                        },
                        "entity_data": {
                            "type": "object",
                            "description": "Data object containing fields for creating or updating the specified entity_type. The required fields vary based on 'entity_type' and 'action'.",
                            "properties": {
                                # Properties relevant for 'configuration_items'
                                "ci_name": {
                                    "type": "string",
                                    "description": "Name of the Configuration Item (required for creating 'configuration_items', must be unique, cannot be empty). Updatable."
                                },
                                "ci_type": {
                                    "type": "string",
                                    "description": "Type of the Configuration Item (required for creating 'configuration_items'). Must be one of: server, application, database, network, storage, service. Updatable.",
                                    "enum": ["server", "application", "database", "network", "storage", "service"]
                                },
                                "environment": {
                                    "type": "string",
                                    "description": "Environment where the CI is deployed (required for creating 'configuration_items'). Must be one of: production, staging, development, testing. Updatable.",
                                    "enum": ["production", "staging", "development", "testing"]
                                },
                                "operational_status": {
                                    "type": "string",
                                    "description": "Operational status of the CI (required for creating 'configuration_items'). Must be one of: operational, degraded, down. Updatable.",
                                    "enum": ["operational", "degraded", "down"]
                                },
                                "responsible_owner": {
                                    "type": "string",
                                    "description": "User ID of the responsible owner for the CI (required for creating 'configuration_items', must be an active user). Updatable."
                                },
                                # Properties relevant for 'ci_client_assignments'
                                "ci_id": {
                                    "type": "string",
                                    "description": "ID of the Configuration Item to assign (required for creating 'ci_client_assignments', must exist). Not updatable for existing assignments."
                                },
                                "client_id": {
                                    "type": "string",
                                    "description": "ID of the Client to assign the CI to (required for creating 'ci_client_assignments', must exist). Not updatable for existing assignments."
                                }
                            }
                        },
                        "entity_id": {
                            "type": "string",
                            "description": "Unique identifier of the entity to update. Required for 'update' action only. For 'configuration_items', this is 'ci_id'. For 'ci_client_assignments', this is 'assignment_id'."
                        }
                    },
                    "required": ["action", "entity_type"]
                }
            }
        }