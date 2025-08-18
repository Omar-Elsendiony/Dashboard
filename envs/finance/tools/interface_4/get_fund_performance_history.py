import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFundPerformanceHistory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], analysis_fund_id: str, 
               start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        funds = data.get("funds", {})
        nav_records = data.get("nav_records", {})
        
        # Validate fund exists
        if str(analysis_fund_id) not in funds:
            raise ValueError(f"Fund {analysis_fund_id} not found")
        
        # Get NAV records for this fund
        fund_navs = []
        for nav in nav_records.values():
            if nav.get("analysis_fund_id") == analysis_fund_id:
                nav_date = nav.get("nav_date")
                
                # Filter by date range if provided
                if start_date and nav_date < start_date:
                    continue
                if end_date and nav_date > end_date:
                    continue
                
                fund_navs.append(nav)
        
        # Sort by date
        fund_navs.sort(key=lambda x: x.get("nav_date", ""))
        
        return json.dumps(fund_navs)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_performance_history",
                "description": "Retrieve historical Net Asset Value data for specific funds over time periods",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "analysis_fund_id": {"type": "string", "description": "ID of the fund"},
                        "start_date": {"type": "string", "description": "Start date for NAV history (YYYY-MM-DD format)"},
                        "end_date": {"type": "string", "description": "End date for NAV history (YYYY-MM-DD format)"}
                    },
                    "required": ["analysis_fund_id"]
                }
            }
        }
