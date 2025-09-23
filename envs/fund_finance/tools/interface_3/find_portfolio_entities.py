import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class FindPortfolioEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover portfolio entities: portfolios and portfolio holdings.
        
        Supported entities:
        - portfolios: Portfolio records by portfolio_id, investor_id, status
        - portfolio_holdings: Portfolio holding records by holding_id, portfolio_id, fund_id, quantity, cost_basis
        """
        if entity_type not in ["portfolios", "portfolio_holdings"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'portfolios' or 'portfolio_holdings'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        id_field = {
            "portfolios": "portfolio_id",
            "portfolio_holdings": "holding_id"
        }[entity_type]
        
        entities = data.get(entity_type, {})
        
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
                "name": "find_portfolio_entities",
                "description": "Discover portfolio entities including portfolios and portfolio holdings. Entity types: 'portfolios' (portfolio records; filterable by portfolio_id (string), investor_id (string), status (enum: 'active', 'inactive', 'archived'), created_at (timestamp), updated_at (timestamp)), 'portfolio_holdings' (portfolio holding records; filterable by holding_id (string), portfolio_id (string), fund_id (string), quantity (decimal), cost_basis (decimal), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'portfolios' or 'portfolio_holdings'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For portfolios, filters are: portfolio_id (string), investor_id (string), status (enum: 'active', 'inactive', 'archived'), created_at (timestamp), updated_at (timestamp). For portfolio_holdings, filters are: holding_id (string), portfolio_id (string), fund_id (string), quantity (decimal), cost_basis (decimal), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
