import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class UpdatePostIncidentReview(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        pir_id: str,
        incident_id: str = None,
        scheduled_date: str = None,
        facilitator_id: str = None,
        timeline_accuracy_rating: int = None,
        communication_effectiveness_rating: int = None,
        technical_response_rating: int = None,
        status: str = None          # scheduled|completed|cancelled
    ) -> str:
        try:
            # Local ISO validator (accepts trailing 'Z')
            def is_iso(ts: str) -> bool:
                try:
                    datetime.fromisoformat(ts.strip().replace("Z", "+00:00"))
                    return True
                except Exception:
                    return False

            pirs = data.get("post_incident_reviews", {})
            if pir_id not in pirs:
                return json.dumps({"success": False, "error": f"Post-incident review {pir_id} not found"})

            valid_status = {"scheduled","completed","cancelled"}
            if status and status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})
            if scheduled_date is not None and not is_iso(scheduled_date):
                return json.dumps({"success": False, "error": "scheduled_date must be ISO timestamp"})

            for name, val in [
                ("timeline_accuracy_rating", timeline_accuracy_rating),
                ("communication_effectiveness_rating", communication_effectiveness_rating),
                ("technical_response_rating", technical_response_rating),
            ]:
                if val is not None and val < 0:
                    return json.dumps({"success": False, "error": f"{name} must be non-negative"})

            r = pirs[pir_id]
            if incident_id is not None: r["incident_id"] = incident_id
            if scheduled_date is not None: r["scheduled_date"] = scheduled_date
            if facilitator_id is not None: r["facilitator_id"] = facilitator_id
            if timeline_accuracy_rating is not None: r["timeline_accuracy_rating"] = timeline_accuracy_rating
            if communication_effectiveness_rating is not None: r["communication_effectiveness_rating"] = communication_effectiveness_rating
            if technical_response_rating is not None: r["technical_response_rating"] = technical_response_rating
            if status is not None: r["status"] = status

            return json.dumps(r)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})
    
    @staticmethod
    def get_info()->Dict[str,Any]:
        return{
            "type":"function",
            "function":{
                "name":"update_post_incident_review",
                "description":"Update a post-incident review; validates enums/timestamps and ratings",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "pir_id":{"type":"string"},
                        "incident_id":{"type":"string"},
                        "scheduled_date":{"type":"string","description":"ISO timestamp"},
                        "facilitator_id":{"type":"string"},
                        "timeline_accuracy_rating":{"type":"integer"},
                        "communication_effectiveness_rating":{"type":"integer"},
                        "technical_response_rating":{"type":"integer"},
                        "status":{"type":"string","description":"scheduled|completed|cancelled"}
                    },
                    "required":["pir_id"]
                }
            }
        }
