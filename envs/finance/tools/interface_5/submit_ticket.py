import json
from datetime import datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class submit_ticket(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], issue_date: str, type: str,
               invoice_id: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        tickets = data.get("tickets", {})
        invoices = data.get("invoices", {})
        
        # Validate invoice if provided
        if str(invoice_id) not in invoices:
            raise ValueError(f"Invoice {invoice_id} not found")
        
        # Validate type
        valid_types = ["missing_payment", "overpayment", "underpayment", "mismatched_amount", "invoice_duplicate", "manual_follow_up"]
        if type not in valid_types:
            raise ValueError(f"Invalid type. Must be one of {valid_types}")
        
        ticket_id = generate_id(tickets)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        new_ticket = {
            "ticket_id": str(ticket_id),
            "invoice_id": invoice_id,
            "issue_date": issue_date,
            "type": type,
            "status": "open",
            "assigned_to": None,
            "resolution_date": None,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        tickets[str(ticket_id)] = new_ticket
        return json.dumps(new_ticket)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "submit_ticket",
                "description": "Submit a new ticket",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "ID of the related invoice"},
                        "issue_date": {"type": "string", "description": "Issue date"},
                        "type": {"type": "string", "description": "Ticket type (missing_payment, overpayment, underpayment, mismatched_amount, invoice_duplicate, manual_follow_up)"},
                    },
                    "required": ["issue_date", "type", "invoice_id"]
                }
            }
        }
