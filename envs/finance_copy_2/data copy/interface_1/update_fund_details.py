import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateFundDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, name: Optional[str] = None,
               fund_type: Optional[str] = None, manager_id: Optional[str] = None,
               size: Optional[float] = None, status: Optional[str] = None) -> str:
        
        funds = data.get("funds", {})
        users = data.get("users", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        fund = funds[str(fund_id)]
        
        # Validate manager if provided
        if manager_id and str(manager_id) not in users:
            raise ValueError(f"Manager {manager_id} not found")
        
        # Validate fund type if provided
        if fund_type:
            valid_fund_types = ["mutual_funds", "exchange_traded_funds", "pension_funds", 
                               "private_equity_funds", "hedge_funds", "sovereign_wealth_funds",
                               "money_market_funds", "real_estate_investment_trusts", 
                               "infrastructure_funds", "multi_asset_funds"]
            if fund_type not in valid_fund_types:
                raise ValueError(f"Invalid fund type. Must be one of {valid_fund_types}")
            fund["fund_type"] = fund_type
        
        # Validate status if provided
        if status:
            valid_statuses = ["open", "closed"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            fund["status"] = status
        
        # Update fields if provided
        if name is not None:
            fund["name"] = name
        if manager_id is not None:
            fund["manager_id"] = str(manager_id)
        if size is not None:
            fund["size"] = size
        
        fund["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(fund)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_fund_details",
                "description": "Update fund details for strategy changes and fee updates",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "name": {"type": "string", "description": "Fund name (optional)"},
                        "fund_type": {"type": "string", "description": "Fund type (optional)"},
                        "manager_id": {"type": "string", "description": "Manager user ID (optional)"},
                        "size": {"type": "number", "description": "Fund size (optional)"},
                        "status": {"type": "string", "description": "Fund status (optional)"}
                    },
                    "required": ["fund_id"]
                }
            }
        }
