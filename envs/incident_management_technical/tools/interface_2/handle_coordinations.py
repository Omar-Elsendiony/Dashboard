import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class HandleCoordinations(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        entity_type: str,
        action: str,
        bridge_data: Optional[Dict[str, Any]] = None,
        bridge_id: Optional[str] = None,
        participant_data: Optional[Dict[str, Any]] = None,
        participant_id: Optional[str] = None
    ) -> str:
        """
        Create or update bridge records and bridge participant assignments.

        Entity Types:
        - bridge: Manage incident bridge records
        - bridge_participant: Manage bridge participant assignments

        Actions:
        - create: Create a new record (requires bridge_data or participant_data)
        - update: Update an existing record (requires bridge_id/participant_id and corresponding data)
        """

        def generate_id(table: Dict[str, Any], prefix: str) -> str:
            if not table:
                return 1
            return str(max(int(k) for k in table.keys()) + 1)

        def generate_bridge_number(table: Dict[str, Any]) -> str:
            if not table:
                return "BRG0000001"
            max_num = 0
            for bridge in table.values():
                bridge_num = bridge.get("bridge_number", "")
                if bridge_num.startswith("BRG"):
                    try:
                        num = int(bridge_num[3:])
                        if num > max_num:
                            max_num = num
                    except ValueError:
                        continue
            return f"BRG{max_num + 1:07d}"

        timestamp = "2025-10-07T12:00:00"

        # Validate entity_type and action
        if entity_type not in ["bridge", "bridge_participant"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'bridge' or 'bridge_participant'"
            })

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

        bridges = data.get("bridges", {})
        bridge_participants = data.get("bridge_participants", {})
        users = data.get("users", {})
        incidents = data.get("incidents", {})

        # Define valid enums based on DBML schema
        valid_bridge_types = ["major_incident", "coordination", "technical"]
        valid_bridge_statuses = ["active", "closed"]
        valid_participant_roles = ["host", "technical_support", "account_manager", "executive"]

        # ============================================================================
        # BRIDGE HANDLEMENT
        # ============================================================================
        if entity_type == "bridge":
            if action == "create":
                if not bridge_data:
                    return json.dumps({
                        "success": False,
                        "error": "bridge_data is required for create action"
                    })

                # Validate required fields
                required_fields = ["incident_id", "bridge_type", "bridge_host"]
                missing_fields = [field for field in required_fields if field not in bridge_data]
                if missing_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Missing required fields: {', '.join(missing_fields)}"
                    })
                
                # Validate non-empty required fields
                for field in required_fields:
                    if not bridge_data[field] or (isinstance(bridge_data[field], str) and bridge_data[field].strip() == ""):
                        return json.dumps({
                            "success": False,
                            "error": f"Field '{field}' cannot be empty"
                        })
                    
                # Validate non-empty start_time, end_time if provided
                optional_fields = ["start_time", "end_time"]
                for field in optional_fields:
                    if field in bridge_data:
                        if not bridge_data[field] or (isinstance(bridge_data[field], str) and bridge_data[field].strip() == ""):
                            return json.dumps({
                                "success": False,
                                "error": f"Field '{field}' cannot be empty"
                            })

                # Validate bridge_type enum
                if bridge_data["bridge_type"] not in valid_bridge_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid bridge_type '{bridge_data['bridge_type']}'. Must be one of: {', '.join(valid_bridge_types)}"
                    })

                # Validate incident exists
                incident_id = str(bridge_data["incident_id"]).strip().strip('"')
                if incident_id not in incidents:
                    return json.dumps({
                        "success": False,
                        "error": f"Incident '{incident_id}' not found"
                    })
                
                # Validate incident status (must be open or in_progress)
                incident_status = incidents[incident_id].get("status")
                if incident_status not in ["open", "in_progress"]:
                    return json.dumps({
                        "success": False,
                        "error": f"Incident '{incident_id}' has invalid status '{incident_status}' for bridge creation. Must be 'open' or 'in_progress'"
                    })

                # Validate bridge_host user exists and is active
                bridge_host = str(bridge_data["bridge_host"]).strip().strip('"')
                if bridge_host not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"Bridge host user '{bridge_host}' not found"
                    })
                if users[bridge_host]["status"] != "active":
                    return json.dumps({
                        "success": False,
                        "error": f"Bridge host user '{bridge_host}' is not active"
                    })

                # Status defaults to 'active' if not provided
                status = bridge_data.get("status", "active")
                if status not in valid_bridge_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status '{status}'. Must be one of: {', '.join(valid_bridge_statuses)}"
                    })

                # start_time defaults to current timestamp if not provided
                start_time = bridge_data.get("start_time", timestamp)

                new_id = generate_id(bridges, "")
                new_bridge_number = generate_bridge_number(bridges)
                
                new_bridge = {
                    "bridge_id": new_id,
                    "bridge_number": new_bridge_number,
                    "incident_id": incident_id,
                    "bridge_type": bridge_data["bridge_type"],
                    "bridge_host": bridge_host,
                    "start_time": start_time,
                    "end_time": bridge_data.get("end_time"),
                    "status": status,
                    "created_at": timestamp
                }
                bridges[new_id] = new_bridge
                return json.dumps({
                    "success": True,
                    "entity_type": "bridge",
                    "action": "create",
                    "bridge_id": new_id,
                    "bridge_data": new_bridge
                })

            elif action == "update":
                if not bridge_id:
                    return json.dumps({
                        "success": False,
                        "error": "bridge_id is required for update action"
                    })
                bridge_id = str(bridge_id).strip().strip('"')
                if bridge_id not in bridges:
                    return json.dumps({
                        "success": False,
                        "error": f"Bridge '{bridge_id}' not found"
                    })

                if not bridge_data:
                    return json.dumps({
                        "success": False,
                        "error": "bridge_data is required for update action"
                    })

                # Allowed fields for update (bridge_id, bridge_number, incident_id, created_at are not updatable)
                allowed_fields = ["bridge_type", "bridge_host", "start_time", "end_time", "status"]
                invalid_fields = [field for field in bridge_data if field not in allowed_fields]
                if invalid_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid fields for update: {', '.join(invalid_fields)}"
                    })
                
                # Validate non-empty fields (end_time is nullable)
                nullable_fields = ["end_time"]
                for field, value in bridge_data.items():
                    if field not in nullable_fields and (value is None or (isinstance(value, str) and value.strip() == "")):
                        return json.dumps({
                            "success": False,
                            "error": f"Field '{field}' cannot be empty"
                        })
                    elif field in nullable_fields and (isinstance(value, str) and value.strip() == ""):
                        bridge_data[field] = None

                # Validate enums if provided
                if "bridge_type" in bridge_data and bridge_data["bridge_type"] not in valid_bridge_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid bridge_type. Must be one of: {', '.join(valid_bridge_types)}"
                    })
                if "status" in bridge_data and bridge_data["status"] not in valid_bridge_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_bridge_statuses)}"
                    })
                # In the update action for bridge, after validation:
                if "status" in bridge_data and bridge_data["status"] == "closed" and "end_time" not in bridge_data:
                    bridge_data["end_time"] = timestamp  # Auto-set end_time when closing
                # Validate bridge_host if provided
                if "bridge_host" in bridge_data:
                    bridge_host = str(bridge_data["bridge_host"]).strip().strip('"')
                    if bridge_host not in users:
                        return json.dumps({
                            "success": False,
                            "error": f"Bridge host user '{bridge_host}' not found"
                        })
                    if users[bridge_host]["status"] != "active":
                        return json.dumps({
                            "success": False,
                            "error": f"Bridge host user '{bridge_host}' is not active"
                        })
                    bridge_data["bridge_host"] = bridge_host

                updated_bridge = bridges[bridge_id].copy()
                for key, value in bridge_data.items():
                    updated_bridge[key] = value
                bridges[bridge_id] = updated_bridge
                return json.dumps({
                    "success": True,
                    "entity_type": "bridge",
                    "action": "update",
                    "bridge_id": bridge_id,
                    "bridge_data": updated_bridge
                })

        # ============================================================================
        # BRIDGE PARTICIPANT HANDLEMENT
        # ============================================================================
        elif entity_type == "bridge_participant":
            if action == "create":
                if not participant_data:
                    return json.dumps({
                        "success": False,
                        "error": "participant_data is required for create action"
                    })

                # Validate required fields
                required_fields = ["bridge_id", "user_id", "role_in_bridge"]
                missing_fields = [field for field in required_fields if field not in participant_data]
                if missing_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Missing required fields: {', '.join(missing_fields)}"
                    })
                
                # Validate non-empty required fields
                for field in required_fields:
                    if not participant_data[field] or (isinstance(participant_data[field], str) and participant_data[field].strip() == ""):
                        return json.dumps({
                            "success": False,
                            "error": f"Field '{field}' cannot be empty"
                        })

                # Validate bridge exists and is active
                bridge_id_for_participant = str(participant_data["bridge_id"]).strip().strip('"')
                if bridge_id_for_participant not in bridges:
                    return json.dumps({
                        "success": False,
                        "error": f"Bridge '{bridge_id_for_participant}' not found"
                    })
                if bridges[bridge_id_for_participant]["status"] != "active":
                    return json.dumps({
                        "success": False,
                        "error": f"Bridge '{bridge_id_for_participant}' is not active"
                    })

                # Validate user exists and is active
                user_id = str(participant_data["user_id"]).strip().strip('"')
                if user_id not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"User '{user_id}' not found"
                    })
                if users[user_id]["status"] != "active":
                    return json.dumps({
                        "success": False,
                        "error": f"User '{user_id}' is not active"
                    })

                # Validate role_in_bridge enum
                if participant_data["role_in_bridge"] not in valid_participant_roles:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid role_in_bridge '{participant_data['role_in_bridge']}'. Must be one of: {', '.join(valid_participant_roles)}"
                    })

                # Check for duplicate participant (same user_id + bridge_id)
                for participant in bridge_participants.values():
                    if participant["bridge_id"] == bridge_id_for_participant and participant["user_id"] == user_id:
                        return json.dumps({
                            "success": False,
                            "error": f"User '{user_id}' is already a participant in bridge '{bridge_id_for_participant}'"
                        })

                # joined_at defaults to current timestamp if not provided
                joined_at = participant_data.get("joined_at", timestamp)

                new_id = generate_id(bridge_participants, "")
                
                new_participant = {
                    "participant_id": new_id,
                    "bridge_id": bridge_id_for_participant,
                    "user_id": user_id,
                    "role_in_bridge": participant_data["role_in_bridge"],
                    "joined_at": joined_at
                }
                bridge_participants[new_id] = new_participant
                return json.dumps({
                    "success": True,
                    "entity_type": "bridge_participant",
                    "action": "create",
                    "participant_id": new_id,
                    "participant_data": new_participant
                })

            elif action == "update":
                if not participant_id:
                    return json.dumps({
                        "success": False,
                        "error": "participant_id is required for update action"
                    })
                participant_id = str(participant_id).strip().strip('"')
                if participant_id not in bridge_participants:
                    return json.dumps({
                        "success": False,
                        "error": f"Bridge participant '{participant_id}' not found"
                    })

                if not participant_data:
                    return json.dumps({
                        "success": False,
                        "error": "participant_data is required for update action"
                    })

                # Allowed fields for update (participant_id, bridge_id are not updatable)
                allowed_fields = ["user_id", "role_in_bridge", "joined_at"]
                invalid_fields = [field for field in participant_data if field not in allowed_fields]
                if invalid_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid fields for update: {', '.join(invalid_fields)}"
                    })
                
                # Validate non-empty fields
                for field, value in participant_data.items():
                    if value is None or (isinstance(value, str) and value.strip() == ""):
                        return json.dumps({
                            "success": False,
                            "error": f"Field '{field}' cannot be empty"
                        })

                # Validate role_in_bridge if provided
                if "role_in_bridge" in participant_data and participant_data["role_in_bridge"] not in valid_participant_roles:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid role_in_bridge. Must be one of: {', '.join(valid_participant_roles)}"
                    })

                # Validate user if provided
                if "user_id" in participant_data:
                    user_id = str(participant_data["user_id"]).strip().strip('"')
                    if user_id not in users:
                        return json.dumps({
                            "success": False,
                            "error": f"User '{user_id}' not found"
                        })
                    if users[user_id]["status"] != "active":
                        return json.dumps({
                            "success": False,
                            "error": f"User '{user_id}' is not active"
                        })
                    
                    # Check for duplicate if changing user
                    current_bridge_id = bridge_participants[participant_id]["bridge_id"]
                    for pid, participant in bridge_participants.items():
                        if pid != participant_id and participant["bridge_id"] == current_bridge_id and participant["user_id"] == user_id:
                            return json.dumps({
                                "success": False,
                                "error": f"User '{user_id}' is already a participant in this bridge"
                            })
                    participant_data["user_id"] = user_id

                updated_participant = bridge_participants[participant_id].copy()
                for key, value in participant_data.items():
                    updated_participant[key] = value
                bridge_participants[participant_id] = updated_participant
                return json.dumps({
                    "success": True,
                    "entity_type": "bridge_participant",
                    "action": "update",
                    "participant_id": participant_id,
                    "participant_data": updated_participant
                })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_coordinations",
                "description": "Create or update bridge records and bridge participant assignments for incident coordination. Bridges are used for real-time collaboration during major incidents.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of coordination entity to manage: 'bridge' for incident bridge records, 'bridge_participant' for participant assignments.",
                            "enum": ["bridge", "bridge_participant"]
                        },
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish a new record, 'update' to modify an existing record.",
                            "enum": ["create", "update"]
                        },
                        "bridge_data": {
                            "type": "object",
                            "description": "Data object containing fields for creating or updating a bridge record. Required when entity_type is 'bridge'.",
                            "properties": {
                                "incident_id": {
                                    "type": "string",
                                    "description": "Incident requiring bridge collaboration (required for create, must exist and have status 'open' or 'in_progress'). Not updatable."
                                },
                                "bridge_type": {
                                    "type": "string",
                                    "description": "Type of bridge (required for create). Must be one of: major_incident, coordination, technical. Updatable.",
                                    "enum": ["major_incident", "coordination", "technical"]
                                },
                                "bridge_host": {
                                    "type": "string",
                                    "description": "User ID of the Incident Manager hosting the bridge (required for create, must be an active user). Updatable."
                                },
                                "start_time": {
                                    "type": "string",
                                    "description": "Bridge start timestamp in ISO 8601 format (optional for create, defaults to current time). Updatable."
                                },
                                "end_time": {
                                    "type": "string",
                                    "description": "Bridge end timestamp in ISO 8601 format (optional, used when closing bridge). Updatable, can be set to null."
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Bridge status (optional for create, defaults to 'active'). Must be one of: active, closed. Updatable.",
                                    "enum": ["active", "closed"]
                                }
                            }
                        },
                        "bridge_id": {
                            "type": "string",
                            "description": "The unique identifier of the bridge to update. Required for 'update' action when entity_type is 'bridge'."
                        },
                        "participant_data": {
                            "type": "object",
                            "description": "Data object containing fields for creating or updating a bridge participant. Required when entity_type is 'bridge_participant'.",
                            "properties": {
                                "bridge_id": {
                                    "type": "string",
                                    "description": "Bridge ID for participant assignment (required for create, bridge must exist and be active). Not updatable."
                                },
                                "user_id": {
                                    "type": "string",
                                    "description": "User ID of the participant (required for create, must be an active user). Updatable."
                                },
                                "role_in_bridge": {
                                    "type": "string",
                                    "description": "Participant's role in the bridge (required for create). Must be one of: host, technical_support, account_manager, executive. Updatable.",
                                    "enum": ["host", "technical_support", "account_manager", "executive"]
                                },
                                "joined_at": {
                                    "type": "string",
                                    "description": "Timestamp when participant joined in ISO 8601 format (optional for create, defaults to current time). Updatable."
                                }
                            }
                        },
                        "participant_id": {
                            "type": "string",
                            "description": "The unique identifier of the bridge participant to update. Required for 'update' action when entity_type is 'bridge_participant'."
                        }
                    },
                    "required": ["entity_type", "action"]
                }
            }
        }