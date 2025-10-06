import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManipulateIncidentReports(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, report_data: Dict[str, Any] = None, report_id: str = None) -> str:
        """
        Generate or update incident reports.

        Actions:
        - create: Generate new incident report (requires report_data with incident_id, report_type, generated_by_id)
        - update: Update existing incident report (requires report_id and report_data with fields to change)
        """
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

        incident_reports = data.get("incident_reports", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})

        valid_report_types = ["executive_summary", "technical_details", "business_impact", "compliance_report", "post_mortem"]
        valid_statuses = ["draft", "completed", "distributed"]
        # valid_roles = ["incident_manager", "executive"]

        if action == "create":
            if not report_data:
                return json.dumps({
                    "success": False,
                    "error": "report_data is required for create action"
                })

            required_fields = ["incident_id", "report_type", "generated_by_id"]
            missing = [f for f in required_fields if f not in report_data or not report_data.get(f)]
            if missing:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for report creation: {', '.join(missing)}"
                })

            incident_id = str(report_data["incident_id"])
            report_type = report_data["report_type"]
            generated_by_id = str(report_data["generated_by_id"])
            status = report_data.get("status")

            # Validate incident
            if incident_id not in incidents:
                return json.dumps({
                    "success": False,
                    "error": f"Incident {incident_id} not found"
                })

            # Validate user
            if generated_by_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User {generated_by_id} not found"
                })

            # Validate report type
            if report_type not in valid_report_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid report_type. Must be one of: {', '.join(valid_report_types)}"
                })

            # Post-mortem incident status validation
            if report_type == "post_mortem":
                incident_status = incidents[incident_id].get("status")
                if incident_status not in ["resolved", "closed"]:
                    return json.dumps({
                        "success": False,
                        "error": f"Incident must be 'resolved' or 'closed' for post_mortem report. Current status: {incident_status}"
                    })

            if status and status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })

            # Generate report
            new_id = generate_id(incident_reports)
            new_report = {
                "report_id": str(new_id),
                "incident_id": incident_id,
                "report_type": report_type,
                "generated_by_id": generated_by_id,
                "generated_at": "2025-10-02T12:00:00",
                "status": status if status else "draft",
                "created_at": "2025-10-02T12:00:00",
                "updated_at": "2025-10-02T12:00:00"
            }

            incident_reports[str(new_id)] = new_report

            return json.dumps({
                "success": True,
                "action": "create",
                "report_id": str(new_id),
                "message": f"Incident report {new_id} created successfully",
                "incident_report_data": new_report
            })

        elif action == "update":
            if not report_id:
                return json.dumps({
                    "success": False,
                    "error": "report_id is required for update action"
                })

            if report_id not in incident_reports:
                return json.dumps({
                    "success": False,
                    "error": f"Incident report {report_id} not found"
                })

            if not report_data:
                return json.dumps({
                    "success": False,
                    "error": "report_data is required for update action"
                })

            current_report = incident_reports[report_id].copy()

            # Update allowed fields
            allowed_update_fields = ["report_type", "status", "generated_by_id"]
            invalid_fields = [k for k in report_data.keys() if k not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for report update: {', '.join(invalid_fields)}"
                })

            if "report_type" in report_data:
                rt = report_data["report_type"]
                if rt not in valid_report_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid report_type. Must be one of: {', '.join(valid_report_types)}"
                    })
                current_report["report_type"] = rt

            if "status" in report_data:
                st = report_data["status"]
                if st not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
                current_report["status"] = st

            if "generated_by_id" in report_data:
                gid = str(report_data["generated_by_id"])
                if gid not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"User {gid} not found"
                    })
                
                current_report["generated_by_id"] = gid

            current_report["updated_at"] = "2025-10-02T12:00:00"
            incident_reports[report_id] = current_report

            return json.dumps({
                "success": True,
                "action": "update",
                "report_id": report_id,
                "message": f"Incident report {report_id} updated successfully",
                "incident_report_data": current_report
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manipulate_incident_reports",
                "description": "Generate or update incident reports in the incident management system. Supports executive summaries, technical details, business impact, compliance reports, and post-mortem reports. Restricted to incident managers and executives. Post-mortem reports only allowed for resolved or closed incidents.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' or 'update'",
                            "enum": ["create", "update"]
                        },
                        "report_data": {
                            "type": "object",
                            "description": "Incident report data object. For create: requires incident_id, report_type, generated_by_id. For update: include fields to modify. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "incident_id": {"type": "string", "description": "ID of the incident (required for create)"},
                                "report_type": {
                                    "type": "string",
                                    "description": "Type of report (required for create)",
                                    "enum": ["executive_summary", "technical_details", "business_impact", "compliance_report", "post_mortem"]
                                },
                                "generated_by_id": {"type": "string", "description": "ID of the user generating the report (required for create)"},
                                "status": {"type": "string", "description": "Current status (optional)", "enum": ["draft", "completed", "distributed"]}
                            }
                        },
                        "report_id": {"type": "string", "description": "Unique identifier of the report (required for update action only)"}
                    },
                    "required": ["action"]
                }
            }
        }
