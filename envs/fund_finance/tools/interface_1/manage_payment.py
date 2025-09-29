import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManagePayment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, payment_data: Dict[str, Any] = None, payment_id: str = None) -> str:
        """
        Create or update payment records.
        
        Actions:
        - create: Create new payment (requires payment_data with invoice_id, subscription_id, payment_date, amount, payment_method, finance_officer_approval)
        - update: Update existing payment (requires payment_id and payment_data with changes like status, amount, finance_officer_approval)
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
        
        # Access payments data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for payments"
            })
        
        payments = data.get("payments", {})
        
        if action == "create":
            if not payment_data:
                return json.dumps({
                    "success": False,
                    "error": "payment_data is required for create action"
                })
            
            # Validate required fields for creation - updated per policy
            required_fields = ["invoice_id", "subscription_id", "payment_date", "amount", "payment_method", "finance_officer_approval"]
            missing_fields = [field for field in required_fields if field not in payment_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for payment creation: {', '.join(missing_fields)}. Finance Officer approval is required."
                })
            
            # Validate required approval for creation
            if not payment_data.get("finance_officer_approval"):
                return json.dumps({
                    "success": False,
                    "error": "Finance Officer approval is required for payment creation"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["invoice_id", "subscription_id", "payment_date", "amount", "payment_method", "status", "finance_officer_approval"]
            invalid_fields = [field for field in payment_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for payment creation: {', '.join(invalid_fields)}"
                })
            
            # Validate amount is positive
            if payment_data["amount"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Payment amount must be positive"
                })
            
            # Validate payment_method enum
            valid_payment_methods = ["wire", "cheque", "credit_card", "bank_transfer"]
            if payment_data["payment_method"] not in valid_payment_methods:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid payment_method. Must be one of: {', '.join(valid_payment_methods)}"
                })
            
            # Validate status if provided
            if "status" in payment_data:
                valid_statuses = ["draft", "completed", "failed"]
                if payment_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Generate new payment ID using the same pattern as ManageInstrumentPrice
            new_payment_id = generate_id(payments)
            
            # Create new payment record
            new_payment = {
                "payment_id": str(new_payment_id) if new_payment_id else None ,
                "invoice_id": str(payment_data["invoice_id"]) if payment_data["invoice_id"] else None,
                "subscription_id": str(payment_data["subscription_id"]) if payment_data["subscription_id"] else None,
                "payment_date": payment_data["payment_date"],
                "amount": payment_data["amount"],
                "payment_method": payment_data["payment_method"],
                "status": payment_data.get("status", "draft"),
                "created_at": "2025-10-01T12:00:00"
            }
            
            payments[str(new_payment_id)] = new_payment
            
            return json.dumps({
                "success": True,
                "action": "create",
                "payment_id": str(new_payment_id) if new_payment_id else None ,
                "message": f"Payment {new_payment_id} created successfully for invoice {payment_data['invoice_id']}",
                "payment_data": new_payment
            })
        
        elif action == "update":
            if not payment_id:
                return json.dumps({
                    "success": False,
                    "error": "payment_id is required for update action"
                })
            
            if payment_id not in payments:
                return json.dumps({
                    "success": False,
                    "error": f"Payment {payment_id} not found"
                })
            
            if not payment_data:
                return json.dumps({
                    "success": False,
                    "error": "payment_data is required for update action"
                })
            
            # Validate required approval for updates
            if "finance_officer_approval" not in payment_data:
                return json.dumps({
                    "success": False,
                    "error": "finance_officer_approval is required for payment updates"
                })
            
            if not payment_data.get("finance_officer_approval"):
                return json.dumps({
                    "success": False,
                    "error": "Finance Officer approval is required for payment update"
                })
            
            # Validate only allowed fields are present for updates (cannot update core fields)
            allowed_update_fields = ["status", "amount", "payment_date", "payment_method", "finance_officer_approval"]
            invalid_fields = [field for field in payment_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for payment update: {', '.join(invalid_fields)}. Cannot update invoice_id or subscription_id."
                })
            
            # Get current payment for validation
            current_payment = payments[payment_id]
            current_status = current_payment.get("status", "draft")
            new_status = payment_data.get("status")
            
            # Validate status if provided
            if new_status and new_status not in ["draft", "completed", "failed"]:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: draft, completed, failed"
                })
            
            # Validate status transitions - cannot modify completed/processed payments per policy
            if current_status == "completed" and new_status and new_status != "completed":
                return json.dumps({
                    "success": False,
                    "error": "Cannot modify completed payment - cannot change status from completed to draft or failed"
                })
            
            if current_status == "failed" and new_status == "completed":
                return json.dumps({
                    "success": False,
                    "error": "Cannot change status from failed to completed - create new payment instead"
                })
            
            # Validate amount if provided
            if "amount" in payment_data and payment_data["amount"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Payment amount must be positive"
                })
            
            # Validate payment_method if provided
            if "payment_method" in payment_data:
                valid_payment_methods = ["wire", "cheque", "credit_card", "bank_transfer"]
                if payment_data["payment_method"] not in valid_payment_methods:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid payment_method. Must be one of: {', '.join(valid_payment_methods)}"
                    })
            
            # Update payment record
            updated_payment = current_payment.copy()
            for key, value in payment_data.items():
                if key != "finance_officer_approval":  # Skip approval from being stored
                    updated_payment[key] = value
            
            updated_payment["updated_at"] = "2025-10-01T12:00:00"
            payments[payment_id] = updated_payment
            
            return json.dumps({
                "success": True,
                "action": "update",
                "payment_id": str(payment_id),
                "message": f"Payment {payment_id} updated successfully",
                "payment_data": updated_payment
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_payment",
                "description": "Create or update payment records in the fund management system. This tool manages payment processing for investor subscriptions and invoice settlements with comprehensive validation and regulatory compliance controls. For creation, establishes new payment records linking invoices and subscriptions with proper validation of payment methods, amounts, and Finance Officer authorization. For updates, modifies existing payment records while maintaining data integrity and preventing unauthorized changes to completed payments. Validates payment amounts are positive, ensures proper payment method selection, and enforces status transition rules preventing modification of completed/processed payments per regulatory requirements. Essential for accurate financial record keeping, investor account management, and compliance with payment processing regulations. Supports the complete payment lifecycle from initial payment creation through final settlement processing.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new payment record, 'update' to modify existing payment record",
                            "enum": ["create", "update"]
                        },
                        "payment_data": {
                            "type": "object",
                            "description": "Payment data object. For create: requires invoice_id (target invoice), subscription_id (related subscription), payment_date (settlement date), amount (positive value), payment_method (settlement method), finance_officer_approval (authorization), with optional status (defaults to 'draft'). For update: fields to change with finance_officer_approval (core fields cannot be updated, completed payments cannot be modified). SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "invoice_id": {
                                    "type": "string",
                                    "description": "Unique identifier of the target invoice (required for create only, cannot be updated)"
                                },
                                "subscription_id": {
                                    "type": "string", 
                                    "description": "Unique identifier of the related subscription (required for create only, cannot be updated)"
                                },
                                "payment_date": {
                                    "type": "string",
                                    "description": "Date of payment settlement in YYYY-MM-DD format"
                                },
                                "amount": {
                                    "type": "number",
                                    "description": "Payment amount (must be positive, cannot exceed outstanding invoice balance)"
                                },
                                "payment_method": {
                                    "type": "string",
                                    "description": "Method of payment settlement",
                                    "enum": ["wire", "cheque", "credit_card", "bank_transfer"]
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Payment processing status (defaults to 'draft' for new payments, completed payments cannot be modified)",
                                    "enum": ["draft", "completed", "failed"]
                                },
                                "finance_officer_approval": {
                                    "type": "boolean",
                                    "description": "Finance Officer approval presence (True/False) (required for both create and update operations)"
                                }
                            }
                        },
                        "payment_id": {
                            "type": "string",
                            "description": "Unique identifier of the payment record (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }