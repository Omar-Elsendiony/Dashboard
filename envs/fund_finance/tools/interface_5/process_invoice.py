import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ProcessInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, invoice_data: Dict[str, Any] = None, invoice_id: str = None) -> str:
        """
        Create or update invoice records.
        
        Actions:
        - create: Create new invoice record (requires invoice_data with invoice_date, due_date, amount, finance_officer_approval)
        - update: Update existing invoice record (requires invoice_id and invoice_data with changes, finance_officer_approval)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
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
            required_fields = ["invoice_date", "due_date", "amount", "finance_officer_approval"]
            missing_fields = [field for field in required_fields if field not in invoice_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for invoice creation: {', '.join(missing_fields)}. Finance Officer approval is required."
                })
            
            # Validate that finance_officer_approval is True
            if not invoice_data.get("finance_officer_approval"):
                return json.dumps({
                    "success": False,
                    "error": "Finance Officer approval must be True for invoice creation"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["commitment_id", "invoice_date", "due_date", "amount", "status", "finance_officer_approval"]
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
                    "error": "Invoice amount must be positive - negative or zero values are not allowed"
                })
            
            # Validate status enum if provided
            if "status" in invoice_data:
                valid_statuses = ["issued", "paid"]
                if invoice_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status '{invoice_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Validate date logic (due_date should not be before invoice_date)
            if invoice_data["due_date"] < invoice_data["invoice_date"]:
                return json.dumps({
                    "success": False,
                    "error": "Invalid date logic: due date cannot be before invoice date"
                })
            
            # Validate that invoice_date is not in the future (using current system date)
            from datetime import datetime
            current_date = "2025-10-01"  # Based on policy current date
            if invoice_data["invoice_date"] > current_date:
                return json.dumps({
                    "success": False,
                    "error": "Invalid invoice date: cannot create invoice with future date"
                })
            
            # Check for existing invoice with same commitment_id and invoice_date if commitment_id is provided
            if "commitment_id" in invoice_data and invoice_data["commitment_id"]:
                commitment_id = invoice_data["commitment_id"]
                invoice_date = invoice_data["invoice_date"]
                for existing_invoice in invoices.values():
                    if (existing_invoice.get("commitment_id") == commitment_id and 
                        existing_invoice.get("invoice_date") == invoice_date):
                        return json.dumps({
                            "success": False,
                            "error": f"Invoice already exists for commitment {commitment_id} on date {invoice_date}. Only one invoice per commitment per date is allowed."
                        })
            
            # Generate new invoice ID using the same pattern as other tools
            new_invoice_id = generate_id(invoices)
            
            # Create new invoice record
            new_invoice = {
                "invoice_id": str(new_invoice_id),
                "commitment_id": str(invoice_data.get("commitment_id")),
                "invoice_date": invoice_data["invoice_date"],
                "due_date": invoice_data["due_date"],
                "amount": invoice_data["amount"],
                "status": invoice_data.get("status", "issued"),
                "updated_at": "2025-10-01T12:00:00"
            }
            
            invoices[str(new_invoice_id)] = new_invoice
            
            return json.dumps({
                "success": True,
                "action": "create",
                "invoice_id": str(new_invoice_id),
                "message": f"Invoice {new_invoice_id} created successfully for commitment {invoice_data.get('commitment_id', 'N/A')} on {invoice_data['invoice_date']}",
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
                    "error": f"Invoice record {invoice_id} not found"
                })
            
            if not invoice_data:
                return json.dumps({
                    "success": False,
                    "error": "invoice_data is required for update action"
                })
            
            # Validate required approval for updates
            if "finance_officer_approval" not in invoice_data:
                return json.dumps({
                    "success": False,
                    "error": "Missing required approval for invoice update: finance_officer_approval. Finance Officer approval is required."
                })
            
            # Validate that finance_officer_approval is True
            if not invoice_data.get("finance_officer_approval"):
                return json.dumps({
                    "success": False,
                    "error": "Finance Officer approval must be True for invoice update"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["status", "due_date", "amount", "commitment_id", "finance_officer_approval"]
            invalid_fields = [field for field in invoice_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for invoice update: {', '.join(invalid_fields)}. Cannot update invoice_date."
                })
            
            # Get current invoice data for validation
            current_invoice = invoices[invoice_id].copy()
            current_status = current_invoice.get("status", "issued")
            
            # Check if invoice is already paid (cannot modify paid invoices except specific fields)
            if current_status == "paid" and "status" in invoice_data and invoice_data["status"] != "paid":
                return json.dumps({
                    "success": False,
                    "error": "Cannot change status from paid to issued - paid invoices cannot be unpaid"
                })
            
            # Validate amount if provided
            if "amount" in invoice_data and invoice_data["amount"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Invoice amount must be positive - negative or zero values are not allowed"
                })
            
            # Validate status if provided
            if "status" in invoice_data:
                valid_statuses = ["issued", "paid"]
                if invoice_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status '{invoice_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Update current invoice with new values for validation
            temp_invoice = current_invoice.copy()
            for key, value in invoice_data.items():
                if key not in ["finance_officer_approval"]:
                    temp_invoice[key] = value
            
            # Validate date logic after update if due_date is being changed
            if "due_date" in invoice_data:
                if temp_invoice["due_date"] < temp_invoice["invoice_date"]:
                    return json.dumps({
                        "success": False,
                        "error": "Invalid date logic: due date cannot be before invoice date"
                    })
            
            # Check for duplicate commitment_id and invoice_date combination if commitment_id is being updated
            if "commitment_id" in invoice_data and invoice_data["commitment_id"]:
                commitment_id = invoice_data["commitment_id"]
                invoice_date = temp_invoice["invoice_date"]
                for existing_id, existing_invoice in invoices.items():
                    if (existing_id != invoice_id and 
                        existing_invoice.get("commitment_id") == commitment_id and 
                        existing_invoice.get("invoice_date") == invoice_date):
                        return json.dumps({
                            "success": False,
                            "error": f"Invoice already exists for commitment {commitment_id} on date {invoice_date}. Only one invoice per commitment per date is allowed."
                        })
            
            # Update invoice record
            updated_invoice = current_invoice.copy()
            for key, value in invoice_data.items():
                if key not in ["finance_officer_approval"]:
                    updated_invoice[key] = value
            
            updated_invoice["updated_at"] = "2025-10-01T12:00:00"
            invoices[invoice_id] = updated_invoice
            
            return json.dumps({
                "success": True,
                "action": "update",
                "invoice_id": str(invoice_id) if invoice_id is not None else None,
                "message": f"Invoice {invoice_id} updated successfully",
                "invoice_data": updated_invoice
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_invoice",
                "description": "Create or update invoice records in the fund management system. This tool manages invoice lifecycle from creation to payment processing with comprehensive validation to ensure data integrity and compliance with business rules. For creation, establishes new invoice records with validation to prevent duplicate invoices for the same commitment and date combination. For updates, modifies existing invoice records while maintaining data integrity and preventing invalid state transitions. Requires Finance Officer approval for all operations as mandated by regulatory requirements. Validates date logic (due date >= invoice date), ensures positive amounts, and enforces proper status transitions. Essential for accurate billing processes, commitment tracking, and financial reporting. Supports the complete invoice lifecycle from initial creation to payment completion.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new invoice record, 'update' to modify existing invoice record",
                            "enum": ["create", "update"]
                        },
                        "invoice_data": {
                            "type": "object",
                            "description": "Invoice data object. For create: requires invoice_date, due_date (>= invoice_date), amount (positive), finance_officer_approval, with optional commitment_id and status (defaults to 'issued'). For update: includes invoice fields to change with finance_officer_approval (invoice_date cannot be updated). SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "commitment_id": {
                                    "type": "string",
                                    "description": "Reference to related commitment (optional, unique with invoice_date if provided)"
                                },
                                "invoice_date": {
                                    "type": "string",
                                    "description": "Date of invoice issuance in YYYY-MM-DD format (required for create only, cannot be updated, cannot be future date)"
                                },
                                "due_date": {
                                    "type": "string",
                                    "description": "Payment due date in YYYY-MM-DD format (must be >= invoice_date)"
                                },
                                "amount": {
                                    "type": "number",
                                    "description": "Invoice amount with high precision (must be positive)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Invoice status: 'issued' or 'paid' (defaults to 'issued' for new invoices, cannot change from paid to issued)",
                                    "enum": ["issued", "paid"]
                                },
                                "finance_officer_approval": {
                                    "type": "boolean",
                                    "description": "Finance Officer approval presence (True/False) (required for both create and update operations)"
                                }
                            }
                        },
                        "invoice_id": {
                            "type": "string",
                            "description": "Unique identifier of the invoice record (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }