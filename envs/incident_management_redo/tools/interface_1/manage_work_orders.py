import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManageWorkOrders(Tool):
    """
    Create and update work orders for incidents and changes.
    """
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        work_order_id: Optional[str] = None,
        change_id: Optional[str] = None,
        incident_id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        assigned_to: Optional[str] = None,
        status: Optional[str] = None,
        scheduled_date: Optional[str] = None,
        priority: Optional[str] = None,
        created_by: Optional[str] = None
    ) -> str:
        """
        Create or update work order records.

        Actions:
        - create: Create new work order (requires title, description, assigned_to)
        - update: Update existing work order (requires work_order_id and at least one field to update)
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        def generate_work_order_number(order_id: str) -> str:
            """Generate a formatted work order number."""
            return f"WO{order_id.zfill(8)}"

        timestamp = "2025-10-01T12:00:00"
        work_orders = data.get("work_orders", {})
        incidents = data.get("incidents", {})
        changes = data.get("change_requests", {})
        users = data.get("users", {})

        valid_statuses = ["pending", "in_progress", "on_hold", "completed", "cancelled"]
        valid_priorities = ["low", "medium", "high", "critical", "emergency"]

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": "Invalid action. Must be 'create' or 'update'"
            })

        if action == "update" and not work_order_id:
            return json.dumps({
                "success": False,
                "error": "work_order_id is required for update action"
            })

        if action == "create":
            # Validate required fields
            if not all([title, description, assigned_to, created_by]):
                return json.dumps({
                    "success": False,
                    "error": "title, description, assigned_to, and created_by are required for create action"
                })

            # Validate users exist and are active
            for user_id in [assigned_to, created_by]:
                if user_id not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"User with ID {user_id} not found"
                    })
                if users[user_id]["status"] != "active":
                    return json.dumps({
                        "success": False,
                        "error": f"User with ID {user_id} is not active"
                    })

            # Validate title and description
            if not title.strip():
                return json.dumps({
                    "success": False,
                    "error": "title cannot be empty"
                })
            if not description.strip():
                return json.dumps({
                    "success": False,
                    "error": "description cannot be empty"
                })

            # Validate related records if provided
            if incident_id and incident_id not in incidents:
                return json.dumps({
                    "success": False,
                    "error": f"Incident with ID {incident_id} not found"
                })
            if change_id and change_id not in changes:
                return json.dumps({
                    "success": False,
                    "error": f"Change request with ID {change_id} not found"
                })

            # Validate priority if provided
            if priority and priority not in valid_priorities:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid priority. Must be one of: {', '.join(valid_priorities)}"
                })

            new_id = generate_id(work_orders)
            work_order_number = generate_work_order_number(new_id)
            new_order = {
                "work_order_id": new_id,
                "work_order_number": work_order_number,
                "change_id": change_id,
                "incident_id": incident_id,
                "title": title.strip(),
                "description": description.strip(),
                "assigned_to": assigned_to,
                "created_by": created_by,
                "status": status or "pending",
                "priority": priority or "medium",
                "scheduled_date": scheduled_date,
                "completed_at": None,
                "created_at": timestamp,
                "updated_at": timestamp,
                "last_modified_by": created_by,
                "version": 1,
                "history": [{
                    "timestamp": timestamp,
                    "action": "created",
                    "user_id": created_by,
                    "details": "Work order created"
                }]
            }
            work_orders[new_id] = new_order

            return json.dumps({
                "success": True,
                "action": "create",
                "work_order_id": new_id,
                "work_order_number": work_order_number,
                "work_order_data": new_order
            })

        if action == "update":
            if work_order_id not in work_orders:
                return json.dumps({
                    "success": False,
                    "error": f"Work order with ID {work_order_id} not found"
                })

            # Validate at least one field is being updated
            update_fields = [title, description, assigned_to, status, scheduled_date, priority]
            if all(v is None for v in update_fields):
                return json.dumps({
                    "success": False,
                    "error": "At least one field must be provided for update"
                })

            existing_order = work_orders[work_order_id]

            # Validate users if being updated
            if assigned_to is not None:
                if assigned_to not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"User with ID {assigned_to} not found"
                    })
                if users[assigned_to]["status"] != "active":
                    return json.dumps({
                        "success": False,
                        "error": f"User with ID {assigned_to} is not active"
                    })

            history_entry = {
                "timestamp": timestamp,
                "action": "updated",
                "user_id": created_by or assigned_to,
                "changes": []
            }

            if title is not None:
                if not title.strip():
                    return json.dumps({
                        "success": False,
                        "error": "title cannot be empty"
                    })
                history_entry["changes"].append({"field": "title", "old": existing_order["title"], "new": title.strip()})
                existing_order["title"] = title.strip()

            if description is not None:
                if not description.strip():
                    return json.dumps({
                        "success": False,
                        "error": "description cannot be empty"
                    })
                history_entry["changes"].append({"field": "description", "old": existing_order["description"], "new": description.strip()})
                existing_order["description"] = description.strip()

            if assigned_to is not None:
                history_entry["changes"].append({"field": "assigned_to", "old": existing_order["assigned_to"], "new": assigned_to})
                existing_order["assigned_to"] = assigned_to

            if status is not None:
                if status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
                history_entry["changes"].append({"field": "status", "old": existing_order["status"], "new": status})
                existing_order["status"] = status
                if status == "completed":
                    existing_order["completed_at"] = timestamp

            if priority is not None:
                if priority not in valid_priorities:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid priority. Must be one of: {', '.join(valid_priorities)}"
                    })
                history_entry["changes"].append({"field": "priority", "old": existing_order["priority"], "new": priority})
                existing_order["priority"] = priority

            if scheduled_date is not None:
                history_entry["changes"].append({"field": "scheduled_date", "old": existing_order["scheduled_date"], "new": scheduled_date})
                existing_order["scheduled_date"] = scheduled_date

            existing_order["updated_at"] = timestamp
            existing_order["last_modified_by"] = created_by or assigned_to
            existing_order["version"] += 1
            existing_order["history"].append(history_entry)

            return json.dumps({
                "success": True,
                "action": "update",
                "work_order_id": work_order_id,
                "work_order_number": existing_order["work_order_number"],
                "work_order_data": existing_order
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns comprehensive information about the tool's capabilities, parameters, and data schema.
        """
        return {
            "type": "function",
            "function": {
                "name": "manage_work_orders",
                "description": "Create/update work orders for incidents and changes. Actions: 'create' (requires title, description, assigned_to, created_by; optional: change_id, incident_id, status, priority, scheduled_date), 'update' (requires work_order_id; optional: title, description, assigned_to, status, priority, scheduled_date).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' or 'update'",
                            "enum": ["create", "update"]
                        },
                        "work_order_id": {
                            "type": "string",
                            "description": "Required for update. ID of the work order to update"
                        },
                        "change_id": {
                            "type": "string",
                            "description": "Optional. ID of the related change request"
                        },
                        "incident_id": {
                            "type": "string",
                            "description": "Optional. ID of the related incident"
                        },
                        "title": {
                            "type": "string",
                            "description": "Brief title describing the work to be done (must not be empty)"
                        },
                        "description": {
                            "type": "string",
                            "description": "Detailed description of the work order (must not be empty)"
                        },
                        "assigned_to": {
                            "type": "string",
                            "description": "ID of the active user assigned to complete the work"
                        },
                        "status": {
                            "type": "string",
                            "description": "Status: pending, in_progress, on_hold, completed, cancelled",
                            "enum": ["pending", "in_progress", "on_hold", "completed", "cancelled"]
                        },
                        "scheduled_date": {
                            "type": "string",
                            "description": "Planned date/time for the work (ISO format)"
                        },
                        "priority": {
                            "type": "string",
                            "description": "Priority level",
                            "enum": ["low", "medium", "high", "critical", "emergency"]
                        },
                        "created_by": {
                            "type": "string",
                            "description": "Required for create. ID of the user creating the work order"
                        }
                    },
                    "required": ["action"]
                }
            }
        }