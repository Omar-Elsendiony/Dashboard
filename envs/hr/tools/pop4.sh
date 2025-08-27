#!/bin/bash

# Create directory for tools if it doesn't exist
mkdir -p hr_tools

# 1. Create Skills Management
cat > hr_tools/create_skill.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateSkill(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], skill_name: str, status: str = "active") -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        skills = data.setdefault("skills", {})
        
        # Validate status
        valid_statuses = ["active", "inactive"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Check if skill already exists
        for skill in skills.values():
            if skill.get("skill_name").lower() == skill_name.lower():
                raise ValueError(f"Skill '{skill_name}' already exists")
        
        skill_id = generate_id(skills)
        timestamp = "2025-10-01T00:00:00"
        
        new_skill = {
            "skill_id": skill_id,
            "skill_name": skill_name,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        skills[skill_id] = new_skill
        return json.dumps({"skill_id": skill_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_skill",
                "description": "Create a new skill in the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "skill_name": {"type": "string", "description": "Name of the skill"},
                        "status": {"type": "string", "description": "Skill status (active, inactive), defaults to active"}
                    },
                    "required": ["skill_name"]
                }
            }
        }
EOF

# 2. Update Skill
cat > hr_tools/update_skill.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateSkill(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], skill_id: str, skill_name: str = None, status: str = None) -> str:
        skills = data.get("skills", {})
        
        if skill_id not in skills:
            raise ValueError(f"Skill {skill_id} not found")
        
        skill = skills[skill_id]
        
        if skill_name is not None:
            skill["skill_name"] = skill_name
        
        if status is not None:
            valid_statuses = ["active", "inactive"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            skill["status"] = status
        
        skill["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Skill updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_skill",
                "description": "Update an existing skill",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "skill_id": {"type": "string", "description": "ID of the skill to update"},
                        "skill_name": {"type": "string", "description": "Updated skill name"},
                        "status": {"type": "string", "description": "Updated status (active, inactive)"}
                    },
                    "required": ["skill_id"]
                }
            }
        }
EOF

# 3. Assign Skill to Job Position
cat > hr_tools/assign_skill_to_position.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AssignSkillToPosition(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], position_id: str, skill_id: str) -> str:
        job_positions = data.get("job_positions", {})
        skills = data.get("skills", {})
        job_position_skills = data.setdefault("job_position_skills", {})
        
        # Validate position exists
        if position_id not in job_positions:
            raise ValueError(f"Job position {position_id} not found")
        
        # Validate skill exists
        if skill_id not in skills:
            raise ValueError(f"Skill {skill_id} not found")
        
        # Check if assignment already exists
        for assignment in job_position_skills.values():
            if (assignment.get("position_id") == position_id and 
                assignment.get("skill_id") == skill_id):
                return json.dumps({"status": "already_assigned"})
        
        # Create composite key for the assignment
        assignment_key = f"{position_id}_{skill_id}"
        
        new_assignment = {
            "position_id": position_id,
            "skill_id": skill_id,
            "created_at": "2025-10-01T00:00:00"
        }
        
        job_position_skills[assignment_key] = new_assignment
        return json.dumps({"success": True, "message": "Skill assigned to position"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "assign_skill_to_position",
                "description": "Assign a skill requirement to a job position",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "position_id": {"type": "string", "description": "ID of the job position"},
                        "skill_id": {"type": "string", "description": "ID of the skill"}
                    },
                    "required": ["position_id", "skill_id"]
                }
            }
        }
EOF

# 4. Create Leave Request
cat > hr_tools/create_leave_request.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateLeaveRequest(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, leave_type: str, 
               start_date: str, end_date: str, days_requested: float, 
               reason: str = None) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        employees = data.get("employees", {})
        leave_requests = data.setdefault("leave_requests", {})
        
        # Validate employee exists
        if employee_id not in employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        # Validate leave type
        valid_leave_types = ["annual", "sick", "fmla", "personal", "bereavement", "jury_duty"]
        if leave_type not in valid_leave_types:
            raise ValueError(f"Invalid leave type. Must be one of {valid_leave_types}")
        
        leave_id = generate_id(leave_requests)
        timestamp = "2025-10-01T00:00:00"
        
        new_leave_request = {
            "leave_id": leave_id,
            "employee_id": employee_id,
            "leave_type": leave_type,
            "start_date": start_date,
            "end_date": end_date,
            "days_requested": days_requested,
            "reason": reason,
            "status": "pending",
            "approved_by": None,
            "approval_date": None,
            "remaining_balance": None,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        leave_requests[leave_id] = new_leave_request
        return json.dumps({"leave_id": leave_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_leave_request",
                "description": "Create a new leave request for an employee",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "ID of the employee"},
                        "leave_type": {"type": "string", "description": "Type of leave (annual, sick, fmla, personal, bereavement, jury_duty)"},
                        "start_date": {"type": "string", "description": "Start date of leave"},
                        "end_date": {"type": "string", "description": "End date of leave"},
                        "days_requested": {"type": "number", "description": "Number of days requested"},
                        "reason": {"type": "string", "description": "Reason for leave (optional)"}
                    },
                    "required": ["employee_id", "leave_type", "start_date", "end_date", "days_requested"]
                }
            }
        }
EOF

# 5. Approve/Reject Leave Request
cat > hr_tools/process_leave_request.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ProcessLeaveRequest(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], leave_id: str, status: str, 
               approved_by: str, remaining_balance: float = None) -> str:
        leave_requests = data.get("leave_requests", {})
        users = data.get("users", {})
        
        if leave_id not in leave_requests:
            raise ValueError(f"Leave request {leave_id} not found")
        
        if approved_by not in users:
            raise ValueError(f"Approver user {approved_by} not found")
        
        valid_statuses = ["approved", "rejected", "cancelled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        leave_request = leave_requests[leave_id]
        leave_request["status"] = status
        leave_request["approved_by"] = approved_by
        leave_request["approval_date"] = "2025-10-01T00:00:00"
        leave_request["updated_at"] = "2025-10-01T00:00:00"
        
        if remaining_balance is not None:
            leave_request["remaining_balance"] = remaining_balance
        
        return json.dumps({"success": True, "message": f"Leave request {status}"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_leave_request",
                "description": "Approve or reject a leave request",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "leave_id": {"type": "string", "description": "ID of the leave request"},
                        "status": {"type": "string", "description": "New status (approved, rejected, cancelled)"},
                        "approved_by": {"type": "string", "description": "ID of the user processing the request"},
                        "remaining_balance": {"type": "number", "description": "Remaining leave balance after approval"}
                    },
                    "required": ["leave_id", "status", "approved_by"]
                }
            }
        }
EOF

# 6. Create Expense Reimbursement
cat > hr_tools/create_expense_reimbursement.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateExpenseReimbursement(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, expense_date: str, 
               amount: float, expense_type: str, description: str, 
               receipt_file_path: str = None) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        employees = data.get("employees", {})
        expense_reimbursements = data.setdefault("expense_reimbursements", {})
        
        # Validate employee exists
        if employee_id not in employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        # Validate expense type
        valid_expense_types = ["travel", "meals", "equipment", "training", "other"]
        if expense_type not in valid_expense_types:
            raise ValueError(f"Invalid expense type. Must be one of {valid_expense_types}")
        
        reimbursement_id = generate_id(expense_reimbursements)
        timestamp = "2025-10-01T00:00:00"
        
        new_reimbursement = {
            "reimbursement_id": reimbursement_id,
            "employee_id": employee_id,
            "expense_date": expense_date,
            "amount": amount,
            "expense_type": expense_type,
            "description": description,
            "receipt_file_path": receipt_file_path,
            "status": "submitted",
            "approved_by": None,
            "payment_date": None,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        expense_reimbursements[reimbursement_id] = new_reimbursement
        return json.dumps({"reimbursement_id": reimbursement_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_expense_reimbursement",
                "description": "Create a new expense reimbursement request",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "ID of the employee"},
                        "expense_date": {"type": "string", "description": "Date of the expense"},
                        "amount": {"type": "number", "description": "Amount to be reimbursed"},
                        "expense_type": {"type": "string", "description": "Type of expense (travel, meals, equipment, training, other)"},
                        "description": {"type": "string", "description": "Description of the expense"},
                        "receipt_file_path": {"type": "string", "description": "Path to receipt file (optional)"}
                    },
                    "required": ["employee_id", "expense_date", "amount", "expense_type", "description"]
                }
            }
        }
EOF

# 7. Process Expense Reimbursement
cat > hr_tools/process_expense_reimbursement.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ProcessExpenseReimbursement(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], reimbursement_id: str, status: str, 
               approved_by: str, payment_date: str = None) -> str:
        expense_reimbursements = data.get("expense_reimbursements", {})
        users = data.get("users", {})
        
        if reimbursement_id not in expense_reimbursements:
            raise ValueError(f"Expense reimbursement {reimbursement_id} not found")
        
        if approved_by not in users:
            raise ValueError(f"Approver user {approved_by} not found")
        
        valid_statuses = ["approved", "rejected", "paid"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        reimbursement = expense_reimbursements[reimbursement_id]
        reimbursement["status"] = status
        reimbursement["approved_by"] = approved_by
        reimbursement["updated_at"] = "2025-10-01T00:00:00"
        
        if payment_date and status == "paid":
            reimbursement["payment_date"] = payment_date
        
        return json.dumps({"success": True, "message": f"Expense reimbursement {status}"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_expense_reimbursement",
                "description": "Process an expense reimbursement request",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reimbursement_id": {"type": "string", "description": "ID of the expense reimbursement"},
                        "status": {"type": "string", "description": "New status (approved, rejected, paid)"},
                        "approved_by": {"type": "string", "description": "ID of the user processing the request"},
                        "payment_date": {"type": "string", "description": "Payment date if status is paid"}
                    },
                    "required": ["reimbursement_id", "status", "approved_by"]
                }
            }
        }
EOF

# 8. Add Payroll Deduction
cat > hr_tools/add_payroll_deduction.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddPayrollDeduction(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], payroll_id: str, deduction_type: str, 
               amount: float, created_by: str) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        payroll_records = data.get("payroll_records", {})
        users = data.get("users", {})
        payroll_deductions = data.setdefault("payroll_deductions", {})
        
        # Validate payroll record exists
        if payroll_id not in payroll_records:
            raise ValueError(f"Payroll record {payroll_id} not found")
        
        # Validate user exists
        if created_by not in users:
            raise ValueError(f"User {created_by} not found")
        
        # Validate deduction type
        valid_deduction_types = ["tax", "insurance", "retirement", "garnishment", "equipment", "other"]
        if deduction_type not in valid_deduction_types:
            raise ValueError(f"Invalid deduction type. Must be one of {valid_deduction_types}")
        
        deduction_id = generate_id(payroll_deductions)
        timestamp = "2025-10-01T00:00:00"
        
        new_deduction = {
            "deduction_id": deduction_id,
            "payroll_id": payroll_id,
            "deduction_type": deduction_type,
            "amount": amount,
            "created_by": created_by,
            "created_at": timestamp
        }
        
        payroll_deductions[deduction_id] = new_deduction
        return json.dumps({"deduction_id": deduction_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_payroll_deduction",
                "description": "Add a deduction to a payroll record",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payroll_id": {"type": "string", "description": "ID of the payroll record"},
                        "deduction_type": {"type": "string", "description": "Type of deduction (tax, insurance, retirement, garnishment, equipment, other)"},
                        "amount": {"type": "number", "description": "Deduction amount"},
                        "created_by": {"type": "string", "description": "ID of the user creating the deduction"}
                    },
                    "required": ["payroll_id", "deduction_type", "amount", "created_by"]
                }
            }
        }
EOF

# 9. Get Skills
cat > hr_tools/get_skills.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetSkills(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], skill_id: str = None, status: str = None) -> str:
        skills = data.get("skills", {})
        results = []
        
        for skill in skills.values():
            if skill_id and skill.get("skill_id") != skill_id:
                continue
            if status and skill.get("status") != status:
                continue
            results.append(skill)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_skills",
                "description": "Retrieve skills with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "skill_id": {"type": "string", "description": "Filter by skill ID"},
                        "status": {"type": "string", "description": "Filter by status (active, inactive)"}
                    },
                    "required": []
                }
            }
        }
EOF

# 10. Get Leave Requests
cat > hr_tools/get_leave_requests.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetLeaveRequests(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], leave_id: str = None, employee_id: str = None, 
               leave_type: str = None, status: str = None) -> str:
        leave_requests = data.get("leave_requests", {})
        results = []
        
        for leave in leave_requests.values():
            if leave_id and leave.get("leave_id") != leave_id:
                continue
            if employee_id and leave.get("employee_id") != employee_id:
                continue
            if leave_type and leave.get("leave_type") != leave_type:
                continue
            if status and leave.get("status") != status:
                continue
            results.append(leave)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_leave_requests",
                "description": "Retrieve leave requests with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "leave_id": {"type": "string", "description": "Filter by leave request ID"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "leave_type": {"type": "string", "description": "Filter by leave type"},
                        "status": {"type": "string", "description": "Filter by status"}
                    },
                    "required": []
                }
            }
        }
EOF

