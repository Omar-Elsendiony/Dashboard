import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetInvestorPortfolio(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, action: str) -> str:
        """
        Get investor portfolio information or detailed holdings breakdown.
        
        Args:
            data: Main data dictionary containing investors, portfolios, holdings, and funds
            investor_id: ID of the investor (required)
            action: Specify 'portfolio' for basic portfolio info or 'portfolio_holdings' for detailed holdings
        
        Returns:
            JSON string of portfolio data or holdings data based on action
        """
        investors = data.get("investors", {})
        portfolios = data.get("portfolios", {})
        
        # Validate investor exists for both actions
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        if action == "portfolio":
            
            results = []
            
            for portfolio in portfolios.values():
                if portfolio.get("investor_id") == str(investor_id):
                    results.append(portfolio)
            
            return json.dumps(results)
            
        elif action == "portfolio_holdings":
            # Handle detailed portfolio holdings retrieval
            portfolio_holdings = data.get("portfolio_holdings", {})
            funds = data.get("funds", {})
            
            # Find investor's portfolio
            investor_portfolio = None
            for portfolio in portfolios.values():
                if portfolio.get("investor_id") == str(investor_id):
                    investor_portfolio = portfolio
                    break
            
            if not investor_portfolio:
                return json.dumps([])
            
            # Get holdings for this portfolio
            holdings = []
            for holding in portfolio_holdings.values():
                if holding.get("portfolio_id") == investor_portfolio.get("portfolio_id"):
                    # Enrich with fund details
                    fund_id = holding.get("fund_id")
                    fund_details = funds.get(str(fund_id), {})
                    
                    enriched_holding = {
                        **holding,
                        "fund_name": fund_details.get("name"),
                        "fund_type": fund_details.get("fund_type"),
                        "fund_status": fund_details.get("status")
                    }
                    holdings.append(enriched_holding)
            
            return json.dumps(holdings)
        
        else:
            raise ValueError(f"Invalid action: {action}. Must be 'portfolio' or 'portfolio_holdings'")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_investor_portfolio_details",
                "description": """Retrieve investor portfolio information for client servicing and performance tracking.
                
                ACTIONS:
                1. 'portfolio' - Get basic portfolio information:
                   - Returns portfolio metadata, summary information
                   - Used for high-level portfolio overview
                   - Includes portfolio ID, investor ID, creation dates, etc.
                   
                2. 'portfolio_holdings' - Get detailed holdings breakdown:
                   - Returns individual fund holdings within the portfolio
                   - Enriched with fund details (name, type, status)
                   - Used for detailed portfolio composition analysis
                   - Shows quantities, values, fund characteristics
                
                USAGE EXAMPLES:
                - Get portfolio overview: action='portfolio', investor_id='INV123'
                - Get detailed holdings: action='portfolio_holdings', investor_id='INV123'
                
                VALIDATION:
                - Investor ID is validated against the investor database
                - Returns empty array if investor has no portfolio
                - Holdings are enriched with fund information for better analysis
                
                RETURN DATA:
                - 'portfolio': Array of portfolio objects with metadata
                - 'portfolio_holdings': Array of holding objects with fund details included
                """,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {
                            "type": "string", 
                            "description": "Required: ID of the investor whose portfolio information to retrieve"
                        },
                        "action": {
                            "type": "string",
                            "description": "Required: Specify 'portfolio' for basic portfolio info or 'portfolio_holdings' for detailed holdings breakdown",
                            "enum": ["portfolio", "portfolio_holdings"]
                        }
                    },
                    "required": ["investor_id", "action"]
                }
            }
        }