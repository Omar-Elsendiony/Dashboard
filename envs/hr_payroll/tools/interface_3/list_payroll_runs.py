import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListPayrollRuns(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        run_id: str = None,
        organization_id: str = None,
        status: str = None,
        currency: str = None,
        run_date: str = None
    ) -> str:
        runs = data.get("payroll_runs", {})

        def matches(rid, run):
            if run_id and rid != run_id:
                return False
            if organization_id and run.get("organization_id") != organization_id:
                return False
            if status and run.get("status") != status:
                return False
            if currency and run.get("currency") != currency:
                return False
            if run_date and run.get("run_date") != run_date:
                return False
            return True

        filtered = [
            {**run, "run_id": rid}
            for rid, run in runs.items()
            if matches(rid, run)
        ]

        return json.dumps(filtered)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_payroll_runs",
                "description": (
                    "Fetches a list of payroll runs with optional filters on run_id (key), "
                    "organization_id, status, currency, or run_date. Only run_id guarantees a unique result."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "run_id": {
                            "type": "string",
                            "description": "Filter by payroll run ID (key)"
                        },
                        "organization_id": {
                            "type": "string",
                            "description": "Filter by organization ID"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by run status (e.g., processed, error)"
                        },
                        "currency": {
                            "type": "string",
                            "description": "Filter by currency code"
                        },
                        "run_date": {
                            "type": "string",
                            "description": "Filter by exact run date (ISO format: YYYY-MM-DDTHH:MM:SSZ)"
                        }
                    },
                    "required": []
                }
            }
        }
