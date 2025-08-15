import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GenerateReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], report_type: str, period: str, 
               requester_role: str, fund_id: Optional[str] = None, 
               investor_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        reports = data.get("reports", {})
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        users = data.get("users", {})
        
        # Validate report type
        valid_types = ["performance", "financial", "holding"]
        if report_type.lower() not in valid_types:
            return json.dumps({"success": False, "message": f"Invalid report type. Must be one of {valid_types}", "halt": True})
        
        # Validate requester role
        valid_roles = ["admin", "employee"]
        if requester_role.lower() not in valid_roles:
            return json.dumps({"success": False, "message": f"Invalid requester role. Must be one of {valid_roles}", "halt": True})
        
        # If fund_id provided, validate it exists
        if fund_id and str(fund_id) not in funds:
            return json.dumps({"success": False, "message": "Fund not found", "halt": True})
        
        # If investor_id provided, validate it exists
        if investor_id and str(investor_id) not in investors:
            return json.dumps({"success": False, "message": "Investor not found", "halt": True})
        
        # Find a user with the appropriate role to be the generator
        generated_by = None
        for user_id, user in users.items():
            if user.get("role") == requester_role.lower():
                generated_by = user_id
                break
        
        if not generated_by:
            return json.dumps({"success": False, "message": "No authorized user found to generate report", "halt": True})
        
        report_id = generate_id(reports)
        timestamp = "2025-10-01T00:00:00"
        
        # Set fund_id to first available fund if not specified and needed
        if not fund_id and funds:
            fund_id = list(funds.keys())[0]
        
        new_report = {
            "report_id": report_id,
            "fund_id": fund_id,
            "investor_id": investor_id,
            "report_date": "2025-10-01",
            "report_type": report_type.lower(),
            "generated_by": generated_by,
            "status": "completed",
            "created_at": timestamp,
            "export_period_end": "2025-10-01"
        }
        
        reports[str(report_id)] = new_report
        
        return json.dumps({"report_id": str(report_id), "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "generate_report",
                "description": "Generate a report for funds or investors",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "report_type": {"type": "string", "description": "Type of report: performance, financial, holding"},
                        "fund_id": {"type": "string", "description": "ID of the fund 'optional'"},
                        "investor_id": {"type": "string", "description": "ID of the investor 'optional'"},
                        "period": {"type": "string", "description": "Reporting period"},
                        "requester_role": {"type": "string", "description": "Role of the person requesting the report"}
                    },
                    "required": ["report_type", "period", "requester_role"]
                }
            }
        }
