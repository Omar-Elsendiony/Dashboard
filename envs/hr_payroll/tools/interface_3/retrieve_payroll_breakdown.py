
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RetrievePayrollBreakdown(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], payroll_run_id: str) -> str:
        items = data.get("payroll_items", {})
        breakdown = {}
        for item in items.values():
            if item.get("run_id") != payroll_run_id:
                continue
            status = item.get("status")
            breakdown[status] = breakdown.get(status, 0) + item.get("amount", 0)

        return json.dumps({
            "payroll_run_id": payroll_run_id,
            "breakdown_by_status": breakdown
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_payroll_breakdown",
                "description": "Returns categorized payroll items for a payroll run",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payroll_run_id": {
                            "type": "string",
                            "description": "The ID of the payroll run to summarize"
                        }
                    },
                    "required": ["payroll_run_id"]
                }
            }
        }
