import json
import re
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ExecuteEmployeeOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manage employee record creation and updates.
        
        Operations:
        - create_employee: Create new employee record (requires first_name, last_name, employee_type, department_id, location_id, job_title, start_date, tax_id, bank_account_number, routing_number, work_email, user_id)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        def validate_date_format(date_str: str, field_name: str) -> Optional[str]:
            if date_str:
                # Convert YYYY-MM-DD format for internal storage
                date_pattern = r'^\d{4}-\d{2}-\d{2}$'
                if not re.match(date_pattern, date_str):
                    return f"Invalid {field_name} format. Must be YYYY-MM-DD"
            return None
        
        def convert_date_format(date_str: str) -> str:
            """Convert YYYY-MM-DD format for internal storage"""
            if date_str and re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                return date_str
            return date_str
        
        def validate_tax_id_format(tax_id: str) -> Optional[str]:
            """Validate tax ID format ###-##-####"""
            if tax_id:
                tax_pattern = r'^\d{3}-\d{2}-\d{4}$'
                if not re.match(tax_pattern, tax_id):
                    return "Invalid tax_id format. Must be ###-##-####"
            return None
        
        def validate_bank_account_number(account_number: Any) -> Optional[str]:
            """Validate bank account number (8–17 digits, accepts string or number)"""
            if account_number is not None:
                acc_str = str(account_number)
                if not re.match(r'^\d{8,17}$', acc_str):
                    return "Invalid bank_account_number format. Must be 8–17 digits"
            return None
        
        def validate_routing_number(routing_number: Any) -> Optional[str]:
            """Validate bank routing number (9 digits, accepts string or number)"""
            if routing_number is not None:
                routing_str = str(routing_number)
                if not re.match(r'^\d{9}$', routing_str):
                    return "Invalid routing_number format. Must be exactly 9 digits"
            return None
        
        def validate_email_format(email: str) -> Optional[str]:
            """Validate email format"""
            if email:
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, email):
                    return "Invalid work_email format"
            return None
        
        # Validate operation_type
        valid_operations = ["create_employee", "update_employee_data"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "employee_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })
        
        # Access related data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "employee_id": None,
                "message": "Invalid data format for employee operations"
            })
        
        employees = data.get("employees", {})
        departments = data.get("departments", {})
        locations = data.get("locations", {})
        users = data.get("users", {})
        candidates = data.get("candidates", {})
        
        if operation_type == "create_employee":
            # Validate required fields for employee creation
            required_fields = [
                "first_name", "last_name", "employee_type", "department_id", "location_id",
                "job_title", "start_date", "tax_id", "bank_account_number", "routing_number",
                "work_email", "user_id"
            ]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "employee_id": None,
                    "message": f"Missing required fields for employee creation: {', '.join(missing_fields)}"
                })
            
            # Validate employee_type enum
            valid_employee_types = ["Full-time", "Part-time", "Contractor"]
            if kwargs["employee_type"] not in valid_employee_types:
                return json.dumps({
                    "success": False,
                    "employee_id": None,
                    "message": f"Invalid employee_type. Must be one of: {', '.join(valid_employee_types)}"
                })
            
            # Validate department exists
            if str(kwargs["department_id"]) not in departments:
                return json.dumps({
                    "success": False,
                    "employee_id": None,
                    "message": f"Department {kwargs['department_id']} not found"
                })
            
            # Validate location exists
            if str(kwargs["location_id"]) not in locations:
                return json.dumps({
                    "success": False,
                    "employee_id": None,
                    "message": f"Location {kwargs['location_id']} not found"
                })
            
            # Validate user exists
            if str(kwargs["user_id"]) not in users:
                return json.dumps({
                    "success": False,
                    "employee_id": None,
                    "message": f"User {kwargs['user_id']} not found"
                })
            
            # Validate candidate exists if provided
            if "candidate_id" in kwargs and kwargs["candidate_id"] is not None:
                if str(kwargs["candidate_id"]) not in candidates:
                    return json.dumps({
                        "success": False,
                        "employee_id": None,
                        "message": f"Candidate {kwargs['candidate_id']} not found"
                    })
            
            # Validate manager exists if provided
            if "manager_id" in kwargs and kwargs["manager_id"] is not None:
                if str(kwargs["manager_id"]) not in users:
                    return json.dumps({
                        "success": False,
                        "employee_id": None,
                        "message": f"Manager {kwargs['manager_id']} not found"
                    })
            
            # Validate tax_filing_status if provided
            if "tax_filing_status" in kwargs and kwargs["tax_filing_status"] is not None:
                valid_tax_statuses = ["single", "married_filing_joint", "married_filing_separate", "head_of_household", "qualifying_widow"]
                if kwargs["tax_filing_status"] not in valid_tax_statuses:
                    return json.dumps({
                        "success": False,
                        "employee_id": None,
                        "message": f"Invalid tax_filing_status. Must be one of: {', '.join(valid_tax_statuses)}"
                    })
            
            # Validate date format
            date_error = validate_date_format(kwargs["start_date"], "start_date")
            if date_error:
                return json.dumps({
                    "success": False,
                    "employee_id": None,
                    "message": date_error
                })
            
            # Validate tax_id format
            tax_error = validate_tax_id_format(kwargs["tax_id"])
            if tax_error:
                return json.dumps({
                    "success": False,
                    "employee_id": None,
                    "message": tax_error
                })
            
            # Validate bank account number format
            bank_error = validate_bank_account_number(kwargs["bank_account_number"])
            if bank_error:
                return json.dumps({
                    "success": False,
                    "employee_id": None,
                    "message": bank_error
                })
            
            # Validate routing number format
            routing_error = validate_routing_number(kwargs["routing_number"])
            if routing_error:
                return json.dumps({
                    "success": False,
                    "employee_id": None,
                    "message": routing_error
                })
            
            # Validate email format
            email_error = validate_email_format(kwargs["work_email"])
            if email_error:
                return json.dumps({
                    "success": False,
                    "employee_id": None,
                    "message": email_error
                })
            
            # Check for duplicate work email
            for employee in employees.values():
                if employee.get("work_email") == kwargs["work_email"]:
                    return json.dumps({
                        "success": False,
                        "employee_id": None,
                        "message": "An employee with this work email already exists"
                    })
            
            # Generate new employee ID and create record
            new_employee_id = generate_id(employees)
            timestamp = "2025-10-10T12:00:00"
            
            # Convert employee_type to lowercase with underscore for internal storage
            employee_type_internal = kwargs["employee_type"].lower().replace("-", "_")
            
            new_employee = {
                "employee_id": str(new_employee_id),
                "first_name": kwargs["first_name"],
                "last_name": kwargs["last_name"],
                "employee_type": employee_type_internal,
                "department_id": str(kwargs["department_id"]),
                "location_id": str(kwargs["location_id"]),
                "job_title": kwargs["job_title"],
                "start_date": convert_date_format(kwargs["start_date"]),
                "tax_id": kwargs["tax_id"],
                "bank_account_number": kwargs["bank_account_number"],
                "routing_number": kwargs["routing_number"],
                "work_email": kwargs["work_email"],
                "phone_number": kwargs.get("phone_number"),
                "manager_id": str(kwargs["manager_id"]) if kwargs.get("manager_id") else None,
                "tax_filing_status": kwargs.get("tax_filing_status"),
                "candidate_id": str(kwargs["candidate_id"]) if kwargs.get("candidate_id") else None,
                "employment_status": "active",
                "created_at": timestamp,
                "updated_at": timestamp
            }
            
            employees[str(new_employee_id)] = new_employee
            
            return json.dumps({
                "success": True,
                "employee": new_employee,
                "message": f"Employee {new_employee_id} created successfully"
            })
        
        elif operation_type == "update_employee_data":
            # Validate required fields for employee update
            required_fields = ["employee_id", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "employee_id": None,
                    "message": f"Missing required fields for employee update: {', '.join(missing_fields)}"
                })
            
            # Validate employee exists and is active
            employee = employees.get(str(kwargs["employee_id"]))
            if not employee or employee.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "employee_id": None,
                    "message": "Halt: Employee not found or inactive"
                })
            
            # Validate user has appropriate role
            user = users.get(str(kwargs["user_id"]))
            if not user or user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "employee_id": None,
                    "message": "Halt: User not found or inactive"
                })
            
            valid_roles = ["hr_admin", "hr_manager", "hr_director", "finance_manager"]
            if user.get("role") not in valid_roles:
                return json.dumps({
                    "success": False,
                    "employee_id": None,
                    "message": "Halt: User lacks authorization to perform this action"
                })
            
            # Update fields if provided
            updatable_fields = ["first_name", "last_name", "employee_type", "department_id", "location_id", 
                              "job_title", "tax_id", "bank_account_number", "routing_number", "manager_id", 
                              "tax_filing_status", "employment_status"]
            
            for field in updatable_fields:
                if field in kwargs and kwargs[field] is not None:
                    employee[field] = kwargs[field]
            
            employee["updated_at"] = "2025-10-10T12:00:00"
            
            return json.dumps({
                "success": True,
                "employee_id": kwargs["employee_id"],
                "message": f"Employee {kwargs['employee_id']} updated successfully"
            })
        
        return json.dumps({
            "success": False,
            "employee_id": None,
            "message": "Unhandled operation type"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "execute_employee_operations",
                "description": "Manage employee record creation and updates in the HR talent management system. This tool handles the complete employee onboarding process from initial record creation through ongoing employee data management. For creation, establishes new employee records with comprehensive validation to ensure data integrity, regulatory compliance, and business rule adherence. Validates employee details including personal information, employment type, department and location assignments, job titles, start dates, tax identification, banking information, and contact details. Prevents duplicate employee creation by checking existing work email addresses. Requires validation of department, location, and user existence before proceeding. Essential for employee lifecycle management, payroll setup, and compliance with employment regulations. Supports the complete employee onboarding workflow from initial hire through ongoing employment management.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation to perform: 'create_employee' to establish new employee record, 'update_employee_data' to update existing employee",
                            "enum": ["create_employee", "update_employee_data"]
                        },
                        "first_name": {
                            "type": "string",
                            "description": "Employee's legal first name. Enter the employee's first name as text (e.g., 'John', 'Sarah', 'Michael'). This field is required only when operation_type is 'create_employee'. Should match legal documents for payroll and tax purposes. Example: 'Jennifer'"
                        },
                        "last_name": {
                            "type": "string",
                            "description": "Employee's legal last name or surname. Enter the employee's last name as text (e.g., 'Smith', 'Johnson', 'Garcia'). This field is required only when operation_type is 'create_employee'. Should match legal documents for payroll and tax purposes. Example: 'Anderson'"
                        },
                        "employee_type": {
                            "type": "string",
                            "description": "Type of employment classification. Select from: 'Full-time' for regular full-time employees (typically 40 hours/week), 'Part-time' for part-time employees (less than full-time hours), or 'Contractor' for contract workers. This field is required only when operation_type is 'create_employee'. Must be exactly one of these three values with proper capitalization and hyphenation. Determines benefits eligibility and employment terms. Example: 'Full-time'",
                            "enum": ["Full-time", "Part-time", "Contractor"]
                        },
                        "department_id": {
                            "type": "string",
                            "description": "Unique identifier of the department where the employee will work. Enter the department ID as a string (e.g., '101', '205'). This field is required only when operation_type is 'create_employee'. The system validates that this department exists in the database before creating the employee record. Used for organizational structure and reporting. Example: '304'"
                        },
                        "location_id": {
                            "type": "string",
                            "description": "Unique identifier of the physical work location or office. Enter the location ID as a string (e.g., '1', '5', '12'). This field is required only when operation_type is 'create_employee'. The system validates that this location exists in the database. Determines office assignment, timezone, and local HR policies. Example: '7'"
                        },
                        "job_title": {
                            "type": "string",
                            "description": "Official job title or position name. Enter the full job title as text (e.g., 'Software Engineer II', 'Senior Marketing Specialist', 'Accountant'). This field is required only when operation_type is 'create_employee'. Should match the title in the offer letter and organizational hierarchy. Example: 'Senior Product Manager'"
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Employee's first day of employment. Enter date in YYYY-MM-DD format (e.g., '2025-03-15' for March 15, 2025). This field is required only when operation_type is 'create_employee'. Must follow the exact format YYYY-MM-DD with hyphens as separators. The system validates the date format. Used for benefits eligibility, tenure calculations, and onboarding scheduling. Example: '2025-04-01'"
                        },
                        "tax_id": {
                            "type": "string",
                            "description": "Tax identification number or Social Security Number (SSN). Enter in the format ###-##-#### (e.g., '123-45-6789'). This field is required only when operation_type is 'create_employee'. Must follow the exact format with three digits, hyphen, two digits, hyphen, four digits. The system validates the format. Required for payroll tax reporting and compliance. Example: '987-65-4321'"
                        },
                        "bank_account_number": {
                            "type": "string",
                            "description": "Employee's bank account number for direct deposit of salary. Enter as 8-17 digits (e.g., '12345678' or '12345678901234567'). This field is required only when operation_type is 'create_employee'. Must contain only digits, with a minimum of 8 digits and maximum of 17 digits. The system validates the length. Required for payroll direct deposit setup. Example: '987654321012'"
                        },
                        "routing_number": {
                            "type": "string",
                            "description": "Bank routing number for direct deposit transactions. Enter as exactly 9 digits (e.g., '123456789'). This field is required only when operation_type is 'create_employee'. Must be precisely 9 digits with no hyphens or spaces. The system validates the length. Used with bank_account_number for payroll direct deposit. Example: '021000021'"
                        },
                        "work_email": {
                            "type": "string",
                            "description": "Employee's company email address. Enter in valid email format (e.g., 'john.smith@company.com'). This field is required only when operation_type is 'create_employee'. Must be a properly formatted email address with @ symbol and valid domain. The system validates email format and checks that this email is not already in use by another employee. Used for system access and communications. Example: 'sarah.jones@company.com'"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Unique identifier of the HR user creating or updating the employee record. Enter the user ID as a string (e.g., '5001'). This field is required when operation_type is 'create_employee'. The system validates that this user exists in the database. Used for audit trail to track who created the employee record. Example: '6002'"
                        },
                        "employee_id": {
                            "type": "string",
                            "description": "Unique identifier of the existing employee to be updated. Enter the employee ID as a string (e.g., '3001'). This field is required only when operation_type is 'update_employee_data'. The system validates that this employee exists and has an 'active' status. Used to identify which employee record to modify. Example: '4005'"
                        },
                        "candidate_id": {
                            "type": "string",
                            "description": "Unique identifier linking this employee to their candidate record from the recruiting process. Enter the candidate ID as a string (e.g., '2001'). This field is optional for operation_type 'create_employee'. If provided, the system validates that this candidate exists in the database. Creates connection between recruiting and employee records for reporting. Example: '1503'"
                        },
                        "phone_number": {
                            "type": "string",
                            "description": "Employee's contact phone number. Enter phone number as text (e.g., '555-123-4567', '(555) 123-4567', or '+1-555-123-4567'). This field is optional for operation_type 'create_employee'. No specific format is enforced. Used for employee contact and emergency purposes. Example: '425-555-0123'"
                        },
                        "manager_id": {
                            "type": "string",
                            "description": "Unique identifier of the employee's direct manager or supervisor. Enter the manager's user ID as a string (e.g., '7001'). This field is optional for operation_type 'create_employee'. If provided, the system validates that this user exists in the database. Establishes reporting hierarchy for organizational structure. Example: '8003'"
                        },
                        "tax_filing_status": {
                            "type": "string",
                            "description": "Employee's tax filing status for withholding purposes. Select from: 'single' for single filers, 'married_filing_joint' for married filing jointly, 'married_filing_separate' for married filing separately, 'head_of_household' for head of household, or 'qualifying_widow' for qualifying widow(er). This field is optional for operation_type 'create_employee'. Must be exactly one of these five values. Affects payroll tax withholding calculations. Example: 'married_filing_joint'",
                            "enum": ["single", "married_filing_joint", "married_filing_separate", "head_of_household", "qualifying_widow"]
                        },
                        "employment_status": {
                            "type": "string",
                            "description": "Current employment status of the employee. Enter status value as text (e.g., 'active', 'terminated', 'on_leave'). This field is optional and only applicable when operation_type is 'update_employee_data'. Used to update an existing employee's status. Common values include 'active' for currently employed, 'terminated' for ended employment, 'on_leave' for temporary leave. Example: 'active'"
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }
