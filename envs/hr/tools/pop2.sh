#!/bin/bash

# Create directory for the tools
mkdir -p hr_tools_2

# Tool 26: create_training_program
cat > hr_tools_2/create_training_program.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateTrainingProgram(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], program_name: str, program_type: str,
               duration_hours: int, delivery_method: str, description: Optional[str] = None,
               mandatory: bool = False, status: str = 'active') -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        training_programs = data.get("training_programs", {})
        
        # Validate program_type
        valid_program_types = ['onboarding', 'compliance', 'technical', 'leadership', 'safety', 'diversity', 'ai_ethics']
        if program_type not in valid_program_types:
            return json.dumps({"success": False, "error": f"Invalid program_type. Must be one of {valid_program_types}", "halt": True})
        
        # Validate delivery_method
        valid_delivery_methods = ['in_person', 'online', 'hybrid', 'self_paced']
        if delivery_method not in valid_delivery_methods:
            return json.dumps({"success": False, "error": f"Invalid delivery_method. Must be one of {valid_delivery_methods}", "halt": True})
        
        # Validate status
        valid_statuses = ['active', 'inactive', 'draft']
        if status not in valid_statuses:
            return json.dumps({"success": False, "error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        program_id = generate_id(training_programs)
        timestamp = "2025-10-01T00:00:00"
        
        new_program = {
            "program_id": program_id,
            "program_name": program_name,
            "program_type": program_type,
            "description": description,
            "duration_hours": duration_hours,
            "delivery_method": delivery_method,
            "mandatory": mandatory,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        training_programs[program_id] = new_program
        return json.dumps({"program_id": program_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_training_program",
                "description": "Create a new training program",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "program_name": {"type": "string", "description": "Program name"},
                        "program_type": {"type": "string", "description": "Program type (onboarding, compliance, technical, leadership, safety, diversity, ai_ethics)"},
                        "duration_hours": {"type": "integer", "description": "Duration in hours"},
                        "delivery_method": {"type": "string", "description": "Delivery method (in_person, online, hybrid, self_paced)"},
                        "description": {"type": "string", "description": "Program description"},
                        "mandatory": {"type": "boolean", "description": "Whether program is mandatory (True/False)"},
                        "status": {"type": "string", "description": "Status (active, inactive, draft), defaults to active"}
                    },
                    "required": ["program_name", "program_type", "duration_hours", "delivery_method"]
                }
            }
        }
EOF

# Tool 27: update_training_program
cat > hr_tools_2/update_training_program.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateTrainingProgram(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], program_id: str, program_name: Optional[str] = None,
               description: Optional[str] = None, duration_hours: Optional[int] = None,
               delivery_method: Optional[str] = None, mandatory: Optional[bool] = None,
               status: Optional[str] = None) -> str:
        
        training_programs = data.get("training_programs", {})
        
        # Validate program exists
        if program_id not in training_programs:
            return json.dumps({"success": False, "error": f"Training program {program_id} not found", "halt": True})
        
        program = training_programs[program_id]
        
        # Validate delivery_method if provided
        if delivery_method is not None:
            valid_delivery_methods = ['in_person', 'online', 'hybrid', 'self_paced']
            if delivery_method not in valid_delivery_methods:
                return json.dumps({"success": False, "error": f"Invalid delivery_method. Must be one of {valid_delivery_methods}", "halt": True})
        
        # Validate status if provided
        if status is not None:
            valid_statuses = ['active', 'inactive', 'draft']
            if status not in valid_statuses:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Update fields
        if program_name is not None:
            program["program_name"] = program_name
        if description is not None:
            program["description"] = description
        if duration_hours is not None:
            program["duration_hours"] = duration_hours
        if delivery_method is not None:
            program["delivery_method"] = delivery_method
        if mandatory is not None:
            program["mandatory"] = mandatory
        if status is not None:
            program["status"] = status
        
        program["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Training program updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_training_program",
                "description": "Update an existing training program",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "program_id": {"type": "string", "description": "Program ID"},
                        "program_name": {"type": "string", "description": "Updated program name"},
                        "description": {"type": "string", "description": "Updated description"},
                        "duration_hours": {"type": "integer", "description": "Updated duration in hours"},
                        "delivery_method": {"type": "string", "description": "Updated delivery method (in_person, online, hybrid, self_paced)"},
                        "mandatory": {"type": "boolean", "description": "Updated mandatory flag (True/False)"},
                        "status": {"type": "string", "description": "Updated status (active, inactive, draft)"}
                    },
                    "required": ["program_id"]
                }
            }
        }
EOF

# Tool 28: enroll_employee_training
cat > hr_tools_2/enroll_employee_training.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class EnrollEmployeeTraining(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, program_id: str,
               enrollment_date: str, status: str = 'enrolled') -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        employees = data.get("employees", {})
        training_programs = data.get("training_programs", {})
        employee_training = data.get("employee_training", {})
        
        # Validate employee exists
        if employee_id not in employees:
            return json.dumps({"success": False, "error": f"Employee {employee_id} not found", "halt": True})
        
        # Validate training program exists
        if program_id not in training_programs:
            return json.dumps({"success": False, "error": f"Training program {program_id} not found", "halt": True})
        
        # Validate status
        valid_statuses = ['enrolled', 'in_progress', 'completed', 'failed', 'cancelled']
        if status not in valid_statuses:
            return json.dumps({"success": False, "error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        training_record_id = generate_id(employee_training)
        timestamp = "2025-10-01T00:00:00"
        
        new_training = {
            "training_record_id": training_record_id,
            "employee_id": employee_id,
            "program_id": program_id,
            "enrollment_date": enrollment_date,
            "completion_date": None,
            "status": status,
            "score": None,
            "certificate_issued": False,
            "expiry_date": None,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        employee_training[training_record_id] = new_training
        return json.dumps({"training_record_id": training_record_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "enroll_employee_training",
                "description": "Enroll an employee in a training program",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "Employee ID"},
                        "program_id": {"type": "string", "description": "Training program ID"},
                        "enrollment_date": {"type": "string", "description": "Enrollment date"},
                        "status": {"type": "string", "description": "Status (enrolled, in_progress, completed, failed, cancelled), defaults to enrolled"}
                    },
                    "required": ["employee_id", "program_id", "enrollment_date"]
                }
            }
        }
EOF

# Tool 29: complete_employee_training
cat > hr_tools_2/complete_employee_training.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CompleteEmployeeTraining(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], training_record_id: str, completion_date: str,
               status: str, score: Optional[float] = None, certificate_issued: bool = False,
               expiry_date: Optional[str] = None) -> str:
        
        employee_training = data.get("employee_training", {})
        
        # Validate training record exists
        if training_record_id not in employee_training:
            return json.dumps({"success": False, "error": f"Training record {training_record_id} not found", "halt": True})
        
        # Validate status
        valid_statuses = ['completed', 'failed']
        if status not in valid_statuses:
            return json.dumps({"success": False, "error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Validate score if provided
        if score is not None and (score < 0 or score > 100):
            return json.dumps({"success": False, "error": "Score must be between 0 and 100", "halt": True})
        
        training_record = employee_training[training_record_id]
        
        # Update training record
        training_record["completion_date"] = completion_date
        training_record["status"] = status
        training_record["score"] = score
        training_record["certificate_issued"] = certificate_issued
        training_record["expiry_date"] = expiry_date
        training_record["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Training completion recorded"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "complete_employee_training",
                "description": "Record completion of employee training",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "training_record_id": {"type": "string", "description": "Training record ID"},
                        "completion_date": {"type": "string", "description": "Completion date"},
                        "status": {"type": "string", "description": "Status (completed, failed)"},
                        "score": {"type": "number", "description": "Training score (0-100)"},
                        "certificate_issued": {"type": "boolean", "description": "Whether certificate was issued (True/False)"},
                        "expiry_date": {"type": "string", "description": "Certificate expiry date"}
                    },
                    "required": ["training_record_id", "completion_date", "status"]
                }
            }
        }
EOF

