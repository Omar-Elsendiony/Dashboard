import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFundDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str) -> str:
        funds = data.get("funds", {})
        users = data.get("users", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        fund = funds[str(fund_id)]
        
        # Enrich with manager details
        manager_id = fund.get("manager_id")
        manager_details = users.get(str(manager_id), {})
        
        enriched_fund = {
            **fund,
            "manager_name": f"{manager_details.get('first_name', '')} {manager_details.get('last_name', '')}".strip(),
            "manager_email": manager_details.get("email")
        }
        
        return json.dumps(enriched_fund)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_fund_details",
                "description": "Get comprehensive information about a specific fund including strategy, fees, and performance",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"}
                    },
                    "required": ["fund_id"]
                }
            }
        }
