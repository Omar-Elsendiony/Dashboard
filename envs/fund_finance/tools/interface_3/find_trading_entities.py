import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class FindTradingEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover trading entities.
        
        Supported entities:
        - trades: Trade records by trade_id, fund_id, instrument_id, trade_date, quantity, price, side, status
        """
        if entity_type not in ["trades"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'trades'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("trades", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "trade_id": str(entity_id)})
            else:
                results.append({**entity_data, "trade_id": str(entity_id)})
        
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
                "name": "find_trading_entities",
                "description": "Discover trading entities. Entity types: 'trades' (trade records; filterable by trade_id (string), fund_id (string), instrument_id (string), trade_date (timestamp), quantity (decimal), price (decimal), side (enum: 'buy', 'sell'), status (enum: 'approved', 'executed', 'pending', 'failed'), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'trades'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For trades, filters are: trade_id (string), fund_id (string), instrument_id (string), trade_date (timestamp), quantity (decimal), price (decimal), side (enum: 'buy', 'sell'), status (enum: 'approved', 'executed', 'pending', 'failed'), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
