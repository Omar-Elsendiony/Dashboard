import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class DiscoverInvestmentEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover funds, instruments, portfolios, and portfolio holdings.
        
        Supported entities:
        - funds: Investment funds by name, fund_type, manager_id, status
        - instruments: Financial instruments by ticker, name, instrument_type, status
        - portfolios: Investor portfolios by investor_id, status
        - portfolio_holdings: Holdings within portfolios by portfolio_id, fund_id, quantity, cost_basis
        """
        if entity_type not in ["funds", "instruments", "portfolios", "portfolio_holdings"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'funds', 'instruments', 'portfolios', or 'portfolio_holdings'"
            })
        
        # Access the entity data directly from the JSON structure (data is the specific entity file content)
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        # Determine ID field name
        id_field = {
            "funds": "fund_id",
            "instruments": "instrument_id", 
            "portfolios": "portfolio_id",
            "portfolio_holdings": "holding_id"
        }[entity_type]
        
        # Apply filters if provided
        if entity_type == "funds":
            entities = data.get("funds", {})
        elif entity_type == "instruments":
            entities = data.get("instruments", {})
        elif entity_type == "portfolios":
            entities = data.get("portfolios", {})
        elif entity_type == "portfolio_holdings":
            entities = data.get("portfolio_holdings", {})

        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_investment_entities",
                "description": "Discover investment-related entities including funds, instruments, portfolios, and holdings. Entity types: 'funds' (investment funds; filterable by name, fund_type, manager_id, status), 'instruments' (financial instruments; filterable by ticker, name, instrument_type, status), 'portfolios' (investor portfolios; filterable by investor_id, status), 'portfolio_holdings' (holdings within portfolios; filterable by portfolio_id, fund_id, quantity, cost_basis).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'funds', 'instruments', 'portfolios', or 'portfolio_holdings'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For funds, filters are: name, fund_type, manager_id, status. For instruments: ticker, name, instrument_type, status. For portfolios, filters are: investor_id, status. For portfolio_holdings, filters are: portfolio_id, fund_id, quantity, cost_basis"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }