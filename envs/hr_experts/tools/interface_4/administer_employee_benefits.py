
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AdministerEmployeeBenefits(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, benefits_data: Dict[str, Any] = None, enrollment_id: str = None) -> str:
        """
        Create or update employee benefits records.
        
        Actions:
        - create: Create new employee benefits enrollment (requires benefits_data with employee_id, plan_id, enrollment_date, coverage_level)
        - update: Update existing enrollment (requires enrollment_id and benefits_data with changes)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
            
        def is_future_date(date_str: str) -> bool:
            """Check if date is in future - simplified for demo"""
            # In real implementation, would compare with current date
            # For demo purposes, assume dates starting with "2026" or later are future
            return date_str.startswith("2026") or date_str.startswith("2027")
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for employee benefits"
            })
        
        employee_benefits = data.get("employee_benefits", {})
        employees = data.get("employees", {})
        benefits_plans = data.get("benefits_plans", {})
        
        if action == "create":
            if not benefits_data:
                return json.dumps({
                    "success": False,
                    "error": "benefits_data is required for create action"
                })
            
            # Validate required fields
            required_fields = ["employee_id", "plan_id", "enrollment_date", "coverage_level"]
            missing_fields = [field for field in required_fields if field not in benefits_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or plan not found or inactive - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate that employee exists and has active status
            employee_id = str(benefits_data["employee_id"])
            if employee_id not in employees:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or plan not found or inactive"
                })
            
            employee = employees[employee_id]
            if employee.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or plan not found or inactive"
                })
            
            # Validate that benefits plan exists and has active status
            plan_id = str(benefits_data["plan_id"])
            if plan_id not in benefits_plans:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or plan not found or inactive"
                })
            
            plan = benefits_plans[plan_id]
            if plan.get("status") != "active":
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or plan not found or inactive"
                })
            
            # Validate that enrollment date is not in future
            enrollment_date = benefits_data["enrollment_date"]
            if is_future_date(enrollment_date):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid enrollment date or coverage level - enrollment date cannot be in future"
                })
            
            # Validate coverage_level enum according to schema
            valid_levels = ["employee_only", "employee_spouse", "employee_children", "family"]
            if benefits_data["coverage_level"] not in valid_levels:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid enrollment date or coverage level - coverage_level must be one of: {', '.join(valid_levels)}"
                })
            
            # Check that employee is not already enrolled in the same plan type
            plan_type = plan.get("plan_type")
            for existing_enrollment in employee_benefits.values():
                if (existing_enrollment.get("employee_id") == employee_id and 
                    existing_enrollment.get("status") == "active"):
                    existing_plan_id = str(existing_enrollment.get("plan_id"))
                    if existing_plan_id in benefits_plans:
                        existing_plan_type = benefits_plans[existing_plan_id].get("plan_type")
                        if existing_plan_type == plan_type:
                            return json.dumps({
                                "success": False,
                                "error": f"Halt: Employee already enrolled in same plan type"
                            })
            
            # Validate only allowed fields are present
            allowed_fields = ["employee_id", "plan_id", "enrollment_date", "coverage_level", "status",
                            "beneficiary_name", "beneficiary_relationship"]
            invalid_fields = [field for field in benefits_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for benefits enrollment: {', '.join(invalid_fields)}"
                })
            
            # Generate new enrollment ID
            new_enrollment_id = generate_id(employee_benefits)
            
            # Create new employee benefits record
            new_benefits = {
                "enrollment_id": str(new_enrollment_id),
                "employee_id": employee_id,
                "plan_id": plan_id,
                "enrollment_date": enrollment_date,
                "status": benefits_data.get("status", "active"),  # If enrollment status is not specified during enrollment, set it to active
                "coverage_level": benefits_data["coverage_level"],
                "beneficiary_name": benefits_data.get("beneficiary_name"),
                "beneficiary_relationship": benefits_data.get("beneficiary_relationship"),
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            employee_benefits[str(new_enrollment_id)] = new_benefits
            
            return json.dumps({
                "success": True,
                "action": "create",
                "enrollment_id": str(new_enrollment_id),
                "message": f"Employee benefits enrollment {new_enrollment_id} created successfully",
                "benefits_data": new_benefits
            })
        
        elif action == "update":
            if not enrollment_id:
                return json.dumps({
                    "success": False,
                    "error": "enrollment_id is required for update action"
                })
            
            if enrollment_id not in employee_benefits:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Enrollment not found"
                })
            
            if not benefits_data:
                return json.dumps({
                    "success": False,
                    "error": "benefits_data is required for update action"
                })
            
            # Validate at least one optional field is provided
            update_fields = ["employee_id", "plan_id", "enrollment_date", "status", "coverage_level", "beneficiary_name", "beneficiary_relationship"]
            provided_fields = [field for field in update_fields if field in benefits_data]
            if not provided_fields:
                return json.dumps({
                    "success": False,
                    "error": "At least one optional field must be provided for updates"
                })
            
            # Get current enrollment for validation
            current_benefits = employee_benefits[enrollment_id]
            
            # Validate only allowed fields for updates
            invalid_fields = [field for field in benefits_data.keys() if field not in update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for benefits enrollment update: {', '.join(invalid_fields)}"
                })
            
            # Validate status transitions if status is being updated
            if "status" in benefits_data:
                valid_statuses = ["active", "terminated", "pending"]
                new_status = benefits_data["status"]
                
                if new_status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Benefits enrollment operation failed - status must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Validate coverage_level enum if provided
            if "coverage_level" in benefits_data:
                valid_levels = ["employee_only", "employee_spouse", "employee_children", "family"]
                if benefits_data["coverage_level"] not in valid_levels:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Benefits enrollment operation failed - coverage_level must be one of: {', '.join(valid_levels)}"
                    })
            
            # Update employee benefits record
            updated_benefits = current_benefits.copy()
            for key, value in benefits_data.items():
                updated_benefits[key] = value
            
            updated_benefits["updated_at"] = "2025-10-01T12:00:00"
            employee_benefits[enrollment_id] = updated_benefits
            
            return json.dumps({
                "success": True,
                "action": "update",
                "enrollment_id": enrollment_id,
                "message": f"Employee benefits enrollment {enrollment_id} updated successfully",
                "benefits_data": updated_benefits
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "administer_employee_benefits",
                "description": "Create or update employee benefits enrollment records in the HR system. This tool manages employee benefits enrollments with comprehensive validation and data integrity controls. For creation, establishes new benefits enrollments with proper validation of employee/plan existence, enrollment dates, and duplicate prevention. For updates, modifies existing enrollments while maintaining data integrity and validating status transitions. Validates coverage levels, prevents duplicate enrollments in same plan type, and ensures enrollment dates are not in future. Essential for benefits administration, employee enrollment management, and maintaining accurate benefits records.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new benefits enrollment, 'update' to modify existing enrollment",
                            "enum": ["create", "update"]
                        },
                        "benefits_data": {
                            "type": "object",
                            "description": "Benefits enrollment data object. For create: requires employee_id, plan_id, enrollment_date, coverage_level. Optional: status, beneficiary_name, beneficiary_relationship. For update: at least one of employee_id, plan_id, enrollment_date, status, coverage_level, beneficiary_name, beneficiary_relationship. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "employee_id": {
                                    "type": "string",
                                    "description": "Employee identifier (required for create)"
                                },
                                "plan_id": {
                                    "type": "string",
                                    "description": "Benefits plan identifier (required for create)"
                                },
                                "enrollment_date": {
                                    "type": "string",
                                    "description": "Enrollment date in YYYY-MM-DD format (required for create, must not be in future)"
                                },
                                "coverage_level": {
                                    "type": "string",
                                    "description": "Coverage level for benefits",
                                    "enum": ["employee_only", "employee_spouse", "employee_children", "family"]
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Enrollment status",
                                    "enum": ["active", "terminated", "pending"]
                                },
                                "beneficiary_name": {
                                    "type": "string",
                                    "description": "Name of benefits beneficiary"
                                },
                                "beneficiary_relationship": {
                                    "type": "string",
                                    "description": "Relationship of beneficiary to employee"
                                }
                            }
                        },
                        "enrollment_id": {
                            "type": "string",
                            "description": "Unique identifier of the benefits enrollment (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }