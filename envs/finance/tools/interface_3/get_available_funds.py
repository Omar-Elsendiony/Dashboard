import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetAvailableFunds(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None, investor_id: Optional[str] = None, 
               fund_type: Optional[str] = None, status: Optional[str] = None, name: Optional[str] = None) -> str:
        """
        Get available funds for investment based on filters.
        
        Args:
            data: Main data dictionary containing funds and investors
            investor_id: Optional investor ID for validation
            fund_type: Optional fund type filter. Valid types:
                - mutual_funds
                - exchange_traded_funds
                - pension_funds
                - private_equity_funds
                - hedge_funds
                - sovereign_wealth_funds
                - money_market_funds
                - real_estate_investment_trusts
                - infrastructure_funds
                - multi_asset_funds
            status: Optional status filter (open, closed)
            name: Optional fund name filter (case-insensitive partial match)
        
        Returns:
            JSON string of matching fund objects
        """
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        results = []
        
        # Valid fund types from database schema
        valid_fund_types = {
            'mutual_funds',
            'exchange_traded_funds',
            'pension_funds',
            'private_equity_funds',
            'hedge_funds',
            'sovereign_wealth_funds',
            'money_market_funds',
            'real_estate_investment_trusts',
            'infrastructure_funds',
            'multi_asset_funds'
        }
        
        # Valid statuses from database schema
        valid_statuses = {'open', 'closed'}
        
        # Validate fund_type if provided
        if fund_type and fund_type not in valid_fund_types:
            raise ValueError(f"Invalid fund_type '{fund_type}'. Valid types are: {', '.join(sorted(valid_fund_types))}")
        
        # Validate status if provided
        if status and status not in valid_statuses:
            raise ValueError(f"Invalid status '{status}'. Valid statuses are: {', '.join(sorted(valid_statuses))}")
        
        # If investor_id is provided, validate it exists
        if investor_id and str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        if fund_id:
            fund = funds.get(fund_id)
            if not fund:
                raise ValueError(f"Fund {fund_id} not found")
            # If a specific fund is requested, filter by it
            funds = {fund_id: fund}

        for fund in funds.values():
            # Filter by fund type if specified
            if fund_type and fund.get("fund_type") != fund_type:
                continue
            
            # Filter by status if specified (default to "open" if not specified)
            if status and fund.get("status") != status:
                continue
            elif not status and fund.get("status") != "open":
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
                "name": "get_available_funds",
                "description": "List all funds available for investment based on investor's accreditation and eligibility",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {
                            "type": "string",
                            "description": "ID of the fund (optional)"
                        },
                        "investor_id": {
                            "type": "string", 
                            "description": "ID of the investor (optional)"
                        },
                        "fund_type": {
                            "type": "string", 
                            "description": "Filter by fund type",
                            "enum": [
                                "mutual_funds",
                                "exchange_traded_funds", 
                                "pension_funds",
                                "private_equity_funds",
                                "hedge_funds",
                                "sovereign_wealth_funds",
                                "money_market_funds",
                                "real_estate_investment_trusts",
                                "infrastructure_funds",
                                "multi_asset_funds"
                            ]
                        },
                        "status": {
                            "type": "string", 
                            "description": "Filter by fund status",
                            "enum": ["open", "closed"]
                        },
                        "name": {
                            "type": "string",
                            "description": "Filter by fund name (case-insensitive partial match)"
                        }
                    },
                    "required": []
                }
            }
        }