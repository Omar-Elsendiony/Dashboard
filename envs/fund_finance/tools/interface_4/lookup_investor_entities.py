import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class LookupInvestorEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover investor entities.
        
        Supported entities:
        - investors: Investor records by investor_id, name, registration_number, date_of_incorporation, country, address, tax_id, source_of_funds, status, contact_email, accreditation_status
        """
        if entity_type not in ["investors"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'investors'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("investors", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "investor_id": entity_id})
            else:
                results.append({**entity_data, "investor_id": entity_id})
        
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
                "name": "lookup_investor_entities",
                "description": "Discover investor entities. Entity types: 'investors' (investor records; filterable by investor_id (string), name (string), registration_number (string), date_of_incorporation (date), country (string), address (string), tax_id (string), source_of_funds (enum: 'retained_earnings', 'shareholder_capital', 'asset_sale', 'loan_facility', 'external_investment', 'government_grant', 'merger_or_acquisition_proceeds', 'royalty_or_licensing_income', 'dividend_income', 'other'), status (enum: 'onboarded', 'offboarded'), contact_email (string), accreditation_status (enum: 'accredited', 'non_accredited'), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'investors'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For investors, filters are: investor_id (string), name (string), registration_number (string), date_of_incorporation (date), country (string), address (string), tax_id (string), source_of_funds (enum: 'retained_earnings', 'shareholder_capital', 'asset_sale', 'loan_facility', 'external_investment', 'government_grant', 'merger_or_acquisition_proceeds', 'royalty_or_licensing_income', 'dividend_income', 'other'), status (enum: 'onboarded', 'offboarded'), contact_email (string), accreditation_status (enum: 'accredited', 'non_accredited'), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
