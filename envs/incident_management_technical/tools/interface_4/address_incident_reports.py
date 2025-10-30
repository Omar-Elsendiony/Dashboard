import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddressIncidentReports(Tool):
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
        generated_by: Optional[str] = None,
        report_status: Optional[str] = None
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
            return f"RPT{report_id.zfill(7)}"

        timestamp = "2025-10-07T12:00:00"
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        reports = data.get("incident_reports", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})

        valid_report_types = ["post_incident_review", "client_impact", "compliance"]
        valid_statuses = ["draft", "completed", "approved", "archived"]
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": "Invalid action. Must be 'create' or 'update'"
            })

        if action == "create":
            # Validate required fields are provided
            if not all([incident_id, report_title, report_type, report_content, generated_by]):
                missing_fields = []
                if not incident_id: missing_fields.append("incident_id")
                if not report_title: missing_fields.append("report_title")
                if not report_type: missing_fields.append("report_type")
                if not report_content: missing_fields.append("report_content")
                if not generated_by: missing_fields.append("generated_by")
                
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                })

            # Validate non-empty required fields
            if not str(incident_id).strip():
                return json.dumps({
                    "success": False,
                    "error": "Field 'incident_id' cannot be empty"
                })
            
            if not str(report_title).strip():
                return json.dumps({
                    "success": False,
                    "error": "Field 'report_title' cannot be empty"
                })
            
            if not str(report_type).strip():
                return json.dumps({
                    "success": False,
                    "error": "Field 'report_type' cannot be empty"
                })
            
            if not str(report_content).strip():
                return json.dumps({
                    "success": False,
                    "error": "Field 'report_content' cannot be empty"
                })
            
            if not str(generated_by).strip():
                return json.dumps({
                    "success": False,
                    "error": "Field 'generated_by' cannot be empty"
                })

            # Validate incident exists
            if str(incident_id) not in incidents:
                return json.dumps({
                    "success": False,
                    "error": f"Incident with ID {incident_id} not found"
                })
            
            # Validate incident status is resolved or closed
            incident = incidents[str(incident_id)]
            if incident["status"] not in ["resolved", "closed"]:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Incident must have status 'resolved' or 'closed' to generate report"
                })

            # Validate user exists and is active
            if str(generated_by) not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User with ID {generated_by} not found"
                })
            if users[str(generated_by)]["status"] != "active":
                return json.dumps({
                    "success": False,
                    "error": f"User with ID {generated_by} is not active"
                })

            if report_type not in valid_report_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid report_type. Must be one of: {', '.join(valid_report_types)}"
                })

            new_id = generate_id(reports)
            report_number = generate_report_number(new_id)
            new_report = {
                "report_id": new_id,
                "report_number": report_number,
                "report_title": report_title,
                "incident_id": str(incident_id),
                "report_type": report_type,
                "report_content": report_content,
                "generated_by": str(generated_by),
                "generation_date": timestamp,
                "report_status": "draft"
            }
            reports[new_id] = new_report

            return json.dumps({
                "success": True,
                "action": "create",
                "report_id": new_id,
                "report_number": report_number,
                "report_data": new_report
            })

        elif action == "update":
            if not report_id:
                return json.dumps({
                    "success": False,
                    "error": "report_id is required for update action"
                })

            if str(report_id) not in reports:
                return json.dumps({
                    "success": False,
                    "error": f"Report with ID {report_id} not found"
                })

            # Validate at least one field is being updated
            if all(v is None for v in [report_title, report_type, report_content, report_status]):
                return json.dumps({
                    "success": False,
                    "error": "At least one field must be provided for update"
                })

            existing_report = reports[str(report_id)]

            # Validate non-empty fields
            if report_title is not None and not str(report_title).strip():
                return json.dumps({
                    "success": False,
                    "error": "Field 'report_title' cannot be empty"
                })

            if report_type is not None and not str(report_type).strip():
                return json.dumps({
                    "success": False,
                    "error": "Field 'report_type' cannot be empty"
                })

            if report_content is not None and not str(report_content).strip():
                return json.dumps({
                    "success": False,
                    "error": "Field 'report_content' cannot be empty"
                })

            if report_status is not None and not str(report_status).strip():
                return json.dumps({
                    "success": False,
                    "error": "Field 'report_status' cannot be empty"
                })

            if report_type is not None:
                if report_type not in valid_report_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid report_type. Must be one of: {', '.join(valid_report_types)}"
                    })
                existing_report["report_type"] = report_type

            if report_title is not None:
                existing_report["report_title"] = report_title

            if report_content is not None:
                existing_report["report_content"] = report_content

            if report_status is not None:
                if report_status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid report_status. Must be one of: {', '.join(valid_statuses)}"
                    })
                existing_report["report_status"] = report_status

            return json.dumps({
                "success": True,
                "action": "update",
                "report_id": str(report_id),
                "report_number": existing_report["report_number"],
                "report_data": existing_report
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "address_incident_reports",
                "description": "Create or update incident reports for formal documentation and tracking. Manages comprehensive incident reporting including post-incident reviews, client impact assessments, and compliance documentation. Validates report types, user permissions, and maintains report status workflow.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to create new report or 'update' to modify existing report"
                        },
                        "report_id": {
                            "type": "string",
                            "description": "Unique identifier of the report. Required for update action only."
                        },
                        "incident_id": {
                            "type": "string",
                            "description": "Identifier of the incident this report belongs to (required for create, cannot be empty, must exist in system)"
                        },
                        "report_title": {
                            "type": "string",
                            "description": "Title or summary of the report (required for create, cannot be empty)"
                        },
                        "report_type": {
                            "type": "string",
                            "description": "Type of incident report (required for create). Must be one of: post_incident_review, client_impact, compliance"
                        },
                        "report_content": {
                            "type": "string",
                            "description": "Detailed content of the report (required for create, cannot be empty)"
                        },
                        "generated_by": {
                            "type": "string",
                            "description": "User identifier who created the report (required for create, cannot be empty, must be active user)"
                        },
                        "report_status": {
                            "type": "string",
                            "description": "Status of the report (optional for update). Must be one of: draft, completed, approved, archived"
                        }
                    },
                    "required": ["action"]
                }
            }
        }