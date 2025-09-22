import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FilterFunds(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None, 
               investor_id: Optional[str] = None, manager_id: Optional[str] = None,
               fund_type: Optional[str] = None, status: Optional[str] = None, 
               name: Optional[str] = None, min_size: Optional[float] = None, 
               max_size: Optional[float] = None) -> str:
        """
        Filter funds based on multiple criteria for investment screening and selection.
        
        Args:
            data: Main data dictionary containing funds and investors
            fund_id: Optional specific fund ID to retrieve
            investor_id: Optional investor ID for validation
            manager_id: Optional manager ID filter
            fund_type: Optional fund type filter
            status: Optional status filter (defaults to 'open' if not specified)
            name: Optional fund name filter (case-insensitive partial match)
            min_size: Optional minimum fund size filter
            max_size: Optional maximum fund size filter
        
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
        
        # If fund_id is provided, filter to that specific fund
        if fund_id:
            fund = funds.get(fund_id)
            if not fund:
                raise ValueError(f"Fund {fund_id} not found")
            funds = {fund_id: fund}

        for fund in funds.values():
            # Filter by manager ID if specified
            if manager_id and fund.get("manager_id") != str(manager_id):
                continue
            
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
            
            # Filter by minimum size if specified
            if min_size is not None and (fund.get("size") is None or fund.get("size") < min_size):
                continue
            
            # Filter by maximum size if specified
            if max_size is not None and (fund.get("size") is None or fund.get("size") > max_size):
                continue
            
            results.append(fund)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "filter_fund_details",
                "description": """Filter and retrieve funds based on multiple criteria for investment screening and selection.
                
                FILTERING OPTIONS:
                1. SPECIFIC FUND LOOKUP:
                   - fund_id: Get a specific fund by its ID
                   
                2. VALIDATION FILTERS:
                   - investor_id: Validate investor exists in system
                   
                3. FUND CHARACTERISTICS:
                   - fund_type: Filter by fund category (mutual_funds, hedge_funds, etc.)
                   - status: Filter by operational status (open/closed, defaults to 'open')
                   - name: Search by fund name (partial, case-insensitive)
                   
                4. MANAGEMENT FILTERS:
                   - manager_id: Filter by fund manager
                   
                5. SIZE FILTERS:
                   - min_size: Minimum fund size
                   - max_size: Maximum fund size
                
                USAGE EXAMPLES:
                - Get all open equity mutual funds: fund_type='mutual_funds', status='open'
                - Find large hedge funds: fund_type='hedge_funds', min_size=1000000000
                - Search funds by name: name='Growth'
                - Get funds managed by specific manager: manager_id='MGR123'
                - Size range filter: min_size=100000000, max_size=500000000
                - Get specific fund details: fund_id='FUND123'
                
                DEFAULT BEHAVIOR: If no status is specified, only 'open' funds are returned.
                """,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {
                            "type": "string",
                            "description": "Optional: Get specific fund by ID"
                        },
                        "investor_id": {
                            "type": "string", 
                            "description": "Optional: Validate investor exists in system"
                        },
                        "manager_id": {
                            "type": "string",
                            "description": "Optional: Filter by fund manager ID"
                        },
                        "fund_type": {
                            "type": "string", 
                            "description": "Optional: Filter by fund type/category",
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
                            "description": "Optional: Filter by fund status (defaults to 'open' if not specified)",
                            "enum": ["open", "closed"]
                        },
                        "name": {
                            "type": "string",
                            "description": "Optional: Filter by fund name (case-insensitive partial match)"
                        },
                        "min_size": {
                            "type": "number",
                            "description": "Optional: Minimum fund size (AUM) filter"
                        },
                        "max_size": {
                            "type": "number",
                            "description": "Optional: Maximum fund size (AUM) filter"
                        }
                    },
                    "required": []
                }
            }
        }