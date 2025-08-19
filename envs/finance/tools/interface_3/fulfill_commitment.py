import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FulfillCommitment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str, payment_receipt_amount: float, 
               payment_date: str, payment_method: str) -> str:

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        commitments = data.get("commitments", {})
        invoices = data.get("invoices", {})
        payments = data.get("payments", {})
        
        # Validate commitment exists
        if str(commitment_id) not in commitments:
            return json.dumps({"success": False, "message": "Commitment not found", "halt": True})
        
        commitment = commitments[str(commitment_id)]
        
        # Validate payment method
        valid_methods = ["wire", "cheque", "credit_card", "bank_transfer"]
        if payment_method.lower() not in valid_methods:
            return json.dumps({"success": False, "message": f"Invalid payment method. Must be one of {valid_methods}", "halt": True})
        
        # Validate amount
        if payment_receipt_amount <= 0:
            return json.dumps({"success": False, "message": "Payment amount must be positive", "halt": True})
        
        # Create invoice if not exists
        invoice_id = None
        for inv_id, inv in invoices.items():
            if inv.get("commitment_id") == commitment_id:
                invoice_id = inv_id
                break
        
        if not invoice_id:
            invoice_id = generate_id(invoices)
            new_invoice = {
                "invoice_id": invoice_id,
                "commitment_id": str(commitment_id),
                "invoice_date": payment_date,
                "due_date": payment_date,
                "amount": commitment["commitment_amount"],
                "status": "issued",
                "updated_at": "2025-10-01T00:00:00"
            }
            invoices[str(invoice_id)] = new_invoice
        
        # Create payment record
        payment_id = generate_id(payments)
        timestamp = "2025-10-01T00:00:00"
        
        new_payment = {
            "payment_id": payment_id,
            "invoice_id": str(invoice_id),
            "payment_date": timestamp,
            "amount": payment_receipt_amount,
            "payment_method": payment_method.lower(),
            "status": "completed",
            "created_at": timestamp
        }
        
        payments[str(payment_id)] = new_payment
        
        # Update commitment status
        if payment_receipt_amount >= commitment["commitment_amount"]:
            commitment["status"] = "fulfilled"
            status = "fulfilled"
        else:
            status = "pending"
        
        commitment["updated_at"] = timestamp
        
        # Update invoice status if payment covers full amount
        if payment_receipt_amount >= invoices[str(invoice_id)]["amount"]:
            invoices[str(invoice_id)]["status"] = "paid"
            invoices[str(invoice_id)]["updated_at"] = timestamp
        
        return json.dumps({
            "commitment_id": str(commitment_id), 
            "success": True, 
            "status": status, 
            "amount": payment_receipt_amount
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fulfill_commitment",
                "description": "Fulfill a commitment by recording payment receipt",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "ID of the commitment"},
                        "payment_receipt_amount": {"type": "number", "description": "Amount received"},
                        "payment_date": {"type": "string", "description": "Date of payment (YYYY-MM-DD)"},
                        "payment_method": {"type": "string", "description": "Method of payment: wire, cheque, credit_card, bank_transfer"}
                    },
                    "required": ["commitment_id", "payment_receipt_amount", "payment_date", "payment_method"]
                }
            }
        }