# 11. Get Expense Reimbursements
cat > hr_tools/get_expense_reimbursements.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetExpenseReimbursements(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], reimbursement_id: str = None, 
               employee_id: str = None, expense_type: str = None, 
               status: str = None) -> str:
        expense_reimbursements = data.get("expense_reimbursements", {})
        results = []
        
        for reimbursement in expense_reimbursements.values():
            if reimbursement_id and reimbursement.get("reimbursement_id") != reimbursement_id:
                continue
            if employee_id and reimbursement.get("employee_id") != employee_id:
                continue
            if expense_type and reimbursement.get("expense_type") != expense_type:
                continue
            if status and reimbursement.get("status") != status:
                continue
            results.append(reimbursement)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_expense_reimbursements",
                "description": "Retrieve expense reimbursements with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reimbursement_id": {"type": "string", "description": "Filter by reimbursement ID"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "expense_type": {"type": "string", "description": "Filter by expense type"},
                        "status": {"type": "string", "description": "Filter by status"}
                    },
                    "required": []
                }
            }
        }
EOF

# 12. Get Payroll Deductions
cat > hr_tools/get_payroll_deductions.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPayrollDeductions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], deduction_id: str = None, 
               payroll_id: str = None, deduction_type: str = None) -> str:
        payroll_deductions = data.get("payroll_deductions", {})
        results = []
        
        for deduction in payroll_deductions.values():
            if deduction_id and deduction.get("deduction_id") != deduction_id:
                continue
            if payroll_id and deduction.get("payroll_id") != payroll_id:
                continue
            if deduction_type and deduction.get("deduction_type") != deduction_type:
                continue
            results.append(deduction)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_payroll_deductions",
                "description": "Retrieve payroll deductions with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "deduction_id": {"type": "string", "description": "Filter by deduction ID"},
                        "payroll_id": {"type": "string", "description": "Filter by payroll ID"},
                        "deduction_type": {"type": "string", "description": "Filter by deduction type"}
                    },
                    "required": []
                }
            }
        }
EOF

# 13. Get Job Position Skills
cat > hr_tools/get_job_position_skills.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetJobPositionSkills(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], position_id: str = None, skill_id: str = None) -> str:
        job_position_skills = data.get("job_position_skills", {})
        results = []
        
        for assignment in job_position_skills.values():
            if position_id and assignment.get("position_id") != position_id:
                continue
            if skill_id and assignment.get("skill_id") != skill_id:
                continue
            results.append(assignment)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_job_position_skills",
                "description": "Retrieve skill assignments for job positions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "position_id": {"type": "string", "description": "Filter by job position ID"},
                        "skill_id": {"type": "string", "description": "Filter by skill ID"}
                    },
                    "required": []
                }
            }
        }
EOF

# 14. Remove Skill from Position
cat > hr_tools/remove_skill_from_position.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RemoveSkillFromPosition(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], position_id: str, skill_id: str) -> str:
        job_position_skills = data.get("job_position_skills", {})
        
        # Find and remove the assignment
        assignment_key = f"{position_id}_{skill_id}"
        
        if assignment_key in job_position_skills:
            del job_position_skills[assignment_key]
            return json.dumps({"success": True, "message": "Skill removed from position"})
        
        # If composite key doesn't exist, search through all assignments
        for key, assignment in list(job_position_skills.items()):
            if (assignment.get("position_id") == position_id and 
                assignment.get("skill_id") == skill_id):
                del job_position_skills[key]
                return json.dumps({"success": True, "message": "Skill removed from position"})
        
        raise ValueError(f"Skill assignment not found for position {position_id} and skill {skill_id}")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_skill_from_position",
                "description": "Remove a skill requirement from a job position",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "position_id": {"type": "string", "description": "ID of the job position"},
                        "skill_id": {"type": "string", "description": "ID of the skill"}
                    },
                    "required": ["position_id", "skill_id"]
                }
            }
        }
EOF

# 15. Update Leave Request
cat > hr_tools/update_leave_request.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateLeaveRequest(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], leave_id: str, start_date: str = None, 
               end_date: str = None, days_requested: float = None, 
               reason: str = None) -> str:
        leave_requests = data.get("leave_requests", {})
        
        if leave_id not in leave_requests:
            raise ValueError(f"Leave request {leave_id} not found")
        
        leave_request = leave_requests[leave_id]
        
        # Only allow updates if status is pending
        if leave_request.get("status") != "pending":
            raise ValueError("Cannot update leave request that is not pending")
        
        if start_date is not None:
            leave_request["start_date"] = start_date
        
        if end_date is not None:
            leave_request["end_date"] = end_date
        
        if days_requested is not None:
            leave_request["days_requested"] = days_requested
        
        if reason is not None:
            leave_request["reason"] = reason
        
        leave_request["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Leave request updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_leave_request",
                "description": "Update a pending leave request",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "leave_id": {"type": "string", "description": "ID of the leave request to update"},
                        "start_date": {"type": "string", "description": "Updated start date"},
                        "end_date": {"type": "string", "description": "Updated end date"},
                        "days_requested": {"type": "number", "description": "Updated number of days requested"},
                        "reason": {"type": "string", "description": "Updated reason for leave"}
                    },
                    "required": ["leave_id"]
                }
            }
        }
