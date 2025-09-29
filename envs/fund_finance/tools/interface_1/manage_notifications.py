import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManageNotifications(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, notification_data: Dict[str, Any] = None, notification_id: str = None) -> str:
        """
        Create or update notification records.
        
        Actions:
        - create: Create new notification (requires notification_data with email, type, class, optional reference_id)
        - update: Update existing notification (requires notification_id and notification_data with changes like status)
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
        
        # Access notifications data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for notifications"
            })
        
        notifications = data.get("notifications", {})
        
        if action == "create":
            if not notification_data:
                return json.dumps({
                    "success": False,
                    "error": "notification_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["email", "type", "class"]
            missing_fields = [field for field in required_fields if field not in notification_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for notification creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["email", "type", "class", "reference_id", "status"]
            invalid_fields = [field for field in notification_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for notification creation: {', '.join(invalid_fields)}"
                })
            
            # Validate enum fields
            valid_types = ["alert", "report", "reminder", "subscription_update"]
            if notification_data["type"] not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid type. Must be one of: {', '.join(valid_types)}"
                })
            
            valid_classes = ["funds", "investors", "portfolios", "trades", "invoices", "reports", "documents", "subscriptions", "commitments"]
            if notification_data["class"] not in valid_classes:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid class. Must be one of: {', '.join(valid_classes)}"
                })
            
            # Validate type-class combinations per policy
            notification_type = notification_data["type"]
            notification_class = notification_data["class"]
            
            valid_combinations = {
                "alert": ["funds", "investors", "portfolios", "trades", "invoices", "subscriptions", "commitments"],
                "report": ["funds", "investors", "portfolios", "reports", "documents"],
                "reminder": ["invoices", "subscriptions", "commitments"],
                "subscription_update": ["subscriptions", "commitments"]
            }
            
            if notification_class not in valid_combinations[notification_type]:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid type-class combination: {notification_type} notifications are not valid for {notification_class}. Valid classes for {notification_type}: {', '.join(valid_combinations[notification_type])}"
                })
            
            # Validate status if provided
            if "status" in notification_data:
                valid_statuses = ["pending", "sent", "failed"]
                if notification_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Basic email validation
            email = notification_data["email"]
            if "@" not in email or "." not in email.split("@")[-1]:
                return json.dumps({
                    "success": False,
                    "error": "Invalid email format"
                })
            
            new_notification_id = generate_id(notifications)
            
            # Create new notification record
            new_notification = {
                "notification_id": str(new_notification_id) if new_notification_id else None,
                "email": notification_data["email"],
                "type": notification_data["type"],
                "class": notification_data["class"],
                "reference_id": str(notification_data.get("reference_id")) if notification_data.get("reference_id") else None,
                "status": notification_data.get("status", "pending"),
                "sent_at": None,
                "created_at": "2025-10-01T12:00:00"
            }
            
            notifications[str(new_notification_id)] = new_notification
            
            return json.dumps({
                "success": True,
                "action": "create",
                "notification_id": str(new_notification_id) if new_notification_id else None,
                "message": f"Notification {new_notification_id} created successfully for {notification_data['email']}",
                "notification_data": new_notification
            })
        
        elif action == "update":
            if not notification_id:
                return json.dumps({
                    "success": False,
                    "error": "notification_id is required for update action"
                })
            
            if notification_id not in notifications:
                return json.dumps({
                    "success": False,
                    "error": f"Notification {notification_id} not found"
                })
            
            if not notification_data:
                return json.dumps({
                    "success": False,
                    "error": "notification_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["status", "sent_at"]
            invalid_fields = [field for field in notification_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for notification update: {', '.join(invalid_fields)}. Cannot update email, type, class, or reference_id."
                })
            
            if "status" in notification_data:
                valid_statuses = ["pending", "sent", "failed"]
                if notification_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            current_notification = notifications[notification_id]
            current_status = current_notification.get("status", "pending")
            new_status = notification_data.get("status")
            
            if new_status and current_status == "sent" and new_status in ["pending", "failed"]:
                return json.dumps({
                    "success": False,
                    "error": "Cannot change status from 'sent' to 'pending' or 'failed'"
                })
            
            if new_status == "sent" and current_status != "sent":
                notification_data["sent_at"] = "2025-10-01T12:00:00"
            
            updated_notification = current_notification.copy()
            for key, value in notification_data.items():
                updated_notification[key] = value
            
            notifications[notification_id] = updated_notification
            
            return json.dumps({
                "success": True,
                "action": "update",
                "notification_id": str(notification_id),
                "message": f"Notification {notification_id} updated successfully",
                "notification_data": updated_notification
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_notifications",
                "description": "Create or update notification records in the fund management system. This tool manages communication notifications for various fund management activities including alerts, reports, reminders, and subscription updates. For creation, establishes new notification records with comprehensive validation to ensure proper type-class combinations per regulatory requirements and prevents invalid notification configurations. For updates, modifies existing notification records while maintaining data integrity. Ensures proper email format validation and manages notification lifecycle from creation through delivery status tracking. Essential for regulatory compliance, investor communications, and operational workflow management.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' or 'update'",
                            "enum": ["create", "update"]
                        },
                        "notification_data": {
                            "type": "object",
                            "description": "Notification data object. For create: requires email (valid format), type (notification category), class (business entity type), with optional reference_id (linked entity) and status (defaults to 'pending'). For update: fields to change (core fields cannot be updated). Must follow type-class combination rules per policy. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "email": {
                                    "type": "string",
                                    "description": "Recipient email address (required for create only, cannot be updated)"
                                },
                                "type": {
                                    "type": "string",
                                    "description": "Notification type (required for create only, cannot be updated)",
                                    "enum": ["alert", "report", "reminder", "subscription_update"]
                                },
                                "class": {
                                    "type": "string",
                                    "description": "Notification class/category (required for create only, cannot be updated)",
                                    "enum": ["funds", "investors", "portfolios", "trades", "invoices", "reports", "documents", "subscriptions", "commitments"]
                                },
                                "reference_id": {
                                    "type": "string",
                                    "description": "Optional reference to related record (for create only, cannot be updated)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Notification status (defaults to 'pending' for new notifications)",
                                    "enum": ["pending", "sent", "failed"]
                                },
                                "sent_at": {
                                    "type": "string",
                                    "description": "Timestamp when notification was sent (automatically set when status changes to 'sent')"
                                }
                            }
                        },
                        "notification_id": {
                            "type": "string",
                            "description": "Unique identifier of the notification (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
