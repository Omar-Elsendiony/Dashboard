import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverFundEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover fund entities.
        
        Supported entities:
        - funds: Fund records by fund_id, name, fund_type, manager_id, size, status
        """
        if entity_type not in ["funds"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'funds'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("funds", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "fund_id": entity_id})
            else:
                results.append({**entity_data, "fund_id": entity_id})
        
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
                "name": "discover_fund_entities",
                "description": "Discover fund entities. Entity types: 'funds' (fund records; filterable by fund_id (string), name (string), fund_type (enum: 'mutual_funds', 'exchange_traded_funds', 'pension_funds', 'private_equity_funds', 'hedge_funds', 'sovereign_wealth_funds', 'money_market_funds', 'real_estate_investment_trusts', 'infrastructure_funds', 'multi_asset_funds'), manager_id (string), size (decimal), status (enum: 'open', 'closed'), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'funds'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For funds, filters are: fund_id (string), name (string), fund_type (enum: 'mutual_funds', 'exchange_traded_funds', 'pension_funds', 'private_equity_funds', 'hedge_funds', 'sovereign_wealth_funds', 'money_market_funds', 'real_estate_investment_trusts', 'infrastructure_funds', 'multi_asset_funds'), manager_id (string), size (decimal), status (enum: 'open', 'closed'), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
