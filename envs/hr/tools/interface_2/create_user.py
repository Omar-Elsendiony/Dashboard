import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], first_name: str, last_name: str, email: str, 
               phone_number: Optional[str] = None, role: str = "employee", 
               status: str = "active", mfa_enabled: bool = True,
               hr_director_approval: Optional[bool] = None, 
               it_admin_approval: Optional[bool] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        users = data.get("users", {})
        
        # Validate required fields
        if not first_name or not last_name or not email:
            raise ValueError("First name, last name, and email are required")
        
        # Check email uniqueness
        for user in users.values():
            if user.get("email", "").lower() == email.lower():
                raise ValueError(f"Email {email} already exists")
        
        # Validate role
        valid_roles = ['hr_director', 'hr_manager', 'recruiter', 'payroll_administrator', 
                      'hiring_manager', 'finance_officer', 'it_administrator', 
                      'compliance_officer', 'employee']
        if role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of {valid_roles}")
        
        # Validate status
        valid_statuses = ['active', 'inactive', 'suspended']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Check approval requirements for elevated roles
        elevated_roles = ['hr_director', 'hr_manager', 'payroll_administrator', 
                         'finance_officer', 'it_administrator', 'compliance_officer']
        if role in elevated_roles:
            if hr_director_approval is None or it_admin_approval is None:
                return json.dumps({
                    "error": "HR Director and IT Administrator approval required for elevated roles",
                    "halt": True
                })
            if not hr_director_approval or not it_admin_approval:
                return json.dumps({
                    "error": "Approval denied for elevated role creation",
                    "halt": True
                })
        
        user_id = generate_id(users)
        timestamp = "2025-10-01T00:00:00"
        
        new_user = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "role": role,
            "status": status,
            "mfa_enabled": mfa_enabled,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        users[user_id] = new_user
        return json.dumps({"user_id": user_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_user",
                "description": "Create a new user in the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string", "description": "First name of the user"},
                        "last_name": {"type": "string", "description": "Last name of the user"},
                        "email": {"type": "string", "description": "Email address (must be unique)"},
                        "phone_number": {"type": "string", "description": "Phone number (optional)"},
                        "role": {"type": "string", "description": "Role: hr_director, hr_manager, recruiter, payroll_administrator, hiring_manager, finance_officer, it_administrator, compliance_officer, employee"},
                        "status": {"type": "string", "description": "Status: active, inactive, suspended (defaults to active)"},
                        "mfa_enabled": {"type": "boolean", "description": "Multi-factor authentication enabled (True/False, defaults to True)"},
                        "hr_director_approval": {"type": "boolean", "description": "HR Director approval for elevated roles (True/False)"},
                        "it_admin_approval": {"type": "boolean", "description": "IT Administrator approval for elevated roles (True/False)"}
                    },
                    "required": ["email", "first_name", "last_name"]
                }
            }
        }
