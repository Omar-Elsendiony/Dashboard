import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RegisterIncidentUpdateRecord(Tool):
    """
    Create an audit record in incident_updates documenting an incident change.
    Does NOT modify the incident itself. No ID existence validations (agent handles that).
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        updated_by_id: str,
        update_type: str,           # status_change|severity_change|assignment|workaround|resolution|communication
        field_name: str,            # e.g., status, severity, assigned_manager_id, note, etc.
        new_value: Optional[str] = None,
        old_value: Optional[str] = None
    ) -> str:
        # Enum checks only (per instructions)
        valid_update_types = {"status_change","severity_change","assignment","workaround","resolution","communication"}
        if update_type not in valid_update_types:
            return json.dumps({"success": False, "error": f"Invalid update_type. Must be one of {sorted(valid_update_types)}"})

        allowed_fields = {
            "status","severity","assigned_manager_id","component_id","category",
            "impact","urgency","resolved_at","closed_at","note","workaround"
        }
        if field_name not in allowed_fields:
            return json.dumps({"success": False, "error": f"Invalid field_name. Must be one of {sorted(allowed_fields)}"})

        updates = data.setdefault("incident_updates", {})

        # generate_id must be within invoke
        def generate_id(table: Dict[str, Any]) -> str:
            return str(max([int(k) for k in table.keys()] + [0]) + 1)

        update_id = generate_id(updates)
        timestamp = "2025-10-01T00:00:00"  # fixed timestamp for create APIs

        updates[update_id] = {
            "update_id": update_id,
            "incident_id": incident_id,
            "updated_by_id": updated_by_id,
            "update_type": update_type,
            "field_name": field_name,
            "old_value": None if old_value is None else str(old_value),
            "new_value": None if new_value is None else str(new_value),
            "created_at": timestamp
        }

        return json.dumps({"success": True, "update_id": update_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "register_incident_update_record",
                "description": "Create an audit record in incident_updates documenting an incident change. Does not modify the incident.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string"},
                        "updated_by_id": {"type": "string"},
                        "update_type": {"type": "string", "description": "status_change|severity_change|assignment|workaround|resolution|communication"},
                        "field_name": {"type": "string", "description": "status|severity|assigned_manager_id|component_id|category|impact|urgency|resolved_at|closed_at|note|workaround"},
                        "new_value": {"type": "string"},
                        "old_value": {"type": "string", "description": "Optional; pass previous value if known"}
                    },
                    "required": ["incident_id","updated_by_id","update_type","field_name"]
                }
            }
        }
