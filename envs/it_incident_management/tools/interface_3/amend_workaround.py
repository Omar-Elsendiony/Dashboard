import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class AmendWorkaround(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        workaround_id: str,
        incident_id: str = None,
        implemented_by_id: str = None,
        effectiveness: str = None,   # complete|partial|minimal
        status: str = None,          # active|inactive|replaced
        implemented_at: str = None
    ) -> str:
        try:
            # Helper inside invoke per requirement
            def is_iso(ts: str) -> bool:
                try:
                    datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    return True
                except Exception:
                    return False

            wars = data.get("workarounds", {})
            if workaround_id not in wars:
                return json.dumps({"success": False, "error": f"Workaround {workaround_id} not found"})

            valid_eff = {"complete","partial","minimal"}
            valid_status = {"active","inactive","replaced"}

            if effectiveness and effectiveness not in valid_eff:
                return json.dumps({"success": False, "error": f"Invalid effectiveness. Must be one of {sorted(valid_eff)}"})
            if status and status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})
            if implemented_at is not None and not is_iso(implemented_at):
                return json.dumps({"success": False, "error": "implemented_at must be ISO timestamp"})

            w = wars[workaround_id]
            if incident_id is not None: w["incident_id"] = incident_id
            if implemented_by_id is not None: w["implemented_by_id"] = implemented_by_id
            if effectiveness is not None: w["effectiveness"] = effectiveness
            if status is not None: w["status"] = status
            if implemented_at is not None: w["implemented_at"] = implemented_at

            return json.dumps(w)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info()->Dict[str,Any]:
        return{
            "type":"function",
            "function":{
                "name":"amend_workaround",
                "description":"Update a workaround; validates enums/timestamp",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "workaround_id":{"type":"string"},
                        "incident_id":{"type":"string"},
                        "implemented_by_id":{"type":"string"},
                        "effectiveness":{"type":"string","description":"complete|partial|minimal"},
                        "status":{"type":"string","description":"active|inactive|replaced"},
                        "implemented_at":{"type":"string","description":"ISO timestamp"}
                    },
                    "required":["workaround_id"]
                }
            }
        }
