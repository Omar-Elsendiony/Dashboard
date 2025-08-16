import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class retrieve_notifications(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        email: Optional[str] = None,
        type: Optional[str] = None,
        class_: Optional[str] = None,
        reference_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> str:
        notifications = data.get("notifications", {})
        results = []

        # Validate status if provided
        valid_statuses = {"pending", "sent", "failed"}
        if status is not None and status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")

        # Validate type if provided
        valid_types = {"alert", "report", "reminder", "subscription_update"}
        if type is not None and type not in valid_types:
            raise ValueError(f"Invalid type. Must be one of {valid_types}")

        # Validate class if provided
        valid_classes = {
            "funds","investors","portfolios","trades","invoices",
            "reports","documents","subscriptions","commitments",
            "tickets","users","portfolio_holdings"
        }
        if class_ is not None and class_ not in valid_classes:
            raise ValueError(f"Invalid class. Must be one of {valid_classes}")

        for notif in notifications.values():
            if email is not None and notif.get("email") != email:
                continue
            if type is not None and notif.get("type") != type:
                continue
            if class_ is not None and notif.get("class") != class_:
                continue
            if reference_id is not None and str(notif.get("reference_id")) != str(reference_id):
                continue
            if status is not None and notif.get("status") != status:
                continue
            results.append(notif)

        # Sort by creation timestamp descending
        results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_notifications",
                "description": (
                    "Retrieve notifications filtered by optional parameters: "
                    "email, type, class, reference_id, or status."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "Filter by recipient email"
                        },
                        "type": {
                            "type": "string",
                            "description": "Filter by notification type (alert, report, reminder, subscription_update)"
                        },
                        "class_": {
                            "type": "string",
                            "description": "Filter by entity class"
                        },
                        "reference_id": {
                            "type": "string",
                            "description": "Filter by related record ID"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by notification status (pending, sent, failed)"
                        }
                    },
                    "required": []
                }
            }
        }