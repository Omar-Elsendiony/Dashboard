import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FulfillInvestmentCommitment(Tool):
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
        
        # Validate commitment_amount
        if payment_receipt_amount <= 0:
            return json.dumps({"success": False, "message": "Payment commitment_amount must be positive", "halt": True})
        
        # Create invoice if not exists
        commitment_invoice_id = None
        for inv_id, inv in invoices.items():
            if inv.get("commitment_id") == commitment_id:
                commitment_invoice_id = inv_id
                break
        
        if not commitment_invoice_id:
            commitment_invoice_id = generate_id(invoices)
            new_invoice = {
                "commitment_invoice_id": commitment_invoice_id,
                "commitment_id": commitment_id,
                "invoice_date": payment_date,
                "commitment_due_date": payment_date,
                "commitment_amount": commitment["commitment_amount"],
                "commitment_status": "issued",
                "updated_at": "2025-10-01T00:00:00"
            }
            invoices[str(commitment_invoice_id)] = new_invoice
        
        # Create payment record
        payment_id = generate_id(payments)
        timestamp = "2025-10-01T00:00:00"
        
        new_payment = {
            "payment_id": payment_id,
            "commitment_invoice_id": str(commitment_invoice_id),
            "payment_date": timestamp,
            "commitment_amount": payment_receipt_amount,
            "payment_method": payment_method.lower(),
            "commitment_status": "completed",
            "created_at": timestamp
        }
        
        payments[str(payment_id)] = new_payment
        
        # Update commitment commitment_status
        if payment_receipt_amount >= commitment["commitment_amount"]:
            commitment["commitment_status"] = "fulfilled"
            commitment_status = "fulfilled"
        else:
            commitment_status = "pending"
        
        commitment["updated_at"] = timestamp
        
        # Update invoice commitment_status if payment covers full commitment_amount
        if payment_receipt_amount >= invoices[str(commitment_invoice_id)]["commitment_amount"]:
            invoices[str(commitment_invoice_id)]["commitment_status"] = "paid"
            invoices[str(commitment_invoice_id)]["updated_at"] = timestamp
        
        return json.dumps({
            "commitment_id": commitment_id, 
            "success": True, 
            "commitment_status": commitment_status, 
            "commitment_amount": payment_receipt_amount
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
