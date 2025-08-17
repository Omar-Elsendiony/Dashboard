import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetInvestors(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        investors = data.get("investors", {})
        results = list(investors.values())
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investors",
                "description": "Get all investors for client relationship management",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
