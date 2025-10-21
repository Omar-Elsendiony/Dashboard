import json
import re
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageNotificationOperations(Tool):
    
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manages notification operations including creation and status updates.
        """
        
        # --- Utility Functions ---
        def generate_id(table: Dict[str, Any]) -> int:
            """Utility to generate a new sequential ID for the notifications table."""
            if not table:
                return 8001
            return max(int(k) for k in table.keys()) + 1

        def validate_email_format(email: str) -> bool:
            """Basic email format validation."""
            if not email:
                return False
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(pattern, email))
        
        valid_operations = ["create_notification", "update_notification_status"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "notification_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "notification_id": None,
                "message": "Invalid data format for notification operations"
            })
        
        notifications = data.get("notifications", {})
        users = data.get("users", {})

        # --- Notification Creation (create_notification) ---
        if operation_type == "create_notification":
            required_fields = ["sender_user_id", "notification_type", "reference_type", "subject"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "notification_id": None,
                    "message": f"Missing mandatory fields: {', '.join(missing_fields)}"
                })

            # 1. Validate sender user exists and is active
            sender_user = users.get(str(kwargs["sender_user_id"]))
            if not sender_user or sender_user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "notification_id": None,
                    "message": "Halt: Sender user not found or inactive"
                })

            # 2. Validate recipient information - either recipient_user_id OR recipient_email must be provided
            recipient_user_id = kwargs.get("recipient_user_id")
            recipient_email = kwargs.get("recipient_email")
            
            if not recipient_user_id and not recipient_email:
                return json.dumps({
                    "success": False,
                    "notification_id": None,
                    "message": "Halt: Either recipient_user_id or recipient_email must be provided"
                })

            # 2.1. If recipient_user_id is provided, validate user exists and is active
            if recipient_user_id:
                recipient_user = users.get(str(recipient_user_id))
                if not recipient_user or recipient_user.get("employment_status") != "active":
                    return json.dumps({
                        "success": False,
                        "notification_id": None,
                        "message": "Halt: Recipient user not found or inactive"
                    })
                
                user_email = recipient_user.get("email")
                if not user_email:
                    return json.dumps({
                        "success": False,
                        "notification_id": None,
                        "message": "Halt: Recipient user has no email address"
                    })
                
                # If both recipient_user_id and recipient_email are provided, check if they match
                if recipient_email:
                    if user_email.lower() != recipient_email.lower():
                        return json.dumps({
                            "success": False,
                            "notification_id": None,
                            "message": f"Halt: Recipient email '{recipient_email}' does not match the user's email '{user_email}'. Either leave recipient_email out or ensure they match"
                        })
                    # Use the provided recipient_email (they match)
                    recipient_email = recipient_email
                else:
                    # Use recipient user's email
                    recipient_email = user_email
            # 2.2. If only recipient_email is provided, validate email format
            else:
                if not validate_email_format(recipient_email):
                    return json.dumps({
                        "success": False,
                        "notification_id": None,
                        "message": "Halt: Invalid recipient_email format"
                    })
                if len(recipient_email) > 320:
                    return json.dumps({
                        "success": False,
                        "notification_id": None,
                        "message": "Halt: Recipient email cannot exceed 320 characters"
                    })

            # 3. Validate notification_type enum
            valid_notification_types = [
                "application_acknowledgment", "interview_scheduled", "offer_issued", 
                "onboarding_welcome", "payslip_released", "payment_processed", 
                "benefits_enrollment", "payroll_query_update", "exit_confirmation", 
                "document_request", "other"
            ]
            if kwargs["notification_type"] not in valid_notification_types:
                return json.dumps({
                    "success": False,
                    "notification_id": None,
                    "message": f"Invalid notification_type. Must be one of: {', '.join(valid_notification_types)}"
                })

            # 4. Validate reference_type enum
            valid_reference_types = [
                "application", "interview", "offer", "employee", "payroll", 
                "benefit", "document", "exit"
            ]
            if kwargs["reference_type"] not in valid_reference_types:
                return json.dumps({
                    "success": False,
                    "notification_id": None,
                    "message": f"Halt: Invalid reference_type. Must be one of: {', '.join(valid_reference_types)}"
                })
            
            # 4.1. Validate reference_id if provided
            reference_id = kwargs.get("reference_id")
            if reference_id is not None and (not isinstance(reference_id, str) or len(reference_id.strip()) == 0):
                return json.dumps({
                    "success": False,
                    "notification_id": None,
                    "message": "Halt: reference_id must be a non-empty string if provided"
                })

            # 5. Validate subject length
            subject = kwargs["subject"]
            if not subject or len(subject.strip()) == 0:
                return json.dumps({
                    "success": False,
                    "notification_id": None,
                    "message": "Subject cannot be empty"
                })
            if len(subject) > 255:
                return json.dumps({
                    "success": False,
                    "notification_id": None,
                    "message": "Subject cannot exceed 255 characters"
                })


            # 7. Create Notification
            new_notification_id = generate_id(notifications)
            timestamp = "2025-10-10T12:00:00"

            new_notification = {
                "notification_id": str(new_notification_id),
                "recipient_user_id": str(recipient_user_id) if recipient_user_id else None,
                "sender_user_id": str(kwargs["sender_user_id"]),
                "recipient_email": recipient_email,
                "notification_type": kwargs["notification_type"],
                "reference_type": kwargs["reference_type"],
                "reference_id": reference_id,
                "subject": subject.strip(),
                "notification_status": "pending",
                "sent_at": None,
                "failed_reason": None,
                "created_at": timestamp
            }
            
            notifications[str(new_notification_id)] = new_notification
            
            return json.dumps({
                "success": True,
                "notification_id": str(new_notification_id),
                "message": f"Notification {new_notification_id} created successfully",
                "notification_data": new_notification
            })

        # --- Notification Status Update (update_notification_status) ---
        elif operation_type == "update_notification_status":
            required_fields = ["notification_id", "notification_status", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "notification_id": None,
                    "message": f"Missing mandatory fields: {', '.join(missing_fields)}"
                })

            notification_id_str = str(kwargs["notification_id"])
            notification = notifications.get(notification_id_str)
            
            # 1. Verify notification exists
            if not notification:
                return json.dumps({
                    "success": False,
                    "notification_id": notification_id_str,
                    "message": "Halt: Notification not found"
                })

            # 2. Validate user authorization
            user = users.get(str(kwargs["user_id"]))
            if not user or user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "notification_id": notification_id_str,
                    "message": "Halt: User not found or inactive"
                })
            
            # 2.1. Validate that user has permission to update notification status
            # For now, any active user can update notification status, but this could be restricted
            # based on business rules (e.g., only sender, recipient, or system admins)

            # 3. Validate notification_status enum
            valid_statuses = ["pending", "sent", "failed", "bounced"]
            if kwargs["notification_status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "notification_id": notification_id_str,
                    "message": f"Invalid notification_status. Must be one of: {', '.join(valid_statuses)}"
                })

            # 4. Validate status transitions
            current_status = notification.get("notification_status")
            new_status = kwargs["notification_status"]
            
            # Define valid status transitions
            valid_transitions = {
                "pending": ["sent", "failed", "bounced"],
                "sent": ["bounced"],  # Can bounce after being sent
                "failed": ["pending"],  # Can retry
                "bounced": []  # Terminal state
            }
            
            if new_status not in valid_transitions.get(current_status, []):
                return json.dumps({
                    "success": False,
                    "notification_id": notification_id_str,
                    "message": f"Invalid status transition from '{current_status}' to '{new_status}'"
                })

            # 5. Validate failed_reason for failed/bounced status
            if new_status in ["failed", "bounced"]:
                failed_reason = kwargs.get("failed_reason")
                if not failed_reason or len(failed_reason.strip()) == 0:
                    return json.dumps({
                        "success": False,
                        "notification_id": notification_id_str,
                        "message": f"Halt: failed_reason is required when status is '{new_status}'"
                    })
            
            # 6. Update notification status
            notification["notification_status"] = new_status
            
            # Set sent_at timestamp if status is being changed to 'sent'
            if new_status == "sent":
                notification["sent_at"] = "2025-10-10T12:00:00"
                notification["failed_reason"] = None
            elif new_status in ["failed", "bounced"]:
                notification["failed_reason"] = kwargs.get("failed_reason", "No reason provided")
            
            return json.dumps({
                "success": True,
                "notification_id": notification_id_str,
                "message": f"Notification {notification_id_str} status updated to '{new_status}' successfully"
            })

        return json.dumps({
            "success": False,
            "notification_id": None,
            "message": "Unhandled operation type"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_notification_operations",
                "description": "Manages notification operations in the HR talent management system. 'create_notification' establishes new notification records with comprehensive validation of sender users, notification types (application_acknowledgment, interview_scheduled, offer_issued, onboarding_welcome, payslip_released, payment_processed, benefits_enrollment, payroll_query_update, exit_confirmation, document_request, other), reference types (application, interview, offer, employee, payroll, benefit, document, exit), and subject content. Supports both internal notifications (via recipient_user_id) and external notifications (via recipient_email). When both recipient_user_id and recipient_email are provided, validates that the emails match. Validates email formats, user existence and active status, and enforces proper notification categorization. 'update_notification_status' manages notification lifecycle by updating status from pending to sent/failed/bounced with proper status transition validation. Essential for communication tracking, audit trails, and ensuring proper notification delivery throughout the employee lifecycle including application acknowledgments, interview scheduling, offer issuance, onboarding welcome messages, payslip releases, payment confirmations, benefits enrollment notifications, and exit confirmations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation: 'create_notification' to create new notification record, 'update_notification_status' to update notification delivery status",
                            "enum": ["create_notification", "update_notification_status"]
                        },
                        "recipient_user_id": {
                            "type": "string",
                            "description": "User ID of the notification recipient (optional for create_notification, must exist and be active if provided. If both recipient_user_id and recipient_email are provided, the emails must match)"
                        },
                        "sender_user_id": {
                            "type": "string",
                            "description": "User ID of the notification sender (required for create_notification, must exist and be active)"
                        },
                        "notification_type": {
                            "type": "string",
                            "description": "Type of notification being sent (required for create_notification)",
                            "enum": ["application_acknowledgment", "interview_scheduled", "offer_issued", "onboarding_welcome", "payslip_released", "payment_processed", "benefits_enrollment", "payroll_query_update", "exit_confirmation", "document_request", "other"]
                        },
                        "reference_type": {
                            "type": "string",
                            "description": "Type of entity this notification references (required for create_notification)",
                            "enum": ["application", "interview", "offer", "employee", "payroll", "benefit", "document", "exit"]
                        },
                        "reference_id": {
                            "type": "string",
                            "description": "ID of the referenced entity (optional for create_notification)"
                        },
                        "subject": {
                            "type": "string",
                            "description": "Notification subject line (required for create_notification, max 255 characters)"
                        },
                        "recipient_email": {
                            "type": "string",
                            "description": "Recipient email address (optional for create_notification, must be provided if recipient_user_id is not provided, must be valid format if provided. If both recipient_user_id and recipient_email are provided, the emails must match)"
                        },
                        "notification_id": {
                            "type": "string",
                            "description": "Notification ID (required for update_notification_status, must exist)"
                        },
                        "notification_status": {
                            "type": "string",
                            "description": "New notification status (required for update_notification_status)",
                            "enum": ["pending", "sent", "failed", "bounced"]
                        },
                        "user_id": {
                            "type": "string",
                            "description": "User ID performing the status update (required for update_notification_status, must exist and be active)"
                        },
                        "failed_reason": {
                            "type": "string",
                            "description": "Reason for notification failure (optional for update_notification_status, used when status is 'failed' or 'bounced')"
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }
