
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateContractPayTerms(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], contract_id: str, new_rate: float, rate_type: str) -> str:
        contracts = data.get("contracts", {})
        if contract_id not in contracts:
            raise ValueError("Contract not found")

        if contracts[contract_id]["status"] in ["terminated", "ended"]:
            raise ValueError("Cannot modify terminated contract")

        contracts[contract_id]["rate"] = round(new_rate, 4)
        contracts[contract_id]["rate_type"] = rate_type
        return json.dumps({"contract_id": contract_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_contract_pay_terms",
                "description": "Modifies payment terms of a contract",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "contract_id": {
                            "type": "string",
                            "description": "The contract to modify"
                        },
                        "new_rate": {
                            "type": "number",
                            "description": "New pay rate"
                        },
                        "rate_type": {
                            "type": "string",
                            "description": "Rate type: hourly, monthly, annual"
                        }
                    },
                    "required": ["contract_id", "new_rate", "rate_type"]
                }
            }
        }
