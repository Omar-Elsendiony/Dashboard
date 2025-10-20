import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManipulateWorkNotes(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        note_data: Optional[Dict[str, Any]] = None,
        note_id: Optional[str] = None
    ) -> str:
        """
        Create or update work note records.

        Actions:
        - create: Create a new work note record (requires note_data)
        - update: Update an existing work note record (requires note_id and note_data)
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

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        work_notes = data.get("work_notes", {})
        incidents = data.get("incidents", {})
        problem_tickets = data.get("problem_tickets", {}) # Added for problem_ticket_id validation
        users = data.get("users", {})

        # Define valid enums based on DBML schema
        valid_note_types = ["progress_update", "troubleshooting", "resolution"]

        if action == "create":
            if not note_data:
                return json.dumps({
                    "success": False,
                    "error": "note_data is required for create action"
                })

            # Validate required fields as per DBML schema (incident_id and problem_ticket_id are now optional but one must exist)
            required_fields = [
                "note_text", "note_type", "created_by"
            ]
            missing_fields = [field for field in required_fields if field not in note_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                })
            
            # Validate non-empty required fields
            for field in required_fields:
                if not note_data[field] or (isinstance(note_data[field], str) and str(note_data[field]).strip() == ""):
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })

            # Validate incident_id OR problem_ticket_id
            incident_id = note_data.get("incident_id")
            problem_ticket_id = note_data.get("problem_ticket_id")

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

            # Validate incident_id FK if provided
            if incident_id:
                if str(incident_id).strip().strip('"') not in incidents:
                    return json.dumps({
                        "success": False,
                        "error": f"Incident '{incident_id}' not found"
                    })
            
            # Validate problem_ticket_id FK if provided
            if problem_ticket_id:
                if str(problem_ticket_id).strip().strip('"') not in problem_tickets:
                    return json.dumps({
                        "success": False,
                        "error": f"Problem ticket '{problem_ticket_id}' not found"
                    })

            # Validate note_type enum
            if note_data["note_type"] not in valid_note_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid note_type '{note_data['note_type']}'. Must be one of: {', '.join(valid_note_types)}"
                })

            # Validate created_by FK
            created_by = str(note_data["created_by"]).strip().strip('"')
            if created_by not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User '{created_by}' not found"
                })
            if users[created_by]["status"] != "active":
                return json.dumps({
                    "success": False,
                    "error": f"User '{created_by}' is not active"
                })

            new_id = generate_id(work_notes, "")
            new_note = {
                "note_id": new_id,
                "incident_id": incident_id if incident_id else None,
                "problem_ticket_id": problem_ticket_id if problem_ticket_id else None,
                "note_text": note_data["note_text"],
                "note_type": note_data["note_type"],
                "created_by": created_by,
                "created_at": timestamp
            }
            work_notes[new_id] = new_note
            return json.dumps({
                "success": True,
                "action": "create",
                "note_id": new_id,
                "note_data": new_note
            })

        elif action == "update":
            if not note_id:
                return json.dumps({
                    "success": False,
                    "error": "note_id is required for update action"
                })
            note_id = str(note_id).strip().strip('"')
            if note_id not in work_notes:
                return json.dumps({
                    "success": False,
                    "error": f"Work note '{note_id}' not found"
                })

            if not note_data:
                return json.dumps({
                    "success": False,
                    "error": "note_data is required for update action"
                })

            # Allowed fields for update (note_text, note_type, incident_id, problem_ticket_id can be updated)
            allowed_fields = ["incident_id", "problem_ticket_id", "note_text", "note_type"]
            invalid_fields = [field for field in note_data if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for update: {', '.join(invalid_fields)}"
                })
            
            # Validate non-empty fields
            for field, value in note_data.items():
                if field not in ["incident_id", "problem_ticket_id"] and value is not None and str(value).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })
                elif field in ["incident_id", "problem_ticket_id"] and value is not None and str(value).strip() == "":
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty if provided"
                    })

            # Validate incident_id OR problem_ticket_id if either is provided
            incident_id_update = note_data.get("incident_id")
            problem_ticket_id_update = note_data.get("problem_ticket_id")

            if incident_id_update is not None and problem_ticket_id_update is not None:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Only one of 'incident_id' or 'problem_ticket_id' can be provided, not both"
                })
            
            # If both are provided as None, it means the user wants to clear both, which is not allowed.
            current_incident_id = work_notes[note_id].get("incident_id")
            current_problem_ticket_id = work_notes[note_id].get("problem_ticket_id")

            final_incident_id = incident_id_update if "incident_id" in note_data else current_incident_id
            final_problem_ticket_id = problem_ticket_id_update if "problem_ticket_id" in note_data else current_problem_ticket_id

            if not final_incident_id and not final_problem_ticket_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Either 'incident_id' or 'problem_ticket_id' must be provided and not null"
                })

            # Validate incident_id FK if provided
            if incident_id_update:
                if str(incident_id_update).strip().strip('"') not in incidents:
                    return json.dumps({
                        "success": False,
                        "error": f"Incident '{incident_id_update}' not found"
                    })
            
            # Validate problem_ticket_id FK if provided
            if problem_ticket_id_update:
                if str(problem_ticket_id_update).strip().strip('"') not in problem_tickets:
                    return json.dumps({
                        "success": False,
                        "error": f"Problem ticket '{problem_ticket_id_update}' not found"
                    })

            # Validate note_type enum if provided
            if "note_type" in note_data and note_data["note_type"] not in valid_note_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid note_type '{note_data['note_type']}'. Must be one of: {', '.join(valid_note_types)}"
                })

            updated_note = work_notes[note_id].copy()
            for key, value in note_data.items():
                if key in ["incident_id", "problem_ticket_id"]:
                    updated_note[key] = str(value) if value not in (None, "") else None
                else:
                    updated_note[key] = value
            
            work_notes[note_id] = updated_note
            return json.dumps({
                "success": True,
                "action": "update",
                "note_id": note_id,
                "note_data": updated_note
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manipulate_work_notes",
                "description": "Create or update work note records in the system. Work notes document incident progress, troubleshooting steps, and resolutions. Either incident_id or problem_ticket_id must be provided, but not both.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to add a new work note, 'update' to modify an existing work note."
                        },
                        "note_data": {
                            "type": "object",
                            "description": "Data object containing fields for creating or updating a work note.",
                            "properties": {
                                "incident_id": {
                                    "type": "string",
                                    "description": "The ID of the incident this note is associated with (required for create if problem_ticket_id is not provided, cannot be empty). Must refer to an existing incident. Can be set to null for update if problem_ticket_id is provided."
                                },
                                "problem_ticket_id": {
                                    "type": "string",
                                    "description": "The ID of the problem ticket this note is associated with (required for create if incident_id is not provided, cannot be empty). Must refer to an existing problem ticket. Can be set to null for update if incident_id is provided."
                                },
                                "note_text": {
                                    "type": "string",
                                    "description": "The content of the work note (required for create, cannot be empty). Updatable."
                                },
                                "note_type": {
                                    "type": "string",
                                    "description": "The type/category of the work note (required for create). Must be one of: progress_update, troubleshooting, resolution. Updatable.",
                                    "enum": ["progress_update", "troubleshooting", "resolution"]
                                },
                                "created_by": {
                                    "type": "string",
                                    "description": "The user ID of the person who created the note (required for create). Must refer to an existing active user."
                                }
                            }
                        },
                        "note_id": {
                            "type": "string",
                            "description": "The unique identifier of the work note to update. Required for 'update' action only."
                        }
                    },
                    "required": ["action"]
                }
            }
        }