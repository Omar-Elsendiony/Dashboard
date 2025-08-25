import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListOpenReimbursements(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str = None,
        worker_id: str = None,
        currency: str = None,
        organization_id: str = None,
        contract_id: str = None,
        submit_date: str = None,
        approve_date: str = None,
        min_amount: float = None,
        max_amount: float = None
    ) -> str:
        reimbursements = data.get("reimbursements", {})
        workers = data.get("workers", {})

        # Resolve user_id if only worker_id is provided
        if not user_id and worker_id:
            if worker_id not in workers:
                return "Error: Worker not found"
            user_id = workers[worker_id].get("user_id")

        def matches(r):
            if r.get("status") != "submitted":
                return False
            if user_id and r.get("user_id") != user_id:
                return False
            if currency and r.get("currency") != currency:
                return False
            if organization_id and r.get("organization_id") != organization_id:
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

        results = [
            {**r, "reimbursement_id": rid}
            for rid, r in reimbursements.items()
            if matches(r)
        ]
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_open_reimbursements",
                "description": "Lists reimbursements with status 'submitted', filtered optionally by user, worker, currency, organization, contract, date, and amount.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "The ID of the worker (used to resolve user_id)"
                        },
                        "currency": {
                            "type": "string",
                            "description": "Currency code to filter by"
                        },
                        "organization_id": {
                            "type": "string",
                            "description": "Organization ID to filter by"
                        },
                        "contract_id": {
                            "type": "string",
                            "description": "Contract ID to filter by"
                        },
                        "submit_date": {
                            "type": "string",
                            "description": "Submission date to filter by (YYYY-MM-DD)"
                        },
                        "approve_date": {
                            "type": "string",
                            "description": "Approval date to filter by (YYYY-MM-DD)"
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
                    "required": []
                }
            }
        }
