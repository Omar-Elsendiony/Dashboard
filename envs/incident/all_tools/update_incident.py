import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateIncident(Tool):
    @staticmethod
    def _record_update(updates_table: Dict[str, Any], incident_id: str, update_type: str, field_name: str, old_value: Any, new_value: Any):
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        update_id = generate_id(updates_table)
        timestamp = "2025-10-01T00:00:00"
        updates_table[update_id] = {
            "update_id": update_id,
            "incident_id": incident_id,
            "updated_by_id": "system",  # no actor param; using system as placeholder
            "update_type": update_type, # status_change|severity_change|assignment|workaround|resolution|communication
            "field_name": field_name,
            "old_value": None if old_value is None else str(old_value),
            "new_value": None if new_value is None else str(new_value),
            "created_at": timestamp
        }

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        status: str = None,
        severity: str = None,
        assigned_manager_id: str = None,
        component_id: str = None,
        category: str = None,
        impact: str = None,
        urgency: str = None,
        note: str = None
    ) -> str:
        try:
            incidents = data.get("incidents", {})
            if incident_id not in incidents:
                return json.dumps({"success": False, "error": f"Incident {incident_id} not found"})

            incident = incidents[incident_id]
            updates_table = data.setdefault("incident_updates", {})

            valid_status = {"open","in_progress","resolved","closed"}
            valid_sev = {"P1","P2","P3","P4"}
            valid_level = {"critical","high","medium","low"}

            timestamp = "2025-10-01T00:00:00"

            # Field-by-field updates with audit
            if status is not None:
                if status not in valid_status:
                    return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})
                if incident.get("status") != status:
                    UpdateIncident._record_update(updates_table, incident_id, "status_change", "status", incident.get("status"), status)
                    incident["status"] = status
                    if status == "resolved" and not incident.get("resolved_at"):
                        incident["resolved_at"] = timestamp
                        UpdateIncident._record_update(updates_table, incident_id, "resolution", "resolved_at", None, timestamp)
                    if status == "closed" and not incident.get("closed_at"):
                        incident["closed_at"] = timestamp
                        UpdateIncident._record_update(updates_table, incident_id, "status_change", "closed_at", None, timestamp)

            if severity is not None:
                if severity not in valid_sev:
                    return json.dumps({"success": False, "error": f"Invalid severity. Must be one of {sorted(valid_sev)}"})
                if incident.get("severity") != severity:
                    UpdateIncident._record_update(updates_table, incident_id, "severity_change", "severity", incident.get("severity"), severity)
                    incident["severity"] = severity

            if assigned_manager_id is not None and incident.get("assigned_manager_id") != assigned_manager_id:
                UpdateIncident._record_update(updates_table, incident_id, "assignment", "assigned_manager_id", incident.get("assigned_manager_id"), assigned_manager_id)
                incident["assigned_manager_id"] = assigned_manager_id

            if component_id is not None and incident.get("component_id") != component_id:
                UpdateIncident._record_update(updates_table, incident_id, "assignment", "component_id", incident.get("component_id"), component_id)
                incident["component_id"] = component_id

            if category is not None and incident.get("category") != category:
                UpdateIncident._record_update(updates_table, incident_id, "status_change", "category", incident.get("category"), category)
                incident["category"] = category

            if impact is not None:
                if impact not in valid_level:
                    return json.dumps({"success": False, "error": f"Invalid impact. Must be one of {sorted(valid_level)}"})
                if incident.get("impact") != impact:
                    UpdateIncident._record_update(updates_table, incident_id, "status_change", "impact", incident.get("impact"), impact)
                    incident["impact"] = impact

            if urgency is not None:
                if urgency not in valid_level:
                    return json.dumps({"success": False, "error": f"Invalid urgency. Must be one of {sorted(valid_level)}"})
                if incident.get("urgency") != urgency:
                    UpdateIncident._record_update(updates_table, incident_id, "status_change", "urgency", incident.get("urgency"), urgency)
                    incident["urgency"] = urgency

            if note is not None and note != "":
                # Log a communication-type audit entry; incident record itself does not store the note
                UpdateIncident._record_update(updates_table, incident_id, "communication", "note", None, note)

            incident["updated_at"] = timestamp
            return json.dumps({"success": True, "data": incident})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_incident",
                "description": "Update incident fields; write audit rows; set resolved_at/closed_at when status transitions; update updated_at",
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
                        "urgency": {"type": "string", "description": "critical|high|medium|low"},
                        "note": {"type": "string", "description": "Free-form note to log as communication"}
                    },
                    "required": ["incident_id"]
                }
            }
        }
