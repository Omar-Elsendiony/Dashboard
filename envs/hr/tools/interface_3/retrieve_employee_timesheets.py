import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetEmployeeTimesheets(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], timesheet_id: Optional[str] = None,
               employee_id: Optional[str] = None, work_date: Optional[str] = None,
               status: Optional[str] = None) -> str:
        employee_timesheets = data.get("employee_timesheets", {})
        results = []
        
        for timesheet in employee_timesheets.values():
            if timesheet_id and timesheet.get("timesheet_id") != timesheet_id:
                continue
            if employee_id and timesheet.get("employee_id") != employee_id:
                continue
            if work_date and timesheet.get("work_date") != work_date:
                continue
            if status and timesheet.get("status") != status:
                continue
            results.append(timesheet)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_employee_timesheets",
                "description": "Get employee timesheets with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "timesheet_id": {"type": "string", "description": "Filter by timesheet ID"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "work_date": {"type": "string", "description": "Filter by work date"},
                        "status": {"type": "string", "description": "Filter by status (draft, submitted, approved, rejected)"}
                    },
                    "required": []
                }
            }
        }