EOF

# 16. Update Expense Reimbursement
cat > hr_tools/update_expense_reimbursement.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateExpenseReimbursement(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], reimbursement_id: str, amount: float = None, 
               description: str = None, receipt_file_path: str = None) -> str:
        expense_reimbursements = data.get("expense_reimbursements", {})
        
        if reimbursement_id not in expense_reimbursements:
            raise ValueError(f"Expense reimbursement {reimbursement_id} not found")
        
        reimbursement = expense_reimbursements[reimbursement_id]
        
        # Only allow updates if status is submitted
        if reimbursement.get("status") != "submitted":
            raise ValueError("Cannot update expense reimbursement that is not in submitted status")
        
        if amount is not None:
            reimbursement["amount"] = amount
        
        if description is not None:
            reimbursement["description"] = description
        
        if receipt_file_path is not None:
            reimbursement["receipt_file_path"] = receipt_file_path
        
        reimbursement["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Expense reimbursement updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_expense_reimbursement",
                "description": "Update a submitted expense reimbursement",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reimbursement_id": {"type": "string", "description": "ID of the expense reimbursement to update"},
                        "amount": {"type": "number", "description": "Updated amount"},
                        "description": {"type": "string", "description": "Updated description"},
                        "receipt_file_path": {"type": "string", "description": "Updated receipt file path"}
                    },
                    "required": ["reimbursement_id"]
                }
            }
        }
EOF

# 17. Delete Payroll Deduction
cat > hr_tools/delete_payroll_deduction.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeletePayrollDeduction(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], deduction_id: str, deleted_by: str) -> str:
        payroll_deductions = data.get("payroll_deductions", {})
        users = data.get("users", {})
        
        if deduction_id not in payroll_deductions:
            raise ValueError(f"Payroll deduction {deduction_id} not found")
        
        if deleted_by not in users:
            raise ValueError(f"User {deleted_by} not found")
        
        del payroll_deductions[deduction_id]
        
        return json.dumps({"success": True, "message": "Payroll deduction deleted"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_payroll_deduction",
                "description": "Delete a payroll deduction",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "deduction_id": {"type": "string", "description": "ID of the deduction to delete"},
                        "deleted_by": {"type": "string", "description": "ID of the user deleting the deduction"}
                    },
                    "required": ["deduction_id", "deleted_by"]
                }
            }
        }
EOF

# 18. Calculate Employee Leave Balance
cat > hr_tools/calculate_leave_balance.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CalculateLeaveBalance(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, leave_type: str, 
               annual_allocation: float) -> str:
        employees = data.get("employees", {})
        leave_requests = data.get("leave_requests", {})
        
        if employee_id not in employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        # Calculate used leave days
        used_days = 0
        for leave in leave_requests.values():
            if (leave.get("employee_id") == employee_id and 
                leave.get("leave_type") == leave_type and 
                leave.get("status") == "approved"):
                used_days += leave.get("days_requested", 0)
        
        remaining_balance = annual_allocation - used_days
        
        balance_info = {
            "employee_id": employee_id,
            "leave_type": leave_type,
            "annual_allocation": annual_allocation,
            "used_days": used_days,
            "remaining_balance": remaining_balance
        }
        
        return json.dumps(balance_info)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_leave_balance",
                "description": "Calculate remaining leave balance for an employee",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "ID of the employee"},
                        "leave_type": {"type": "string", "description": "Type of leave to calculate"},
                        "annual_allocation": {"type": "number", "description": "Annual leave allocation for this type"}
                    },
                    "required": ["employee_id", "leave_type", "annual_allocation"]
                }
            }
        }
EOF

# 19. Get Employee Summary Report
cat > hr_tools/get_employee_summary_report.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetEmployeeSummaryReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str) -> str:
        employees = data.get("employees", {})
        users = data.get("users", {})
        job_positions = data.get("job_positions", {})
        departments = data.get("departments", {})
        performance_reviews = data.get("performance_reviews", {})
        employee_training = data.get("employee_training", {})
        leave_requests = data.get("leave_requests", {})
        
        if employee_id not in employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        employee = employees[employee_id]
        user = users.get(employee.get("user_id"), {})
        position = job_positions.get(employee.get("position_id"), {})
        department = departments.get(position.get("department_id"), {})
        
        # Count performance reviews
        review_count = sum(1 for review in performance_reviews.values() 
                          if review.get("employee_id") == employee_id)
        
        # Count completed training
        training_count = sum(1 for training in employee_training.values() 
                           if (training.get("employee_id") == employee_id and 
                               training.get("status") == "completed"))
        
        # Count leave requests
        leave_count = sum(1 for leave in leave_requests.values() 
                         if leave.get("employee_id") == employee_id)
        
        summary = {
            "employee_id": employee_id,
            "name": f"{user.get('first_name', '')} {user.get('last_name', '')}",
            "email": user.get("email"),
            "position_title": position.get("title"),
            "department_name": department.get("department_name"),
            "hire_date": employee.get("hire_date"),
            "employment_status": employee.get("employment_status"),
            "performance_reviews_count": review_count,
            "completed_training_count": training_count,
            "leave_requests_count": leave_count
        }
        
        return json.dumps(summary)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_employee_summary_report",
                "description": "Get a comprehensive summary report for an employee",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "ID of the employee"}
                    },
                    "required": ["employee_id"]
                }
            }
        }
EOF

# 20. Get Department Summary Report
cat > hr_tools/get_department_summary_report.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetDepartmentSummaryReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], department_id: str) -> str:
        departments = data.get("departments", {})
        employees = data.get("employees", {})
        job_positions = data.get("job_positions", {})
        users = data.get("users", {})
        
        if department_id not in departments:
            raise ValueError(f"Department {department_id} not found")
        
        department = departments[department_id]
        
        # Count positions in department
        position_count = sum(1 for position in job_positions.values() 
                           if position.get("department_id") == department_id)
        
        # Count employees in department
        department_positions = [pos_id for pos_id, pos in job_positions.items() 
                               if pos.get("department_id") == department_id]
        
        employee_count = sum(1 for employee in employees.values() 
                           if (employee.get("position_id") in department_positions and 
                               employee.get("employment_status") == "active"))
        
        # Get manager info
        manager = employees.get(department.get("manager_id"), {})
        manager_user = users.get(manager.get("user_id"), {})
        
        summary = {
            "department_id": department_id,
            "department_name": department.get("department_name"),
            "manager_name": f"{manager_user.get('first_name', '')} {manager_user.get('last_name', '')}",
            "budget": department.get("budget"),
            "status": department.get("status"),
            "total_positions": position_count,
            "active_employees": employee_count,
            "created_at": department.get("created_at")
        }
        
        return json.dumps(summary)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_department_summary_report",
                "description": "Get a comprehensive summary report for a department",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "department_id": {"type": "string", "description": "ID of the department"}
                    },
                    "required": ["department_id"]
                }
            }
        }
EOF

# 21. Get Training Completion Report
cat > hr_tools/get_training_completion_report.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetTrainingCompletionReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], program_id: str = None, 
               department_id: str = None) -> str:
        training_programs = data.get("training_programs", {})
        employee_training = data.get("employee_training", {})
        employees = data.get("employees", {})
        job_positions = data.get("job_positions", {})
        users = data.get("users", {})
        
        results = []
        
        for program_key, program in training_programs.items():
            if program_id and program_key != program_id:
                continue
            
            # Count enrollments and completions for this program
            total_enrolled = 0
            completed = 0
            failed = 0
            in_progress = 0
            
            for training in employee_training.values():
                if training.get("program_id") != program_key:
                    continue
                
                # Filter by department if specified
                if department_id:
                    employee = employees.get(training.get("employee_id"), {})
                    position = job_positions.get(employee.get("position_id"), {})
                    if position.get("department_id") != department_id:
                        continue
                
                total_enrolled += 1
                status = training.get("status")
                if status == "completed":
                    completed += 1
                elif status == "failed":
                    failed += 1
                elif status in ["enrolled", "in_progress"]:
                    in_progress += 1
            
            completion_rate = (completed / total_enrolled * 100) if total_enrolled > 0 else 0
            
            report = {
                "program_id": program_key,
                "program_name": program.get("program_name"),
                "program_type": program.get("program_type"),
                "total_enrolled": total_enrolled,
                "completed": completed,
                "failed": failed,
                "in_progress": in_progress,
                "completion_rate_percent": round(completion_rate, 2)
            }
            
            results.append(report)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_training_completion_report",
                "description": "Get training completion statistics",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "program_id": {"type": "string", "description": "Filter by specific training program"},
                        "department_id": {"type": "string", "description": "Filter by department"}
                    },
                    "required": []
                }
            }
        }
EOF

