import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetCommitmentPaymentHistory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_invoice_id: Optional[str] = None,
               subscription_id: Optional[str] = None,
               payment_method: Optional[str] = None, commitment_status: Optional[str] = None,
               start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        payments = data.get("payments", {})
        results = []
        
        for payment in payments.values():
            if commitment_invoice_id and payment.get("commitment_invoice_id") != commitment_invoice_id:
                continue
            if subscription_id and payment.get("subscription_id") != subscription_id:
                continue
            if payment_method and payment.get("payment_method") != payment_method:
                continue
            if commitment_status and payment.get("commitment_status") != commitment_status:
                continue
            if start_date and payment.get("payment_date", "") < start_date:
                continue
            if end_date and payment.get("payment_date", "") > end_date:
                continue
            results.append(payment)
        
        # Sort by payment_date descending (most recent first)
        results.sort(key=lambda x: x.get("payment_date", ""), reverse=True)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_payment_history",
                "description": "Get payment history with optional filters for reconciliation and audit",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_invoice_id": {"type": "string", "description": "Filter by invoice ID"},
                        "subscription_id": {"type": "string", "description": "Filter by subscription ID"},
                        "payment_method": {"type": "string", "description": "Filter by payment method (wire, cheque, credit_card, bank_transfer)"},
                        "commitment_status": {"type": "string", "description": "Filter by commitment_status (draft, completed, failed)"},
                        "start_date": {"type": "string", "description": "Filter payments from this date onwards"},
                        "end_date": {"type": "string", "description": "Filter payments up to this date"}
                    },
                    "required": []
                }
            }
        }
