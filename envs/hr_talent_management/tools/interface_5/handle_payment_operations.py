import json
import re
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool
from datetime import datetime, date

class HandlePaymentOperations(Tool):

    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manages payment operations for released payslips and payment status updates.
        """
        
        # --- Utility Functions ---
        def _generate_id(table: Dict[str, Any]) -> int:
            """Utility to generate a new sequential ID. Aligned start ID."""
            if not table:
                return 10001
            return max(int(k) for k in table.keys()) + 1

        def _validate_date_format(date_str: str, field_name: str, allow_future: bool = True) -> Optional[str]:
            """Validates date format (YYYY-MM-DD) and checks if it's not in the future."""
            if date_str:
                date_pattern = r'^\d{4}-\d{2}-\d{2}$'
                if not re.match(date_pattern, date_str):
                    return f"Invalid {field_name} format. Must be YYYY-MM-DD"
                
                try:
                    dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    # Check for future date if not allowed
                    if not allow_future:
                        simulated_today = date(2025, 10, 1) # Using same simulated date as other tools
                        if dt_obj.date() > simulated_today:
                             return f"{field_name} cannot be in the future (compared to the system date)."
                except ValueError:
                    return f"Invalid date value provided for {field_name}. Please check year/month/day validity."
            return None

        def _convert_date_format(date_str: str) -> str:
            """Convert YYYY-MM-DD format for internal storage."""
            if date_str and re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                return date_str
            return date_str

        def _validate_status_field(status_value: str, field_name: str, valid_statuses: list) -> Optional[str]:
            """Validate status field against allowed values."""
            if status_value and status_value not in valid_statuses:
                return f"Invalid {field_name}. Must be one of: {', '.join(valid_statuses)}"
            return None

        valid_operations = ["create_payment", "update_payment_status"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "payment_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "payment_id": None,
                "message": "Invalid data format for payment operations"
            })

        payments = data.get("payments", {})
        payslips = data.get("payslips", {})
        employees = data.get("employees", {})
        users = data.get("users", {})

        # --- Payment Creation (create_payment) ---
        if operation_type == "create_payment":
            required_fields = ["employee_id", "cycle_id", "payslip_id", "amount", "payment_date", "payment_method", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]

            if missing_fields:
                return json.dumps({
                    "success": False,
                    "payment_id": None,
                    "message": f"Halt: Missing mandatory fields: {', '.join(missing_fields)}",
                    "transfer_to_human": True
                })

            # 1. Validation Checks (Full SOP)
            employee_id_str = str(kwargs["employee_id"])
            cycle_id_str = str(kwargs["cycle_id"])
            payslip_id_str = str(kwargs["payslip_id"])
            requester_id_str = str(kwargs["user_id"]) if kwargs.get("user_id") is not None else None

            # SOP: Verify user is an active Finance Manager or HR Director/Admin
            requester = users.get(requester_id_str)
            if not requester:
                return json.dumps({"success": False, "payment_id": None, "message": "Halt: Operation failed due to system errors - requester user not found", "transfer_to_human": True})

            if requester.get("employment_status") != "active" or requester.get("role") not in ["finance_manager", "hr_manager", "hr_admin"]:
                return json.dumps({"success": False, "payment_id": None, "message": "Halt: Unauthorized requester attempting to process payment - must be active Finance Manager or HR Director/Admin", "transfer_to_human": True})

            # Verify payslip exists and is released
            payslip = payslips.get(payslip_id_str)
            if not payslip:
                return json.dumps({"success": False, "payment_id": None, "message": "Halt: Payslip not found", "transfer_to_human": True})

            if payslip.get("payslip_status") != "released":
                return json.dumps({"success": False, "payment_id": None, "message": "Halt: Payslip not in 'released' status", "transfer_to_human": True})

            # Verify payslip belongs to the specified employee and cycle
            if payslip.get("employee_id") != employee_id_str or payslip.get("cycle_id") != cycle_id_str:
                return json.dumps({"success": False, "payment_id": None, "message": "Halt: Payslip does not match specified employee or cycle", "transfer_to_human": True})

            # Verify amount matches payslip net_pay
            try:
                payment_amount = float(kwargs["amount"])
                payslip_net_pay = float(payslip.get("net_pay", 0))
                if abs(payment_amount - payslip_net_pay) > 0.01:
                    return json.dumps({"success": False, "payment_id": None, "message": "Halt: Amount mismatch with payslip net_pay", "transfer_to_human": True})
            except (ValueError, TypeError):
                return json.dumps({"success": False, "payment_id": None, "message": "Halt: Invalid amount format", "transfer_to_human": True})

            # Validate payment_method
            valid_payment_methods = ["bank_transfer", "check", "cash"]
            method_error = _validate_status_field(kwargs["payment_method"], "payment_method", valid_payment_methods)
            if method_error:
                return json.dumps({"success": False, "payment_id": None, "message": f"Halt: {method_error}", "transfer_to_human": True})

            # Validate payment_date format and ensure it's not in the future
            date_error = _validate_date_format(kwargs["payment_date"], "payment_date", allow_future=False)
            if date_error:
                return json.dumps({"success": False, "payment_id": None, "message": f"Halt: {date_error}", "transfer_to_human": True})

            # Verify employee bank details are valid IF using bank_transfer
            employee = employees.get(employee_id_str)
            if not employee:
                return json.dumps({"success": False, "payment_id": None, "message": "Halt: Employee not found", "transfer_to_human": True})

            if kwargs["payment_method"] == "bank_transfer" and (not employee.get("bank_account_number") or not employee.get("routing_number")):
                return json.dumps({"success": False, "payment_id": None, "message": "Halt: Employee bank details missing for bank_transfer", "transfer_to_human": True})

            # Check for existing payment for this payslip
            existing_payment = any(p.get("payslip_id") == payslip_id_str for p in payments.values())
            if existing_payment:
                return json.dumps({"success": False, "payment_id": None, "message": "Halt: Payment already exists for this payslip", "transfer_to_human": True})

            # 2. Create Payment Record
            new_payment_id = _generate_id(payments)
            timestamp = datetime.now().isoformat()
            converted_payment_date = _convert_date_format(kwargs["payment_date"])

            new_payment = {
                "payment_id": str(new_payment_id),
                "employee_id": employee_id_str,
                "cycle_id": cycle_id_str,
                "payslip_id": payslip_id_str,
                "amount": payment_amount,
                "payment_date": converted_payment_date,
                "payment_method": kwargs["payment_method"],
                "payment_status": "pending",
                "transaction_id": None,
                "bank_confirmation_date": None,
                "created_at": timestamp
            }

            payments[str(new_payment_id)] = new_payment

            # SOP: Create Audit Entry
            try:
                audit_trails = data.setdefault("audit_trails", {})
                new_audit_id = str(max([int(k) for k in audit_trails.keys()] + [0]) + 1)
                audit_entry = {
                    "audit_id": new_audit_id,
                    "reference_id": str(new_payment_id),
                    "reference_type": "payment",
                    "action": "create",
                    "user_id": requester_id_str,
                    "field_name": None,
                    "old_value": None,
                    "new_value": json.dumps({"created_by": requester_id_str, "amount": payment_amount, "method": kwargs["payment_method"]}),
                    "created_at": timestamp
                }
                audit_trails[new_audit_id] = audit_entry
            except Exception:
                pass

            return json.dumps({
                "success": True,
                "payment_id": str(new_payment_id),
                "message": f"Payment {new_payment_id} created successfully. Status: pending. Transfer initiated."
            })

        # --- Update Payment Status ---
        elif operation_type == "update_payment_status":
            required_fields = ["payment_id", "payment_status", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]

            if missing_fields:
                return json.dumps({
                    "success": False,
                    "payment_id": None,
                    "message": f"Missing required fields for status update: {', '.join(missing_fields)}"
                })

            payment_id_str = str(kwargs["payment_id"])
            if payment_id_str not in payments:
                return json.dumps({
                    "success": False,
                    "payment_id": None,
                    "message": f"Payment {payment_id_str} not found"
                })

            valid_statuses = ["pending", "processed", "failed", "reversed"]
            status_error = _validate_status_field(kwargs["payment_status"], "payment_status", valid_statuses)
            if status_error:
                return json.dumps({"success": False, "payment_id": None, "message": status_error})

            # Validate bank_confirmation_date format if provided
            if "bank_confirmation_date" in kwargs and kwargs["bank_confirmation_date"] is not None:
                # Allowing future dates for confirmation date by default
                date_error = _validate_date_format(kwargs["bank_confirmation_date"], "bank_confirmation_date", allow_future=True)
                if date_error:
                    return json.dumps({"success": False, "payment_id": None, "message": date_error})

            # Execute Update
            payment = payments[payment_id_str]
            old_status = payment["payment_status"]
            requester_id_str = str(kwargs["user_id"])
            timestamp = datetime.now().isoformat()

            # Update fields
            payment["payment_status"] = kwargs["payment_status"]

            if "transaction_id" in kwargs and kwargs["transaction_id"] is not None:
                payment["transaction_id"] = kwargs["transaction_id"]

            if "bank_confirmation_date" in kwargs and kwargs["bank_confirmation_date"] is not None:
                payment["bank_confirmation_date"] = _convert_date_format(kwargs["bank_confirmation_date"])

            payment["updated_at"] = timestamp

            # SOP: Create Audit Entry
            try:
                audit_trails = data.setdefault("audit_trails", {})
                new_audit_id = str(max([int(k) for k in audit_trails.keys()] + [0]) + 1)
                audit_entry = {
                    "audit_id": new_audit_id,
                    "reference_id": payment_id_str,
                    "reference_type": "payment",
                    "action": "update_status",
                    "user_id": requester_id_str,
                    "field_name": "payment_status",
                    "old_value": old_status,
                    "new_value": kwargs["payment_status"],
                    "created_at": timestamp
                }
                audit_trails[new_audit_id] = audit_entry
            except Exception:
                pass

            return json.dumps({
                "success": True,
                "payment_id": payment_id_str,
                "message": f"Payment {payment_id_str} status updated to '{kwargs['payment_status']}' successfully"
            })

        return json.dumps({
            "success": False,
            "payment_id": None,
            "message": "Unhandled operation type"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_payment_operations",
                "description": "Manages core employee payment processing, including initiating new payments for released payslips and updating their status based on bank confirmation. The 'create_payment' operation validates payment details, ensures no duplicate payments exist for the payslip, checks user permissions (must be active Finance Manager or HR Director/Admin), verifies the payslip status is 'released', checks the amount against the payslip's net_pay, and confirms employee bank details before setting the initial status to 'pending' and creating an audit trail. The 'update_payment_status' operation records the final outcome (processed, failed, reversed) and optional transaction/confirmation details, also generating an audit trail.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation to perform: 'create_payment' or 'update_payment_status'.",
                            "enum": ["create_payment", "update_payment_status"]
                        },
                        "employee_id": {
                            "type": "string",
                            "description": "Unique identifier of the employee (required for create_payment)."
                        },
                        "cycle_id": {
                            "type": "string",
                            "description": "Payroll cycle identifier (required for create_payment)."
                        },
                        "payslip_id": {
                            "type": "string",
                            "description": "Payslip identifier (required for create_payment)."
                        },
                        "amount": {
                            "type": "number",
                            "description": "The net pay amount to be transferred (required for create_payment, must match payslip net_pay)."
                        },
                        "payment_date": {
                            "type": "string",
                            "description": "The date the payment is scheduled/processed in MM-DD-YYYY format (required for create_payment, must not be in the future).",
                            "pattern": "^\\d{2}-\\d{2}-\\d{4}$"
                        },
                        "payment_method": {
                            "type": "string",
                            "description": "Payment method (required for create_payment).",
                            "enum": ["bank_transfer", "check", "cash"]
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Unique identifier of the Finance Manager or HR Director/Admin initiating the action (required for both operations)."
                        },
                        "payment_id": {
                            "type": "string",
                            "description": "Unique identifier of the payment record (required for update_payment_status)."
                        },
                        "payment_status": {
                            "type": "string",
                            "description": "The status of the payment (must align with schema: 'pending', 'processed', 'failed', or 'reversed') (required for update_payment_status).",
                            "enum": ["pending", "processed", "failed", "reversed"]
                        },
                        "transaction_id": {
                            "type": "string",
                            "description": "Optional: The bank-generated transaction ID (optional for update_payment_status)."
                        },
                        "bank_confirmation_date": {
                            "type": "string",
                            "description": "Optional: The date the bank confirmed the status, in MM-DD-YYYY format (optional for update_payment_status).",
                            "pattern": "^\\d{2}-\\d{2}-\\d{4}$"
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }
