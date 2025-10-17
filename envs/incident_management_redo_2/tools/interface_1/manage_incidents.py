import json
import os
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageIncidents(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        incident_id: Optional[str] = None,
        incident_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        # Always resolve the correct "data" directory inside this environment
        TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
        ENV_DIR = os.path.dirname(TOOL_DIR)
        DATA_DIR = os.path.join(ENV_DIR, "data")
        INCIDENTS_FP = os.path.join(DATA_DIR, "incidents.json")

        def ensure_dirs() -> None:
            os.makedirs(DATA_DIR, exist_ok=True)

        def load_incidents() -> Dict[str, Any]:
            """Read incidents from the correct JSON file."""
            if os.path.exists(INCIDENTS_FP):
                try:
                    with open(INCIDENTS_FP, "r") as f:
                        return json.load(f)
                except Exception:
                    return {}
            return {}

        def save_incidents(incidents_dict: Dict[str, Any]) -> None:
            """Write incidents back to the same JSON file."""
            ensure_dirs()
            with open(INCIDENTS_FP, "w") as f:
                json.dump(incidents_dict, f, indent=2)

        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        def generate_incident_number(incidents_dict: Dict[str, Any]) -> str:
            if not incidents_dict:
                return "INC0000001"
            max_num = 0
            for inc in incidents_dict.values():
                inc_num = inc.get("incident_number", "INC0000000")
                try:
                    num = int(inc_num.replace("INC", ""))
                except Exception:
                    num = 0
                if num > max_num:
                    max_num = num
            return f"INC{str(max_num + 1).zfill(7)}"

        timestamp = "2025-10-01T00:00:00"

        incidents = data.setdefault("incidents", {})
        clients = data.setdefault("clients", {})
        configuration_items = data.setdefault("configuration_items", {})
        users = data.setdefault("users", {})
        problem_tickets = data.setdefault("problem_tickets", {})

        # Load existing file contents into memory
        if not incidents:
            loaded = load_incidents()
            if loaded:
                incidents.update(loaded)

        # Validate action
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

        # ---------------- CREATE ----------------
        if action == "create":
            if not incident_data:
                return json.dumps({
                    "success": False,
                    "error": "incident_data is required for create action"
                })

            required_fields = [
                "title", "description", "client_id", "affected_ci_id",
                "severity", "impact", "urgency", "reported_by", "detection_time"
            ]
            missing = [f for f in required_fields if f not in incident_data]
            if missing:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing)}"
                })

            # Referential checks
            client_id = str(incident_data["client_id"])
            if client_id not in clients:
                return json.dumps({"success": False, "error": f"Client with ID '{client_id}' not found"})

            ci_id = str(incident_data["affected_ci_id"])
            if ci_id not in configuration_items:
                return json.dumps({"success": False, "error": f"Configuration item with ID '{ci_id}' not found"})

            reported_by = str(incident_data["reported_by"])
            if reported_by not in users:
                return json.dumps({"success": False, "error": f"User with ID '{reported_by}' not found"})

            if "assigned_to" in incident_data and incident_data["assigned_to"]:
                assigned_to = str(incident_data["assigned_to"])
                if assigned_to not in users:
                    return json.dumps({"success": False, "error": f"User with ID '{assigned_to}' not found"})

            if "problem_id" in incident_data and incident_data["problem_id"]:
                pid = str(incident_data["problem_id"])
                if pid not in problem_tickets:
                    return json.dumps({"success": False, "error": f"Problem ticket with ID '{pid}' not found"})

            # Enum validations
            valid_severities = ["P1", "P2", "P3", "P4"]
            valid_impacts = ["critical", "high", "medium", "low"]
            valid_urgencies = ["critical", "high", "medium", "low"]
            valid_categories = ["inquiry/help", "software", "hardware", "Network", "Database"]
            valid_statuses = ["open", "in_progress", "monitoring", "resolved", "closed"]

            if incident_data["severity"] not in valid_severities:
                return json.dumps({"success": False, "error": f"Invalid severity. Must be one of: {', '.join(valid_severities)}"})
            if incident_data["impact"] not in valid_impacts:
                return json.dumps({"success": False, "error": f"Invalid impact. Must be one of: {', '.join(valid_impacts)}"})
            if incident_data["urgency"] not in valid_urgencies:
                return json.dumps({"success": False, "error": f"Invalid urgency. Must be one of: {', '.join(valid_urgencies)}"})
            if "category" in incident_data and incident_data["category"]:
                if incident_data["category"] not in valid_categories:
                    return json.dumps({"success": False, "error": f"Invalid category. Must be one of: {', '.join(valid_categories)}"})
            if "status" in incident_data:
                if incident_data["status"] not in valid_statuses:
                    return json.dumps({"success": False, "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})

            # Create new record
            new_id = generate_id(incidents)
            new_number = generate_incident_number(incidents)

            new_incident = {
                "incident_id": new_id,
                "problem_id": str(incident_data["problem_id"]) if incident_data.get("problem_id") else None,
                "incident_number": new_number,
                "title": incident_data["title"],
                "description": incident_data["description"],
                "category": incident_data.get("category"),
                "client_id": client_id,
                "affected_ci_id": ci_id,
                "severity": incident_data["severity"],
                "impact": incident_data["impact"],
                "urgency": incident_data["urgency"],
                "status": incident_data.get("status", "open"),
                "reported_by": reported_by,
                "assigned_to": str(incident_data["assigned_to"]) if incident_data.get("assigned_to") else None,
                "detection_time": incident_data["detection_time"],
                "acknowledged_at": incident_data.get("acknowledged_at"),
                "resolved_at": incident_data.get("resolved_at"),
                "closed_at": incident_data.get("closed_at"),
                "created_at": timestamp,
                "updated_at": timestamp
            }

            incidents[new_id] = new_incident
            save_incidents(incidents)
            return json.dumps(new_incident)

        # ---------------- UPDATE ----------------
        elif action == "update":
            if not incident_id:
                return json.dumps({"success": False, "error": "incident_id is required for update action"})

            incident_id = str(incident_id).strip()
            if incident_id.startswith('"') and incident_id.endswith('"'):
                incident_id = incident_id[1:-1]

            if incident_id not in incidents:
                return json.dumps({"success": False, "error": f"Incident with ID '{incident_id}' not found"})

            if not incident_data:
                return json.dumps({"success": False, "error": "incident_data is required for update action"})

            current_incident = incidents[incident_id]
            updated_incident = current_incident.copy()

            for key, value in incident_data.items():
                updated_incident[key] = value

            updated_incident["updated_at"] = timestamp
            incidents[incident_id] = updated_incident
            save_incidents(incidents)
            return json.dumps(updated_incident)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_incidents",
                "description": "Create or update incident records with file persistence under envs/incident_management_redo/data/incidents.json.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string", "enum": ["create", "update"]},
                        "incident_id": {"type": "string"},
                        "incident_data": {"type": "object"}
                    },
                    "required": ["action"]
                }
            }
        }
