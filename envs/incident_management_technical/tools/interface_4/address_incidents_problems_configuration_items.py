import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class AddressIncidentsProblemsConfigurationItems(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        entity_type: str,
        association_data: Optional[Dict[str, Any]] = None,
        association_id: Optional[str] = None
    ) -> str:
        """
        Create or update incident-CI and problem-CI association records.

        Actions:
        - create: Create a new association record (requires entity_type and association_data)
        - update: Update an existing association record (requires entity_type, association_id and association_data)
        
        Entity Types:
        - incident_ci: For incident_configuration_items associations
        - problem_ci: For problem_configuration_items associations
        """

        def generate_id(table: Dict[str, Any], prefix: str) -> str:
            if not table:
                return f"{prefix}1"
            max_id = 0
            for k in table.keys():
                try:
                    num = int(k[len(prefix):])
                    if num > max_id:
                        max_id = num
                except ValueError:
                    continue
            return f"{prefix}{max_id + 1}"

        timestamp = "2025-10-07T12:00:00"

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

        if entity_type not in ["incident_ci", "problem_ci"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'incident_ci' or 'problem_ci'"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        configuration_items = data.get("configuration_items", {})

        if entity_type == "incident_ci":
            associations = data.get("incident_configuration_items", {})
            incidents = data.get("incidents", {})
            parent_key = "incident_id"
            parent_table = incidents
            parent_name = "Incident"
            id_field = "incident_ci_id"
            prefix = ""
        else:  # problem_ci
            associations = data.get("problem_configuration_items", {})
            problem_tickets = data.get("problem_tickets", {})
            parent_key = "problem_id"
            parent_table = problem_tickets
            parent_name = "Problem"
            id_field = "problem_ci_id"
            prefix = ""

        if action == "create":
            if not association_data:
                return json.dumps({
                    "success": False,
                    "error": "association_data is required for create action"
                })

            # Validate required fields
            required_fields = [parent_key, "ci_id"]
            missing_fields = [field for field in required_fields if field not in association_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                })
            
            # Validate non-empty required fields
            for field in required_fields:
                if not association_data[field] or (isinstance(association_data[field], str) and str(association_data[field]).strip() == ""):
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })

            # Validate parent FK (incident_id or problem_id)
            parent_id = str(association_data[parent_key]).strip().strip('"')
            if parent_id not in parent_table:
                return json.dumps({
                    "success": False,
                    "error": f"{parent_name} '{parent_id}' not found"
                })

            # Validate ci_id FK
            ci_id = str(association_data["ci_id"]).strip().strip('"')
            if ci_id not in configuration_items:
                return json.dumps({
                    "success": False,
                    "error": f"Configuration item '{ci_id}' not found"
                })

            # Check for duplicate association (unique constraint on parent_id + ci_id)
            for assoc in associations.values():
                if assoc[parent_key] == parent_id and assoc["ci_id"] == ci_id:
                    return json.dumps({
                        "success": False,
                        "error": f"Association between {parent_name.lower()} '{parent_id}' and CI '{ci_id}' already exists"
                    })

            new_id = generate_id(associations, prefix)
            new_association = {
                id_field: new_id,
                parent_key: parent_id,
                "ci_id": ci_id,
                "created_at": timestamp
            }
            associations[new_id] = new_association
            return json.dumps({
                "success": True,
                "action": "create",
                "association_id": new_id,
                "association_data": new_association
            })

        elif action == "update":
            if not association_id:
                return json.dumps({
                    "success": False,
                    "error": "association_id is required for update action"
                })
            association_id = str(association_id).strip().strip('"')
            if association_id not in associations:
                return json.dumps({
                    "success": False,
                    "error": f"Association '{association_id}' not found"
                })

            if not association_data:
                return json.dumps({
                    "success": False,
                    "error": "association_data is required for update action"
                })

            # Allowed fields for update (only parent_id and ci_id can be updated)
            allowed_fields = [parent_key, "ci_id"]
            invalid_fields = [field for field in association_data if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for update: {', '.join(invalid_fields)}"
                })
            
            # Validate non-empty fields
            for field, value in association_data.items():
                if value is None or (isinstance(value, str) and str(value).strip() == ""):
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })

            # Validate parent FK if provided
            if parent_key in association_data:
                parent_id = str(association_data[parent_key]).strip().strip('"')
                if parent_id not in parent_table:
                    return json.dumps({
                        "success": False,
                        "error": f"{parent_name} '{parent_id}' not found"
                    })
                association_data[parent_key] = parent_id

            # Validate ci_id FK if provided
            if "ci_id" in association_data:
                ci_id = str(association_data["ci_id"]).strip().strip('"')
                if ci_id not in configuration_items:
                    return json.dumps({
                        "success": False,
                        "error": f"Configuration item '{ci_id}' not found"
                    })
                association_data["ci_id"] = ci_id

            # Check for duplicate association if updating
            updated_parent_id = association_data.get(parent_key, associations[association_id][parent_key])
            updated_ci_id = association_data.get("ci_id", associations[association_id]["ci_id"])
            
            for existing_id, assoc in associations.items():
                if existing_id != association_id and assoc[parent_key] == updated_parent_id and assoc["ci_id"] == updated_ci_id:
                    return json.dumps({
                        "success": False,
                        "error": f"Association between {parent_name.lower()} '{updated_parent_id}' and CI '{updated_ci_id}' already exists"
                    })

            updated_association = associations[association_id].copy()
            for key, value in association_data.items():
                updated_association[key] = value
            
            associations[association_id] = updated_association
            return json.dumps({
                "success": True,
                "action": "update",
                "association_id": association_id,
                "association_data": updated_association
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "address_incidents_problems_configuration_items",
                "description": "Create or update associations between incidents/problems and configuration items. Links incidents or problems to the CIs they affect or are related to. Enforces unique constraints to prevent duplicate associations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to add a new association, 'update' to modify an existing association."
                        },
                        "entity_type": {
                            "type": "string",
                            "description": "Type of association to manage: 'incident_ci' for incident-CI associations, 'problem_ci' for problem-CI associations.",
                            "enum": ["incident_ci", "problem_ci"]
                        },
                        "association_data": {
                            "type": "object",
                            "description": "Data object containing fields for creating or updating an association.",
                            "properties": {
                                "incident_id": {
                                    "type": "string",
                                    "description": "The ID of the incident (required for create when entity_type is 'incident_ci', cannot be empty). Must refer to an existing incident. Updatable."
                                },
                                "problem_id": {
                                    "type": "string",
                                    "description": "The ID of the problem (required for create when entity_type is 'problem_ci', cannot be empty). Must refer to an existing problem. Updatable."
                                },
                                "ci_id": {
                                    "type": "string",
                                    "description": "The ID of the configuration item (required for create, cannot be empty). Must refer to an existing CI. Updatable."
                                }
                            }
                        },
                        "association_id": {
                            "type": "string",
                            "description": "The unique identifier of the association to update. Required for 'update' action only."
                        }
                    },
                    "required": ["action", "entity_type"]
                }
            }
        }