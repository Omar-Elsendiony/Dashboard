import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class DiscoverTransactionEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover transaction-related entities: subscriptions, commitments, redemptions, and trades.
        
        Supported entities:
        - subscriptions: Fund subscriptions by fund_id, investor_id, amount, status, request_date
        - commitments: Investment commitments by fund_id, investor_id, amount, status
        - redemptions: Redemption requests by subscription_id, amount, status, request_date
        - trades: Trading transactions by fund_id, instrument_id, quantity, price, side, status
        """
        if entity_type not in ["subscriptions", "commitments", "redemptions", "trades"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'subscriptions', 'commitments', 'redemptions', or 'trades'"
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
            "subscriptions": "subscription_id",
            "commitments": "commitment_id",
            "redemptions": "redemption_id",
            "trades": "trade_id"
        }[entity_type]
        
        # Apply filters if provided
        if entity_type == "subscriptions":
            entities = data.get("subscriptions", {})
        elif entity_type == "commitments":
            entities = data.get("commitments", {})
        elif entity_type == "redemptions":
            entities = data.get("redemptions", {})
        elif entity_type == "trades":
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
                "name": "discover_transaction_entities",
                "description": "Discover transaction-related entities including subscriptions, commitments, redemptions, and trades. Entity types: 'subscriptions' (fund subscriptions; filterable by fund_id, investor_id, amount, status, request_date), 'commitments' (investment commitments; filterable by fund_id, investor_id, amount, status), 'redemptions' (redemption requests; filterable by subscription_id, amount, status, request_date), 'trades' (trading transactions; filterable by fund_id, instrument_id, quantity, price, side, status).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'subscriptions', 'commitments', 'redemptions', or 'trades'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For subscriptions, filters are: fund_id, investor_id, amount, status, request_date. For commitments, filters are: fund_id, investor_id, amount, status. For redemptions, filters are: subscription_id, amount, status, request_date. For trades, filters are: fund_id, instrument_id, quantity, price, side, status."
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }