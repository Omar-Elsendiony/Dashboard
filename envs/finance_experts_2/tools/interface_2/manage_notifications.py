import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManageNotifications(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, notification_data: Dict[str, Any] = None, notification_id: str = None) -> str:
        """
        Create or update notification records.
        
        Actions:
        - create: Create new notification (requires notification_data with email, type, class, approval_code, optional reference_id)
        - update: Update existing notification (requires notification_id and notification_data with changes like status, approval_code)
        """
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
            required_fields = ["email", "type", "class", "approval_code"]
            missing_fields = [field for field in required_fields if field not in notification_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for notification creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["email", "type", "class", "reference_id", "status", "approval_code"]
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
            
            # Validate status if provided
            if "status" in notification_data:
                valid_statuses = ["pending", "sent", "failed"]
                if notification_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Generate new notification ID
            existing_ids = [int(nid) for nid in notifications.keys() if nid.isdigit()]
            new_notification_id = str(max(existing_ids, default=0) + 1)
            
            # Create new notification record
            new_notification = {
                "notification_id": new_notification_id,
                "email": notification_data["email"],
                "type": notification_data["type"],
                "class": notification_data["class"],
                "reference_id": notification_data.get("reference_id"),
                "status": notification_data.get("status", "pending"),
                "sent_at": None,
                "created_at": "2025-10-01T12:00:00"
            }
            
            notifications[new_notification_id] = new_notification
            
            return json.dumps({
                "success": True,
                "action": "create",
                "notification_id": new_notification_id,
                "message": f"Notification {new_notification_id} created successfully",
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
            allowed_update_fields = ["status", "sent_at", "approval_code"]
            invalid_fields = [field for field in notification_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for notification update: {', '.join(invalid_fields)}"
                })
            
            # Validate status if provided
            if "status" in notification_data:
                valid_statuses = ["pending", "sent", "failed"]
                if notification_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Update notification record
            updated_notification = notifications[notification_id].copy()
            for key, value in notification_data.items():
                if key not in ["approval_code"]:  # Skip approval_code from being stored
                    updated_notification[key] = value
            
            notifications[notification_id] = updated_notification
            
            return json.dumps({
                "success": True,
                "action": "update",
                "notification_id": notification_id,
                "message": f"Notification {notification_id} updated successfully",
                "notification_data": updated_notification
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_notifications",
                "description": "Create or update notification records in the fund management system. For creation, requires email, type (alert/report/reminder/subscription_update), class (funds/investors/portfolios/trades/invoices/reports/documents/subscriptions/commitments), and approval_code, with optional reference_id and status (defaults to 'pending'). For updates, requires notification_id and fields to change with approval_code.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' or 'update'"
                        },
                        "notification_data": {
                            "type": "object",
                            "description": "Notification data. For create: email, type, class, approval_code, optional reference_id, status. For update: fields to change with approval_code",
                            "additionalProperties": True
                        },
                        "notification_id": {
                            "type": "string",
                            "description": "Notification ID (required for update action)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }