import json
import os
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageWorkNotes(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        note_id: Optional[str] = None,
        note_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
        ENV_DIR = os.path.dirname(TOOL_DIR)
        DATA_DIR = os.path.join(ENV_DIR, "data")
        WORK_NOTES_FP = os.path.join(DATA_DIR, "work_notes.json")

        def ensure_dirs() -> None:
            os.makedirs(DATA_DIR, exist_ok=True)

        def load_work_notes() -> Dict[str, Any]:
            if os.path.exists(WORK_NOTES_FP):
                try:
                    with open(WORK_NOTES_FP, "r") as f:
                        return json.load(f)
                except Exception:
                    return {}
            return {}

        def save_work_notes(notes_dict: Dict[str, Any]) -> None:
            ensure_dirs()
            with open(WORK_NOTES_FP, "w") as f:
                json.dump(notes_dict, f, indent=2)

        timestamp = "2025-11-01T00:00:00"
        work_notes = data.setdefault("work_notes", {})
        incidents = data.setdefault("incidents", {})
        users = data.setdefault("users", {})

        if not work_notes:
            loaded = load_work_notes()
            if loaded:
                work_notes.update(loaded)

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

        if action == "create":
            if not note_data:
                return json.dumps({
                    "success": False,
                    "error": "note_data is required for create action"
                })

            required_fields = ["incident_id", "note_text", "created_by"]
            missing_fields = [field for field in required_fields if field not in note_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                })

            incident_id = str(note_data["incident_id"])
            if incident_id not in incidents:
                return json.dumps({
                    "success": False,
                    "error": f"Incident with ID '{incident_id}' not found"
                })

            created_by = str(note_data["created_by"])
            if created_by not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User with ID '{created_by}' not found"
                })

            if not isinstance(note_data.get("note_text"), str) or not note_data["note_text"].strip():
                return json.dumps({
                    "success": False,
                    "error": "note_text must be a non-empty string"
                })

            new_note_id = generate_id(work_notes)
            new_work_note = {
                "note_id": new_note_id,
                "incident_id": incident_id,
                "note_text": note_data["note_text"],
                "created_by": created_by,
                "created_at": timestamp,
                "updated_at": timestamp
            }

            work_notes[new_note_id] = new_work_note
            save_work_notes(work_notes)
            return json.dumps(new_work_note)

        if not note_id:
            return json.dumps({
                "success": False,
                "error": "note_id is required for update action"
            })

        if note_id not in work_notes:
            return json.dumps({
                "success": False,
                "error": f"Work note with ID '{note_id}' not found"
            })

        if not note_data:
            return json.dumps({
                "success": False,
                "error": "note_data is required for update action"
            })

        if "note_text" not in note_data:
            return json.dumps({
                "success": False,
                "error": "Only note_text can be updated"
            })

        if not isinstance(note_data["note_text"], str) or not note_data["note_text"].strip():
            return json.dumps({
                "success": False,
                "error": "note_text must be a non-empty string"
            })

        current_work_note = work_notes[note_id]
        updated_work_note = current_work_note.copy()
        updated_work_note["note_text"] = note_data["note_text"]
        updated_work_note["updated_at"] = timestamp
        work_notes[note_id] = updated_work_note
        save_work_notes(work_notes)
        return json.dumps(updated_work_note)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_work_notes",
                "description": (
                    "Create or update work note records in the incident management system. "
                    "This tool manages work notes with file persistence under data/work_notes.json. "
                    "For creation, establishes new notes linked to incidents with proper validation of user and incident existence. "
                    "For updates, modifies existing work notes (only note_text can be changed)."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": (
                                "Action to perform:\n"
                                "- 'create': Add a new work note (requires note_data with incident_id, note_text, created_by)\n"
                                "- 'update': Modify an existing note (requires note_id and note_data with new note_text)"
                            ),
                            "enum": ["create", "update"]
                        },
                        "note_id": {
                            "type": "string",
                            "description": (
                                "Unique identifier of the work note. Required only for 'update' action. "
                                "Use the note_id returned by the create action when updating."
                            )
                        },
                        "note_data": {
                            "type": "object",
                            "description": (
                                "Work note data object.\n\n"
                                "For 'create': requires the following fields:\n"
                                "  - incident_id: ID of the linked incident (must exist in incidents)\n"
                                "  - note_text: the content of the work note\n"
                                "  - created_by: user ID of the author (must exist in users)\n\n"
                                "For 'update': only note_text is required.\n\n"
                                "Examples:\n"
                                "- Create: {\"incident_id\": \"1\", \"note_text\": \"Restarted service\", \"created_by\": \"100\"}\n"
                                "- Update: {\"note_text\": \"Issue resolved and verified\"}"
                            ),
                            "properties": {
                                "incident_id": {
                                    "type": "string",
                                    "description": "Incident identifier (required for create, must exist in system)"
                                },
                                "note_text": {
                                    "type": "string",
                                    "description": "Content of the work note (required for create and update)"
                                },
                                "created_by": {
                                    "type": "string",
                                    "description": "User ID who created the note (required for create, must exist in users)"
                                }
                            }
                        }
                    },
                    "required": ["action"]
                }
            }
        }
