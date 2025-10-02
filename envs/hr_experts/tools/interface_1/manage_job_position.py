import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManageJobPosition(Tool):
    """
    Manages job position records including creation and updates.
    """
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        position_id: Optional[str] = None,
        title: Optional[str] = None,
        department_id: Optional[str] = None,
        job_level: Optional[str] = None,
        employment_type: Optional[str] = None,
        status: Optional[str] = None,
        hourly_rate_min: Optional[float] = None,
        hourly_rate_max: Optional[float] = None,
    ) -> str:
        """
        Executes the specified action (create or update) on job position records.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        job_positions = data.get("job_positions", {})
        departments = data.get("departments", {})

        # Validate supported job levels
        supported_job_levels = ["entry", "junior", "mid", "senior", "lead", "manager", "director", "executive"]
        
        # Validate supported employment types
        supported_employment_types = ["full_time", "part_time", "contract", "intern"]
        
        # Validate supported statuses
        supported_statuses = ["draft", "open", "closed"]

        if action == "create":
            # Required fields for job position creation
            if not all([title, department_id, job_level, employment_type, status]):
                return json.dumps({
                    "error": "Missing required parameters for create operation. Required: title, department_id, job_level, employment_type, status"
                })

            # Validate department_id exists
            if department_id not in departments:
                return json.dumps({
                    "error": f"Department with ID '{department_id}' not found"
                })

            # Validate job_level
            if job_level not in supported_job_levels:
                return json.dumps({
                    "error": f"Invalid job_level '{job_level}'. Must be one of: {', '.join(supported_job_levels)}"
                })

            # Validate employment_type
            if employment_type not in supported_employment_types:
                return json.dumps({
                    "error": f"Invalid employment_type '{employment_type}'. Must be one of: {', '.join(supported_employment_types)}"
                })

            # Validate status
            if status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Validate hourly rates if provided
            if hourly_rate_min is not None and hourly_rate_min < 0:
                return json.dumps({
                    "error": "hourly_rate_min must be non-negative"
                })

            if hourly_rate_max is not None and hourly_rate_max < 0:
                return json.dumps({
                    "error": "hourly_rate_max must be non-negative"
                })

            if (hourly_rate_min is not None and hourly_rate_max is not None and 
                hourly_rate_min > hourly_rate_max):
                return json.dumps({
                    "error": "hourly_rate_min cannot be greater than hourly_rate_max"
                })

            # Generate new position ID
            new_position_id = generate_id(job_positions)

            # Create new job position record
            new_position = {
                "position_id": new_position_id,
                "title": title,
                "department_id": department_id,
                "job_level": job_level,
                "employment_type": employment_type,
                "status": status,
                "created_at": timestamp,
                "updated_at": timestamp
            }

            # Add hourly rates if provided
            if hourly_rate_min is not None:
                new_position["hourly_rate_min"] = hourly_rate_min
            
            if hourly_rate_max is not None:
                new_position["hourly_rate_max"] = hourly_rate_max

            # Add to job positions data
            job_positions[new_position_id] = new_position

            return json.dumps({
                "success": True,
                "message": f"Job position created successfully with ID {new_position_id}",
                "position_id": new_position_id,
                "position_data": new_position
            })

        elif action == "update":
            # position_id is required for update
            if not position_id:
                return json.dumps({
                    "error": "Missing required parameter 'position_id' for update operation"
                })

            # Check if position exists
            if position_id not in job_positions:
                return json.dumps({
                    "error": f"Job position with ID {position_id} not found"
                })

            position_to_update = job_positions[position_id]

            # Validate department_id if being updated
            if department_id and department_id not in departments:
                return json.dumps({
                    "error": f"Department with ID '{department_id}' not found"
                })

            # Validate job_level if being updated
            if job_level and job_level not in supported_job_levels:
                return json.dumps({
                    "error": f"Invalid job_level '{job_level}'. Must be one of: {', '.join(supported_job_levels)}"
                })

            # Validate employment_type if being updated
            if employment_type and employment_type not in supported_employment_types:
                return json.dumps({
                    "error": f"Invalid employment_type '{employment_type}'. Must be one of: {', '.join(supported_employment_types)}"
                })

            # Validate status if being updated
            if status and status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Validate hourly rates if being updated
            if hourly_rate_min is not None and hourly_rate_min < 0:
                return json.dumps({
                    "error": "hourly_rate_min must be non-negative"
                })

            if hourly_rate_max is not None and hourly_rate_max < 0:
                return json.dumps({
                    "error": "hourly_rate_max must be non-negative"
                })

            # Check rate relationship if both are being updated
            current_min = position_to_update.get("hourly_rate_min")
            current_max = position_to_update.get("hourly_rate_max")
            
            effective_min = hourly_rate_min if hourly_rate_min is not None else current_min
            effective_max = hourly_rate_max if hourly_rate_max is not None else current_max
            
            if (effective_min is not None and effective_max is not None and 
                effective_min > effective_max):
                return json.dumps({
                    "error": "hourly_rate_min cannot be greater than hourly_rate_max"
                })

            # Track what fields are being updated
            updated_fields = []

            # Update fields if provided
            if title:
                position_to_update["title"] = title
                updated_fields.append("title")
            
            if department_id:
                position_to_update["department_id"] = department_id
                updated_fields.append("department_id")
            
            if job_level:
                position_to_update["job_level"] = job_level
                updated_fields.append("job_level")
            
            if employment_type:
                position_to_update["employment_type"] = employment_type
                updated_fields.append("employment_type")
            
            if status:
                position_to_update["status"] = status
                updated_fields.append("status")
            
            if hourly_rate_min is not None:
                position_to_update["hourly_rate_min"] = hourly_rate_min
                updated_fields.append("hourly_rate_min")
            
            if hourly_rate_max is not None:
                position_to_update["hourly_rate_max"] = hourly_rate_max
                updated_fields.append("hourly_rate_max")

            # Update timestamp
            position_to_update["updated_at"] = timestamp

            if not updated_fields:
                return json.dumps({
                    "error": "No fields provided to update. At least one optional field must be provided"
                })

            return json.dumps({
                "success": True,
                "message": f"Job position {position_id} updated successfully",
                "updated_fields": updated_fields,
                "position_data": position_to_update
            })

        else:
            return json.dumps({
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_job_position",
                "description": "Manages job position records for recruitment and HR operations. Supports creating new job positions with proper validation and updating existing positions for status changes, posting, and closing openings. For creation, validates required fields (title, department_id, job_level, employment_type, status) and optional fields (hourly_rate_min, hourly_rate_max). For updates, validates position existence and allows modification of any position field. Validates department IDs against departments table and enforces proper rate relationships. Supported job levels: entry, junior, mid, senior, lead, manager, director, executive. Supported employment types: full_time, part_time, contract, intern. Supported statuses: draft, open, closed. Hourly rates must be non-negative and min cannot exceed max.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform: 'create' for new position, 'update' for modifying existing position",
                            "enum": ["create", "update"]
                        },
                        "position_id": {
                            "type": "string",
                            "description": "Job position ID (required for update operations)"
                        },
                        "title": {
                            "type": "string",
                            "description": "Job position title (required for create)"
                        },
                        "department_id": {
                            "type": "string",
                            "description": "ID of the department (required for create, must exist in departments)"
                        },
                        "job_level": {
                            "type": "string",
                            "description": "Job level (required for create)",
                            "enum": ["entry", "junior", "mid", "senior", "lead", "manager", "director", "executive"]
                        },
                        "employment_type": {
                            "type": "string",
                            "description": "Employment type (required for create)",
                            "enum": ["full_time", "part_time", "contract", "intern"]
                        },
                        "status": {
                            "type": "string",
                            "description": "Position status (required for create)",
                            "enum": ["draft", "open", "closed"]
                        },
                        "hourly_rate_min": {
                            "type": "number",
                            "description": "Minimum hourly rate (optional, must be non-negative)"
                        },
                        "hourly_rate_max": {
                            "type": "number",
                            "description": "Maximum hourly rate (optional, must be non-negative and >= min)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }