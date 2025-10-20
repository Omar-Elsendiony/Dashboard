import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddressIncidents(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        incident_data: Optional[Dict[str, Any]] = None,
        incident_id: Optional[str] = None
    ) -> str:
        """
        Create or update incident records.

        Actions:
        - create: Create a new incident record (requires incident_data)
        - update: Update an existing incident record (requires incident_id and incident_data)
        """

        def generate_id(table: Dict[str, Any], prefix: str) -> str:
            if not table:
                return f"{prefix}1"
            max_id = 0
            for k in table.keys():
                try:
                    num = int(k[len(prefix):])
                    if num > max_id:
                        max_id = num
                except ValueError:
                    continue
            return f"{prefix}{max_id + 1}"

        def generate_incident_number(table: Dict[str, Any]) -> str:
            if not table:
                return "INC0000001"
            max_num = 0
            for incident in table.values():
                incident_num = incident.get("incident_number", "")
                if incident_num.startswith("INC"):
                    try:
                        num = int(incident_num[3:])
                        if num > max_num:
                            max_num = num
                    except ValueError:
                        continue
            return f"INC{max_num + 1:07d}"

        timestamp = "2025-10-07T12:00:00"

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        incidents = data.get("incidents", {})
        users = data.get("users", {})
        problem_tickets = data.get("problem_tickets", {})

        # Define valid enums based on DBML schema
        valid_categories = ["inquiry/help", "software", "hardware", "network", "database"]
        valid_severities = ["P1", "P2", "P3", "P4"]
        valid_impacts = ["low", "medium", "high", "critical"]
        valid_urgencies = ["low", "medium", "high", "critical"]
        valid_statuses = ["open", "in_progress", "monitoring", "resolved", "closed"]

        if action == "create":
            if not incident_data:
                return json.dumps({
                    "success": False,
                    "error": "incident_data is required for create action"
                })

            # Validate required fields as per DBML (incident_number is auto-generated)
            required_fields = [
                "title", "description", "category",
                "severity", "impact", "urgency", "reported_by", "detection_time"
            ]
            missing_fields = [field for field in required_fields if field not in incident_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                })
            
            # Validate non-empty required fields
            for field in required_fields:
                if not incident_data[field] or (isinstance(incident_data[field], str) and str(incident_data[field]).strip() == ""):
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })

            # Validate enums
            if incident_data["category"] not in valid_categories:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid category '{incident_data['category']}'. Must be one of: {', '.join(valid_categories)}"
                })
            if incident_data["severity"] not in valid_severities:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid severity '{incident_data['severity']}'. Must be one of: {', '.join(valid_severities)}"
                })
            if incident_data["impact"] not in valid_impacts:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid impact '{incident_data['impact']}'. Must be one of: {', '.join(valid_impacts)}"
                })
            if incident_data["urgency"] not in valid_urgencies:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid urgency '{incident_data['urgency']}'. Must be one of: {', '.join(valid_urgencies)}"
                })
            
            # Status is 'open' by default, if provided, must be valid
            status = incident_data.get("status", "open")
            if status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}"
                })

            # Validate reported_by FK
            reported_by = str(incident_data["reported_by"]).strip().strip('"')
            if reported_by not in users:
                return json.dumps({
                    "success": False,
                    "error": f"Reported by user '{reported_by}' not found"
                })
            if users[reported_by]["status"] != "active":
                return json.dumps({
                    "success": False,
                    "error": f"Reported by user '{reported_by}' is not active"
                })

            # Validate assigned_to FK if provided
            assigned_to = incident_data.get("assigned_to")
            if assigned_to:
                assigned_to = str(assigned_to).strip().strip('"')
                if assigned_to not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"Assigned to user '{assigned_to}' not found"
                    })
                if users[assigned_to]["status"] != "active":
                    return json.dumps({
                        "success": False,
                        "error": f"Assigned to user '{assigned_to}' is not active"
                    })
            
            # Validate problem_id FK if provided
            problem_id = incident_data.get("problem_id")
            if problem_id:
                problem_id = str(problem_id).strip().strip('"')
                if problem_id not in problem_tickets:
                    return json.dumps({
                        "success": False,
                        "error": f"Problem ticket '{problem_id}' not found"
                    })

            new_id = generate_id(incidents, "")
            incident_number = generate_incident_number(incidents)
            
            new_incident = {
                "incident_id": new_id,
                "problem_id": problem_id if problem_id else None,
                "incident_number": incident_number,
                "title": incident_data["title"],
                "description": incident_data["description"],
                "category": incident_data["category"],
                "severity": incident_data["severity"],
                "impact": incident_data["impact"],
                "urgency": incident_data["urgency"],
                "status": status,
                "reported_by": reported_by,
                "assigned_to": assigned_to if assigned_to else None,
                "detection_time": incident_data["detection_time"],
                "acknowledged_at": incident_data.get("acknowledged_at"), # Nullable
                "resolved_at": incident_data.get("resolved_at"), # Nullable
                "closed_at": incident_data.get("closed_at"), # Nullable
                "created_at": timestamp,
                "updated_at": timestamp
            }
            incidents[new_id] = new_incident
            return json.dumps({
                "success": True,
                "action": "create",
                "incident_id": new_id,
                "incident_data": new_incident
            })

        elif action == "update":
            if not incident_id:
                return json.dumps({
                    "success": False,
                    "error": "incident_id is required for update action"
                })
            incident_id = str(incident_id).strip().strip('"')
            if incident_id not in incidents:
                return json.dumps({
                    "success": False,
                    "error": f"Incident '{incident_id}' not found"
                })

            if not incident_data:
                return json.dumps({
                    "success": False,
                    "error": "incident_data is required for update action"
                })

            # Allowed fields for update (incident_id, incident_number, created_at are not updatable)
            allowed_fields = [
                "problem_id", "title", "description", "category",
                "severity", "impact", "urgency", "status", "reported_by",
                "assigned_to", "detection_time", "acknowledged_at", "resolved_at", "closed_at"
            ]
            invalid_fields = [field for field in incident_data if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for update: {', '.join(invalid_fields)}"
                })
            
            # Validate non-empty fields (if provided, they shouldn't be empty strings, but nullable fields can be None)
            # Note: title, description, category, severity, impact, urgency, reported_by, detection_time are NOT NULL
            nullable_fields = [
                "problem_id", "assigned_to", "acknowledged_at", "resolved_at", "closed_at"
            ]
            for field, value in incident_data.items():
                if field not in nullable_fields and (value is None or (isinstance(value, str) and str(value).strip() == "")):
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })
                elif field in nullable_fields and (isinstance(value, str) and str(value).strip() == ""):
                    incident_data[field] = None # Treat empty string as null for nullable fields

            # Validate enums if provided
            if "category" in incident_data and incident_data["category"] not in valid_categories:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid category '{incident_data['category']}'. Must be one of: {', '.join(valid_categories)}"
                })
            if "severity" in incident_data and incident_data["severity"] not in valid_severities:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid severity '{incident_data['severity']}'. Must be one of: {', '.join(valid_severities)}"
                })
            if "impact" in incident_data and incident_data["impact"] not in valid_impacts:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid impact '{incident_data['impact']}'. Must be one of: {', '.join(valid_impacts)}"
                })
            if "urgency" in incident_data and incident_data["urgency"] not in valid_urgencies:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid urgency '{incident_data['urgency']}'. Must be one of: {', '.join(valid_urgencies)}"
                })
            if "status" in incident_data and incident_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status '{incident_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                })

            # Validate reported_by FK if provided
            if "reported_by" in incident_data:
                reported_by = str(incident_data["reported_by"]).strip().strip('"')
                if reported_by not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"Reported by user '{reported_by}' not found"
                    })
                if users[reported_by]["status"] != "active":
                    return json.dumps({
                        "success": False,
                        "error": f"Reported by user '{reported_by}' is not active"
                    })
                incident_data["reported_by"] = reported_by

            # Validate assigned_to FK if provided
            if "assigned_to" in incident_data and incident_data["assigned_to"] is not None:
                assigned_to = str(incident_data["assigned_to"]).strip().strip('"')
                if assigned_to not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"Assigned to user '{assigned_to}' not found"
                    })
                if users[assigned_to]["status"] != "active":
                    return json.dumps({
                        "success": False,
                        "error": f"Assigned to user '{assigned_to}' is not active"
                    })
                incident_data["assigned_to"] = assigned_to
            elif "assigned_to" in incident_data and incident_data["assigned_to"] is None:
                incident_data["assigned_to"] = None # Allow setting to null

            # Validate problem_id FK if provided
            if "problem_id" in incident_data and incident_data["problem_id"] is not None:
                problem_id = str(incident_data["problem_id"]).strip().strip('"')
                if problem_id not in problem_tickets:
                    return json.dumps({
                        "success": False,
                        "error": f"Problem ticket '{problem_id}' not found"
                    })
                incident_data["problem_id"] = problem_id
            elif "problem_id" in incident_data and incident_data["problem_id"] is None:
                incident_data["problem_id"] = None # Allow setting to null

            updated_incident = incidents[incident_id].copy()
            for key, value in incident_data.items():
                updated_incident[key] = value
            updated_incident["updated_at"] = timestamp
            incidents[incident_id] = updated_incident
            return json.dumps({
                "success": True,
                "action": "update",
                "incident_id": incident_id,
                "incident_data": updated_incident
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "address_incidents",
                "description": "Create or update incident records in the system. This tool allows for managing incident details, including linking to problem tickets, assigning to users, and tracking status. Incident numbers are automatically generated.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to add a new incident, 'update' to modify an existing incident."
                        },
                        "incident_data": {
                            "type": "object",
                            "description": "Data object containing fields for creating or updating an incident.",
                            "properties": {
                                "problem_id": {
                                    "type": "string",
                                    "description": "The ID of the associated problem ticket (optional). Must refer to an existing problem ticket. Updatable, can be set to null."
                                },
                                "title": {
                                    "type": "string",
                                    "description": "A brief, descriptive title for the incident (required for create, cannot be empty). Updatable."
                                },
                                "description": {
                                    "type": "string",
                                    "description": "A detailed description of the incident, including symptoms and impact (required for create, cannot be empty). Updatable."
                                },
                                "category": {
                                    "type": "string",
                                    "description": "The category of the incident (required for create). Must be one of: inquiry/help, software, hardware, Network, Database. Updatable.",
                                    "enum": ["inquiry/help", "software", "hardware", "Network", "Database"]
                                },
                                "severity": {
                                    "type": "string",
                                    "description": "The severity level of the incident (required for create). Must be one of: P1, P2, P3, P4. Updatable.",
                                    "enum": ["P1", "P2", "P3", "P4"]
                                },
                                "impact": {
                                    "type": "string",
                                    "description": "The impact of the incident on services or users (required for create). Must be one of: low, medium, high, critical. Updatable.",
                                    "enum": ["low", "medium", "high", "critical"]
                                },
                                "urgency": {
                                    "type": "string",
                                    "description": "The urgency of resolving the incident (required for create). Must be one of: low, medium, high, critical. Updatable.",
                                    "enum": ["low", "medium", "high", "critical"]
                                },
                                "status": {
                                    "type": "string",
                                    "description": "The current status of the incident (optional for create, defaults to 'open'). Must be one of: open, in_progress, monitoring, resolved, closed. Updatable.",
                                    "enum": ["open", "in_progress", "monitoring", "resolved", "closed"]
                                },
                                "reported_by": {
                                    "type": "string",
                                    "description": "The user ID of the person who reported the incident (required for create). Must refer to an existing active user. Updatable."
                                },
                                "assigned_to": {
                                    "type": "string",
                                    "description": "The user ID of the person assigned to resolve the incident (optional). Must refer to an existing active user. Updatable, can be set to null."
                                },
                                "detection_time": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "The timestamp when the incident was detected (required for create, cannot be empty). Updatable."
                                },
                                "acknowledged_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "The timestamp when the incident was acknowledged (optional). Updatable, can be set to null."
                                },
                                "resolved_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "The timestamp when the incident was resolved (optional). Updatable, can be set to null."
                                },
                                "closed_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "The timestamp when the incident was closed (optional). Updatable, can be set to null."
                                }
                            }
                        },
                        "incident_id": {
                            "type": "string",
                            "description": "The unique identifier of the incident to update. Required for 'update' action only."
                        }
                    },
                    "required": ["action"]
                }
            }
        }