import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManagePayment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, payment_data: Dict[str, Any] = None, payment_id: str = None) -> str:
        """
        Create or update payment records.
        
        Actions:
        - create: Create new payment (requires payment_data with invoice_id, subscription_id, payment_date, amount, payment_method, approval_code)
        - update: Update existing payment (requires payment_id and payment_data with changes like status, amount, approval_code)
        """
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
            
            # Validate required fields for creation
            required_fields = ["invoice_id", "subscription_id", "payment_date", "amount", "payment_method", "approval_code"]
            missing_fields = [field for field in required_fields if field not in payment_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for payment creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["invoice_id", "subscription_id", "payment_date", "amount", "payment_method", "status", "approval_code"]
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
            
            # Generate new payment ID
            existing_ids = [int(pid) for pid in payments.keys() if pid.isdigit()]
            new_payment_id = str(max(existing_ids, default=0) + 1)
            
            # Create new payment record
            new_payment = {
                "payment_id": new_payment_id,
                "invoice_id": payment_data["invoice_id"],
                "subscription_id": payment_data["subscription_id"],
                "payment_date": payment_data["payment_date"],
                "amount": payment_data["amount"],
                "payment_method": payment_data["payment_method"],
                "status": payment_data.get("status", "draft"),
                "created_at": "2025-10-01T12:00:00"
            }
            
            payments[new_payment_id] = new_payment
            
            return json.dumps({
                "success": True,
                "action": "create",
                "payment_id": new_payment_id,
                "message": f"Payment {new_payment_id} created successfully",
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
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["status", "amount", "payment_date", "payment_method", "approval_code"]
            invalid_fields = [field for field in payment_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for payment update: {', '.join(invalid_fields)}"
                })
            
            # Validate status transitions
            current_payment = payments[payment_id]
            current_status = current_payment.get("status", "draft")
            new_status = payment_data.get("status")
            
            if new_status and new_status not in ["draft", "completed", "failed"]:
                return json.dumps({
                    "success": False,
                    "error": "Invalid status. Must be one of: draft, completed, failed"
                })
            
            if new_status and current_status == "completed" and new_status in ["draft", "failed"]:
                return json.dumps({
                    "success": False,
                    "error": "Cannot change status from completed to draft or failed"
                })
            
            if new_status and current_status == "failed" and new_status == "completed":
                return json.dumps({
                    "success": False,
                    "error": "Cannot change status from failed to completed (create new payment instead)"
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
                if key not in ["approval_code"]:  # Skip approval_code from being stored
                    updated_payment[key] = value
            
            updated_payment["updated_at"] = "2025-10-01T12:00:00"
            payments[payment_id] = updated_payment
            
            return json.dumps({
                "success": True,
                "action": "update",
                "payment_id": payment_id,
                "message": f"Payment {payment_id} updated successfully",
                "payment_data": updated_payment
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_payment",
                "description": "Create or update payment records in the fund management system. For creation, requires invoice_id, subscription_id, payment_date, amount, payment_method, and approval_code. For updates, requires payment_id and fields to change (status, amount, etc.) with approval_code. Validates status transitions and business rules.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' or 'update'"
                        },
                        "payment_data": {
                            "type": "object",
                            "description": "Payment data. For create: invoice_id, subscription_id, payment_date, amount, payment_method, approval_code, optional status. For update: fields to change with approval_code"
                        },
                        "payment_id": {
                            "type": "string",
                            "description": "Payment ID (required for update action)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
