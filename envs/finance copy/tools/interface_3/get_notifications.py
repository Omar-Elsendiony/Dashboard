import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_notifications(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        email: Optional[str] = None,
        status: Optional[str] = None,
        type: Optional[str] = None,
        class_: Optional[str] = None,
        reference_id: Optional[str] = None
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

        # Validate class/reference_id pairing
        if (class_ is None) ^ (reference_id is None):
            raise ValueError("Both 'class' and 'reference_id' must be provided together")

        # If class/reference_id provided, validate class
        valid_classes = {
            "funds","investors","portfolios","trades","invoices",
            "reports","documents","subscriptions","commitments",
            "tickets","users","portfolio_holdings"
        }
        if class_ is not None and class_ not in valid_classes:
            raise ValueError(f"Invalid class. Must be one of {valid_classes}")

        for notif in notifications.values():
            # Filter by email
            if email is not None and notif.get("email") != email:
                continue
            # Filter by status
            if status is not None and notif.get("status") != status:
                continue
            # Filter by type
            if type is not None and notif.get("type") != type:
                continue
            # Filter by class & reference_id
            if class_ is not None:
                if notif.get("class") != class_ or str(notif.get("reference_id")) != str(reference_id):
                    continue

            results.append(notif)

        # Sort by created_at descending
        results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_notifications",
                "description": (
                    "Retrieve notifications filtered by optional criteria. "
                    "You can filter by email, status, type, and/or specify both class_ and reference_id."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "Filter by recipient email address"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by notification status (pending, sent, failed)"
                        },
                        "type": {
                            "type": "string",
                            "description": "Filter by notification type (alert, report, reminder, subscription_update)"
                        },
                        "class_": {
                            "type": "string",
                            "description": (
                                "Filter by entity class: funds, investors, portfolios, trades, invoices, "
                                "reports, documents, subscriptions, commitments, tickets, users, or portfolio_holdings"
                            )
                        },
                        "reference_id": {
                            "type": "string",
                            "description": "Filter by the related record ID; must be used together with 'class_'"
                        }
                    },
                    "required": []
                }
            }
        }