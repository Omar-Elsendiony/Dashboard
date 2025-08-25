
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPayrollRunDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], payroll_run_id: str) -> str:
        runs = data.get("payroll_runs", {})
        if payroll_run_id not in runs:
            raise ValueError("Payroll run not found")

        if runs[payroll_run_id]["status"] != "confirmed":
            raise ValueError("Payroll run is not in a confirmed state")

        items = [
            item for item in data.get("payroll_items", {}).values()
            if item.get("run_id") == payroll_run_id
        ]
        return json.dumps({
            "payroll_run_id": payroll_run_id,
            "items": items
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_payroll_run_details",
                "description": "Fetches detailed line items of a payroll run",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payroll_run_id": {
                            "type": "string",
                            "description": "The ID of the payroll run to retrieve"
                        }
                    },
                    "required": ["payroll_run_id"]
                }
            }
        }
