import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class RetrieveRootCauseAnalyses(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        rca_id: str = None,
        incident_id: str = None,
        conducted_by_id: str = None,
        analysis_method: str = None,
        status: str = None
    ) -> str:
        try:
            rcas: Dict[str, Any] = data.get("root_cause_analysis", {}) or data.get("root_cause_analyses", {}) or data.get("root_cause_analysis_records", {})
            # Normalize: prefer a single dict key
            if not rcas:
                rcas = data.get("root_cause_analysis", {})
            results: List[Dict[str, Any]] = []

            for r in rcas.values():
                if rca_id and r.get("rca_id") != rca_id:
                    continue
                if incident_id and r.get("incident_id") != incident_id:
                    continue
                if conducted_by_id and r.get("conducted_by_id") != conducted_by_id:
                    continue
                if analysis_method and r.get("analysis_method") != analysis_method:
                    continue
                if status and r.get("status") != status:
                    continue
                results.append(r)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_root_cause_analyses",
                "description": "Unified list/get for root cause analysis (RCA) records",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "rca_id": {"type": "string"},
                        "incident_id": {"type": "string"},
                        "conducted_by_id": {"type": "string"},
                        "analysis_method": {"type": "string", "description": "five_whys|fishbone|timeline_analysis|fault_tree"},
                        "status": {"type": "string", "description": "in_progress|completed|approved"}
                    },
                    "required": []
                }
            }
        }
