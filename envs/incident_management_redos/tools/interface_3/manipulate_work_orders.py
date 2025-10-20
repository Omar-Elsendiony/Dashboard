import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManipulateWorkOrders(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        work_order_data: Optional[Dict[str, Any]] = None,
        work_order_id: Optional[str] = None
    ) -> str:
        """
        Create or update work order records.

        Actions:
        - create: Create a new work order record (requires work_order_data)
        - update: Update an existing work order record (requires work_order_id and work_order_data)
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

        work_orders = data.get("work_orders", {})
        users = data.get("users", {})
        change_requests = data.get("change_requests", {})
        incidents = data.get("incidents", {})

        # Define valid enums based on DBML schema
        valid_statuses = ["pending", "in_progress", "completed", "cancelled"]

        if action == "create":
            if not work_order_data:
                return json.dumps({
                    "success": False,
                    "error": "work_order_data is required for create action"
                })

            # Validate required fields as per DBML schema
            required_fields = [
                "work_order_number", "title", "description", "assigned_to", "scheduled_date"
            ]
            missing_fields = [field for field in required_fields if field not in work_order_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                })
            
            # Validate non-empty required fields
            for field in required_fields:
                if not work_order_data[field] or (isinstance(work_order_data[field], str) and str(work_order_data[field]).strip() == ""):
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })

            # Validate work_order_number uniqueness
            work_order_number = str(work_order_data["work_order_number"]).strip()
            for work_order in work_orders.values():
                if work_order["work_order_number"].lower() == work_order_number.lower():
                    return json.dumps({
                        "success": False,
                        "error": f"Work order with number '{work_order_number}' already exists."
                    })

            # Status is 'pending' by default, if provided, must be valid
            status = work_order_data.get("status", "pending")
            if status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}"
                })

            # Validate assigned_to FK
            assigned_to = str(work_order_data["assigned_to"]).strip().strip('"')
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

            # Validate change_id FK if provided (nullable)
            change_id = work_order_data.get("change_id")
            if change_id:
                change_id = str(change_id).strip().strip('"')
                if change_id not in change_requests:
                    return json.dumps({
                        "success": False,
                        "error": f"Change request '{change_id}' not found"
                    })

            # Validate incident_id FK if provided (nullable)
            incident_id = work_order_data.get("incident_id")
            if incident_id:
                incident_id = str(incident_id).strip().strip('"')
                if incident_id not in incidents:
                    return json.dumps({
                        "success": False,
                        "error": f"Incident '{incident_id}' not found"
                    })

            new_id = generate_id(work_orders, "WO")
            new_work_order = {
                "work_order_id": new_id,
                "work_order_number": work_order_number,
                "change_id": change_id if change_id else None,
                "incident_id": incident_id if incident_id else None,
                "title": work_order_data["title"],
                "description": work_order_data["description"],
                "assigned_to": assigned_to,
                "status": status,
                "scheduled_date": work_order_data["scheduled_date"],
                "completed_at": work_order_data.get("completed_at"),  # Nullable
                "created_at": timestamp
            }
            work_orders[new_id] = new_work_order
            return json.dumps({
                "success": True,
                "action": "create",
                "work_order_id": new_id,
                "work_order_data": new_work_order
            })

        elif action == "update":
            if not work_order_id:
                return json.dumps({
                    "success": False,
                    "error": "work_order_id is required for update action"
                })
            work_order_id = str(work_order_id).strip().strip('"')
            if work_order_id not in work_orders:
                return json.dumps({
                    "success": False,
                    "error": f"Work order '{work_order_id}' not found"
                })

            if not work_order_data:
                return json.dumps({
                    "success": False,
                    "error": "work_order_data is required for update action"
                })

            # Allowed fields for update (all except work_order_id, created_at)
            allowed_fields = [
                "work_order_number", "change_id", "incident_id", "title", 
                "description", "assigned_to", "status", "scheduled_date", "completed_at"
            ]
            invalid_fields = [field for field in work_order_data if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for update: {', '.join(invalid_fields)}"
                })
            
            # Validate non-empty fields (nullable fields can be None)
            # NOT NULL fields: work_order_number, title, description, assigned_to, scheduled_date
            nullable_fields = ["change_id", "incident_id", "completed_at"]
            for field, value in work_order_data.items():
                if field not in nullable_fields and (value is None or (isinstance(value, str) and str(value).strip() == "")):
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })
                elif field in nullable_fields and (isinstance(value, str) and str(value).strip() == ""):
                    work_order_data[field] = None  # Treat empty string as null for nullable fields

            # Validate work_order_number uniqueness if updated
            if "work_order_number" in work_order_data:
                updated_work_order_number = str(work_order_data["work_order_number"]).strip()
                for existing_work_order_id, work_order in work_orders.items():
                    if existing_work_order_id != work_order_id and work_order["work_order_number"].lower() == updated_work_order_number.lower():
                        return json.dumps({
                            "success": False,
                            "error": f"Work order with number '{updated_work_order_number}' already exists."
                        })
                work_order_data["work_order_number"] = updated_work_order_number

            # Validate status enum if provided
            if "status" in work_order_data and work_order_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status '{work_order_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                })

            # Validate assigned_to FK if provided
            if "assigned_to" in work_order_data:
                assigned_to = str(work_order_data["assigned_to"]).strip().strip('"')
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
                work_order_data["assigned_to"] = assigned_to

            # Validate change_id FK if provided
            if "change_id" in work_order_data and work_order_data["change_id"] is not None:
                change_id = str(work_order_data["change_id"]).strip().strip('"')
                if change_id not in change_requests:
                    return json.dumps({
                        "success": False,
                        "error": f"Change request '{change_id}' not found"
                    })
                work_order_data["change_id"] = change_id

            # Validate incident_id FK if provided
            if "incident_id" in work_order_data and work_order_data["incident_id"] is not None:
                incident_id = str(work_order_data["incident_id"]).strip().strip('"')
                if incident_id not in incidents:
                    return json.dumps({
                        "success": False,
                        "error": f"Incident '{incident_id}' not found"
                    })
                work_order_data["incident_id"] = incident_id

            updated_work_order = work_orders[work_order_id].copy()
            for key, value in work_order_data.items():
                updated_work_order[key] = value
            
            work_orders[work_order_id] = updated_work_order
            return json.dumps({
                "success": True,
                "action": "update",
                "work_order_id": work_order_id,
                "work_order_data": updated_work_order
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manipulate_work_orders",
                "description": "Create or update work order records in the system. Work orders represent scheduled tasks or maintenance activities that may be related to change requests or incidents.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to add a new work order, 'update' to modify an existing work order."
                        },
                        "work_order_data": {
                            "type": "object",
                            "description": "Data object containing fields for creating or updating a work order.",
                            "properties": {
                                "work_order_number": {
                                    "type": "string",
                                    "description": "A unique identifier for the work order (required for create, must be unique, cannot be empty). Updatable."
                                },
                                "change_id": {
                                    "type": "string",
                                    "description": "The ID of the related change request (optional). Must refer to an existing change request if provided. Updatable, can be set to null."
                                },
                                "incident_id": {
                                    "type": "string",
                                    "description": "The ID of the related incident (optional). Must refer to an existing incident if provided. Updatable, can be set to null."
                                },
                                "title": {
                                    "type": "string",
                                    "description": "A brief, descriptive title for the work order (required for create, cannot be empty). Updatable."
                                },
                                "description": {
                                    "type": "string",
                                    "description": "A detailed description of the work order (required for create, cannot be empty). Updatable."
                                },
                                "assigned_to": {
                                    "type": "string",
                                    "description": "The user ID of the person assigned to complete the work order (required for create). Must refer to an existing active user. Updatable."
                                },
                                "status": {
                                    "type": "string",
                                    "description": "The current status of the work order (optional for create, defaults to 'pending'). Must be one of: pending, in_progress, completed, cancelled. Updatable.",
                                    "enum": ["pending", "in_progress", "completed", "cancelled"]
                                },
                                "scheduled_date": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "The timestamp when the work order is scheduled to be executed (required for create, cannot be empty). Updatable."
                                },
                                "completed_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "The timestamp when the work order was completed (optional). Updatable, can be set to null."
                                }
                            }
                        },
                        "work_order_id": {
                            "type": "string",
                            "description": "The unique identifier of the work order to update. Required for 'update' action only."
                        }
                    },
                    "required": ["action"]
                }
            }
        }