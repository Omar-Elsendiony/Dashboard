import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetFinancialProviderDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], provider_id: str) -> str:
        providers = data.get("financial_providers", {})
        provider = providers.get(provider_id)
        if not provider:
            raise ValueError("Financial provider not found")

        return json.dumps(provider)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_financial_provider_details",
                "description": "Fetches metadata about a financial provider such as name, country, and supported currencies",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "provider_id": {
                            "type": "string",
                            "description": "The unique identifier of the financial provider"
                        }
                    },
                    "required": ["provider_id"]
                }
            }
        }
