import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverInvestmentFlowEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover investment flow entities: subscriptions, commitments, and redemptions.
        
        Supported entities:
        - subscriptions: Subscription records by subscription_id, fund_id, investor_id, amount, status, request_assigned_to, request_date, approval_date
        - commitments: Commitment records by commitment_id, fund_id, investor_id, commitment_amount, commitment_date, status
        - redemptions: Redemption records by redemption_id, subscription_id, request_date, redemption_amount, status, processed_date, redemption_fee
        """
        if entity_type not in ["subscriptions", "commitments", "redemptions"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'subscriptions', 'commitments', or 'redemptions'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        id_field = {
            "subscriptions": "subscription_id",
            "commitments": "commitment_id",
            "redemptions": "redemption_id"
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
                "name": "discover_investment_flow_entities",
                "description": "Discover investment flow entities including subscriptions, commitments, and redemptions. Entity types: 'subscriptions' (subscription records; filterable by subscription_id (string), fund_id (string), investor_id (string), amount (decimal), status (enum: 'pending', 'approved', 'cancelled'), request_assigned_to (string), request_date (date), approval_date (date), updated_at (timestamp)), 'commitments' (commitment records; filterable by commitment_id (string), fund_id (string), investor_id (string), commitment_amount (decimal), commitment_date (date), status (enum: 'pending', 'fulfilled'), updated_at (timestamp)), 'redemptions' (redemption records; filterable by redemption_id (string), subscription_id (string), request_date (date), redemption_amount (decimal), status (enum: 'pending', 'approved', 'processed', 'cancelled'), processed_date (date), redemption_fee (decimal), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'subscriptions', 'commitments', or 'redemptions'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For subscriptions, filters are: subscription_id (string), fund_id (string), investor_id (string), amount (decimal), status (enum: 'pending', 'approved', 'cancelled'), request_assigned_to (string), request_date (date), approval_date (date), updated_at (timestamp). For commitments, filters are: commitment_id (string), fund_id (string), investor_id (string), commitment_amount (decimal), commitment_date (date), status (enum: 'pending', 'fulfilled'), updated_at (timestamp). For redemptions, filters are: redemption_id (string), subscription_id (string), request_date (date), redemption_amount (decimal), status (enum: 'pending', 'approved', 'processed', 'cancelled'), processed_date (date), redemption_fee (decimal), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
