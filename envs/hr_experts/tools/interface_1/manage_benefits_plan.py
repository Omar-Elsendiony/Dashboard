import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManageBenefitsPlan(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, plan_data: Dict[str, Any] = None, plan_id: str = None) -> str:
        """
        Create or update benefits plan records.
        
        Actions:
        - create: Create new benefits plan (requires plan_data with plan_name, plan_type, effective_date)
        - update: Update existing benefits plan (requires plan_id and plan_data with changes)
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
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for benefits plans"
            })
        
        benefits_plans = data.get("benefits_plans", {})
        
        if action == "create":
            if not plan_data:
                return json.dumps({
                    "success": False,
                    "error": "plan_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["plan_name", "plan_type", "effective_date"]
            missing_fields = [field for field in required_fields if field not in plan_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Missing or invalid inputs - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate plan_type enum according to schema
            valid_types = ["health_insurance", "dental", "vision", "life_insurance", "disability", "retirement_401k", "pto", "flexible_spending"]
            if plan_data["plan_type"] not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid plan type or dates - plan_type must be one of: {', '.join(valid_types)}"
                })
            
            # Validate cost amounts are non-negative monetary values if provided
            for cost_field in ["employee_cost", "employer_cost"]:
                if cost_field in plan_data:
                    cost_value = plan_data[cost_field]
                    if cost_value is not None and (not isinstance(cost_value, (int, float)) or cost_value < 0):
                        return json.dumps({
                            "success": False,
                            "error": f"Halt: Invalid plan type or dates - {cost_field} must be non-negative"
                        })
            
            # Validate date consistency - expiration date must occur after effective date if provided
            effective_date = plan_data["effective_date"]
            expiration_date = plan_data.get("expiration_date")
            if expiration_date and expiration_date <= effective_date:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid plan type or dates - expiration date must be after effective date"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["plan_name", "plan_type", "provider", "employee_cost", "employer_cost", 
                            "status", "effective_date", "expiration_date"]
            invalid_fields = [field for field in plan_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for benefits plan creation: {', '.join(invalid_fields)}"
                })
            
            # Generate new plan ID
            new_plan_id = generate_id(benefits_plans)
            
            # Create new benefits plan
            new_plan = {
                "plan_id": str(new_plan_id),
                "plan_name": plan_data["plan_name"],
                "plan_type": plan_data["plan_type"],
                "provider": plan_data.get("provider"),
                "employee_cost": plan_data.get("employee_cost"),
                "employer_cost": plan_data.get("employer_cost"),
                "status": plan_data.get("status", "active"),  # If status is not specified during creation, set it to active
                "effective_date": plan_data["effective_date"],
                "expiration_date": plan_data.get("expiration_date"),
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            benefits_plans[str(new_plan_id)] = new_plan
            
            return json.dumps({
                "success": True,
                "action": "create",
                "plan_id": str(new_plan_id),
                "message": f"Benefits plan {new_plan_id} created successfully",
                "plan_data": new_plan
            })
        
        elif action == "update":
            if not plan_id:
                return json.dumps({
                    "success": False,
                    "error": "plan_id is required for update action"
                })
            
            if plan_id not in benefits_plans:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Plan not found"
                })
            
            if not plan_data:
                return json.dumps({
                    "success": False,
                    "error": "plan_data is required for update action"
                })
            
            # Validate at least one optional field is provided
            update_fields = ["plan_name", "plan_type", "provider", "employee_cost", "employer_cost", 
                           "status", "effective_date", "expiration_date"]
            provided_fields = [field for field in update_fields if field in plan_data]
            if not provided_fields:
                return json.dumps({
                    "success": False,
                    "error": "At least one optional field must be provided for updates"
                })
            
            # Get current plan for validation
            current_plan = benefits_plans[plan_id]
            
            # Validate only allowed fields for updates
            invalid_fields = [field for field in plan_data.keys() if field not in update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for benefits plan update: {', '.join(invalid_fields)}"
                })
            
            # Validate status enum if provided
            if "status" in plan_data:
                valid_statuses = ["active", "inactive"]
                if plan_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Benefits plan operation failed - status must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Validate plan_type enum if provided
            if "plan_type" in plan_data:
                valid_types = ["health_insurance", "dental", "vision", "life_insurance", "disability", "retirement_401k", "pto", "flexible_spending"]
                if plan_data["plan_type"] not in valid_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Benefits plan operation failed - plan_type must be one of: {', '.join(valid_types)}"
                    })
            
            # Validate cost amounts are non-negative monetary values if provided
            for cost_field in ["employee_cost", "employer_cost"]:
                if cost_field in plan_data:
                    cost_value = plan_data[cost_field]
                    if cost_value is not None and (not isinstance(cost_value, (int, float)) or cost_value < 0):
                        return json.dumps({
                            "success": False,
                            "error": f"Halt: Benefits plan operation failed - {cost_field} must be non-negative"
                        })
            
            # Validate date consistency
            effective_date = plan_data.get("effective_date", current_plan.get("effective_date"))
            expiration_date = plan_data.get("expiration_date", current_plan.get("expiration_date"))
            
            if effective_date and expiration_date and expiration_date <= effective_date:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Benefits plan operation failed - expiration date must be after effective date"
                })
            
            # Update benefits plan
            updated_plan = current_plan.copy()
            for key, value in plan_data.items():
                updated_plan[key] = value
            
            updated_plan["updated_at"] = "2025-10-01T12:00:00"
            benefits_plans[plan_id] = updated_plan
            
            return json.dumps({
                "success": True,
                "action": "update",
                "plan_id": plan_id,
                "message": f"Benefits plan {plan_id} updated successfully",
                "plan_data": updated_plan
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_benefits_plan",
                "description": "Create or update benefits plan records in the HR system. This tool manages employee benefits plans with comprehensive validation. For creation, establishes new benefits plans with proper validation of plan details, cost amounts. For updates, modifies existing plans while maintaining data integrity and date consistency. Validates plan types against supported categories, ensures cost amounts are non-negative, and enforces proper date relationships. Essential for benefits administration, employee enrollment management, and compliance with benefits regulations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new benefits plan, 'update' to modify existing plan",
                            "enum": ["create", "update"]
                        },
                        "plan_data": {
                            "type": "object",
                            "description": "Benefits plan data object. For create: requires plan_name, plan_type, effective_date. Optional: provider, employee_cost, employer_cost, status, expiration_date. For update: at least one of plan_name, plan_type, provider, employee_cost, employer_cost, status, effective_date, expiration_date. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "plan_name": {
                                    "type": "string",
                                    "description": "Name of the benefits plan"
                                },
                                "plan_type": {
                                    "type": "string",
                                    "description": "Type of benefits plan",
                                    "enum": ["health_insurance", "dental", "vision", "life_insurance", "disability", "retirement_401k", "pto", "flexible_spending"]
                                },
                                "provider": {
                                    "type": "string",
                                    "description": "Benefits plan provider/carrier name"
                                },
                                "employee_cost": {
                                    "type": "number",
                                    "description": "Monthly cost to employee (must be non-negative)"
                                },
                                "employer_cost": {
                                    "type": "number",
                                    "description": "Monthly cost to employer (must be non-negative)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Plan status",
                                    "enum": ["active", "inactive"]
                                },
                                "effective_date": {
                                    "type": "string",
                                    "description": "Plan effective date in YYYY-MM-DD format (required for create)"
                                },
                                "expiration_date": {
                                    "type": "string",
                                    "description": "Plan expiration date in YYYY-MM-DD format (must be after effective_date)"
                                }
                            }
                        },
                        "plan_id": {
                            "type": "string",
                            "description": "Unique identifier of the benefits plan (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }

