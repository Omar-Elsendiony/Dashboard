import json
from typing import Any, Dict, Optional, List
from datetime import datetime
from tau_bench.envs.tool import Tool

class ListIncidentReports(Tool):
    @staticmethod
    def _parse_iso(ts: Optional[str]) -> Optional[datetime]:
        if not ts:
            return None
        ts = ts.replace("Z", "+00:00")
        return datetime.fromisoformat(ts)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        report_id: str = None,
        incident_id: str = None,
        report_type: str = None,   # executive_summary|technical_details|business_impact|compliance_report|post_mortem
        status: str = None,        # draft|completed|distributed
        generated_since: str = None
    ) -> str:
        try:
            reports: Dict[str, Any] = data.get("incident_reports", {})
            results: List[Dict[str, Any]] = []
            since_dt = ListIncidentReports._parse_iso(generated_since) if generated_since else None

            for r in reports.values():
                if report_id and r.get("report_id") != report_id:
                    continue
                if incident_id and r.get("incident_id") != incident_id:
                    continue
                if report_type and r.get("report_type") != report_type:
                    continue
                if status and r.get("status") != status:
                    continue

                if since_dt:
                    ga = r.get("generated_at")
                    if not ga:
                        continue
                    try:
                        ga_dt = ListIncidentReports._parse_iso(ga)
                        if ga_dt < since_dt:
                            continue
                    except Exception:
                        continue

                results.append(r)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return  {
            "type": "function",
            "function": {
                "name": "list_incident_reports",
                "description": "Unified get/list for incident reports with optional filtering",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "report_id": {"type": "string"},
                        "incident_id": {"type": "string"},
                        "report_type": {"type": "string", "description": "executive_summary|technical_details|business_impact|compliance_report|post_mortem"},
                        "status": {"type": "string", "description": "draft|completed|distributed"},
                        "generated_since": {"type": "string", "description": "ISO timestamp lower bound"}
                    },
                    "required": []
                }
            }
        }
