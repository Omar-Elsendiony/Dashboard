import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class create_new_commitment(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        fund_id: str,
        investor_id: str,
        commitment_amount: float,
        currency: str,
        commitment_date: str
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            return str(max((int(k) for k in table.keys()), default=0) + 1)

        funds = data.get("funds", {})
        investors = data.get("investors", {})
        commitments = data.setdefault("commitments", {})

        # Validate fund exists
        if fund_id not in funds:
            raise ValueError(f"Fund {fund_id} not found")

        # Validate investor exists
        if investor_id not in investors:
            raise ValueError(f"Investor {investor_id} not found")

        # Validate currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if currency not in valid_currencies:
            raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")

        commitment_id = generate_id(commitments)
        now = "2025-08-07T00:00:00Z"

        new_commitment = {
            "commitment_id": commitment_id,
            "fund_id": fund_id,
            "investor_id": investor_id,
            "commitment_amount": round(float(commitment_amount), 2),
            "currency": currency,
            "commitment_date": commitment_date,
            "status": "pending",
            "updated_at": now
        }

        commitments[commitment_id] = new_commitment
        return json.dumps(new_commitment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_new_commitment",
                "description": "Create a new commitment for an investor to a fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {
                            "type": "string",
                            "description": "ID of the fund"
                        },
                        "investor_id": {
                            "type": "string",
                            "description": "ID of the investor"
                        },
                        "commitment_amount": {
                            "type": "number",
                            "description": "Commitment amount"
                        },
                        "currency": {
                            "type": "string",
                            "enum": ["USD", "EUR", "GBP", "NGN"],
                            "description": "Currency code"
                        },
                        "commitment_date": {
                            "type": "string",
                            "format": "date",
                            "description": "Commitment date (YYYY-MM-DD)"
                        }
                    },
                    "required": [
                        "fund_id",
                        "investor_id",
                        "commitment_amount",
                        "currency",
                        "commitment_date"
                    ]
                }
            }
        }