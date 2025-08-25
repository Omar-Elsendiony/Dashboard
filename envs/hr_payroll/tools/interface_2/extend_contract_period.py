
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ExtendContractPeriod(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], contract_id: str, new_end_date: str) -> str:
        contracts = data.get("contracts", {})
        if contract_id not in contracts:
            raise ValueError("Contract not found")

        contract = contracts[contract_id]
        if new_end_date <= contract.get("start_date"):
            raise ValueError("End date must be after start date")

        contract["end_date"] = new_end_date
        return json.dumps(contract)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "extend_contract_period",
                "description": "Extends contract end date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "contract_id": {
                            "type": "string",
                            "description": "The ID of the contract to extend"
                        },
                        "new_end_date": {
                            "type": "string",
                            "description": "The new end date in YYYY-MM-DD format"
                        }
                    },
                    "required": ["contract_id", "new_end_date"]
                }
            }
        }
