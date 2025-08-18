import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_name: str, fund_type: str,
               initial_fund_size: float, fund_manager_id: str, 
               fund_approval_code: str) -> str:

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        # Validate approval code exists
        approvals = data.get("approvals", {})
        approval_found = False
        for approval_id, approval in approvals.items():
            if approval.get("code") == fund_approval_code and approval.get("approver_role") == "fund_manager":
                approval_found = True
                break
        
        if not approval_found:
            return json.dumps({"error": f"Fund Manager approval code {fund_approval_code} not found or invalid. Process halted."})
        
        funds = data.get("funds", {})
        users = data.get("users", {})
        
        # Validate manager exists
        if str(fund_manager_id) not in users:
            return json.dumps({"error": f"Fund Manager {fund_manager_id} not found"})
        
        # Validate fund type
        valid_types = ["mutual_funds", "exchange_traded_funds", "pension_funds", "private_equity_funds",
                      "hedge_funds", "sovereign_wealth_funds", "money_market_funds", 
                      "real_estate_investment_trusts", "infrastructure_funds", "multi_asset_funds"]
        if fund_type not in valid_types:
            return json.dumps({"error": f"Invalid fund type. Must be one of {valid_types}"})
        
        fund_id = generate_id(funds)
        timestamp = "2025-10-01T00:00:00"
        
        new_fund = {
            "fund_id": fund_id,
            "name": fund_name,
            "fund_type": fund_type,
            "manager_id": int(fund_manager_id),
            "size": initial_fund_size,
            "status": "open", # status can be open, closed, or suspended
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        funds[str(fund_id)] = new_fund
        return json.dumps({"fund_id": str(fund_id)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_fund",
                "description": "Create a new fund with fund manager approval code verification for Fund Management & Trading Operations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_name": {"type": "string", "description": "Name of the fund to be created"},
                        "fund_type": {"type": "string", "description": "Type of fund. Must be one of: 'mutual_funds', 'exchange_traded_funds', 'pension_funds', 'private_equity_funds', 'hedge_funds', 'sovereign_wealth_funds', 'money_market_funds', 'real_estate_investment_trusts', 'infrastructure_funds', 'multi_asset_funds'"},
                        "initial_fund_size": {"type": "number", "description": "Initial size/assets under management of the fund"},
                        "fund_manager_id": {"type": "string", "description": "ID of the designated fund manager"},
                        "fund_approval_code": {"type": "string", "description": "Fund manager approval code for authorization"}
                    },
                    "required": ["fund_name", "fund_type", "initial_fund_size", "fund_manager_id", 
                            "fund_approval_code"]
                }
            }
        }
