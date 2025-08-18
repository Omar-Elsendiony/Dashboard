import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FilterFundsWithCriteria(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_type: Optional[str] = None,
               manager_id: Optional[str] = None, status: Optional[str] = None,
               min_size: Optional[float] = None, max_size: Optional[float] = None,
               name: Optional[str] = None) -> str:
        """
        Filter funds with criteria for investment screening and selection.
        
        Args:
            data: Main data dictionary containing funds
            fund_type: Optional fund type filter
            manager_id: Optional manager ID filter
            status: Optional status filter
            min_size: Optional minimum fund size filter
            max_size: Optional maximum fund size filter
            name: Optional fund name filter (case-insensitive partial match)
        
        Returns:
            JSON string of matching fund objects
        """
        funds = data.get("funds", {})
        results = []
        
        for fund in funds.values():
            if fund_type and fund.get("fund_type") != fund_type:
                continue
            if manager_id and fund.get("manager_id") != str(manager_id):
                continue
            if status and fund.get("status") != status:
                continue
            if min_size is not None and (fund.get("size") is None or fund.get("size") < min_size):
                continue
            if max_size is not None and (fund.get("size") is None or fund.get("size") > max_size):
                continue
            # Filter by name if specified (case-insensitive partial match)
            if name and name.lower() not in fund.get("name", "").lower():
                continue
            
            results.append(fund)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "filter_funds_with_criteria",
                "description": "Filter funds with criteria for investment screening and selection",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_type": {"type": "string", "description": "Filter by fund type"},
                        "manager_id": {"type": "string", "description": "Filter by manager ID"},
                        "status": {"type": "string", "description": "Filter by status"},
                        "min_size": {"type": "number", "description": "Minimum fund size"},
                        "max_size": {"type": "number", "description": "Maximum fund size"},
                        "name": {"type": "string", "description": "Filter by fund name (case-insensitive partial match)"}
                    },
                    "required": []
                }
            }
        }