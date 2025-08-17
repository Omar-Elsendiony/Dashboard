import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPaymentHistory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: Optional[str] = None,
               subscription_id: Optional[str] = None,
               payment_method: Optional[str] = None, status: Optional[str] = None,
               start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        payments = data.get("payments", {})
        results = []
        
        for payment in payments.values():
            if invoice_id and payment.get("invoice_id") != invoice_id:
                continue
            if subscription_id and payment.get("subscription_id") != subscription_id:
                continue
            if payment_method and payment.get("payment_method") != payment_method:
                continue
            if status and payment.get("status") != status:
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
                        "invoice_id": {"type": "string", "description": "Filter by invoice ID"},
                        "subscription_id": {"type": "string", "description": "Filter by subscription ID"},
                        "payment_method": {"type": "string", "description": "Filter by payment method (wire, cheque, credit_card, bank_transfer)"},
                        "status": {"type": "string", "description": "Filter by status (draft, completed, failed)"},
                        "start_date": {"type": "string", "description": "Filter payments from this date onwards"},
                        "end_date": {"type": "string", "description": "Filter payments up to this date"}
                    },
                    "required": []
                }
            }
        }
