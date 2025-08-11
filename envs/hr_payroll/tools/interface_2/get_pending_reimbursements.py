import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPendingReimbursements(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        organization_id: str,
        user_id: str = None,
        worker_id: str = None,
        currency: str = None,
        contract_id: str = None,
        submit_date: str = None,
        approve_date: str = None,
        min_amount: float = None,
        max_amount: float = None
    ) -> str:
        reimbursements = data.get("reimbursements", {})

        def matches(r):
            if r.get("status") != "submitted":
                return False
            if r.get("organization_id") != organization_id:
                return False
            if user_id and r.get("user_id") != user_id:
                return False
            if worker_id and r.get("worker_id") != worker_id:
                return False
            if currency and r.get("currency") != currency:
                return False
            if contract_id and r.get("contract_id") != contract_id:
                return False
            if submit_date and r.get("submit_date") != submit_date:
                return False
            if approve_date and r.get("approve_date") != approve_date:
                return False
            if min_amount is not None and r.get("amount", 0) < min_amount:
                return False
            if max_amount is not None and r.get("amount", 0) > max_amount:
                return False
            return True

        result = [
            {**r, "reimbursement_id": rid}
            for rid, r in reimbursements.items()
            if matches(r)
        ]
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_pending_reimbursements",
                "description": (
                    "Returns reimbursements with status 'submitted' for a given organization, "
                    "optionally filtered by user ID, worker ID, currency, contract ID, date fields, and amount range."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "organization_id": {
                            "type": "string",
                            "description": "Organization ID for which reimbursements are being retrieved"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Filter by user ID"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "Filter by worker ID"
                        },
                        "currency": {
                            "type": "string",
                            "description": "Filter by currency code"
                        },
                        "contract_id": {
                            "type": "string",
                            "description": "Filter by contract ID"
                        },
                        "submit_date": {
                            "type": "string",
                            "description": "Filter by exact submit date (YYYY-MM-DD)"
                        },
                        "approve_date": {
                            "type": "string",
                            "description": "Filter by exact approve date (YYYY-MM-DD)"
                        },
                        "min_amount": {
                            "type": "number",
                            "description": "Minimum reimbursement amount"
                        },
                        "max_amount": {
                            "type": "number",
                            "description": "Maximum reimbursement amount"
                        }
                    },
                    "required": ["organization_id"]
                }
            }
        }
