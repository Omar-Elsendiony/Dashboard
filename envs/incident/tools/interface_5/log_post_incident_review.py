import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class LogPostIncidentReview(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        scheduled_date: str,   # ISO timestamp
        facilitator_id: str,
        status: str = "scheduled"
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            pirs = data.setdefault("post_incident_reviews", {})
            valid_status = {"scheduled","completed","cancelled"}
            if status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

            pir_id = generate_id(pirs)
            timestamp = "2025-10-01T00:00:00"

            new_pir = {
                "pir_id": pir_id,
                "incident_id": incident_id,
                "scheduled_date": scheduled_date,
                "facilitator_id": facilitator_id,
                "timeline_accuracy_rating": None,
                "communication_effectiveness_rating": None,
                "technical_response_rating": None,
                "status": status,
                "created_at": timestamp
            }

            pirs[pir_id] = new_pir
            return json.dumps({"pir_id": pir_id, "status": status, "success": True})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return  {
            "type": "function",
            "function": {
                "name": "log_post_incident_review",
                "description": "Create a post-incident review; sets created_at and initializes rating fields",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string"},
                        "scheduled_date": {"type": "string", "description": "ISO timestamp"},
                        "facilitator_id": {"type": "string"},
                        "status": {"type": "string", "description": "scheduled|completed|cancelled (default scheduled)"}
                    },
                    "required": ["incident_id","scheduled_date","facilitator_id"]
                }
            }
        }
