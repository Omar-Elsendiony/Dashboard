import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverFinancialEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover financial data entities: NAV records, instrument prices, invoices, and payments.
        
        Supported entities:
        - nav_records: Net Asset Value records by fund_id, nav_date, nav_value
        - instrument_prices: Price data by instrument_id, price_date, close_price
        - invoices: Invoice records by commitment_id, amount, status, due_date
        - payments: Payment records by invoice_id, subscription_id, amount, status, payment_method
        """
        if entity_type not in ["nav_records", "instrument_prices", "invoices", "payments"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'nav_records', 'instrument_prices', 'invoices', or 'payments'"
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
            "nav_records": "nav_id",
            "instrument_prices": "price_id",
            "invoices": "invoice_id",
            "payments": "payment_id"
        }[entity_type]
        
        # Apply filters if provided
        if entity_type == "nav_records":
            entities = data.get("nav_records", {})
        elif entity_type == "instrument_prices":
            entities = data.get("instrument_prices", {})
        elif entity_type == "invoices":
            entities = data.get("invoices", {})
        elif entity_type == "payments":
            entities = data.get("payments", {})

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
                "name": "discover_financial_entities",
                "description": "Discover financial data entities including NAV records, instrument prices, invoices, and payments. Entity types: 'nav_records' (Net Asset Value records; filterable by fund_id, nav_date, nav_value), 'instrument_prices' (price data; filterable by instrument_id, price_date, close_price, open_price, high_price, low_price), 'invoices' (invoice records; filterable by commitment_id, amount, status, due_date, invoice_date), 'payments' (payment records; filterable by invoice_id, subscription_id, amount, status, payment_method, payment_date).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'nav_records', 'instrument_prices', 'invoices', or 'payments'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to apply. For nav_records: fund_id, nav_date, nav_value. For instrument_prices: instrument_id, price_date, close_price, open_price, high_price, low_price. For invoices: commitment_id, amount, status, due_date, invoice_date. For payments: invoice_id, subscription_id, amount, status, payment_method, payment_date",
                            "additionalProperties": True
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }