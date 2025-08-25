import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SubmitReimbursementReceipt(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], reimbursement_id: str, **kwargs) -> str:
        reimbursements = data.setdefault("reimbursements", {})

        # If reimbursement does not exist, create a new record
        if reimbursement_id not in reimbursements:
            reimbursements[reimbursement_id] = {}

        # Filter out document_id — do not store it
        filtered_kwargs = {k: v for k, v in kwargs.items() if k != "document_id"}

        # Update the reimbursement with the remaining fields
        reimbursements[reimbursement_id].update(filtered_kwargs)

        return json.dumps({
            "reimbursement_id": reimbursement_id,
            **reimbursements[reimbursement_id]
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "submit_reimbursement_receipt",
                "description": "Submits or updates a reimbursement record. Accepts any fields, but ignores document_id as it is not part of the reimbursement schema.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reimbursement_id": {
                            "type": "string",
                            "description": "The unique ID of the reimbursement (new or existing)"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "The user associated with the reimbursement"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "The worker associated with the reimbursement"
                        },
                        "amount": {
                            "type": "number",
                            "description": "The reimbursement amount"
                        },
                        "status": {
                            "type": "string",
                            "description": "The status of the reimbursement"
                        },
                        "currency": {
                            "type": "string",
                            "description": "The reimbursement currency (e.g., USD)"
                        },
                        "organization_id": {
                            "type": "string",
                            "description": "The ID of the associated organization"
                        },
                        "submit_date": {
                            "type": "string",
                            "description": "Date the reimbursement was submitted (YYYY-MM-DD)"
                        },
                        "approve_date": {
                            "type": "string",
                            "description": "Date the reimbursement was approved (optional)"
                        },
                        "contract_id": {
                            "type": "string",
                            "description": "Contract related to the reimbursement"
                        },
                        "document_id": {
                            "type": "string",
                            "description": "Receipt document ID (will be ignored during update)"
                        }
                    },
                    "required": ["reimbursement_id"]
                }
            }
        }
