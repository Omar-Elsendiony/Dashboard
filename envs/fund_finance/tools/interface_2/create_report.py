import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateReport(Tool):
    """
    A tool to generate a new report record for a fund.
    """

    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, report_date: str, export_period_end: str, generated_by: str, investor_id: Optional[str] = None, report_type: str = "performance", status: str = "pending") -> str:
        """
        Generates a new report record.

        Args:
            data: The database json.
            fund_id: ID of the fund for the report.
            report_date: The date the report is generated.
            export_period_end: The end date for the reporting period.
            generated_by: ID of the user generating the report.
            investor_id: Optional ID of the investor for the report.
            report_type: The type of report.
            status: The initial status of the report.

        Returns:
            A json string of the new report record or an error.
        """
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        reports = data.get("reports", {})
        funds = data.get("funds", {})
        users = data.get("users", {})
        investors = data.get("investors", {})

        if fund_id not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        if generated_by not in users:
            return json.dumps({"error": f"User {generated_by} not found"})
        if investor_id and investor_id not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        
        valid_report_types = ["performance", "holding", "financial"]
        if report_type not in valid_report_types:
            return json.dumps({"error": f"Invalid report_type. Must be one of {valid_report_types}"})
            
        valid_statuses = ["pending", "completed", "failed"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}"})
        
        report_id = str(generate_id(reports))
        timestamp = "2025-10-01T00:00:00"
        
        new_report = {
            "report_id": str(report_id) if report_id is not None else None,
            "fund_id": str(fund_id) if fund_id is not None else None,
            "investor_id": str(investor_id) if investor_id is not None else None,
            "report_date": report_date,
            "report_type": report_type,
            "generated_by": generated_by,
            "status": status,
            "created_at": timestamp,
            "export_period_end": export_period_end
        }
        
        reports[report_id] = new_report
        return json.dumps(new_report)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns the schema for the GenerateReport tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "create_report",
                "description": "Creates a new report for a fund.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {
                            "type": "string",
                            "description": "ID of the fund for which the report is generated."
                        },
                        "report_date": {
                            "type": "string",
                            "description": "The date the report is generated (YYYY-MM-DD)."
                        },
                        "export_period_end": {
                            "type": "string",
                            "description": "The end date for the reporting period (YYYY-MM-DD)."
                        },
                        "generated_by": {
                            "type": "string",
                            "description": "The ID of the user generating the report."
                        },
                        "investor_id": {
                            "type": "string",
                            "description": "The ID of the investor the report is for (optional)."
                        },
                        "report_type": {
                            "type": "string",
                            "description": "Type of the report. Allowed values: performance, holding, financial. Defaults to 'performance'."
                        },
                        "status": {
                            "type": "string",
                            "description": "The initial status of the report. Allowed values: pending, completed, failed. Defaults to 'pending'."
                        }
                    },
                    "required": ["fund_id", "report_date", "export_period_end", "generated_by"]
                }
            }
        }
