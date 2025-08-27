import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPayrollRecords(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], payroll_id: Optional[str] = None,
               employee_id: Optional[str] = None, pay_period_start: Optional[str] = None,
               pay_period_end: Optional[str] = None, status: Optional[str] = None) -> str:
        payroll_records = data.get("payroll_records", {})
        results = []
        
        for payroll in payroll_records.values():
            if payroll_id and payroll.get("payroll_id") != payroll_id:
                continue
            if employee_id and payroll.get("employee_id") != employee_id:
                continue
            if pay_period_start and payroll.get("pay_period_start") != pay_period_start:
                continue
            if pay_period_end and payroll.get("pay_period_end") != pay_period_end:
                continue
            if status and payroll.get("status") != status:
                continue
            results.append(payroll)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_payroll_records",
                "description": "Get payroll records with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payroll_id": {"type": "string", "description": "Filter by payroll ID"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "pay_period_start": {"type": "string", "description": "Filter by pay period start date"},
                        "pay_period_end": {"type": "string", "description": "Filter by pay period end date"},
                        "status": {"type": "string", "description": "Filter by status (draft, approved, paid, cancelled)"}
                    },
                    "required": []
                }
            }
        }
