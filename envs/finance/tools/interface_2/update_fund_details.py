import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class update_fund_details(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        fund_id: str,
        name: Optional[str] = None,
        fund_type: Optional[str] = None,
        base_currency: Optional[str] = None,
        size: Optional[float] = None,
        status: Optional[str] = None
    ) -> str:
        funds = data.get("funds", {})

        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund with ID {fund_id} not found")
        fund = funds[str(fund_id)]

        # Validate and apply updates
        if fund_type is not None:
            valid_fund_types = ["equity", "fixed_income", "multi_asset", "hedge"]
            if fund_type not in valid_fund_types:
                raise ValueError(f"Invalid fund type. Must be one of {valid_fund_types}")
            fund["fund_type"] = fund_type

        if base_currency is not None:
            valid_currencies = ["USD", "EUR", "GBP", "NGN"]
            if base_currency not in valid_currencies:
                raise ValueError(f"Invalid base currency. Must be one of {valid_currencies}")
            fund["base_currency"] = base_currency

        if status is not None:
            valid_statuses = ["open", "closed"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            fund["status"] = status

        if name is not None:
            fund["name"] = name

        if size is not None:
            if size < 0:
                raise ValueError("Size must be non-negative")
            fund["size"] = size

        # Only update timestamp if any field changed
        fund["updated_at"] = "2025-08-07T00:00:00Z"

        return json.dumps(fund)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_fund_details",
                "description": (
                    "Update one or more fields of a fund. "
                    "Provide fund_id plus any of: name, fund_type, base_currency, size, status."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund to update"},
                        "name": {"type": "string", "description": "New fund name"},
                        "fund_type": {
                            "type": "string",
                            "description": "New fund type (equity, fixed_income, multi_asset, hedge)"
                        },
                        "base_currency": {
                            "type": "string",
                            "description": "New base currency (USD, EUR, GBP, NGN)"
                        },
                        "size": {"type": "number", "description": "New fund size (non-negative)"},
                        "status": {"type": "string", "description": "New status (open, closed)"}
                    },
                    "required": ["fund_id"]
                }
            }
        }