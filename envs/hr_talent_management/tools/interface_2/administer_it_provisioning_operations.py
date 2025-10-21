import json
import re
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class AdministerItProvisioningOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manage IT provisioning task creation and updates.

        Operations:
        - create_task: Create a new IT provisioning task (requires employee_id, task_type, assigned_by)
        - update_task: Update an existing IT provisioning task (requires task_id, task_status, user_id; optional completion_date)
        """

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        def validate_date_format(date_str: str, field_name: str) -> Optional[str]:
            if date_str:
                date_pattern = r'^\d{4}-\d{2}-\d{2}$'
                if not re.match(date_pattern, date_str):
                    return f"Invalid {field_name} format. Must be YYYY-MM-DD"
            return None

        def convert_date_format(date_str: str) -> str:
            if date_str and re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                return date_str
            return date_str

        # Validate operation_type
        valid_operations = ["create_task", "update_task"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "task_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })

        # Access data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "task_id": None,
                "message": "Invalid data format for IT provisioning operations"
            })

        it_tasks = data.get("it_provisioning_tasks", {})
        employees = data.get("employees", {})
        users = data.get("users", {})

        if operation_type == "create_task":
            required_fields = ["employee_id", "task_type", "assigned_by"]
            missing_fields = [f for f in required_fields if f not in kwargs or kwargs[f] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "task_id": None,
                    "message": f"Missing required fields for task creation: {', '.join(missing_fields)}"
                })

            # Validate employee exists
            if str(kwargs["employee_id"]) not in employees:
                return json.dumps({
                    "success": False,
                    "task_id": None,
                    "message": f"Employee {kwargs['employee_id']} not found"
                })

            # Validate assigned_by user exists
            if str(kwargs["assigned_by"]) not in users:
                return json.dumps({
                    "success": False,
                    "task_id": None,
                    "message": f"Assigned-by user {kwargs['assigned_by']} not found"
                })

            # Validate task_type enum
            valid_task_types = ["email_account", "laptop", "access_badge", "system_access", "software_license"]
            if kwargs["task_type"] not in valid_task_types:
                return json.dumps({
                    "success": False,
                    "task_id": None,
                    "message": f"Invalid task_type. Must be one of: {', '.join(valid_task_types)}"
                })

            # Additional validations
            # 1) Verify that the employee's status is active
            employee_record = employees.get(str(kwargs["employee_id"]), {})
            employee_status = str(employee_record.get("status", "")).strip().lower()
            if employee_status and employee_status != "active":
                return json.dumps({
                    "success": False,
                    "task_id": None,
                    "message": f"Employee {kwargs['employee_id']} is not active"
                })

            # 2) Check that assigned_by is an active IT administrator
            assigner_record = users.get(str(kwargs["assigned_by"]), {})
            assigner_status = str(assigner_record.get("status", "")).strip().lower()
            assigner_role = str(assigner_record.get("role", "")).strip().lower()

            if assigner_status and assigner_status != "active":
                return json.dumps({
                    "success": False,
                    "task_id": None,
                    "message": f"Assigned-by user {kwargs['assigned_by']} is not active"
                })

            # 3) Ensure only an IT administrator can create a task
            if assigner_role != "it_administrator":
                return json.dumps({
                    "success": False,
                    "task_id": None,
                    "message": f"Only users with role 'it_administrator' can create IT provisioning tasks"
                })

            # Create task
            new_task_id = generate_id(it_tasks)
            timestamp = "2025-10-10T12:00:00"

            new_task = {
                "task_id": str(new_task_id),
                "employee_id": str(kwargs["employee_id"]),
                "task_type": kwargs["task_type"],
                "assigned_by": str(kwargs["assigned_by"]),
                "task_status": "pending",
                "completion_date": None,
                "created_at": timestamp
            }

            it_tasks[str(new_task_id)] = new_task

            return json.dumps({
                "success": True,
                "task_id": str(new_task_id),
                "message": f"IT provisioning task {new_task_id} created successfully"
            })

        elif operation_type == "update_task":
            required_fields = ["task_id", "task_status", "user_id"]
            missing_fields = [f for f in required_fields if f not in kwargs or kwargs[f] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "task_id": None,
                    "message": f"Missing required fields for task update: {', '.join(missing_fields)}"
                })

            # Validate task exists
            if str(kwargs["task_id"]) not in it_tasks:
                return json.dumps({
                    "success": False,
                    "task_id": None,
                    "message": f"Task {kwargs['task_id']} not found"
                })

            # Validate user exists
            if str(kwargs["user_id"]) not in users:
                return json.dumps({
                    "success": False,
                    "task_id": None,
                    "message": f"User {kwargs['user_id']} not found"
                })

            # Validate user is active and has IT administrator role
            user_record = users.get(str(kwargs["user_id"]), {})
            user_status = str(user_record.get("status", "")).strip().lower()
            user_role = str(user_record.get("role", "")).strip().lower()

            if user_status and user_status != "active":
                return json.dumps({
                    "success": False,
                    "task_id": None,
                    "message": f"User {kwargs['user_id']} is not active"
                })

            if user_role != "it_administrator":
                return json.dumps({
                    "success": False,
                    "task_id": None,
                    "message": f"Only users with role 'it_administrator' can update IT provisioning tasks"
                })

            # Validate task_status enum
            valid_statuses = ["pending", "in_progress", "completed", "failed"]
            if kwargs["task_status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "task_id": None,
                    "message": f"Invalid task_status. Must be one of: {', '.join(valid_statuses)}"
                })

            # Validate completion_date if provided
            if "completion_date" in kwargs and kwargs["completion_date"] is not None:
                date_error = validate_date_format(kwargs["completion_date"], "completion_date")
                if date_error:
                    return json.dumps({
                        "success": False,
                        "task_id": None,
                        "message": date_error
                    })

            # Update task
            task = it_tasks[str(kwargs["task_id"])]
            task["task_status"] = kwargs["task_status"]
            if "completion_date" in kwargs and kwargs["completion_date"] is not None:
                task["completion_date"] = convert_date_format(kwargs["completion_date"])

            return json.dumps({
                "success": True,
                "task_id": str(kwargs["task_id"]),
                "message": f"IT provisioning task {kwargs['task_id']} updated successfully"
            })

        return json.dumps({
            "success": False,
            "task_id": None,
            "message": "Unhandled operation type"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "administer_it_provisioning_operations",
                "description": "Manage IT provisioning task creation and updates in the HR talent management system. This tool supports the full lifecycle of IT onboarding tasks including account setup, device allocation, access provisioning, and software licensing. For creation, establishes new tasks with validation of employee and assigning user, and standardized task types. For updates, validates authorized updates with user context, enforces valid status transitions, and records optional completion dates with proper formatting. Essential for coordinated onboarding and IT operations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation to perform: 'create_task' to create a new IT provisioning task, 'update_task' to update an existing task",
                            "enum": ["create_task", "update_task"]
                        },
                        "employee_id": {
                            "type": "string",
                            "description": "Unique identifier of the employee for whom the IT provisioning task is being created. Enter the employee ID as a string (e.g., '3001', '5042'). This field is required only when operation_type is 'create_task'. The system validates that this employee exists and has an 'active' status before creating the task. Each task represents one IT provisioning item needed for the employee's onboarding. Example: '4008'"
                        },
                        "task_type": {
                            "type": "string",
                            "description": "Type of IT resource or access to be provisioned. Select from: 'email_account' for corporate email setup, 'laptop' for computer hardware assignment, 'access_badge' for physical building access card, 'system_access' for software system login credentials, or 'software_license' for specific software licenses. This field is required only when operation_type is 'create_task'. Must be exactly one of these five values. Each task type represents a different IT provisioning requirement. Example: 'laptop'",
                            "enum": ["email_account", "laptop", "access_badge", "system_access", "software_license"]
                        },
                        "assigned_by": {
                            "type": "string",
                            "description": "Unique identifier of the IT administrator creating and assigning this provisioning task. Enter the user ID as a string (e.g., '7001', '8005'). This field is required only when operation_type is 'create_task'. The system validates that this user exists, has an 'active' status, and has the role 'it_administrator' before allowing task creation. Only IT administrators can create provisioning tasks. Used for accountability and task assignment tracking. Example: '9002'"
                        },
                        "task_id": {
                            "type": "string",
                            "description": "Unique identifier of an existing IT provisioning task to be updated. Enter the task ID as a string (e.g., '101', '205'). This field is required only when operation_type is 'update_task'. The system validates that this task exists in the database. Used to identify which specific provisioning task to update with new status or completion information. Example: '143'"
                        },
                        "task_status": {
                            "type": "string",
                            "description": "Current status of the IT provisioning task. Select from: 'pending' for task not yet started, 'in_progress' for task currently being worked on, 'completed' for task successfully finished, or 'failed' for task that could not be completed. This field is required only when operation_type is 'update_task'. Must be exactly one of these four values. Tracks the progress and outcome of provisioning activities. When status is 'completed', consider also providing completion_date. Example: 'completed'",
                            "enum": ["pending", "in_progress", "completed", "failed"]
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Unique identifier of the IT administrator performing the task update. Enter the user ID as a string (e.g., '7001', '9003'). This field is required only when operation_type is 'update_task'. The system validates that this user exists, has an 'active' status, and has the role 'it_administrator'. Only IT administrators can update provisioning tasks. Used for audit trail to track who modified the task. Example: '8004'"
                        },
                        "completion_date": {
                            "type": "string",
                            "description": "Date when the IT provisioning task was completed. Enter date in YYYY-MM-DD format (e.g., '2025-04-05' for April 5, 2025). This field is optional and only applies when operation_type is 'update_task'. Must follow the exact format YYYY-MM-DD with hyphens as separators. The system validates the date format. Typically provided when task_status is updated to 'completed'. Documents when the provisioning item was delivered or configured. Example: '2025-05-20'"
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }