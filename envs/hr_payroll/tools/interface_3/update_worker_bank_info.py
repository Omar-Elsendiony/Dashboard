import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateWorkerBankInfo(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        worker_id: str = None,
        user_id: str = None,
        bank_info: Dict[str, Any] = None
    ) -> str:
        if not bank_info:
            raise ValueError("bank_info is required")

        workers = data.get("workers", {})
        bank_accounts = data.setdefault("bank_accounts", {})

        # Resolve user_id from worker_id if not provided
        if worker_id:
            if worker_id not in workers:
                raise ValueError("Worker not found")
            resolved_user_id = workers[worker_id]["user_id"]
            if user_id and user_id != resolved_user_id:
                raise ValueError("Provided user_id does not match worker_id")
            user_id = resolved_user_id

        if not user_id:
            raise ValueError("Either worker_id or user_id must be provided")

        # Update the bank account
        updated = None
        for acct_id, acct in bank_accounts.items():
            if acct.get("user_id") == user_id:
                acct.update(bank_info)
                updated = acct
                break

        if not updated:
            raise ValueError("Bank account not found for user")

        return json.dumps({
            "user_id": user_id,
            "worker_id": worker_id,
            "updated": updated
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_worker_bank_info",
                "description": (
                    "Updates the bank details for a worker using either worker_id or user_id. "
                    "If both are given, they must resolve to the same person."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "The ID of the worker (used to resolve user_id)"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "The user ID linked to the bank account (used directly if worker_id not provided)"
                        },
                        "bank_info": {
                            "type": "object",
                            "description": "Bank info fields to update (e.g., account_number, currency, bank_name)",
                            "properties": {
                                "account_number": {"type": "string"},
                                "currency": {"type": "string"},
                                "bank_name": {"type": "string"}
                            }
                        }
                    },
                    "required": ["bank_info"]
                }
            }
        }
