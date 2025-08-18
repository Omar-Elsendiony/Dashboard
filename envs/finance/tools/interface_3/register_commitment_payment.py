import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RegisterCommitmentPayment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_invoice_id: str, payment_date: str,
               commitment_amount: str, payment_method: str, commitment_status: str = "draft") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        invoices = data.get("invoices", {})
        payments = data.get("payments", {})
        
        # Validate invoice exists
        if str(commitment_invoice_id) not in invoices:
            raise ValueError(f"Invoice {commitment_invoice_id} not found")
        
        # Validate payment method
        valid_methods = ["wire", "cheque", "credit_card", "bank_transfer"]
        if payment_method not in valid_methods:
            raise ValueError(f"Invalid payment method. Must be one of {valid_methods}")
        
        # Validate commitment_status
        valid_statuses = ["draft", "completed", "failed"]
        if commitment_status not in valid_statuses:
            raise ValueError(f"Invalid commitment_status. Must be one of {valid_statuses}")
        
        payment_id = generate_id(payments)
        timestamp = "2025-10-01T00:00:00"
        
        new_payment = {
            "payment_id": payment_id,
            "commitment_invoice_id": commitment_invoice_id,
            "payment_date": payment_date,
            "commitment_amount": commitment_amount,
            "payment_method": payment_method,
            "commitment_status": commitment_status,
            "created_at": timestamp
        }
        
        payments[str(payment_id)] = new_payment
        return json.dumps({"payment_id": payment_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "register_payment",
                "description": "Register a new payment against an invoice",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_invoice_id": {"type": "string", "description": "ID of the invoice"},
                        "payment_date": {"type": "string", "description": "Date of payment"},
                        "commitment_amount": {"type": "string", "description": "Payment commitment_amount"},
                        "payment_method": {"type": "string", "description": "Payment method (wire, cheque, credit_card, bank_transfer)"},
                        "commitment_status": {"type": "string", "description": "Payment commitment_status (draft, completed, failed), defaults to draft"}
                    },
                    "required": ["commitment_invoice_id", "payment_date", "commitment_amount", "payment_method"]
                }
            }
        }
