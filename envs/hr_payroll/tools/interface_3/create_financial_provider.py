import json
import uuid
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class CreateFinancialProvider(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        name: str,
        country: str,
        supported_currencies: List[str]
    ) -> str:
        providers = data.setdefault("financial_providers", {})

        provider_id = str(uuid.uuid4())
        providers[provider_id] = {
            "name": name,
            "country": country,
            "supported_currencies": supported_currencies
        }

        return json.dumps({
            "provider_id": provider_id,
            **providers[provider_id]
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_financial_provider",
                "description": "Creates a new financial provider record with name, country, and supported currencies.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the financial provider"
                        },
                        "country": {
                            "type": "string",
                            "description": "Country where the provider operates"
                        },
                        "supported_currencies": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of supported currency codes (e.g., INR, USD, GBP)"
                        }
                    },
                    "required": ["name", "country", "supported_currencies"]
                }
            }
        }
