import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManageIncidentReports(Tool):
    """
    Create and update incident reports for tracking and documenting incidents.
    """
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        report_id: Optional[str] = None,
        incident_id: Optional[str] = None,
        report_title: Optional[str] = None,
        report_type: Optional[str] = None,
        report_content: Optional[str] = None,
        generated_by: Optional[str] = None
    ) -> str:
        """
        Create or update incident report records.

        Actions:
        - create: Create new incident report (requires incident_id, report_title, report_type, report_content, generated_by)
        - update: Update existing incident report (requires report_id and at least one field to update)
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        def generate_report_number(report_id: str) -> str:
            """Generate a formatted report number."""
            return f"IR{report_id.zfill(8)}"

        timestamp = "2025-10-01T12:00:00"
        reports = data.get("incident_reports", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})

        valid_report_types = ["Initial", "Progress", "Technical", "Resolution", "Executive"]
        valid_statuses = ["Draft", "In_Review", "Approved", "Published"]
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": "Invalid action. Must be 'create' or 'update'"
            })

        if action == "update" and not report_id:
            return json.dumps({
                "success": False,
                "error": "report_id is required for update action"
            })

        if action == "create":
            if not all([incident_id, report_title, report_type, report_content, generated_by]):
                return json.dumps({
                    "success": False,
                    "error": "incident_id, report_title, report_type, report_content, and generated_by are required for create action"
                })

            # Validate incident exists
            if incident_id not in incidents:
                return json.dumps({
                    "success": False,
                    "error": f"Incident with ID {incident_id} not found"
                })

            # Validate user exists and is active
            if generated_by not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User with ID {generated_by} not found"
                })
            if users[generated_by]["status"] != "active":
                return json.dumps({
                    "success": False,
                    "error": f"User with ID {generated_by} is not active"
                })

            if report_type not in valid_report_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid report_type. Must be one of: {', '.join(valid_report_types)}"
                })

            if not report_title.strip():
                return json.dumps({
                    "success": False,
                    "error": "report_title cannot be empty"
                })

            if not report_content.strip():
                return json.dumps({
                    "success": False,
                    "error": "report_content cannot be empty"
                })

            new_id = generate_id(reports)
            report_number = generate_report_number(new_id)
            new_report = {
                "report_id": new_id,
                "report_number": report_number,
                "incident_id": incident_id,
                "report_title": report_title,
                "report_type": report_type,
                "report_content": report_content,
                "generated_by": generated_by,
                "generation_date": timestamp,
                "report_status": "Draft",
                "created_at": timestamp,
                "updated_at": timestamp,
                "last_modified_by": generated_by,
                "version": 1
            }
            reports[new_id] = new_report

            return json.dumps({
                "success": True,
                "action": "create",
                "report_id": new_id,
                "report_number": report_number,
                "report_data": new_report
            })

        if action == "update":
            if report_id not in reports:
                return json.dumps({
                    "success": False,
                    "error": f"Report with ID {report_id} not found"
                })

            # Validate at least one field is being updated
            if all(v is None for v in [report_title, report_type, report_content, generated_by]):
                return json.dumps({
                    "success": False,
                    "error": "At least one field must be provided for update"
                })

            existing_report = reports[report_id]

            if generated_by is not None:
                if generated_by not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"User with ID {generated_by} not found"
                    })
                if users[generated_by]["status"] != "active":
                    return json.dumps({
                        "success": False,
                        "error": f"User with ID {generated_by} is not active"
                    })

            if report_type is not None:
                if report_type not in valid_report_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid report_type. Must be one of: {', '.join(valid_report_types)}"
                    })
                existing_report["report_type"] = report_type

            if report_title is not None:
                if not report_title.strip():
                    return json.dumps({
                        "success": False,
                        "error": "report_title cannot be empty"
                    })
                existing_report["report_title"] = report_title

            if report_content is not None:
                if not report_content.strip():
                    return json.dumps({
                        "success": False,
                        "error": "report_content cannot be empty"
                    })
                existing_report["report_content"] = report_content
                existing_report["version"] += 1

            if generated_by is not None:
                existing_report["last_modified_by"] = generated_by

            existing_report["updated_at"] = timestamp

            return json.dumps({
                "success": True,
                "action": "update",
                "report_id": report_id,
                "report_number": existing_report["report_number"],
                "report_data": existing_report
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns comprehensive information about the tool's capabilities, parameters, and data schema.
        """
        return {
            "type": "function",
            "function": {
                "name": "manage_incident_reports",
                "description": "Create/update incident reports for formal documentation. Actions: 'create' (requires incident_id, report_title, report_type, report_content, generated_by), 'update' (requires report_id; optional: report_title, report_type, report_content, generated_by).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' or 'update'",
                            "enum": ["create", "update"]
                        },
                        "report_id": {
                            "type": "string",
                            "description": "Required for update. ID of the report to update"
                        },
                        "incident_id": {
                            "type": "string",
                            "description": "Required for create. ID of the incident this report belongs to"
                        },
                        "report_title": {
                            "type": "string",
                            "description": "Title/summary of the report (must not be empty)"
                        },
                        "report_type": {
                            "type": "string",
                            "description": "Type of incident report: Initial (first report), Progress (updates), Technical (detailed analysis), Resolution (final report), Executive (high-level summary)",
                            "enum": ["Initial", "Progress", "Technical", "Resolution", "Executive"]
                        },
                        "report_content": {
                            "type": "string",
                            "description": "Detailed content of the report (must not be empty)"
                        },
                        "generated_by": {
                            "type": "string",
                            "description": "ID of the active user creating/updating the report"
                        }
                    },
                    "required": ["action"]
                }
            }
        }