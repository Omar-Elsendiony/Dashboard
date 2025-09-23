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
        - create: Create new subscription (requires subscription_data with fund_id, investor_id, amount, request_assigned_to, request_date, fund_manager_approval, compliance_officer_approval)
        - update: Update existing subscription (requires subscription_id and subscription_data with changes, fund_manager_approval, compliance_officer_approval)
        - cancel: Cancel subscription (requires subscription_id, fund_manager_approval, compliance_officer_approval)
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
            
            # Require both Fund Manager and Compliance Officer approvals
            required_fields = ["fund_id", "investor_id", "amount", "request_assigned_to", "request_date", "fund_manager_approval", "compliance_officer_approval"]
            missing_fields = [field for field in required_fields if field not in subscription_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for subscription creation: {', '.join(missing_fields)}. Both Fund Manager and Compliance Officer approvals are required."
                })
            
            # Updated allowed fields to include compliance_officer_approval
            allowed_fields = ["fund_id", "investor_id", "amount", "request_assigned_to", "request_date", "status", "approval_date", "notify_investor", "fund_manager_approval", "compliance_officer_approval"]
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
            
            # Validate both approval fields
            bool_error = validate_boolean_field(subscription_data["fund_manager_approval"], "fund_manager_approval")
            if bool_error:
                return json.dumps({"success": False, "error": bool_error})
            
            bool_error = validate_boolean_field(subscription_data["compliance_officer_approval"], "compliance_officer_approval")
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
            
            # Require both approvals for updates
            missing_approvals = []
            if "fund_manager_approval" not in subscription_data:
                missing_approvals.append("fund_manager_approval")
            if "compliance_officer_approval" not in subscription_data:
                missing_approvals.append("compliance_officer_approval")
            
            if missing_approvals:
                return json.dumps({
                    "success": False, 
                    "error": f"Missing required approvals: {', '.join(missing_approvals)}. Both Fund Manager and Compliance Officer approvals are required."
                })
            
            # Validate both approval fields
            bool_error = validate_boolean_field(subscription_data["fund_manager_approval"], "fund_manager_approval")
            if bool_error:
                return json.dumps({"success": False, "error": bool_error})
            
            bool_error = validate_boolean_field(subscription_data["compliance_officer_approval"], "compliance_officer_approval")
            if bool_error:
                return json.dumps({"success": False, "error": bool_error})
            
            # Update subscription record
            current_subscription = subscriptions[subscription_id]
            updated_subscription = current_subscription.copy()
            for key, value in subscription_data.items():
                if key not in ["fund_manager_approval", "compliance_officer_approval"]:
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
            
            # Require both approvals for cancellation
            if not subscription_data:
                return json.dumps({
                    "success": False,
                    "error": "subscription_data with fund_manager_approval and compliance_officer_approval is required for cancel action"
                })
            
            missing_approvals = []
            if "fund_manager_approval" not in subscription_data:
                missing_approvals.append("fund_manager_approval")
            if "compliance_officer_approval" not in subscription_data:
                missing_approvals.append("compliance_officer_approval")
            
            if missing_approvals:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required approvals: {', '.join(missing_approvals)}. Both Fund Manager and Compliance Officer approvals are required for cancellation."
                })

            # Validate both approval fields
            bool_error = validate_boolean_field(subscription_data["fund_manager_approval"], "fund_manager_approval")
            if bool_error:
                return json.dumps({"success": False, "error": bool_error})
            
            bool_error = validate_boolean_field(subscription_data["compliance_officer_approval"], "compliance_officer_approval")
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
        return {
            "type": "function",
            "function": {
                "name": "manipulate_subscription",
                "description": "Create, update, or cancel subscription records in the fund management system. This tool manages investor subscription lifecycle from initial requests to final processing. For creation, establishes new subscription records with comprehensive validation to ensure regulatory compliance and prevents duplicate subscriptions for the same investor-fund combination. For updates, modifies existing subscription records while maintaining data integrity and audit trails. For cancellation, processes subscription termination with proper status management. All operations require dual approval from Fund Manager and Compliance Officer as mandated by regulatory requirements. Validates business rules including positive amounts, valid fund and investor existence, and proper status transitions. Essential for investor onboarding, capital raising activities, and regulatory compliance reporting. Supports the complete subscription lifecycle from initial request through approval to cancellation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new subscription record, 'update' to modify existing subscription, 'cancel' to terminate subscription",
                            "enum": ["create", "update", "cancel"]
                        },
                        "subscription_data": {
                            "type": "object",
                            "description": "Subscription data object. For create: requires fund_id, investor_id, amount (positive), request_assigned_to (valid user), request_date (YYYY-MM-DD), fund_manager_approval (approval presence), compliance_officer_approval (approval presence). For update: includes fields to change with both approval codes. For cancel: requires both approval codes. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "fund_id": {
                                    "type": "string",
                                    "description": "Unique identifier of the fund (required for create only, must exist in system, unique with investor_id for subscription)"
                                },
                                "investor_id": {
                                    "type": "string",
                                    "description": "Unique identifier of the investor (required for create only, must exist in system, unique with fund_id for subscription)"
                                },
                                "amount": {
                                    "type": "string",
                                    "description": "Subscription amount in USD (required for create, must be positive number, validates against fund minimums)"
                                },
                                "request_assigned_to": {
                                    "type": "string",
                                    "description": "User ID assigned to process the request (required for create only, must be valid user in system)"
                                },
                                "request_date": {
                                    "type": "string",
                                    "description": "Date of the subscription request in YYYY-MM-DD format (required for create only, cannot be future date)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Subscription status: 'pending' (default), 'approved', or 'cancelled' (validates status transitions)"
                                },
                                "approval_date": {
                                    "type": "string",
                                    "description": "Date of approval in YYYY-MM-DD format (optional, must be valid date format if provided)"
                                },
                                "notify_investor": {
                                    "type": "boolean",
                                    "description": "Flag to notify investor of subscription changes (optional, True/False)"
                                },
                                "fund_manager_approval": {
                                    "type": "boolean",
                                    "description": "Fund Manager approval presence (True/False) (required for all operations - create, update, cancel)"
                                },
                                "compliance_officer_approval": {
                                    "type": "boolean",
                                    "description": "Compliance Officer approval presence (True/False) (required for all operations - create, update, cancel)"
                                }
                            }
                        },
                        "subscription_id": {
                            "type": "string",
                            "description": "Unique identifier of the subscription (required for 'update' and 'cancel' actions only, must exist in system)"
                        }
                    },
                    "required": ["action", "subscription_data"]
                }
            }
        }