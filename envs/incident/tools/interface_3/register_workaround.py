import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RegisterWorkaround(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        implemented_by_id: str,
        effectiveness: str,                          # complete|partial|minimal
        status: str = "active",                      # active|inactive|replaced
        implemented_at: Optional[str] = None,        # optional, if omitted we set to ts
    ) -> str:
        workarounds = data.setdefault("workarounds", {})

        valid_eff = {"complete", "partial", "minimal"}
        valid_status = {"active", "inactive", "replaced"}
        if effectiveness not in valid_eff:
            return json.dumps({"success": False, "error": f"Invalid effectiveness. Must be one of {sorted(valid_eff)}"})
        if status not in valid_status:
            return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

        def generate_id(table: Dict[str, Any]) -> str:
            return str(max([int(k) for k in table.keys()] + [0]) + 1)

        workaround_id = generate_id(workarounds)
        ts = "2025-10-01T00:00:00"

        new_workaround = {
            "workaround_id": workaround_id,
            "incident_id": incident_id,
            "implemented_by_id": implemented_by_id,
            "effectiveness": effectiveness,
            "status": status,
            "implemented_at": implemented_at or ts,
            "created_at": ts,
        }

        workarounds[workaround_id] = new_workaround
        return json.dumps({"workaround_id": workaround_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "register_workaround",
                "description": "Create a workaround for an incident. Minimal side effects; just inserts the record.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string"},
                        "implemented_by_id": {"type": "string"},
                        "effectiveness": {"type": "string", "description": "complete|partial|minimal"},
                        "status": {"type": "string", "description": "active|inactive|replaced (default active)"},
                        "implemented_at": {"type": "string", "description": "ISO timestamp; if omitted, defaults to 2025-10-01T00:00:00"}
                    },
                    "required": ["incident_id", "implemented_by_id", "effectiveness"]
                }
            }
        }
