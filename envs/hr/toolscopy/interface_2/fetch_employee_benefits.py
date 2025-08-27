import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FetchEmployeeBenefits(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], enrollment_id: Optional[str] = None,
               employee_id: Optional[str] = None, plan_id: Optional[str] = None,
               status: Optional[str] = None) -> str:
        employee_benefits = data.get("employee_benefits", {})
        results = []
        
        for benefit in employee_benefits.values():
            if enrollment_id and benefit.get("enrollment_id") != enrollment_id:
                continue
            if employee_id and benefit.get("employee_id") != employee_id:
                continue
            if plan_id and benefit.get("plan_id") != plan_id:
                continue
            if status and benefit.get("status") != status:
                continue
            results.append(benefit)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_employee_benefits",
                "description": "Get employee benefits with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "enrollment_id": {"type": "string", "description": "Filter by enrollment ID"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "plan_id": {"type": "string", "description": "Filter by plan ID"},
                        "status": {"type": "string", "description": "Filter by status (active, terminated, pending)"}
                    },
                    "required": []
                }
            }
        }
