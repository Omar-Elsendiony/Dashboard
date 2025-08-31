import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateWorkaround(Tool):
    @staticmethod
    def _record_update(updates_table: Dict[str, Any], incident_id: str, updated_by_id: str, note: Optional[str], workaround_id: str):
        if not note:
            return
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        update_id = generate_id(updates_table)
        timestamp = "2025-10-01T00:00:00"
        updates_table[update_id] = {
            "update_id": update_id,
            "incident_id": incident_id,
            "updated_by_id": updated_by_id,
            "update_type": "workaround",
            "field_name": "note",
            "old_value": None,
            "new_value": f"[workaround:{workaround_id}] {note}",
            "created_at": timestamp
        }

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        implemented_by_id: str,
        effectiveness: str,
        status: str = "active",
        note: str = None
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            workarounds = data.setdefault("workarounds", {})

            valid_eff = {"complete","partial","minimal"}
            if effectiveness not in valid_eff:
                return json.dumps({"success": False, "error": f"Invalid effectiveness. Must be one of {sorted(valid_eff)}"})

            valid_status = {"active","inactive","replaced"}
            if status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

            workaround_id = generate_id(workarounds)
            timestamp = "2025-10-01T00:00:00"

            new_workaround = {
                "workaround_id": workaround_id,
                "incident_id": incident_id,
                "implemented_by_id": implemented_by_id,
                "effectiveness": effectiveness,
                "status": status,
                "implemented_at": timestamp,   # NOW surrogate
                "created_at": timestamp
            }

            workarounds[workaround_id] = new_workaround

            # Optionally log the note into incident_updates
            updates_table = data.setdefault("incident_updates", {})
            CreateWorkaround._record_update(updates_table, incident_id, implemented_by_id, note, workaround_id)

            return json.dumps({"workaround_id": workaround_id, "success": True})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_workaround",
                "description": "Create a workaround for an incident; sets implemented_at and created_at; optionally logs a note",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string"},
                        "implemented_by_id": {"type": "string"},
                        "effectiveness": {"type": "string", "description": "complete|partial|minimal"},
                        "status": {"type": "string", "description": "active|inactive|replaced (default active)"},
                        "note": {"type": "string", "description": "Optional note to log to incident updates"}
                    },
                    "required": ["incident_id","implemented_by_id","effectiveness"]
                }
            }
        }
