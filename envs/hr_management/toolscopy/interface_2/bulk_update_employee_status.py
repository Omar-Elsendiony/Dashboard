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
