import json
import re
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool
from datetime import datetime, date


class ExecuteBenefitPlanOperations(Tool):
    
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manages benefit plan operations including creation and updates.
        """
        
        # --- Utility Functions ---
        def generate_id(table: Dict[str, Any]) -> int:
            """Utility to generate a new sequential ID for the benefit_plans table."""
            if not table:
                return 7001
            return max(int(k) for k in table.keys()) + 1

        def validate_date_format(date_str: str, field_name: str) -> Optional[str]:
            """Validates date format is MM-DD-YYYY."""
            if date_str:
                date_pattern = r'^\d{2}-\d{2}-\d{4}$'
                if not re.match(date_pattern, date_str):
                    return f"Invalid {field_name} format. Must be MM-DD-YYYY"
                
                try:
                    datetime.strptime(date_str, '%m-%d-%Y')
                except ValueError:
                    return f"Invalid date value provided for {field_name}. Please check month/day/year validity."
            return None

        def convert_date_format(date_str: str) -> str:
            """Convert MM-DD-YYYY to YYYY-MM-DD for internal storage."""
            if date_str and re.match(r'^\d{2}-\d{2}-\d{4}$', date_str):
                try:
                    dt = datetime.strptime(date_str, '%m-%d-%Y')
                    return dt.strftime('%Y-%m-%d')
                except ValueError:
                    return date_str
            return date_str

        def validate_numeric_field(value: Any, field_name: str) -> Optional[str]:
            """Validate that a field is a non-negative number."""
            if value is not None:
                try:
                    if float(value) < 0:
                        return f"{field_name} cannot be negative."
                except ValueError:
                    return f"{field_name} must be a valid number."
            return None
        
        valid_operations = ["create_plan", "update_plan"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "plan_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "plan_id": None,
                "message": "Invalid data format for benefit plan operations"
            })
        
        benefit_plans = data.get("benefit_plans", {})
        users = data.get("users", {})
        
        simulated_today = date(2025, 10, 1)

        # --- Benefit Plan Creation (create_plan) ---
        if operation_type == "create_plan":
            required_fields = ["benefit_type", "plan_name", "provider_name", "effective_from", "effective_until", "user_id", "default_employee_contribution", "default_employer_contribution"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "plan_id": None,
                    "message": f"Missing mandatory fields: {', '.join(missing_fields)}"
                })

            # 1. Validate user authorization
            user = users.get(str(kwargs["user_id"]))
            if not user or user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "plan_id": None,
                    "message": "Halt: User lacks authorization to perform this action"
                })
            
            valid_roles = ["hr_manager", "hr_admin", "compliance_officer"]
            if user.get("role") not in valid_roles:
                return json.dumps({
                    "success": False,
                    "plan_id": None,
                    "message": "Halt: User lacks authorization to perform this action"
                })

            # 2. Validate date formats and ranges
            date_fields = ["effective_from", "effective_until"]
            converted_dates = {}
            for field in date_fields:
                date_error = validate_date_format(kwargs[field], field)
                if date_error:
                    return json.dumps({"success": False, "plan_id": None, "message": date_error})
                converted_dates[field] = convert_date_format(kwargs[field])

            # Check date ranges (effective_from >= effective_until)
            effective_from_obj = datetime.strptime(converted_dates["effective_from"], '%Y-%m-%d').date()
            effective_until_obj = datetime.strptime(converted_dates["effective_until"], '%Y-%m-%d').date()
            if effective_from_obj >= effective_until_obj:
                return json.dumps({
                    "success": False,
                    "plan_id": None,
                    "message": "Halt: Invalid date ranges (effective_from >= effective_until)"
                })

            # 3. Validate contribution amounts
            contribution_fields = ["default_employee_contribution", "default_employer_contribution"]
            for field in contribution_fields:
                error = validate_numeric_field(kwargs[field], field)
                if error:
                    return json.dumps({"success": False, "plan_id": None, "message": error})

            # 4. Check for duplicate plan name
            for plan in benefit_plans.values():
                if plan.get("plan_name") == kwargs["plan_name"]:
                    return json.dumps({
                        "success": False,
                        "plan_id": None,
                        "message": "Halt: Duplicate plan name"
                    })

            # 5. Create Benefit Plan
            new_plan_id = generate_id(benefit_plans)
            timestamp = datetime.now().isoformat()

            new_plan = {
                "plan_id": str(new_plan_id),
                "benefit_type": kwargs["benefit_type"],
                "plan_name": kwargs["plan_name"],
                "description": kwargs.get("description"),
                "provider_name": kwargs["provider_name"],
                "default_employee_contribution": float(kwargs["default_employee_contribution"]),
                "default_employer_contribution": float(kwargs["default_employer_contribution"]),
                "plan_status": "active",
                "effective_from": converted_dates["effective_from"],
                "effective_until": converted_dates["effective_until"],
                "created_at": timestamp,
                "updated_at": timestamp
            }
            
            benefit_plans[str(new_plan_id)] = new_plan
            
            return json.dumps({
                "success": True,
                "plan_id": str(new_plan_id),
                "message": f"Benefit plan {new_plan_id} created successfully",
                "plan_data": new_plan
            })

        # --- Benefit Plan Update (update_plan) ---
        elif operation_type == "update_plan":
            required_fields = ["plan_id", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "plan_id": None,
                    "message": f"Missing mandatory fields: {', '.join(missing_fields)}"
                })

            plan_id_str = str(kwargs["plan_id"])
            plan = benefit_plans.get(plan_id_str)
            
            # 1. Verify plan exists and is active
            if not plan or plan.get("plan_status") != "active":
                return json.dumps({
                    "success": False,
                    "plan_id": plan_id_str,
                    "message": "Halt: Plan not found or inactive"
                })

            # 2. Validate user authorization
            user = users.get(str(kwargs["user_id"]))
            if not user or user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "plan_id": plan_id_str,
                    "message": "Halt: User lacks authorization to perform this action"
                })
            
            valid_roles = ["hr_manager", "hr_admin", "compliance_officer"]
            if user.get("role") not in valid_roles:
                return json.dumps({
                    "success": False,
                    "plan_id": plan_id_str,
                    "message": "Halt: User lacks authorization to perform this action"
                })

            # 3. Validate optional fields if provided
            updatable_fields = ["benefit_type", "plan_name", "provider_name", "effective_from", "effective_until", "default_employee_contribution", "default_employer_contribution", "description"]
            
            for field in updatable_fields:
                if field in kwargs and kwargs[field] is not None:
                    if field in ["effective_from", "effective_until"]:
                        date_error = validate_date_format(kwargs[field], field)
                        if date_error:
                            return json.dumps({"success": False, "plan_id": plan_id_str, "message": date_error})
                    elif field in ["default_employee_contribution", "default_employer_contribution"]:
                        error = validate_numeric_field(kwargs[field], field)
                        if error:
                            return json.dumps({"success": False, "plan_id": plan_id_str, "message": error})
                    elif field == "plan_name":
                        # Check for duplicate plan name (excluding current plan)
                        for plan_id, existing_plan in benefit_plans.items():
                            if plan_id != plan_id_str and existing_plan.get("plan_name") == kwargs[field]:
                                return json.dumps({
                                    "success": False,
                                    "plan_id": plan_id_str,
                                    "message": "Halt: Duplicate plan name"
                                })

            # 4. Update plan fields
            for field in updatable_fields:
                if field in kwargs and kwargs[field] is not None:
                    if field in ["effective_from", "effective_until"]:
                        plan[field] = convert_date_format(kwargs[field])
                    elif field in ["default_employee_contribution", "default_employer_contribution"]:
                        plan[field] = float(kwargs[field])
                    else:
                        plan[field] = kwargs[field]

            plan["updated_at"] = datetime.now().isoformat()
            
            return json.dumps({
                "success": True,
                "plan_id": plan_id_str,
                "message": f"Benefit plan {plan_id_str} updated successfully"
            })

        return json.dumps({
            "success": False,
            "plan_id": None,
            "message": "Unhandled operation type"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "execute_benefit_plan_operations",
                "description": "Manages benefit plan operations including creation and updates. 'create_plan' establishes new benefit plans with comprehensive validation of dates, contributions, and plan names. 'update_plan' modifies existing benefit plan details while maintaining data integrity and preventing duplicate plan names. Essential for benefits administration and plan management.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation: 'create_plan' or 'update_plan'.",
                            "enum": ["create_plan", "update_plan"]
                        },
                        "benefit_type": {
                            "type": "string",
                            "description": "Type of benefit (required for create_plan, optional for update_plan)",
                            "enum": ["medical", "dental", "vision", "401k", "life_insurance", "disability"]
                        },
                        "plan_name": {
                            "type": "string",
                            "description": "Name of the benefit plan (required for create_plan, optional for update_plan, must be unique)"
                        },
                        "provider_name": {
                            "type": "string",
                            "description": "Name of the benefit provider (required for create_plan, optional for update_plan)"
                        },
                        "effective_from": {
                            "type": "string",
                            "description": "Plan effective start date in MM-DD-YYYY format (required for create_plan, optional for update_plan)"
                        },
                        "effective_until": {
                            "type": "string",
                            "description": "Plan effective end date in MM-DD-YYYY format (required for create_plan, optional for update_plan)"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "User ID performing the operation (required for all operations, must be active HR Manager, HR Admin, or Compliance Officer)"
                        },
                        "default_employee_contribution": {
                            "type": "number",
                            "description": "Default employee contribution amount (required for create_plan, optional for update_plan, must be non-negative)"
                        },
                        "default_employer_contribution": {
                            "type": "number",
                            "description": "Default employer contribution amount (required for create_plan, optional for update_plan, must be non-negative)"
                        },
                        "description": {
                            "type": "string",
                            "description": "Plan description (optional for both operations)"
                        },
                        "plan_id": {
                            "type": "string",
                            "description": "Plan ID (required for update_plan only, must exist and be active)"
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }
