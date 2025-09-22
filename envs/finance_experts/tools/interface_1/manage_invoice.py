import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManageInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, invoice_data: Dict[str, Any] = None, invoice_id: str = None) -> str:
        """
        Create or update invoice records.
        
        Actions:
        - create: Create new invoice (requires invoice_data with invoice_date, due_date, amount, approval_code, optional commitment_id)
        - update: Update existing invoice (requires invoice_id and invoice_data with changes like status, due_date, approval_code)
        """
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        # Access invoices data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for invoices"
            })
        
        invoices = data.get("invoices", {})
        
        if action == "create":
            if not invoice_data:
                return json.dumps({
                    "success": False,
                    "error": "invoice_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["invoice_date", "due_date", "amount", "approval_code"]
            missing_fields = [field for field in required_fields if field not in invoice_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for invoice creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["commitment_id", "invoice_date", "due_date", "amount", "status", "approval_code"]
            invalid_fields = [field for field in invoice_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for invoice creation: {', '.join(invalid_fields)}"
                })
            
            # Validate amount is positive
            if invoice_data["amount"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Invoice amount must be positive"
                })
            
            # Validate status enum if provided
            if "status" in invoice_data:
                valid_statuses = ["issued", "paid"]
                if invoice_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Generate new invoice ID
            existing_ids = [int(iid) for iid in invoices.keys() if iid.isdigit()]
            new_invoice_id = str(max(existing_ids, default=0) + 1)
            
            # Create new invoice record
            new_invoice = {
                "invoice_id": new_invoice_id,  # Add invoice_id to the record
                "commitment_id": invoice_data.get("commitment_id"),
                "invoice_date": invoice_data["invoice_date"],
                "due_date": invoice_data["due_date"],
                "amount": invoice_data["amount"],
                "status": invoice_data.get("status", "issued"),
                "updated_at": "2025-10-01T12:00:00"
            }
            
            invoices[new_invoice_id] = new_invoice
            
            return json.dumps({
                "success": True,
                "action": "create",
                "invoice_id": new_invoice_id,
                "message": f"Invoice {new_invoice_id} created successfully",
                "invoice_data": new_invoice
            })
        
        elif action == "update":
            if not invoice_id:
                return json.dumps({
                    "success": False,
                    "error": "invoice_id is required for update action"
                })
            
            if invoice_id not in invoices:
                return json.dumps({
                    "success": False,
                    "error": f"Invoice {invoice_id} not found"
                })
            
            if not invoice_data:
                return json.dumps({
                    "success": False,
                    "error": "invoice_data is required for update action"
                })
            
            # Validate required approval for updates
            if "approval_code" not in invoice_data:
                return json.dumps({
                    "success": False,
                    "error": "approval_code is required for invoice updates"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["status", "due_date", "amount", "commitment_id", "approval_code"]
            invalid_fields = [field for field in invoice_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for invoice update: {', '.join(invalid_fields)}"
                })
            
            # Get current invoice and validate status transitions
            current_invoice = invoices[invoice_id]
            current_status = current_invoice.get("status", "issued")
            new_status = invoice_data.get("status")
            
            # Check if invoice is already paid (cannot modify paid invoices)
            if current_status == "paid":
                return json.dumps({
                    "success": False,
                    "error": "Cannot modify paid invoices"
                })
            
            # Validate status if provided
            if new_status:
                if new_status not in ["issued", "paid"]:
                    return json.dumps({
                        "success": False,
                        "error": "Invalid status. Must be one of: issued, paid"
                    })
                
                if current_status == "paid" and new_status == "issued":
                    return json.dumps({
                        "success": False,
                        "error": "Cannot change status from paid to issued"
                    })
            
            # Validate amount if provided
            if "amount" in invoice_data and invoice_data["amount"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Invoice amount must be positive"
                })
            
            # Update invoice record
            updated_invoice = current_invoice.copy()
            for key, value in invoice_data.items():
                if key != "approval_code":  # Skip approval_code from being stored
                    updated_invoice[key] = value

            updated_invoice["updated_at"] = "2025-10-01T12:00:00"
            invoices[invoice_id] = updated_invoice
            
            return json.dumps({
                "success": True,
                "action": "update",
                "invoice_id": invoice_id,
                "message": f"Invoice {invoice_id} updated successfully",
                "invoice_data": updated_invoice
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_invoice",
                "description": "Create or update invoice records in the fund management system. For creation, requires invoice_date, due_date, amount, approval_code, with optional commitment_id and status (defaults to 'issued'). For updates, requires invoice_id and fields to change with approval_code. Validates amount is positive and prevents invalid status transitions (paid invoices cannot be modified).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' or 'update'",
                            "enum": ["create", "update"]
                        },
                        "invoice_data": {
                            "type": "object",
                            "description": "Invoice data object. For create: requires invoice_date, due_date, amount, approval_code, with optional commitment_id and status. For update: fields to change with approval_code.",
                            "properties": {
                                "commitment_id": {
                                    "type": "integer",
                                    "description": "Optional reference to related commitment"
                                },
                                "invoice_date": {
                                    "type": "string",
                                    "description": "Date of invoice issuance in YYYY-MM-DD format (required for create)"
                                },
                                "due_date": {
                                    "type": "string",
                                    "description": "Payment due date in YYYY-MM-DD format (required for create)"
                                },
                                "amount": {
                                    "type": "number",
                                    "description": "Invoice amount (must be positive)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Invoice status: 'issued' or 'paid' (defaults to 'issued' for new invoices)",
                                    "enum": ["issued", "paid"]
                                },
                                "approval_code": {
                                    "type": "string",
                                    "description": "Authorization code for invoice operations (required for both create and update)"
                                }
                            },
                            "additionalProperties": false
                        },
                        "invoice_id": {
                            "type": "string",
                            "description": "Unique identifier of the invoice (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }