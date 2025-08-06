import json
from datetime import datetime
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class create_report(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str,
               report_date: str, report_type: str, generated_by: str,
               export_period_end: str, status: str = 'pending', investor_id: str = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return '1'
            return str(max(int(k) for k in table.keys()) + 1)
        
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        users = data.get("users", {})
        reports = data.get("reports", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate investor exists
        if investor_id and str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate user exists
        if str(generated_by) not in users:
            raise ValueError(f"User {generated_by} not found")
        
        # Validate report type
        valid_types = ["performance", "holding", "financial"]
        if report_type not in valid_types:
            raise ValueError(f"Invalid report type. Must be one of {valid_types}")

        valid_statuses = ['pending','completed','failed']
        if status not in valid_statuses:
            raise ValueError(f"Invalid report status. Must be one of {valid_statuses}")
        
        report_id = generate_id(reports)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        new_report = {
            "report_id": str(report_id),
            "fund_id": fund_id,
            "investor_id": investor_id,
            "report_date": report_date,
            "report_type": report_type,
            "generated_by": generated_by,
            "status": status,
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
                "description": "Create a new report",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "report_date": {"type": "string", "description": "Report date in YYYY-MM-DD format"},
                        "report_type": {"type": "string", "description": "Report type (performance, holding, financial)"},
                        "generated_by": {"type": "string", "description": "ID of the user generating the report"},
                        "export_period_end": {"type": "string", "description": "Export period end date in YYYY-MM-DD format"}
                    },
                    "required": ["fund_id", "report_date", "report_type", "generated_by", "export_period_end"]
                }
            }
        }