# Tool 30: upload_document
cat > hr_tools_2/upload_document.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UploadDocument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], document_name: str, document_type: str,
               file_path: str, uploaded_by: str, confidentiality_level: str,
               employee_id: Optional[str] = None, retention_period_years: int = 7,
               expiry_date: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        users = data.get("users", {})
        employees = data.get("employees", {})
        document_storage = data.get("document_storage", {})
        
        # Validate uploaded_by user exists
        if uploaded_by not in users:
            return json.dumps({"success": False, "error": f"User {uploaded_by} not found", "halt": True})
        
        # Validate employee exists if provided
        if employee_id is not None and employee_id not in employees:
            return json.dumps({"success": False, "error": f"Employee {employee_id} not found", "halt": True})
        
        # Validate document_type
        valid_document_types = ['contract', 'policy', 'handbook', 'form', 'certificate', 'report', 'resume', 'offer_letter']
        if document_type not in valid_document_types:
            return json.dumps({"success": False, "error": f"Invalid document_type. Must be one of {valid_document_types}", "halt": True})
        
        # Validate confidentiality_level
        valid_confidentiality_levels = ['public', 'internal', 'confidential', 'restricted']
        if confidentiality_level not in valid_confidentiality_levels:
            return json.dumps({"success": False, "error": f"Invalid confidentiality_level. Must be one of {valid_confidentiality_levels}", "halt": True})
        
        document_id = generate_id(document_storage)
        timestamp = "2025-10-01T00:00:00"
        
        new_document = {
            "document_id": document_id,
            "document_name": document_name,
            "document_type": document_type,
            "employee_id": employee_id,
            "file_path": file_path,
            "upload_date": timestamp,
            "uploaded_by": uploaded_by,
            "confidentiality_level": confidentiality_level,
            "retention_period_years": retention_period_years,
            "expiry_date": expiry_date,
            "status": "active",
            "created_at": timestamp
        }
        
        document_storage[document_id] = new_document
        return json.dumps({"document_id": document_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "upload_document",
                "description": "Upload a new document to the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_name": {"type": "string", "description": "Document name"},
                        "document_type": {"type": "string", "description": "Document type (contract, policy, handbook, form, certificate, report, resume, offer_letter)"},
                        "file_path": {"type": "string", "description": "File path"},
                        "uploaded_by": {"type": "string", "description": "User ID of uploader"},
                        "confidentiality_level": {"type": "string", "description": "Confidentiality level (public, internal, confidential, restricted)"},
                        "employee_id": {"type": "string", "description": "Associated employee ID"},
                        "retention_period_years": {"type": "integer", "description": "Retention period in years, defaults to 7"},
                        "expiry_date": {"type": "string", "description": "Document expiry date"}
                    },
                    "required": ["document_name", "document_type", "file_path", "uploaded_by", "confidentiality_level"]
                }
            }
        }
EOF

# Tool 31: update_document
cat > hr_tools_2/update_document.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateDocument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], document_id: str, document_name: Optional[str] = None,
               confidentiality_level: Optional[str] = None, retention_period_years: Optional[int] = None,
               expiry_date: Optional[str] = None, status: Optional[str] = None) -> str:
        
        document_storage = data.get("document_storage", {})
        
        # Validate document exists
        if document_id not in document_storage:
            return json.dumps({"success": False, "error": f"Document {document_id} not found", "halt": True})
        
        document = document_storage[document_id]
        
        # Validate confidentiality_level if provided
        if confidentiality_level is not None:
            valid_confidentiality_levels = ['public', 'internal', 'confidential', 'restricted']
            if confidentiality_level not in valid_confidentiality_levels:
                return json.dumps({"success": False, "error": f"Invalid confidentiality_level. Must be one of {valid_confidentiality_levels}", "halt": True})
        
        # Validate status if provided
        if status is not None:
            valid_statuses = ['active', 'archived', 'deleted']
            if status not in valid_statuses:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Update fields
        if document_name is not None:
            document["document_name"] = document_name
        if confidentiality_level is not None:
            document["confidentiality_level"] = confidentiality_level
        if retention_period_years is not None:
            document["retention_period_years"] = retention_period_years
        if expiry_date is not None:
            document["expiry_date"] = expiry_date
        if status is not None:
            document["status"] = status
        
        return json.dumps({"success": True, "message": "Document updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_document",
                "description": "Update an existing document",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_id": {"type": "string", "description": "Document ID"},
                        "document_name": {"type": "string", "description": "Updated document name"},
                        "confidentiality_level": {"type": "string", "description": "Updated confidentiality level (public, internal, confidential, restricted)"},
                        "retention_period_years": {"type": "integer", "description": "Updated retention period"},
                        "expiry_date": {"type": "string", "description": "Updated expiry date"},
                        "status": {"type": "string", "description": "Updated status (active, archived, deleted)"}
                    },
                    "required": ["document_id"]
                }
            }
        }
EOF

