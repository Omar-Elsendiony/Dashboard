import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrievePayrollDeductions(Tool):
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
                "name": "retrieve_payroll_deductions",
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
