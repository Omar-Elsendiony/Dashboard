import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetContracts(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        contract_id: str = None,
        user_id: str = None,
        worker_id: str = None,
        status: str = None,
        currency: str = None,
        organization_id: str = None,
        rate_type: str = None,
        document_id: str = None,
        min_rate: float = None,
        max_rate: float = None,
        start_date_from: str = None,
        start_date_to: str = None,
        end_date_from: str = None,
        end_date_to: str = None
    ) -> str:
        contracts = data.get("contracts", {})

        def matches(cid, c):
            if contract_id and cid != contract_id:
                return False
            if user_id and c.get("user_id") != user_id:
                return False
            if worker_id and c.get("worker_id") != worker_id:
                return False
            if status and c.get("status") != status:
                return False
            if currency and c.get("currency") != currency:
                return False
            if organization_id and c.get("organization_id") != organization_id:
                return False
            if rate_type and c.get("rate_type") != rate_type:
                return False
            if document_id and c.get("document_id") != document_id:
                return False
            if min_rate is not None and c.get("rate", 0) < min_rate:
                return False
            if max_rate is not None and c.get("rate", 0) > max_rate:
                return False
            if start_date_from and c.get("start_date") < start_date_from:
                return False
            if start_date_to and c.get("start_date") > start_date_to:
                return False
            if end_date_from and c.get("end_date") < end_date_from:
                return False
            if end_date_to and c.get("end_date") > end_date_to:
                return False
            return True

        result = [
            {**c, "contract_id": cid}
            for cid, c in contracts.items()
            if matches(cid, c)
        ]
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_contracts",
                "description": (
                    "Retrieves contracts filtered by any combination of contract_id, user_id, worker_id, status, "
                    "currency, rate_type, organization_id, document_id, rate range, and date ranges."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "contract_id": {"type": "string", "description": "Filter by contract ID"},
                        "user_id": {"type": "string", "description": "Filter by user ID"},
                        "worker_id": {"type": "string", "description": "Filter by worker ID"},
                        "status": {"type": "string", "description": "Filter by contract status"},
                        "currency": {"type": "string", "description": "Filter by currency"},
                        "organization_id": {"type": "string", "description": "Filter by organization ID"},
                        "rate_type": {"type": "string", "description": "Filter by rate type (hourly/monthly)"},
                        "document_id": {"type": "string", "description": "Filter by document ID"},
                        "min_rate": {"type": "number", "description": "Minimum rate"},
                        "max_rate": {"type": "number", "description": "Maximum rate"},
                        "start_date_from": {"type": "string", "description": "Start date from (inclusive)"},
                        "start_date_to": {"type": "string", "description": "Start date to (inclusive)"},
                        "end_date_from": {"type": "string", "description": "End date from (inclusive)"},
                        "end_date_to": {"type": "string", "description": "End date to (inclusive)"}
                    },
                    "required": []
                }
            }
        }
