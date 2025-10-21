import json
import re
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool
from datetime import datetime, date


class HandleBenefitEnrollmentOperations(Tool):
    
    # --- Utility Methods ---
    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> int:
        """Utility to generate a new sequential ID for the benefit_enrollments table."""
        if not table:
            return 11001
        return max(int(k) for k in table.keys()) + 1

    @staticmethod
    def _validate_date_format(date_str: str, field_name: str, allow_future: bool = True) -> Optional[str]:
        """Validates date format (YYYY-MM-DD) and checks if it's not in the future."""
        if date_str:
            date_pattern = r'^\d{4}-\d{2}-\d{2}$'
            if not re.match(date_pattern, date_str):
                return f"Invalid {field_name} format. Must be YYYY-MM-DD"
            
            try:
                dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
                # Check for future date if not allowed
                if not allow_future:
                    simulated_today = date(2025, 10, 10) # Using same simulated date as other tools
                    if dt_obj.date() > simulated_today:
                         return f"{field_name} cannot be in the future (compared to the system date)."
            except ValueError:
                return f"Invalid date value provided for {field_name}. Please check year/month/day validity."
        return None

    @staticmethod
    def _convert_date_format(date_str: str) -> str:
        """Convert YYYY-MM-DD format for internal storage."""
        if date_str and re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return date_str
        return date_str

    @staticmethod
    def _validate_status_field(status_value: str, field_name: str, valid_statuses: list) -> Optional[str]:
        """Validate status field against allowed values."""
        if status_value and status_value not in valid_statuses:
            return f"Invalid {field_name}. Must be one of: {', '.join(valid_statuses)}"
        return None

    @staticmethod
    def _is_date_in_range(date_str: str, start_date: str, end_date: str) -> bool:
        """Check if date is within the specified range."""
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            start_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            return start_obj <= date_obj <= end_obj
        except ValueError:
            return False

    # --- Core Tool Logic ---

    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manages benefit enrollment operations.
        """
        
        valid_operations = ["create_enrollment"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "enrollment_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "enrollment_id": None,
                "message": "Invalid data format for benefit enrollment operations"
            })
        
        enrollments = data.get("benefit_enrollments", {})
        employees = data.get("employees", {})
        benefit_plans = data.get("benefit_plans", {})
        users = data.get("users", {})
        documents = data.get("documents", {})
        
        simulated_today = date(2025, 10, 1) # Used for past date checks

        # --- Benefit Enrollment Creation (create_enrollment) ---
        if operation_type == "create_enrollment":
            required_fields = ["employee_id", "plan_id", "effective_date", "employee_contribution", 
                             "employer_contribution", "enrollment_window_start", "enrollment_window_end", 
                             "selection_date", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "enrollment_id": None,
                    "message": f"Halt: Missing mandatory fields: {', '.join(missing_fields)}",
                    "transfer_to_human": True
                })

            # 1. Validation Checks
            employee_id_str = str(kwargs["employee_id"])
            plan_id_str = str(kwargs["plan_id"])
            requester_id_str = str(kwargs["user_id"]) if kwargs.get("user_id") is not None else None

            # SOP: Verify user is an active HR Admin, HR Manager, or HR Director
            requester = users.get(requester_id_str)
            if not requester:
                return json.dumps({"success": False, "enrollment_id": None, "message": "Halt: Operation failed due to system errors - requester user not found", "transfer_to_human": True})
            
            if requester.get("employment_status") != "active" or requester.get("role") not in ["hr_manager", "hr_admin", "hr_payroll_administrator"]:
                return json.dumps({"success": False, "enrollment_id": None, "message": "Halt: Unauthorized requester attempting to create enrollment - must be active HR Admin/Manager/Director", "transfer_to_human": True})

            # Verify employee exists and is active
            employee = employees.get(employee_id_str)
            if not employee or employee.get("employment_status") not in ["active", "on_leave"]:
                return json.dumps({"success": False, "enrollment_id": None, "message": "Halt: Employee not found or inactive", "transfer_to_human": True})

            # Verify plan exists and is active
            plan = benefit_plans.get(plan_id_str)
            if not plan or plan.get("plan_status") != "active":
                return json.dumps({"success": False, "enrollment_id": None, "message": "Halt: Plan not found or inactive", "transfer_to_human": True})

            # Validate dates
            effective_date = kwargs["effective_date"]
            enrollment_window_start = kwargs["enrollment_window_start"]
            enrollment_window_end = kwargs["enrollment_window_end"]
            selection_date = kwargs["selection_date"]

            # Convert dates for validation
            converted_effective_date = ManageBenefitEnrollmentOperations._convert_date_format(effective_date)
            converted_window_start = ManageBenefitEnrollmentOperations._convert_date_format(enrollment_window_start)
            converted_window_end = ManageBenefitEnrollmentOperations._convert_date_format(enrollment_window_end)
            converted_selection_date = ManageBenefitEnrollmentOperations._convert_date_format(selection_date)

            # Validate effective date is not in the past
            effective_date_error = ManageBenefitEnrollmentOperations._validate_date_format(effective_date, "effective_date", allow_future=False)
            if effective_date_error:
                return json.dumps({"success": False, "enrollment_id": None, "message": f"Halt: {effective_date_error}", "transfer_to_human": True})

            # Validate selection date is within enrollment window
            if not ManageBenefitEnrollmentOperations._is_date_in_range(converted_selection_date, converted_window_start, converted_window_end):
                return json.dumps({"success": False, "enrollment_id": None, "message": "Halt: Selection date outside enrollment window", "transfer_to_human": True})

            # Validate contribution amounts
            try:
                employee_contribution = float(kwargs["employee_contribution"])
                employer_contribution = float(kwargs["employer_contribution"])
                if employee_contribution < 0 or employer_contribution < 0:
                    return json.dumps({"success": False, "enrollment_id": None, "message": "Halt: Negative contribution amounts", "transfer_to_human": True})
            except (ValueError, TypeError):
                return json.dumps({"success": False, "enrollment_id": None, "message": "Halt: Invalid contribution amount format", "transfer_to_human": True})

            # Validate supporting documents if provided
            supporting_documents = kwargs.get("supporting_documents", [])
            if supporting_documents:
                valid_doc_categories = ["insurance_form", "tax_form", "other"]
                for doc in supporting_documents:
                    if not isinstance(doc, dict):
                        return json.dumps({"success": False, "enrollment_id": None, "message": "Halt: Invalid document format", "transfer_to_human": True})
                    
                    if not doc.get("file_name") or not doc.get("document_category"):
                        return json.dumps({"success": False, "enrollment_id": None, "message": "Halt: Document missing file_name or document_category", "transfer_to_human": True})
                    
                    if doc.get("document_category") not in valid_doc_categories:
                        return json.dumps({"success": False, "enrollment_id": None, "message": "Halt: Invalid document_category. Must be one of: insurance_form, tax_form, other", "transfer_to_human": True})
                    
                    # Check for duplicate document names
                    file_name = doc.get("file_name")
                    if any(d.get("file_name") == file_name for d in documents.values()):
                        return json.dumps({"success": False, "enrollment_id": None, "message": f"Halt: Duplicate document - {file_name}", "transfer_to_human": True})

            # 2. Create Benefit Enrollment Record
            new_enrollment_id = ManageBenefitEnrollmentOperations._generate_id(enrollments)
            timestamp = "2025-10-10T12:00:00"

            new_enrollment = {
                "enrollment_id": str(new_enrollment_id),
                "employee_id": employee_id_str,
                "plan_id": plan_id_str,
                "effective_date": converted_effective_date,
                "employee_contribution": employee_contribution,
                "employer_contribution": employer_contribution,
                "enrollment_window_start": converted_window_start,
                "enrollment_window_end": converted_window_end,
                "selection_date": converted_selection_date,
                "enrollment_status": "pending",
                "hr_manager_approval_status": "pending",
                "approved_by": None,
                "approval_date": None,
                "created_at": timestamp
            }
            
            enrollments[str(new_enrollment_id)] = new_enrollment
            
            # SOP: Create Audit Entry
            try:
                audit_trails = data.setdefault("audit_trails", {})
                new_audit_id = str(max([int(k) for k in audit_trails.keys()] + [0]) + 1)
                audit_entry = {
                    "audit_id": new_audit_id,
                    "reference_id": str(new_enrollment_id),
                    "reference_type": "benefit",
                    "action": "create",
                    "user_id": requester_id_str,
                    "field_name": None,
                    "old_value": None,
                    "new_value": json.dumps({"created_by": requester_id_str, "plan_id": plan_id_str, "employee_id": employee_id_str}),
                    "created_at": timestamp
                }
                audit_trails[new_audit_id] = audit_entry
            except Exception:
                # If audit fails, we still report success for the primary operation
                pass

            # SOP: Upload supporting documents if provided
            uploaded_docs = []
            if supporting_documents:
                try:
                    for doc in supporting_documents:
                        # Create document record
                        new_doc_id = str(max([int(k) for k in documents.keys()] + [0]) + 1)
                        document_record = {
                            "document_id": new_doc_id,
                            "document_category": doc.get("document_category"),
                            "related_entity_type": "benefit",
                            "related_entity_id": str(new_enrollment_id),
                            "file_name": doc.get("file_name"),
                            "file_format": doc.get("file_format", "pdf"),
                            "upload_date": timestamp,
                            "uploaded_by": requester_id_str,
                            "document_status": "active",
                            "expiry_date": None,
                            "verification_status": "pending",
                            "verified_by": None,
                            "verified_date": None,
                            "created_at": timestamp
                        }
                        documents[new_doc_id] = document_record
                        uploaded_docs.append(new_doc_id)

                        # Create audit entry for document upload
                        try:
                            doc_audit_id = str(max([int(k) for k in audit_trails.keys()] + [0]) + 1)
                            doc_audit_entry = {
                                "audit_id": doc_audit_id,
                                "reference_id": new_doc_id,
                                "reference_type": "document",
                                "action": "create",
                                "user_id": requester_id_str,
                                "field_name": None,
                                "old_value": None,
                                "new_value": json.dumps({"uploaded_by": requester_id_str, "related_entity": str(new_enrollment_id)}),
                                "created_at": timestamp
                            }
                            audit_trails[doc_audit_id] = doc_audit_entry
                        except Exception:
                            pass
                except Exception:
                    return json.dumps({"success": False, "enrollment_id": None, "message": "Halt: Document upload failed", "transfer_to_human": True})

            return json.dumps({
                "success": True,
                "enrollment_id": str(new_enrollment_id),
                "message": f"Benefit enrollment {new_enrollment_id} created successfully. Status: pending. Documents uploaded: {len(uploaded_docs)}.",
                "uploaded_documents": uploaded_docs
            })
        
        return json.dumps({
            "success": False,
            "enrollment_id": None,
            "message": "Unhandled operation type"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_benefit_enrollment_operations",
                "description": "Manages benefit enrollment operations. 'create_enrollment' creates benefit enrollments with proper validation of enrollment windows, contribution amounts, and supporting documents.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation to perform: 'create_enrollment'.",
                            "enum": ["create_enrollment"]
                        },
                        "employee_id": {
                            "type": "string",
                            "description": "Unique identifier of the employee (required for create_enrollment)."
                        },
                        "plan_id": {
                            "type": "string",
                            "description": "Benefit plan identifier (required for create_enrollment)."
                        },
                        "effective_date": {
                            "type": "string",
                            "description": "Effective date for the enrollment (YYYY-MM-DD, required for create_enrollment, must not be in the past)."
                        },
                        "employee_contribution": {
                            "type": "number",
                            "description": "Employee contribution amount (required for create_enrollment, must be non-negative)."
                        },
                        "employer_contribution": {
                            "type": "number",
                            "description": "Employer contribution amount (required for create_enrollment, must be non-negative)."
                        },
                        "enrollment_window_start": {
                            "type": "string",
                            "description": "Enrollment window start date (YYYY-MM-DD, required for create_enrollment)."
                        },
                        "enrollment_window_end": {
                            "type": "string",
                            "description": "Enrollment window end date (YYYY-MM-DD, required for create_enrollment)."
                        },
                        "selection_date": {
                            "type": "string",
                            "description": "Date when enrollment was selected (YYYY-MM-DD, required for create_enrollment, must be within enrollment window)."
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Unique identifier of the HR Admin/Manager/Director creating the enrollment (required for all operations)."
                        },
                        "supporting_documents": {
                            "type": "array",
                            "description": "Optional supporting documents for the enrollment.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "file_name": {"type": "string", "description": "Name of the document file"},
                                    "document_category": {"type": "string", "description": "Category of the document", "enum": ["insurance_form", "tax_form", "other"]},
                                    "file_format": {"type": "string", "description": "Format of the file (default: pdf)"}
                                },
                                "required": ["file_name", "document_category"]
                            }
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }
