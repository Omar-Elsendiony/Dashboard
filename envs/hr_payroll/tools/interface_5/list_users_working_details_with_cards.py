import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FetchWorkingDetailsUsersWithCards(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        role: str = None,
        status: str = None,
        locale: str = None,
        timezone: str = None
    ) -> str:
        users = data.get("users", {})
        workers = data.get("workers", {})
        contracts = data.get("contracts", {})
        virtual_cards = data.get("virtual_cards", {})

        results = []

        # If user_id is provided, directly fetch that user
        if user_id:
            user = users.get(user_id)
            if user:
                user_workers = [
                    {"worker_id": wid, **w}
                    for wid, w in workers.items()
                    if w.get("user_id") == user_id
                ]

                worker_ids = [w["worker_id"] for w in user_workers]
                user_contracts = [
                    {"contract_id": cid, **c}
                    for cid, c in contracts.items()
                    if c.get("worker_id") in worker_ids
                ]

                user_cards = [
                    {"card_id": cid, **c}
                    for cid, c in virtual_cards.items()
                    if c.get("user_id") == user_id
                ]

                results.append({
                    "user_id": user_id,
                    "user": user,
                    "workers": user_workers,
                    "contracts": user_contracts,
                    "virtual_cards": user_cards
                })

            return json.dumps(results)

        # Otherwise, fall back to filter-based lookup
        for uid, user in users.items():
            if email and user.get("email") != email:
                continue
            if first_name and user.get("first_name") != first_name:
                continue
            if last_name and user.get("last_name") != last_name:
                continue
            if role and user.get("role") != role:
                continue
            if status and user.get("status") != status:
                continue
            if locale and user.get("locale") != locale:
                continue
            if timezone and user.get("timezone") != timezone:
                continue

            user_workers = [
                {"worker_id": wid, **w}
                for wid, w in workers.items()
                if w.get("user_id") == uid
            ]

            worker_ids = [w["worker_id"] for w in user_workers]
            user_contracts = [
                {"contract_id": cid, **c}
                for cid, c in contracts.items()
                if c.get("worker_id") in worker_ids
            ]

            user_cards = [
                {"card_id": cid, **c}
                for cid, c in virtual_cards.items()
                if c.get("user_id") == uid
            ]

            results.append({
                "user_id": uid,
                "user": user,
                "workers": user_workers,
                "contracts": user_contracts,
                "virtual_cards": user_cards
            })

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_users_working_details_with_cards",
                "description": (
                    "Lists users with filters on user fields, returning full working details for each matched user. "
                    "This includes linked workers, their contracts, and any virtual cards issued to the user. "
                    "If `user_id` is provided, it will fetch that user directly and ignore other filters."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "Unique user ID to fetch a specific user's details directly"},
                        "email": {"type": "string", "description": "Filter by user email"},
                        "first_name": {"type": "string", "description": "Filter by user's first name"},
                        "last_name": {"type": "string", "description": "Filter by user's last name"},
                        "role": {"type": "string", "description": "Filter by user role"},
                        "status": {"type": "string", "description": "Filter by account status"},
                        "locale": {"type": "string", "description": "Filter by locale"},
                        "timezone": {"type": "string", "description": "Filter by timezone"}
                    },
                    "required": []
                }
            }
        }
