import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverValuationEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover valuation entities: NAV records and instrument prices.
        
        Supported entities:
        - nav_records: Net Asset Value records by nav_id, fund_id, nav_date, nav_value
        - instrument_prices: Price data by price_id, instrument_id, price_date, open_price, high_price, low_price, close_price
        """
        if entity_type not in ["nav_records", "instrument_prices"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'nav_records' or 'instrument_prices'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        id_field = {
            "nav_records": "nav_id",
            "instrument_prices": "price_id"
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
                "name": "discover_valuation_entities",
                "description": "Discover valuation entities including NAV records and instrument prices. Entity types: 'nav_records' (Net Asset Value records; filterable by nav_id (string), fund_id (string), nav_date (date), nav_value (decimal), updated_at (timestamp)), 'instrument_prices' (price data; filterable by price_id (string), instrument_id (string), price_date (date), open_price (decimal), high_price (decimal), low_price (decimal), close_price (decimal)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'nav_records' or 'instrument_prices'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For nav_records, filters are: nav_id (string), fund_id (string), nav_date (date), nav_value (decimal), updated_at (timestamp). For instrument_prices, filters are: price_id (string), instrument_id (string), price_date (date), open_price (decimal), high_price (decimal), low_price (decimal), close_price (decimal)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
