import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetCommitmentReports(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_fund_id: Optional[str] = None, 
               investor_id: Optional[str] = None, report_type: Optional[str] = None,
               commitment_status: Optional[str] = None) -> str:
        reports = data.get("reports", {})
        results = []
        
        for report in reports.values():
            if commitment_fund_id and report.get("commitment_fund_id") != commitment_fund_id:
                continue
            if investor_id and report.get("investor_id") != investor_id:
                continue
            if report_type and report.get("report_type") != report_type:
                continue
            if commitment_status and report.get("commitment_status") != commitment_status:
                continue
            results.append(report)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_reports",
                "description": "Get reports with optional filters for distribution and access",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "report_type": {"type": "string", "description": "Filter by report type (performance, holding, financial)"},
                        "commitment_status": {"type": "string", "description": "Filter by commitment_status (pending, completed, failed)"}
                    },
                    "required": []
                }
            }
        }