# 22. Get Payroll Summary Report
cat > hr_tools/get_payroll_summary_report.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPayrollSummaryReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], pay_period_start: str = None, 
               pay_period_end: str = None, department_id: str = None) -> str:
        payroll_records = data.get("payroll_records", {})
        payroll_deductions = data.get("payroll_deductions", {})
        employees = data.get("employees", {})
        job_positions = data.get("job_positions", {})
        
        filtered_records = []
        
        for payroll in payroll_records.values():
            # Filter by pay period
            if pay_period_start and payroll.get("pay_period_start") != pay_period_start:
                continue
            if pay_period_end and payroll.get("pay_period_end") != pay_period_end:
                continue
            
            # Filter by department
            if department_id:
                employee = employees.get(payroll.get("employee_id"), {})
                position = job_positions.get(employee.get("position_id"), {})
                if position.get("department_id") != department_id:
                    continue
            
            filtered_records.append(payroll)
        
        # Calculate totals
        total_employees = len(filtered_records)
        total_hours = sum(float(record.get("hours_worked", 0)) for record in filtered_records)
        total_gross_pay = sum(
            float(record.get("hours_worked", 0)) * float(record.get("hourly_rate", 0)) 
            for record in filtered_records
        )
        
        # Calculate total deductions
        total_deductions = 0
        for record in filtered_records:
            payroll_id = record.get("payroll_id")
            for deduction in payroll_deductions.values():
                if deduction.get("payroll_id") == payroll_id:
                    total_deductions += float(deduction.get("amount", 0))
        
        total_net_pay = total_gross_pay - total_deductions
        
        summary = {
            "pay_period_start": pay_period_start,
            "pay_period_end": pay_period_end,
            "department_id": department_id,
            "total_employees": total_employees,
            "total_hours": total_hours,
            "total_gross_pay": total_gross_pay,
            "total_deductions": total_deductions,
            "total_net_pay": total_net_pay
        }
        
        return json.dumps(summary)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_payroll_summary_report",
                "description": "Get payroll summary statistics",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pay_period_start": {"type": "string", "description": "Filter by pay period start date"},
                        "pay_period_end": {"type": "string", "description": "Filter by pay period end date"},
                        "department_id": {"type": "string", "description": "Filter by department"}
                    },
                    "required": []
                }
            }
        }
EOF

# 23. Bulk Update Employee Status
cat > hr_tools/bulk_update_employee_status.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class BulkUpdateEmployeeStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_ids: List[str], 
               employment_status: str, updated_by: str) -> str:
        employees = data.get("employees", {})
        users = data.get("users", {})
        
        if updated_by not in users:
            raise ValueError(f"User {updated_by} not found")
        
        valid_statuses = ["active", "terminated", "on_leave", "suspended"]
        if employment_status not in valid_statuses:
            raise ValueError(f"Invalid employment status. Must be one of {valid_statuses}")
        
        updated_count = 0
        failed_updates = []
        
        for employee_id in employee_ids:
            if employee_id not in employees:
                failed_updates.append({"employee_id": employee_id, "reason": "Employee not found"})
                continue
            
            employees[employee_id]["employment_status"] = employment_status
            employees[employee_id]["updated_at"] = "2025-10-01T00:00:00"
            updated_count += 1
        
        result = {
            "success": True,
            "updated_count": updated_count,
            "total_requested": len(employee_ids),
            "failed_updates": failed_updates
        }
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "bulk_update_employee_status",
                "description": "Update employment status for multiple employees",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_ids": {"type": "array", "items": {"type": "string"}, "description": "List of employee IDs to update"},
                        "employment_status": {"type": "string", "description": "New employment status (active, terminated, on_leave, suspended)"},
                        "updated_by": {"type": "string", "description": "ID of the user performing the update"}
                    },
                    "required": ["employee_ids", "employment_status", "updated_by"]
                }
            }
        }
EOF

# 24. Generate Compliance Report
cat > hr_tools/generate_compliance_report.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GenerateComplianceReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], report_type: str, start_date: str = None, 
               end_date: str = None) -> str:
        employees = data.get("employees", {})
        users = data.get("users", {})
        employee_training = data.get("employee_training", {})
        training_programs = data.get("training_programs", {})
        leave_requests = data.get("leave_requests", {})
        
        valid_report_types = ["diversity", "training_compliance", "leave_analysis", "termination_analysis"]
        if report_type not in valid_report_types:
            raise ValueError(f"Invalid report type. Must be one of {valid_report_types}")
        
        if report_type == "training_compliance":
            # Check for mandatory training completion
            mandatory_programs = {k: v for k, v in training_programs.items() 
                                if v.get("mandatory") == True}
            
            compliance_data = []
            for employee_id, employee in employees.items():
                if employee.get("employment_status") != "active":
                    continue
                
                user = users.get(employee.get("user_id"), {})
                employee_name = f"{user.get('first_name', '')} {user.get('last_name', '')}"
                
                completed_mandatory = 0
                total_mandatory = len(mandatory_programs)
                
                for program_id in mandatory_programs.keys():
                    for training in employee_training.values():
                        if (training.get("employee_id") == employee_id and 
                            training.get("program_id") == program_id and 
                            training.get("status") == "completed"):
                            completed_mandatory += 1
                            break
                
                compliance_rate = (completed_mandatory / total_mandatory * 100) if total_mandatory > 0 else 100
                
                compliance_data.append({
                    "employee_id": employee_id,
                    "employee_name": employee_name,
                    "completed_mandatory": completed_mandatory,
                    "total_mandatory": total_mandatory,
                    "compliance_rate_percent": round(compliance_rate, 2)
                })
            
            report = {
                "report_type": report_type,
                "generated_at": "2025-10-01T00:00:00",
                "total_employees": len(compliance_data),
                "compliance_data": compliance_data
            }
        
        elif report_type == "leave_analysis":
            # Analyze leave patterns
            leave_data = {}
            for leave in leave_requests.values():
                # Filter by date range if specified
                if start_date and leave.get("start_date") < start_date:
                    continue
                if end_date and leave.get("end_date") > end_date:
                    continue
                
                leave_type = leave.get("leave_type")
                if leave_type not in leave_data:
                    leave_data[leave_type] = {"count": 0, "total_days": 0}
                
                leave_data[leave_type]["count"] += 1
                leave_data[leave_type]["total_days"] += leave.get("days_requested", 0)
            
            report = {
                "report_type": report_type,
                "period_start": start_date,
                "period_end": end_date,
                "generated_at": "2025-10-01T00:00:00",
                "leave_analysis": leave_data
            }
        
        else:
            # Placeholder for other report types
            report = {
                "report_type": report_type,
                "generated_at": "2025-10-01T00:00:00",
                "message": f"Report type {report_type} not yet implemented"
            }
        
        return json.dumps(report)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "generate_compliance_report",
                "description": "Generate various compliance and analysis reports",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "report_type": {"type": "string", "description": "Type of report (diversity, training_compliance, leave_analysis, termination_analysis)"},
                        "start_date": {"type": "string", "description": "Start date for analysis period"},
                        "end_date": {"type": "string", "description": "End date for analysis period"}
                    },
                    "required": ["report_type"]
                }
            }
        }
EOF

# 25. Archive Old Records
cat > hr_tools/archive_old_records.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ArchiveOldRecords(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], record_type: str, cutoff_date: str, 
               archived_by: str) -> str:
        users = data.get("users", {})
        
        if archived_by not in users:
            raise ValueError(f"User {archived_by} not found")
        
        valid_record_types = ["documents", "audit_logs", "performance_reviews", "training_records"]
        if record_type not in valid_record_types:
            raise ValueError(f"Invalid record type. Must be one of {valid_record_types}")
        
        archived_count = 0
        
        if record_type == "documents":
            documents = data.get("document_storage", {})
            for doc_id, document in documents.items():
                if (document.get("upload_date", "9999-12-31") < cutoff_date and 
                    document.get("status") == "active"):
                    document["status"] = "archived"
                    document["updated_at"] = "2025-10-01T00:00:00"
                    archived_count += 1
        
        elif record_type == "performance_reviews":
            reviews = data.get("performance_reviews", {})
            for review_id, review in reviews.items():
                if (review.get("review_period_end", "9999-12-31") < cutoff_date and 
                    review.get("status") == "approved"):
                    review["archived"] = True
                    review["updated_at"] = "2025-10-01T00:00:00"
                    archived_count += 1
        
        elif record_type == "training_records":
            training_records = data.get("employee_training", {})
            for record_id, record in training_records.items():
                if (record.get("completion_date") and 
                    record.get("completion_date") < cutoff_date and 
                    record.get("status") == "completed"):
                    record["archived"] = True
                    record["updated_at"] = "2025-10-01T00:00:00"
                    archived_count += 1
        
        result = {
            "success": True,
            "record_type": record_type,
            "cutoff_date": cutoff_date,
            "archived_count": archived_count,
            "archived_by": archived_by,
            "archived_at": "2025-10-01T00:00:00"
        }
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "archive_old_records",
                "description": "Archive records older than specified cutoff date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "record_type": {"type": "string", "description": "Type of records to archive (documents, audit_logs, performance_reviews, training_records)"},
                        "cutoff_date": {"type": "string", "description": "Date before which records should be archived (YYYY-MM-DD)"},
                        "archived_by": {"type": "string", "description": "ID of the user performing the archiving"}
                    },
                    "required": ["record_type", "cutoff_date", "archived_by"]
                }
            }
        }
EOF