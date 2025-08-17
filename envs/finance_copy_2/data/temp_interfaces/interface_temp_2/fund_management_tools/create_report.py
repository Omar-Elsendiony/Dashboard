import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, generated_by: str, 
               export_period_end: str, report_type: str = "performance",
               investor_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        users = data.get("users", {})
        investors = data.get("investors", {})
        reports = data.get("reports", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate user exists
        if str(generated_by) not in users:
            raise ValueError(f"User {generated_by} not found")
        
        # Validate investor if provided
        if investor_id and str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate report type
        valid_types = ["performance", "holding", "financial"]
        if report_type not in valid_types:
            raise ValueError(f"Invalid report type. Must be one of {valid_types}")
        
        report_id = generate_id(reports)
        timestamp = "2025-10-01T00:00:00"
        
        new_report = {
            "report_id": report_id,
            "fund_id": fund_id,
            "investor_id": investor_id,
            "report_date": "2025-10-01",
            "report_type": report_type,
            "generated_by": generated_by,
            "status": "pending",
            "created_at": timestamp,
            "export_period_end": export_period_end
        }
        
        reports[str(report_id)] = new_report
        return json.dumps(new_report)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_report",
                "description": "Create a custom report for specific needs",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "generated_by": {"type": "string", "description": "ID of the user creating the report"},
                        "export_period_end": {"type": "string", "description": "End date for the report period"},
                        "report_type": {"type": "string", "description": "Type of report (performance, holding, financial), defaults to performance"},
                        "investor_id": {"type": "string", "description": "ID of specific investor (optional)"}
                    },
                    "required": ["fund_id", "generated_by", "export_period_end"]
                }
            }
        }
