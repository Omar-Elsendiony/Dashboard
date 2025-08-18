import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ModifyRelationsInvoiceConfig(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], relations_invoice_id: str, 
               invoice_date: Optional[str] = None, due_date: Optional[str] = None,
               amount: Optional[float] = None, status: Optional[str] = None) -> str:
        invoices = data.get("invoices", {})
        
        # Validate invoice exists
        if str(relations_invoice_id) not in invoices:
            raise ValueError(f"Invoice {relations_invoice_id} not found")
        
        invoice = invoices[str(relations_invoice_id)]
        
        # Validate status if provided
        if status:
            valid_statuses = ["issued", "paid"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Validate amount if provided
        if amount is not None and amount <= 0:
            raise ValueError("Amount must be positive")
        
        # Update fields
        if invoice_date:
            invoice["invoice_date"] = invoice_date
        if due_date:
            invoice["due_date"] = due_date
        if amount is not None:
            invoice["amount"] = amount
        if status:
            invoice["status"] = status
        
        invoice["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(invoice)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_invoice_config",
                "description": "Modify the configuration of an existing invoice",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "relations_invoice_id": {"type": "string", "description": "ID of the invoice to modify"},
                        "invoice_date": {"type": "string", "description": "New invoice date in YYYY-MM-DD format"},
                        "due_date": {"type": "string", "description": "New due date in YYYY-MM-DD format"},
                        "amount": {"type": "number", "description": "New invoice amount"},
                        "status": {"type": "string", "description": "New status (issued, paid)"}
                    },
                    "required": ["relations_invoice_id"]
                }
            }
        }
