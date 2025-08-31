import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class UpdateIncidentReport(Tool):
    @staticmethod
    def _is_iso(ts: str) -> bool:
        try:
            datetime.fromisoformat(ts.replace("Z","+00:00"))
            return True
        except Exception:
            return False

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        report_id: str,
        incident_id: str = None,
        report_type: str = None,       # executive_summary|technical_details|business_impact|compliance_report|post_mortem
        generated_by_id: str = None,
        generated_at: str = None,
        status: str = None             # draft|completed|distributed
    ) -> str:
        try:
            reports = data.get("incident_reports", {})
            if report_id not in reports:
                return json.dumps({"success": False, "error": f"Incident report {report_id} not found"})

            valid_types = {"executive_summary","technical_details","business_impact","compliance_report","post_mortem"}
            valid_status = {"draft","completed","distributed"}

            if report_type and report_type not in valid_types:
                return json.dumps({"success": False, "error": f"Invalid report_type. Must be one of {sorted(valid_types)}"})
            if status and status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})
            if generated_at is not None and not UpdateIncidentReport._is_iso(generated_at):
                return json.dumps({"success": False, "error": "generated_at must be ISO timestamp"})

            r = reports[report_id]
            if incident_id is not None: r["incident_id"] = incident_id
            if report_type is not None: r["report_type"] = report_type
            if generated_by_id is not None: r["generated_by_id"] = generated_by_id
            if generated_at is not None: r["generated_at"] = generated_at
            if status is not None: r["status"] = status

            return json.dumps(r)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})
    
    @staticmethod
    def get_info()->Dict[str,Any]:
        return{
            "type":"function",
            "function":{
                "name":"update_incident_report",
                "description":"Update an incident report; validates enums/timestamp",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "report_id":{"type":"string"},
                        "incident_id":{"type":"string"},
                        "report_type":{"type":"string","description":"executive_summary|technical_details|business_impact|compliance_report|post_mortem"},
                        "generated_by_id":{"type":"string"},
                        "generated_at":{"type":"string","description":"ISO timestamp"},
                        "status":{"type":"string","description":"draft|completed|distributed"}
                    },
                    "required":["report_id"]
                }
            }
        }
