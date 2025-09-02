import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AmendIncident(Tool):
    """
    Update fields on an incident in the incidents table.
    No ID existence validations (agent ensures correctness).
    Does NOT write to incident_updates (use create_incident_record first per SOP).
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        status: Optional[str] = None,
        severity: Optional[str] = None,
        assigned_manager_id: Optional[str] = None,
        component_id: Optional[str] = None,
        category: Optional[str] = None,
        impact: Optional[str] = None,
        urgency: Optional[str] = None
    ) -> str:
        incidents = data.setdefault("incidents", {})
        # Ensure a dict exists for the target key without validating presence
        incident = incidents.setdefault(incident_id, {"incident_id": incident_id})

        valid_status = {"open","in_progress","resolved","closed"}
        valid_sev = {"P1","P2","P3","P4"}
        valid_level = {"critical","high","medium","low"}

        # Enum checks only
        if status is not None and status not in valid_status:
            return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})
        if severity is not None and severity not in valid_sev:
            return json.dumps({"success": False, "error": f"Invalid severity. Must be one of {sorted(valid_sev)}"})
        if impact is not None and impact not in valid_level:
            return json.dumps({"success": False, "error": f"Invalid impact. Must be one of {sorted(valid_level)}"})
        if urgency is not None and urgency not in valid_level:
            return json.dumps({"success": False, "error": f"Invalid urgency. Must be one of {sorted(valid_level)}"})

        ts = "2025-09-02T23:59:59"

        # Apply changes (no audit rows here)
        if status is not None:
            prev = incident.get("status")
            incident["status"] = status
            # Lifecycle timestamps on transitions (if not already present)
            if status == "resolved" and not incident.get("resolved_at"):
                incident["resolved_at"] = ts
            if status == "closed" and not incident.get("closed_at"):
                incident["closed_at"] = ts

        if severity is not None:
            incident["severity"] = severity

        if assigned_manager_id is not None:
            incident["assigned_manager_id"] = assigned_manager_id

        if component_id is not None:
            incident["component_id"] = component_id

        if category is not None:
            incident["category"] = category

        if impact is not None:
            incident["impact"] = impact

        if urgency is not None:
            incident["urgency"] = urgency

        incident["updated_at"] = ts
        return json.dumps({"success": True, "data": incident})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "amend_incident",
                "description": "Apply field updates to an incident. Call create_incident_record first per SOP.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string"},
                        "status": {"type": "string", "description": "open|in_progress|resolved|closed"},
                        "severity": {"type": "string", "description": "P1|P2|P3|P4"},
                        "assigned_manager_id": {"type": "string"},
                        "component_id": {"type": "string"},
                        "category": {"type": "string"},
                        "impact": {"type": "string", "description": "critical|high|medium|low"},
                        "urgency": {"type": "string", "description": "critical|high|medium|low"}
                    },
                    "required": ["incident_id"]
                }
            }
        }
