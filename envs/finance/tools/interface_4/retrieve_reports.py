import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class retrieve_reports(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        report_id: Optional[str] = None,
        fund_id: Optional[str] = None,
        investor_id: Optional[str] = None,
        report_type: Optional[str] = None,
        generated_by: Optional[str] = None,
        status: Optional[str] = None
    ) -> str:
        reports = data.get("reports", {})
        users = data.get("users", {})
        results = []

        # Validate status if provided
        valid_statuses = {"pending", "completed", "failed"}
        if status is not None and status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")

        # Validate report_type if provided
        valid_types = {"performance", "holding", "financial"}
        if report_type is not None and report_type not in valid_types:
            raise ValueError(f"Invalid report_type. Must be one of {valid_types}")

        # Validate generated_by if provided
        if generated_by is not None and str(generated_by) not in users:
            raise ValueError(f"User {generated_by} not found")

        for rpt in reports.values():
            if report_id is not None and str(rpt.get("report_id")) != str(report_id):
                continue
            if fund_id is not None and str(rpt.get("fund_id")) != str(fund_id):
                continue
            if investor_id is not None:
                inv = rpt.get("investor_id")
                if inv is None or str(inv) != str(investor_id):
                    continue
            if report_type is not None and rpt.get("report_type") != report_type:
                continue
            if generated_by is not None and str(rpt.get("generated_by")) != str(generated_by):
                continue
            if status is not None and rpt.get("status") != status:
                continue

            results.append(rpt)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_reports",
                "description": (
                    "Retrieve reports filtered by optional parameters: report_id, fund_id, "
                    "investor_id, report_type, generated_by, or status."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "report_id": {
                            "type": "string",
                            "description": "Filter by report ID"
                        },
                        "fund_id": {
                            "type": "string",
                            "description": "Filter by fund ID"
                        },
                        "investor_id": {
                            "type": "string",
                            "description": "Filter by investor ID"
                        },
                        "report_type": {
                            "type": "string",
                            "description": "Filter by type (performance, holding, financial)"
                        },
                        "generated_by": {
                            "type": "string",
                            "description": "Filter by user ID who generated the report"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by status (pending, completed, failed)"
                        }
                    },
                    "required": []
                }
            }
        }