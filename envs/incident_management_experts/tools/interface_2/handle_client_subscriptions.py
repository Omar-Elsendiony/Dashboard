import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class HandleClientSubscriptions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, subscription_data: Dict[str, Any] = None, subscription_id: str = None) -> str:
        """
        Create or update client subscription records.
        
        Actions:
        - create: Create new subscription record (requires subscription_data with client_id, product_id, subscription_type, start_date, sla_tier, rto_hours, status)
        - update: Update existing subscription record (requires subscription_id and subscription_data with changes)
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
        
        # Access client_subscriptions data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for client_subscriptions"
            })
        
        client_subscriptions = data.get("client_subscriptions", {})
        
        if action == "create":
            if not subscription_data:
                return json.dumps({
                    "success": False,
                    "error": "subscription_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["client_id", "product_id", "subscription_type", "start_date", "sla_tier", "rto_hours", "status"]
            missing_fields = [field for field in required_fields if field not in subscription_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for subscription creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["client_id", "product_id", "subscription_type", "start_date", "end_date", "sla_tier", "rto_hours", "status"]
            invalid_fields = [field for field in subscription_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for subscription creation: {', '.join(invalid_fields)}"
                })
            
            # Validate enum fields
            valid_subscription_types = ["full_service", "limited_service", "trial", "custom"]
            if subscription_data["subscription_type"] not in valid_subscription_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid subscription_type '{subscription_data['subscription_type']}'. Must be one of: {', '.join(valid_subscription_types)}"
                })
            
            valid_sla_tiers = ["premium", "standard", "basic"]
            if subscription_data["sla_tier"] not in valid_sla_tiers:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid sla_tier '{subscription_data['sla_tier']}'. Must be one of: {', '.join(valid_sla_tiers)}"
                })
            
            valid_statuses = ["active", "expired", "cancelled", "suspended"]
            if subscription_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status '{subscription_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                })
            
            # Validate RTO hours
            rto_hours = subscription_data["rto_hours"]
            if not isinstance(rto_hours, int) or rto_hours <= 0:
                return json.dumps({
                    "success": False,
                    "error": "rto_hours must be a positive integer"
                })
            
            # Validate date logic if end_date is provided
            if "end_date" in subscription_data and subscription_data["end_date"]:
                if subscription_data["end_date"] <= subscription_data["start_date"]:
                    return json.dumps({
                        "success": False,
                        "error": "end_date must be after start_date"
                    })
            
            # Check for duplicate active subscription for same client and product
            client_id = subscription_data["client_id"]
            product_id = subscription_data["product_id"]
            for existing_subscription in client_subscriptions.values():
                if (existing_subscription.get("client_id") == client_id and 
                    existing_subscription.get("product_id") == product_id and
                    existing_subscription.get("status") == "active"):
                    return json.dumps({
                        "success": False,
                        "error": f"Active subscription already exists for client {client_id} and product {product_id}"
                    })
            
            # Generate new subscription ID
            new_subscription_id = generate_id(client_subscriptions)
            
            # Create new subscription record
            new_subscription = {
                "subscription_id": str(new_subscription_id),
                "client_id": str(subscription_data["client_id"]),
                "product_id": str(subscription_data["product_id"]),
                "subscription_type": subscription_data["subscription_type"],
                "start_date": subscription_data["start_date"],
                "end_date": subscription_data.get("end_date"),
                "sla_tier": subscription_data["sla_tier"],
                "rto_hours": subscription_data["rto_hours"],
                "status": subscription_data["status"],
                "created_at": "2025-10-01T00:00:00",
                "updated_at": "2025-10-01T00:00:00"
            }
            
            client_subscriptions[str(new_subscription_id)] = new_subscription
            
            return json.dumps({
                "success": True,
                "action": "create",
                "subscription_id": str(new_subscription_id),
                "subscription_data": new_subscription
            })
        
        elif action == "update":
            if not subscription_id:
                return json.dumps({
                    "success": False,
                    "error": "subscription_id is required for update action"
                })
            
            if subscription_id not in client_subscriptions:
                return json.dumps({
                    "success": False,
                    "error": f"Subscription record {subscription_id} not found"
                })
            
            if not subscription_data:
                return json.dumps({
                    "success": False,
                    "error": "subscription_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["subscription_type", "end_date", "sla_tier", "rto_hours", "status"]
            invalid_fields = [field for field in subscription_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for subscription update: {', '.join(invalid_fields)}. Cannot update client_id, product_id, or start_date."
                })
            
            # Validate enum fields if provided
            if "subscription_type" in subscription_data:
                valid_subscription_types = ["full_service", "limited_service", "trial", "custom"]
                if subscription_data["subscription_type"] not in valid_subscription_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid subscription_type '{subscription_data['subscription_type']}'. Must be one of: {', '.join(valid_subscription_types)}"
                    })
            
            if "sla_tier" in subscription_data:
                valid_sla_tiers = ["premium", "standard", "basic"]
                if subscription_data["sla_tier"] not in valid_sla_tiers:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid sla_tier '{subscription_data['sla_tier']}'. Must be one of: {', '.join(valid_sla_tiers)}"
                    })
            
            if "status" in subscription_data:
                valid_statuses = ["active", "expired", "cancelled", "suspended"]
                if subscription_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status '{subscription_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Validate RTO hours if provided
            if "rto_hours" in subscription_data:
                rto_hours = subscription_data["rto_hours"]
                if not isinstance(rto_hours, int) or rto_hours <= 0:
                    return json.dumps({
                        "success": False,
                        "error": "rto_hours must be a positive integer"
                    })
            
            # Get current subscription data
            current_subscription = client_subscriptions[subscription_id].copy()
            
            # Validate date logic if end_date is being updated
            if "end_date" in subscription_data and subscription_data["end_date"]:
                if subscription_data["end_date"] <= current_subscription["start_date"]:
                    return json.dumps({
                        "success": False,
                        "error": "end_date must be after start_date"
                    })
            
            # Check for duplicate active subscription if status is being changed to active
            if "status" in subscription_data and subscription_data["status"] == "active":
                client_id = current_subscription["client_id"]
                product_id = current_subscription["product_id"]
                for existing_id, existing_subscription in client_subscriptions.items():
                    if (existing_id != subscription_id and
                        existing_subscription.get("client_id") == client_id and 
                        existing_subscription.get("product_id") == product_id and
                        existing_subscription.get("status") == "active"):
                        return json.dumps({
                            "success": False,
                            "error": f"Active subscription already exists for client {client_id} and product {product_id}"
                        })
            
            # Update subscription record
            updated_subscription = current_subscription.copy()
            for key, value in subscription_data.items():
                updated_subscription[key] = value
            
            updated_subscription["updated_at"] = "2025-10-01T00:00:00"
            client_subscriptions[subscription_id] = updated_subscription
            
            return json.dumps({
                "success": True,
                "action": "update",
                "subscription_id": str(subscription_id),
                "subscription_data": updated_subscription
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_client_subscriptions",
                "description": "Create or update client subscription records in the incident management system. This tool manages client subscriptions to various products and services, including service levels, SLA tiers, and recovery time objectives. For creation, establishes new subscription records with comprehensive validation to ensure proper configuration and prevent duplicate active subscriptions for the same client-product combination. For updates, modifies existing subscription records while maintaining data integrity. Validates subscription types, SLA tiers, status values, and date logic according to business requirements. Essential for client relationship management, service delivery, and SLA compliance tracking.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new subscription record, 'update' to modify existing subscription record",
                            "enum": ["create", "update"]
                        },
                        "subscription_data": {
                            "type": "object",
                            "description": "Subscription data object. For create: requires client_id, product_id, subscription_type, start_date (YYYY-MM-DD), sla_tier, rto_hours (positive integer), status, with optional end_date (YYYY-MM-DD, must be after start_date). For update: includes subscription fields to change (client_id, product_id, start_date cannot be updated). SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "client_id": {
                                    "type": "string",
                                    "description": "Reference to client record (required for create only, cannot be updated)"
                                },
                                "product_id": {
                                    "type": "string",
                                    "description": "Reference to product record (required for create only, cannot be updated)"
                                },
                                "subscription_type": {
                                    "type": "string",
                                    "description": "Type of subscription: 'full_service', 'limited_service', 'trial', 'custom'",
                                    "enum": ["full_service", "limited_service", "trial", "custom"]
                                },
                                "start_date": {
                                    "type": "string",
                                    "description": "Subscription start date in YYYY-MM-DD format (required for create only, cannot be updated)"
                                },
                                "end_date": {
                                    "type": "string",
                                    "description": "Subscription end date in YYYY-MM-DD format (optional, must be after start_date)"
                                },
                                "sla_tier": {
                                    "type": "string",
                                    "description": "Service level agreement tier: 'premium', 'standard', 'basic'",
                                    "enum": ["premium", "standard", "basic"]
                                },
                                "rto_hours": {
                                    "type": "integer",
                                    "description": "Recovery Time Objective in hours (positive integer)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Subscription status: 'active', 'expired', 'cancelled', 'suspended' (only one active subscription per client-product combination)",
                                    "enum": ["active", "expired", "cancelled", "suspended"]
                                }
                            }
                        },
                        "subscription_id": {
                            "type": "string",
                            "description": "Unique identifier of the subscription record (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
