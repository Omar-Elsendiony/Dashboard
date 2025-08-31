import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class UpdateRootCauseAnalysis(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        rca_id: str,
        incident_id: str = None,
        analysis_method: str = None,   # five_whys|fishbone|timeline_analysis|fault_tree
        conducted_by_id: str = None,
        completed_at: str = None,
        status: str = None             # in_progress|completed|approved
    ) -> str:
        try:
            # Helper kept inside invoke per requirement
            def is_iso(ts: str) -> bool:
                try:
                    datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    return True
                except Exception:
                    return False

            rcas = data.get("root_cause_analysis", {})
            if rca_id not in rcas:
                return json.dumps({"success": False, "error": f"RCA {rca_id} not found"})

            valid_methods = {"five_whys","fishbone","timeline_analysis","fault_tree"}
            valid_status = {"in_progress","completed","approved"}

            if analysis_method and analysis_method not in valid_methods:
                return json.dumps({"success": False, "error": f"Invalid analysis_method. Must be one of {sorted(valid_methods)}"})
            if status and status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})
            if completed_at is not None and not is_iso(completed_at):
                return json.dumps({"success": False, "error": "completed_at must be ISO timestamp"})

            r = rcas[rca_id]
            if incident_id is not None: r["incident_id"] = incident_id
            if analysis_method is not None: r["analysis_method"] = analysis_method
            if conducted_by_id is not None: r["conducted_by_id"] = conducted_by_id
            if completed_at is not None: r["completed_at"] = completed_at
            if status is not None: r["status"] = status

            return json.dumps(r)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info()->Dict[str,Any]:
        return{
            "type":"function",
            "function":{
                "name":"update_root_cause_analysis",
                "description":"Update an RCA record; validates enums/timestamp",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "rca_id":{"type":"string"},
                        "incident_id":{"type":"string"},
                        "analysis_method":{"type":"string","description":"five_whys|fishbone|timeline_analysis|fault_tree"},
                        "conducted_by_id":{"type":"string"},
                        "completed_at":{"type":"string","description":"ISO timestamp"},
                        "status":{"type":"string","description":"in_progress|completed|approved"}
                    },
                    "required":["rca_id"]
                }
            }
        }
