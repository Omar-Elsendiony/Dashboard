import json
from typing import Any, Dict, Optional
import datetime
from tau_bench.envs.tool import Tool

class AdministerExpenseReimbursements(Tool):
    """
    Execute expense reimbursements, including creation and processing.
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        operation: str,
        employee_id: Optional[str] = None,
        expense_date: Optional[str] = None,
        amount: Optional[float] = None,
        expense_type: Optional[str] = None,
        receipt_file_path: Optional[str] = None,
        reimbursement_id: Optional[str] = None,
        status: Optional[str] = None,
        approved_by: Optional[str] = None,
        payment_date: Optional[str] = None,
    ) -> str:
        """
        Executes the specified operation (create or update) on expense reimbursements.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        expense_reimbursements = data.get("expense_reimbursements", {})
        employees = data.get("employees", {})
        users = data.get("users", {})

        if operation == "create":
            if not all([employee_id, expense_date, amount, expense_type]):
                return json.dumps({"error": "Missing required parameters for create operation."})

            if employee_id not in employees:
                return json.dumps({"error": f"Employee with ID {employee_id} not found."})

            # --- Start of revised validation logic ---
            if amount <= 0:
                return json.dumps({"error": "Validation failed: The amount must be a positive value."})
            
            try:
                # This check is now just to validate the date format is correct.
                datetime.datetime.strptime(expense_date, '%Y-%m-%d').date()
            except ValueError:
                return json.dumps({"error": "Invalid date format. Please use YYYY-MM-DD."})
            # --- End of revised validation logic ---
            
            valid_expense_types = ["travel", "meals", "equipment", "training", "other"]
            if expense_type not in valid_expense_types:
                return json.dumps({"error": f"Invalid expense type. Must be one of {valid_expense_types}."})

            new_reimbursement_id = generate_id(expense_reimbursements)
            new_reimbursement = {
                "reimbursement_id": new_reimbursement_id,
                "employee_id": employee_id,
                "expense_date": expense_date,
                "amount": amount,
                "expense_type": expense_type,
                "receipt_file_path": receipt_file_path,
                "status": "submitted",
                "approved_by": None,
                "payment_date": None,
                "created_at": timestamp,
                "updated_at": timestamp,
            }
            expense_reimbursements[new_reimbursement_id] = new_reimbursement
            return json.dumps(new_reimbursement)

        elif operation == "update":
            if not all([reimbursement_id, status]):
                return json.dumps({"error": "Missing reimbursement_id or status for update operation."})

            if reimbursement_id not in expense_reimbursements:
                return json.dumps({"error": f"Reimbursement with ID {reimbursement_id} not found."})

            valid_statuses = ["approved", "rejected", "paid"]
            if status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}."})

            if status in ["approved", "rejected"] and not approved_by:
                return json.dumps({"error": f"approved_by is required when status is '{status}'."})
            
            if status == "paid" and not payment_date:
                return json.dumps({"error": "payment_date is required when status is 'paid'."})
            
            if approved_by and approved_by not in users:
                return json.dumps({"error": f"User with ID {approved_by} not found."})

            record_to_update = expense_reimbursements[reimbursement_id]
            record_to_update["status"] = status
            
            if approved_by:
                record_to_update["approved_by"] = approved_by
            if payment_date:
                record_to_update["payment_date"] = payment_date
            
            record_to_update["updated_at"] = timestamp
            return json.dumps(record_to_update)

        else:
            return json.dumps({"error": "Invalid operation. Must be 'create' or 'update'."})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns the schema for the ManageExpenseReimbursements tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "administer_expense_reimbursements",
                "description": "Used by employees to submit new expense claims (create) and by finance to process these claims (update).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {"type": "string", "description": "Action: 'create' or 'update'."},
                        "employee_id": {"type": "string", "description": "The ID of the employee submitting the expense. Required for 'create'."},
                        "expense_date": {"type": "string", "description": "The date the expense was incurred (YYYY-MM-DD). Required for 'create'."},
                        "amount": {"type": "number", "description": "The total amount of the reimbursement claim. Required for 'create'."},
                        "expense_type": {"type": "string", "description": "Category: 'travel', 'meals', 'equipment', 'training', 'other'. Required for 'create'."},
                        "receipt_file_path": {"type": "string", "description": "The storage path to the scanned receipt or invoice. Optional for 'create'."},
                        "reimbursement_id": {"type": "string", "description": "The ID of the expense reimbursement record to modify. Required for 'update'."},
                        "status": {"type": "string", "description": "New status: 'approved', 'rejected', 'paid'. Required for 'update'."},
                        "approved_by": {"type": "string", "description": "The user ID of the finance officer or manager processing the request. Required if status is 'approved' or 'rejected'."},
                        "payment_date": {"type": "string", "description": "The date the payment was issued (YYYY-MM-DD). Required if status is 'paid'."},
                    },
                    "required": ["operation"],
                },
            },
        }