# Tool 32: create_audit_log
cat > hr_tools_2/create_audit_log.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateAuditLog(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, action: str, reference_type: str,
               reference_id: str, field_name: Optional[str] = None,
               old_value: Optional[str] = None, new_value: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        users = data.get("users", {})
        audit_logs = data.get("audit_logs", {})
        
        # Validate user exists
        if user_id not in users:
            return json.dumps({"success": False, "error": f"User {user_id} not found", "halt": True})
        
        # Validate action
        valid_actions = ['create', 'read', 'update', 'delete', 'approve', 'reject']
        if action not in valid_actions:
            return json.dumps({"success": False, "error": f"Invalid action. Must be one of {valid_actions}", "halt": True})
        
        log_id = generate_id(audit_logs)
        timestamp = "2025-10-01T00:00:00"
        
        new_audit_log = {
            "log_id": log_id,
            "user_id": user_id,
            "action": action,
            "reference_type": reference_type,
            "reference_id": reference_id,
            "field_name": field_name,
            "old_value": old_value,
            "new_value": new_value,
            "timestamp": timestamp
        }
        
        audit_logs[log_id] = new_audit_log
        return json.dumps({"log_id": log_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_audit_log",
                "description": "Create a new audit log entry",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User ID performing the action"},
                        "action": {"type": "string", "description": "Action performed (create, read, update, delete, approve, reject)"},
                        "reference_type": {"type": "string", "description": "Type of record being acted upon"},
                        "reference_id": {"type": "string", "description": "ID of the record being acted upon"},
                        "field_name": {"type": "string", "description": "Specific field name if applicable"},
                        "old_value": {"type": "string", "description": "Previous value"},
                        "new_value": {"type": "string", "description": "New value"}
                    },
                    "required": ["user_id", "action", "reference_type", "reference_id"]
                }
            }
        }
EOF

# Tool 33: get_users
cat > hr_tools_2/get_users.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetUsers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: Optional[str] = None,
               email: Optional[str] = None, role: Optional[str] = None,
               status: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        results = []
        
        for user in users.values():
            if user_id and user.get("user_id") != user_id:
                continue
            if email and user.get("email", "").lower() != email.lower():
                continue
            if role and user.get("role") != role:
                continue
            if status and user.get("status") != status:
                continue
            results.append(user)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_users",
                "description": "Get users with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "Filter by user ID"},
                        "email": {"type": "string", "description": "Filter by email"},
                        "role": {"type": "string", "description": "Filter by role"},
                        "status": {"type": "string", "description": "Filter by status"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 34: get_employees
cat > hr_tools_2/get_employees.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetEmployees(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: Optional[str] = None,
               position_id: Optional[str] = None, employment_status: Optional[str] = None,
               manager_id: Optional[str] = None) -> str:
        
        employees = data.get("employees", {})
        results = []
        
        for employee in employees.values():
            if employee_id and employee.get("employee_id") != employee_id:
                continue
            if position_id and employee.get("position_id") != position_id:
                continue
            if employment_status and employee.get("employment_status") != employment_status:
                continue
            if manager_id and employee.get("manager_id") != manager_id:
                continue
            results.append(employee)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_employees",
                "description": "Get employees with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "position_id": {"type": "string", "description": "Filter by position ID"},
                        "employment_status": {"type": "string", "description": "Filter by employment status"},
                        "manager_id": {"type": "string", "description": "Filter by manager ID"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 35: get_departments
cat > hr_tools_2/get_departments.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetDepartments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], department_id: Optional[str] = None,
               manager_id: Optional[str] = None, status: Optional[str] = None) -> str:
        
        departments = data.get("departments", {})
        results = []
        
        for department in departments.values():
            if department_id and department.get("department_id") != department_id:
                continue
            if manager_id and department.get("manager_id") != manager_id:
                continue
            if status and department.get("status") != status:
                continue
            results.append(department)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_departments",
                "description": "Get departments with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "department_id": {"type": "string", "description": "Filter by department ID"},
                        "manager_id": {"type": "string", "description": "Filter by manager ID"},
                        "status": {"type": "string", "description": "Filter by status"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 36: get_job_positions
cat > hr_tools_2/get_job_positions.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetJobPositions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], position_id: Optional[str] = None,
               department_id: Optional[str] = None, job_level: Optional[str] = None,
               status: Optional[str] = None) -> str:
        
        job_positions = data.get("job_positions", {})
        results = []
        
        for position in job_positions.values():
            if position_id and position.get("position_id") != position_id:
                continue
            if department_id and position.get("department_id") != department_id:
                continue
            if job_level and position.get("job_level") != job_level:
                continue
            if status and position.get("status") != status:
                continue
            results.append(position)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_job_positions",
                "description": "Get job positions with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "position_id": {"type": "string", "description": "Filter by position ID"},
                        "department_id": {"type": "string", "description": "Filter by department ID"},
                        "job_level": {"type": "string", "description": "Filter by job level"},
                        "status": {"type": "string", "description": "Filter by status"}
                    },
                    "required": []
                }
            }
        }
EOF

echo "All HR Management System tools have been created successfully!"
echo "The tools are located in the 'hr_tools_2' directory:"
ls -la hr_tools_2/