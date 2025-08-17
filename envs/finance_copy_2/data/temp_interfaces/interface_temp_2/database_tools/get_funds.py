import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetFunds(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        funds = data.get("funds", {})
        results = list(funds.values())
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_funds",
                "description": "Get fund catalog for investors and internal use",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
