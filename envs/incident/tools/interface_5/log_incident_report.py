import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class LogIncidentReport(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        generated_by_id: str,
        report_type: str,
        status: str = "completed"
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            reports = data.setdefault("incident_reports", {})
            valid_types = {
                "executive_summary","technical_details","business_impact","compliance_report","post_mortem"
            }
            if report_type not in valid_types:
                return json.dumps({"success": False, "error": f"Invalid report_type. Must be one of {sorted(valid_types)}"})

            valid_status = {"draft","completed","distributed"}
            if status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

            report_id = generate_id(reports)
            timestamp = "2025-10-01T00:00:00"

            new_report = {
                "report_id": report_id,
                "incident_id": incident_id,
                "report_type": report_type,
                "generated_by_id": generated_by_id,
                "generated_at": timestamp,   # NOW
                "status": status,
                "created_at": timestamp
            }

            reports[report_id] = new_report
            return json.dumps({
                "report_id": report_id,
                "status": status,
                "generated_at": timestamp,
                "success": True
            })
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return  {
            "type": "function",
            "function": {
                "name": "log_incident_report",
                "description": "Create an incident report; sets generated_at (and created_at) to current timestamp surrogate",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string"},
                        "generated_by_id": {"type": "string"},
                        "report_type": {"type": "string", "description": "executive_summary|technical_details|business_impact|compliance_report|post_mortem"},
                        "status": {"type": "string", "description": "draft|completed|distributed (default completed)"}
                    },
                    "required": ["incident_id","generated_by_id","report_type"]
                }
            }
        }
