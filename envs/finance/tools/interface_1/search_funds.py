import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SearchFunds(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_type: Optional[str] = None,
               fund_manager_id: Optional[str] = None, fund_status: Optional[str] = None,
               fund_min_size: Optional[float] = None, fund_max_size: Optional[float] = None) -> str:
        
        funds = data.get("funds", {})
        results = []
        
        for fund in funds.values():
            if fund_type and fund.get("fund_type") != fund_type:
                continue
            if fund_manager_id and fund.get("manager_id") != str(fund_manager_id):
                continue
            if fund_status and fund.get("status") != fund_status:
                continue
            if fund_min_size is not None and (fund.get("size") is None or fund.get("size") < fund_min_size):
                continue
            if fund_max_size is not None and (fund.get("size") is None or fund.get("size") > fund_max_size):
                continue
            results.append(fund)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_funds",
                "description": "Search funds with filters for investment screening and selection",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_type": {"type": "string", "description": "Filter by fund type"},
                        "fund_manager_id": {"type": "string", "description": "Filter by manager ID"},
                        "fund_status": {"type": "string", "description": "Filter by status"},
                        "fund_min_size": {"type": "number", "description": "Minimum fund size"},
                        "fund_max_size": {"type": "number", "description": "Maximum fund size"}
                    },
                    "required": []
                }
            }
        }
