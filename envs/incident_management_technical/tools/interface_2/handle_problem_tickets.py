import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class HandleProblemTickets(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        problem_data: Optional[Dict[str, Any]] = None,
        problem_id: Optional[str] = None
    ) -> str:
        """
        Create or update problem ticket records.

        Actions:
        - create: Create a new problem ticket record (requires problem_data)
        - update: Update an existing problem ticket record (requires problem_id and problem_data)
        """

        def generate_id(table: Dict[str, Any], prefix: str) -> str:
            if not table:
                return 1
            return str(max(int(k) for k in table.keys()) + 1)

        def generate_problem_number(table: Dict[str, Any]) -> str:
            """Generate a unique problem number in format PRB0000001"""
            if not table:
                return "PRB0000001"
            max_num = 0
            for problem in table.values():
                problem_num = problem.get("problem_number", "")
                if problem_num.startswith("PRB"):
                    try:
                        num = int(problem_num[3:])
                        if num > max_num:
                            max_num = num
                    except ValueError:
                        continue
            return f"PRB{max_num + 1:07d}"

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

        problem_tickets = data.get("problem_tickets", {})
        users = data.get("users", {})

        # Define valid enums based on DBML schema
        valid_categories = ["software", "hardware", "network", "database", "security"]
        valid_statuses = ["open", "investigating", "resolved", "closed"]

        if action == "create":
            if not problem_data:
                return json.dumps({
                    "success": False,
                    "error": "problem_data is required for create action"
                })

            # Validate required fields (problem_number is now auto-generated, not required)
            required_fields = [
                "title", "description", "category",
                "reported_by", "assigned_to", "detected_at"
            ]
            missing_fields = [field for field in required_fields if field not in problem_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                })
            
            # Validate non-empty required fields
            for field in required_fields:
                if not problem_data[field] or (isinstance(problem_data[field], str) and str(problem_data[field]).strip() == ""):
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })

            # Validate enums
            if problem_data["category"] not in valid_categories:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid category '{problem_data['category']}'. Must be one of: {', '.join(valid_categories)}"
                })
            
            # Status is 'open' by default, if provided, must be valid
            status = problem_data.get("status", "open")
            if status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}"
                })

            # Validate reported_by FK
            reported_by = str(problem_data["reported_by"]).strip().strip('"')
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

            # Validate assigned_to FK
            assigned_to = str(problem_data["assigned_to"]).strip().strip('"')
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

            new_id = generate_id(problem_tickets, "PRB")
            problem_number = generate_problem_number(problem_tickets)  # Auto-generate
            
            new_problem = {
                "problem_id": new_id,
                "problem_number": problem_number,  # Auto-generated
                "title": problem_data["title"],
                "description": problem_data["description"],
                "category": problem_data["category"],
                "status": status,
                "reported_by": reported_by,
                "assigned_to": assigned_to,
                "detected_at": problem_data["detected_at"],
                "resolved_at": problem_data.get("resolved_at"),  # Nullable
                "closed_at": problem_data.get("closed_at"),  # Nullable
                "created_at": timestamp,
                "updated_at": timestamp
            }
            problem_tickets[new_id] = new_problem
            return json.dumps({
                "success": True,
                "action": "create",
                "problem_id": new_id,
                "problem_data": new_problem
            })

        elif action == "update":
            if not problem_id:
                return json.dumps({
                    "success": False,
                    "error": "problem_id is required for update action"
                })
            problem_id = str(problem_id).strip().strip('"')
            if problem_id not in problem_tickets:
                return json.dumps({
                    "success": False,
                    "error": f"Problem ticket '{problem_id}' not found"
                })

            if not problem_data:
                return json.dumps({
                    "success": False,
                    "error": "problem_data is required for update action"
                })

            # Allowed fields for update (problem_id, problem_number, created_at are not updatable)
            allowed_fields = [
                "title", "description", "category",
                "status", "reported_by", "assigned_to",
                "detected_at", "resolved_at", "closed_at"
            ]
            invalid_fields = [field for field in problem_data if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for update: {', '.join(invalid_fields)}"
                })
            
            # Validate non-empty fields (nullable fields can be None)
            # NOT NULL fields: title, description, category, reported_by, assigned_to, detected_at
            nullable_fields = ["resolved_at", "closed_at"]
            for field, value in problem_data.items():
                if field not in nullable_fields and (value is None or (isinstance(value, str) and str(value).strip() == "")):
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })
                elif field in nullable_fields and (isinstance(value, str) and str(value).strip() == ""):
                    problem_data[field] = None  # Treat empty string as null for nullable fields

            # Validate enums if provided
            if "category" in problem_data and problem_data["category"] not in valid_categories:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid category '{problem_data['category']}'. Must be one of: {', '.join(valid_categories)}"
                })
            if "status" in problem_data and problem_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status '{problem_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                })

            # Validate reported_by FK if provided
            if "reported_by" in problem_data:
                reported_by = str(problem_data["reported_by"]).strip().strip('"')
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
                problem_data["reported_by"] = reported_by

            # Validate assigned_to FK if provided
            if "assigned_to" in problem_data:
                assigned_to = str(problem_data["assigned_to"]).strip().strip('"')
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
                problem_data["assigned_to"] = assigned_to

            updated_problem = problem_tickets[problem_id].copy()
            for key, value in problem_data.items():
                updated_problem[key] = value
            updated_problem["updated_at"] = timestamp
            problem_tickets[problem_id] = updated_problem
            return json.dumps({
                "success": True,
                "action": "update",
                "problem_id": problem_id,
                "problem_data": updated_problem
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_problem_tickets",
                "description": "Create or update problem ticket records in the system. Problem tickets represent underlying issues that may cause multiple incidents.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to add a new problem ticket, 'update' to modify an existing problem ticket."
                        },
                        "problem_data": {
                            "type": "object",
                            "description": "Data object containing fields for creating or updating a problem ticket.",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "A brief, descriptive title for the problem (required for create, cannot be empty). Updatable."
                                },
                                "description": {
                                    "type": "string",
                                    "description": "A detailed description of the problem, including its symptoms and potential impact (required for create, cannot be empty). Updatable."
                                },
                                "category": {
                                    "type": "string",
                                    "description": "The category of the problem (required for create). Must be one of: software, hardware, network, database, security. Updatable.",
                                    "enum": ["software", "hardware", "network", "database", "security"]
                                },
                                "status": {
                                    "type": "string",
                                    "description": "The current status of the problem (optional for create, defaults to 'open'). Must be one of: open, investigating, resolved, closed. Updatable.",
                                    "enum": ["open", "investigating", "resolved", "closed"]
                                },
                                "reported_by": {
                                    "type": "string",
                                    "description": "The user ID of the person who reported the problem (required for create). Must refer to an existing active user. Updatable."
                                },
                                "assigned_to": {
                                    "type": "string",
                                    "description": "The user ID of the person assigned to resolve the problem (required for create). Must refer to an existing active user. Updatable."
                                },
                                "detected_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "The timestamp when the problem was detected (required for create, cannot be empty). Updatable."
                                },
                                "resolved_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "The timestamp when the problem was resolved (optional). Updatable, can be set to null."
                                },
                                "closed_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "The timestamp when the problem ticket was closed (optional). Updatable, can be set to null."
                                }
                            }
                        },
                        "problem_id": {
                            "type": "string",
                            "description": "The unique identifier of the problem ticket to update. Required for 'update' action only."
                        }
                    },
                    "required": ["action"]
                }
            }
        }