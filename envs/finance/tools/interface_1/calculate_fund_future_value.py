import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CalculateFundFutureValue(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_closing_price_or_nav: float, fund_growth_rate: float, 
               fund_number_of_years: int) -> str:
        
        # Validate inputs
        if fund_closing_price_or_nav <= 0:
            return json.dumps({"success": False, "message": "Closing price or NAV must be positive", "halt": True})
        
        if fund_number_of_years < 0:
            return json.dumps({"success": False, "message": "Number of years must be non-negative", "halt": True})
        
        # Calculate future value using formula: FV = PV * (1 + r)^n
        future_value = round(fund_closing_price_or_nav * ((1 + fund_growth_rate) ** fund_number_of_years), 4)
        
        return json.dumps({"future_value": future_value})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_fund_future_value",
                "description": "Calculate fund future value using compound interest formula",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_closing_price_or_nav": {"type": "number", "description": "Closing price of fund or NAV"},
                        "fund_growth_rate": {"type": "number", "description": "Fund growth rate 'r'"},
                        "fund_number_of_years": {"type": "integer", "description": "Number of years 'n'"}
                    },
                    "required": ["fund_closing_price_or_nav", "fund_growth_rate", "fund_number_of_years"]
                }
            }
        }
