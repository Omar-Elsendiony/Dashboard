import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class find_reports(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        fund_id: Optional[str] = None,
        investor_id: Optional[str] = None,
        status: Optional[str] = None,
        generated_by: Optional[str] = None
    ) -> str:
        reports = data.get("reports", {})
        users = data.get("users", {})
        results = []

        # Validate status if provided
        valid_statuses = {"pending", "completed", "failed"}
        if status is not None and status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")

        # Validate generated_by if provided
        if generated_by is not None and str(generated_by) not in users:
            raise ValueError(f"User {generated_by} not found")

        for rpt in reports.values():
            # Apply fund_id filter
            if fund_id is not None and str(rpt.get("fund_id")) != str(fund_id):
                continue
            # Apply investor_id filter
            if investor_id is not None:
                inv = rpt.get("investor_id")
                if inv is None or str(inv) != str(investor_id):
                    continue
            # Apply status filter
            if status is not None and rpt.get("status") != status:
                continue
            # Apply generated_by filter
            if generated_by is not None and str(rpt.get("generated_by")) != str(generated_by):
                continue

            results.append(rpt)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_reports",
                "description": (
                    "Find reports filtered by fund_id, investor_id, status, or generated_by. "
                    "Only existing users may be used for generated_by."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {
                            "type": "string",
                            "description": "Filter by fund ID"
                        },
                        "investor_id": {
                            "type": "string",
                            "description": "Filter by investor ID"
                        },
                        "status": {
                            "type": "string",
                            "description": "Report status: pending, completed, or failed"
                        },
                        "generated_by": {
                            "type": "string",
                            "description": "User ID who generated the report (must exist)"
                        }
                    },
                    "required": []
                }
            }
        }

