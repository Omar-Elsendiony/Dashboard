import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverInstrumentEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover instrument entities.
        
        Supported entities:
        - instruments: Instrument records by instrument_id, ticker, name, status, instrument_type
        """
        if entity_type not in ["instruments"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'instruments'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("instruments", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "instrument_id": entity_id})
            else:
                results.append({**entity_data, "instrument_id": entity_id})
        
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
                "name": "discover_instrument_entities",
                "description": "Discover instrument entities. Entity types: 'instruments' (instrument records; filterable by instrument_id (string), ticker (string), name (string), status (enum: 'active', 'inactive'), instrument_type (enum: 'equities_common_shares', 'equities_preferred_shares', 'equities_indexed', 'equities_domestic', 'equities_international', 'bonds_corporate', 'bonds_municipal', 'bonds_government', 'bonds_inflation_linked', 'bonds_high_yield', 'bonds_distressed', 'money_market_treasury_bills', 'money_market_commercial_paper', 'certificates_of_deposit', 'repurchase_agreements', 'short_term_municipal_notes', 'bankers_acceptances', 'commodities_gold_oil_futures', 'commodities_spot', 'commodities_futures', 'derivatives_options', 'derivatives_futures', 'derivatives_swaps', 'real_estate_direct_property', 'real_estate_reits', 'mortgage_backed_securities', 'property_development_loans', 'private_equity', 'equity_stakes_private_companies', 'equity_stakes_infrastructure_assets', 'mezzanine_financing', 'convertible_preferred_stock', 'leveraged_buyout_debt', 'distressed_debt', 'project_finance_debt', 'infrastructure_bonds', 'ppp_investments', 'infrastructure_debt_equity', 'infrastructure_projects', 'alternative_assets_hedge_funds', 'alternative_assets_commodities')).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'instruments'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For instruments, filters are: instrument_id (string), ticker (string), name (string), status (enum: 'active', 'inactive'), instrument_type (enum: 'equities_common_shares', 'equities_preferred_shares', 'equities_indexed', 'equities_domestic', 'equities_international', 'bonds_corporate', 'bonds_municipal', 'bonds_government', 'bonds_inflation_linked', 'bonds_high_yield', 'bonds_distressed', 'money_market_treasury_bills', 'money_market_commercial_paper', 'certificates_of_deposit', 'repurchase_agreements', 'short_term_municipal_notes', 'bankers_acceptances', 'commodities_gold_oil_futures', 'commodities_spot', 'commodities_futures', 'derivatives_options', 'derivatives_futures', 'derivatives_swaps', 'real_estate_direct_property', 'real_estate_reits', 'mortgage_backed_securities', 'property_development_loans', 'private_equity', 'equity_stakes_private_companies', 'equity_stakes_infrastructure_assets', 'mezzanine_financing', 'convertible_preferred_stock', 'leveraged_buyout_debt', 'distressed_debt', 'project_finance_debt', 'infrastructure_bonds', 'ppp_investments', 'infrastructure_debt_equity', 'infrastructure_projects', 'alternative_assets_hedge_funds', 'alternative_assets_commodities')"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
