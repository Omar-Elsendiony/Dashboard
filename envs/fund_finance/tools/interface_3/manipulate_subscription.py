import json
import re
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManipulateSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, subscription_data: Dict[str, Any], 
           subscription_id: Optional[str] = None) -> str:
        """
        Create, update, or cancel subscription records.
        
        Actions:
        - create: Create new subscription (requires subscription_data with fund_id, investor_id, amount, request_assigned_to, request_date, fund_manager_approval)
        - update: Update existing subscription (requires subscription_id and subscription_data with changes, fund_manager_approval)
        - cancel: Cancel subscription (requires subscription_id and fund_manager_approval)
        """
        
        if isinstance(subscription_data, str):
            try:
                subscription_data = json.loads(subscription_data)
            except json.JSONDecodeError:
                return json.dumps({
                    "success": False,
                    "error": "Invalid JSON format in subscription_data"
                })

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        def validate_date_format(date_str: str, field_name: str) -> Optional[str]:
            if date_str:
                date_pattern = r'^\d{4}-\d{2}-\d{2}$'
                if not re.match(date_pattern, date_str):
                    return f"Invalid {field_name} format. Must be YYYY-MM-DD"
            return None
        
        def validate_boolean_field(value: Any, field_name: str) -> Optional[str]:
            if not isinstance(value, bool):
                return f"Invalid {field_name}. Must be boolean (True/False)"
            return None
        
        # Validate action
        if action not in ["create", "update", "cancel"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create', 'update', or 'cancel'"
            })
        
        # Access related data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for subscriptions"
            })
        
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        users = data.get("users", {})
        subscriptions = data.get("subscriptions", {})
        
        if action == "create":
            if not subscription_data:
                return json.dumps({
                    "success": False,
                    "error": "subscription_data is required for create action"
                })
            
            # MODIFIED: Require only one approval
            required_fields = ["fund_id", "investor_id", "amount", "request_assigned_to", "request_date", "fund_manager_approval"]
            missing_fields = [field for field in required_fields if field not in subscription_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for subscription creation: {', '.join(missing_fields)}. Fund Manager approval is required."
                })
            
            # MODIFIED: Update allowed fields
            allowed_fields = ["fund_id", "investor_id", "amount", "request_assigned_to", "request_date", "status", "approval_date", "notify_investor", "fund_manager_approval"]
            invalid_fields = [field for field in subscription_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for subscription creation: {', '.join(invalid_fields)}"
                })
            
            # Extract and validate core fields
            fund_id = subscription_data["fund_id"]
            investor_id = subscription_data["investor_id"]
            amount = subscription_data["amount"]
            request_assigned_to = subscription_data["request_assigned_to"]
            request_date = subscription_data["request_date"]
            status = subscription_data.get("status", "pending")
            
            # Validate fund exists
            if str(fund_id) not in funds:
                return json.dumps({"success": False, "error": f"Fund {fund_id} not found"})
            
            # Validate investor exists
            if str(investor_id) not in investors:
                return json.dumps({"success": False, "error": f"Investor {investor_id} not found"})
            
            # Validate assigned user exists
            if str(request_assigned_to) not in users:
                return json.dumps({"success": False, "error": f"User {request_assigned_to} not found"})
            
            # Check for duplicate subscriptions
            for subscription in subscriptions.values():
                if (subscription.get("fund_id") == fund_id and 
                    subscription.get("investor_id") == investor_id):
                    return json.dumps({
                        "success": False,
                        "error": f"Subscription already exists for investor {investor_id} and fund {fund_id}."
                    })
            
            # Validate amount is positive
            try:
                if float(amount) <= 0:
                    return json.dumps({"success": False, "error": "Subscription amount must be positive"})
            except ValueError:
                return json.dumps({"success": False, "error": "Invalid amount format"})
            
            # Validate status enum
            if status not in ["pending", "approved", "cancelled"]:
                return json.dumps({"success": False, "error": "Invalid status"})
            
            # Validate date formats
            date_error = validate_date_format(request_date, "request_date")
            if date_error:
                return json.dumps({"success": False, "error": date_error})
            
            if "approval_date" in subscription_data:
                date_error = validate_date_format(subscription_data["approval_date"], "approval_date")
                if date_error:
                    return json.dumps({"success": False, "error": date_error})
            
            # Validate boolean fields
            bool_error = validate_boolean_field(subscription_data["fund_manager_approval"], "fund_manager_approval")
            if bool_error:
                return json.dumps({"success": False, "error": bool_error})
            
            if "notify_investor" in subscription_data:
                bool_error = validate_boolean_field(subscription_data["notify_investor"], "notify_investor")
                if bool_error:
                    return json.dumps({"success": False, "error": bool_error})
            
            # Generate new subscription ID and create record
            new_subscription_id = generate_id(subscriptions)
            new_subscription = {
                "subscription_id": str(new_subscription_id), "fund_id": fund_id, "investor_id": investor_id,
                "amount": amount, "status": status, "request_assigned_to": request_assigned_to,
                "request_date": request_date, "approval_date": subscription_data.get("approval_date"),
                "updated_at": "2025-10-01T00:00:00"
            }
            subscriptions[str(new_subscription_id)] = new_subscription
            
            return json.dumps({
                "success": True, "action": "create", "subscription_id": str(new_subscription_id),
                "message": f"Subscription {new_subscription_id} created successfully.",
                "subscription_data": new_subscription
            })
        
        elif action == "update":
            if not subscription_id or subscription_id not in subscriptions:
                return json.dumps({"success": False, "error": f"Subscription {subscription_id} not found"})
            
            if not subscription_data:
                return json.dumps({"success": False, "error": "subscription_data is required for update action"})
            
            # MODIFIED: Require only one approval
            if "fund_manager_approval" not in subscription_data:
                return json.dumps({"success": False, "error": "Missing required approval: fund_manager_approval"})
            
            bool_error = validate_boolean_field(subscription_data["fund_manager_approval"], "fund_manager_approval")
            if bool_error:
                return json.dumps({"success": False, "error": bool_error})
            
            # Update subscription record
            current_subscription = subscriptions[subscription_id]
            updated_subscription = current_subscription.copy()
            for key, value in subscription_data.items():
                if key != "fund_manager_approval":
                    updated_subscription[key] = value
            
            updated_subscription["updated_at"] = "2025-10-01T00:00:00"
            subscriptions[subscription_id] = updated_subscription
            
            return json.dumps({
                "success": True, "action": "update", "subscription_id": subscription_id,
                "message": f"Subscription {subscription_id} updated successfully.",
                "subscription_data": updated_subscription
            })
        
        elif action == "cancel":
            if not subscription_id or subscription_id not in subscriptions:
                return json.dumps({"success": False, "error": f"Subscription {subscription_id} not found"})
            
            # MODIFIED: Require only one approval
            if not subscription_data or "fund_manager_approval" not in subscription_data:
                return json.dumps({"success": False, "error": "fund_manager_approval is required for cancel action"})

            bool_error = validate_boolean_field(subscription_data["fund_manager_approval"], "fund_manager_approval")
            if bool_error:
                return json.dumps({"success": False, "error": bool_error})
            
            subscription = subscriptions[subscription_id]
            if subscription.get("status") == "cancelled":
                return json.dumps({"success": False, "error": "Subscription is already cancelled"})
            
            subscription["status"] = "cancelled"
            subscription["updated_at"] = "2025-10-01T00:00:00"
            
            return json.dumps({
                "success": True, "action": "cancel", "subscription_id": subscription_id,
                "message": f"Subscription {subscription_id} cancelled successfully.",
                "subscription_data": subscription
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        # MODIFIED: Entire get_info section updated to reflect single approval
        return {
            "type": "function",
            "function": {
                "name": "manipulate_subscription",
                "description": "Create, update, or cancel subscription records. All operations require Fund Manager approval.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create', 'update', or 'cancel'.",
                            "enum": ["create", "update", "cancel"]
                        },
                        "subscription_data": {
                            "type": "object",
                            "description": "Data for the subscription. Requires 'fund_manager_approval'. For 'create', also requires 'fund_id', 'investor_id', 'amount', etc.",
                            "properties": {
                                "fund_id": {"type": "string", "description": "Unique identifier of the fund."},
                                "investor_id": {"type": "string", "description": "Unique identifier of the investor."},
                                "amount": {"type": "string", "description": "Subscription amount (must be positive)."},
                                "request_assigned_to": {"type": "string", "description": "User ID assigned to the request."},
                                "request_date": {"type": "string", "description": "Date of the request in YYYY-MM-DD format."},
                                "status": {"type": "string", "description": "Status: 'pending', 'approved', or 'cancelled'."},
                                "approval_date": {"type": "string", "description": "Date of approval in YYYY-MM-DD format."},
                                "notify_investor": {"type": "boolean", "description": "Notify the investor of changes."},
                                "fund_manager_approval": {
                                    "type": "boolean",
                                    "description": "Fund Manager approval (True/False). Required for all operations."
                                }
                            }
                        },
                        "subscription_id": {
                            "type": "string",
                            "description": "Unique identifier of the subscription (required for 'update' and 'cancel')."
                        }
                    },
                    "required": ["action", "subscription_data"]
                }
            }
        }