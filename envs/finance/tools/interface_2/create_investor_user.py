import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateInvestorUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_first_name: str, investor_last_name: str, 
               investor_email: str, investor_role: str, investor_timezone: str, investor_status: str = "active") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        
        # Check if investor_email already exists
        for user in users.values():
            if user.get("investor_email") == investor_email:
                raise ValueError(f"Email {investor_email} already exists")
        
        # Validate investor_role
        valid_roles = ["system_administrator", "fund_manager", "compliance_officer", 
                      "finance_officer", "trader"]
        if investor_role not in valid_roles:
            raise ValueError(f"Invalid investor_role. Must be one of {valid_roles}")
        
        # Validate investor_status
        valid_statuses = ["active", "inactive", "suspended"]
        if investor_status not in valid_statuses:
            raise ValueError(f"Invalid investor_status. Must be one of {valid_statuses}")
        
        investor_user_id = generate_id(users)
        timestamp = "2025-10-01T00:00:00"
        
        new_user = {
            "investor_user_id": investor_user_id,
            "investor_first_name": investor_first_name,
            "investor_last_name": investor_last_name,
            "investor_email": investor_email,
            "investor_role": investor_role,
            "investor_timezone": investor_timezone,
            "investor_status": investor_status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        users[str(investor_user_id)] = new_user
        return json.dumps({"new_user": new_user})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "investor_name": "add_new_user",
                "description": "Add a new user for staff onboarding",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_first_name": {"type": "string", "description": "User's first investor_name"},
                        "investor_last_name": {"type": "string", "description": "User's last investor_name"},
                        "investor_email": {"type": "string", "description": "User's investor_email investor_address"},
                        "investor_role": {"type": "string", "description": "User investor_role (system_administrator, fund_manager, compliance_officer, finance_officer, trader)"},
                        "investor_timezone": {"type": "string", "description": "User's investor_timezone (e.g., 'UTC', 'America/New_York')"},
                        "investor_status": {"type": "string", "description": "User investor_status (active, inactive, suspended), defaults to active"}
                    },
                    "required": ["investor_first_name", "investor_last_name", "investor_email", "investor_role", "investor_timezone"]
                }
            }
        }
