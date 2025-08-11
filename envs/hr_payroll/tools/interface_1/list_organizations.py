import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListOrganizations(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str = None,
        worker_id: str = None,
        name: str = None,
        country: str = None,
        timezone: str = None,
        address_line1: str = None,
        address_city: str = None,
        address_zip: str = None
    ) -> str:
        workers = data.get("workers", {})
        organizations = data.get("organizations", {})

        # Resolve user_id if worker_id is given
        if worker_id:
            if worker_id not in workers:
                raise ValueError("Worker not found for the given worker_id")
            resolved_user_id = workers[worker_id].get("user_id")
            if user_id and user_id != resolved_user_id:
                raise ValueError("Provided user_id does not match worker_id")
            user_id = resolved_user_id

        # If user_id is present, limit org_ids to those associated with the user
        org_ids = None
        if user_id:
            org_ids = {
                w["organization_id"]
                for w in workers.values()
                if w.get("user_id") == user_id
            }

        def match(org):
            if name and name.lower() not in org.get("name", "").lower():
                return False
            if country and org.get("country") != country:
                return False
            if timezone and org.get("timezone") != timezone:
                return False
            address = org.get("address", {})
            if address_line1 and address.get("line1") != address_line1:
                return False
            if address_city and address.get("city") != address_city:
                return False
            if address_zip and address.get("zip") != address_zip:
                return False
            return True

        # Apply filters
        matched_orgs = [
            {**org, "organization_id": oid}
            for oid, org in organizations.items()
            if (org_ids is None or oid in org_ids) and match(org)
        ]


        return json.dumps(matched_orgs)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_organizations",
                "description": "Returns organizations associated with a user or worker, optionally filtered by organization fields like name, country, timezone, or address.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user whose associated organizations are to be listed"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "The ID of the worker (used to resolve user_id if user_id is not provided)"
                        },
                        "name": {
                            "type": "string",
                            "description": "Optional name filter (partial match)"
                        },
                        "country": {
                            "type": "string",
                            "description": "Optional country filter"
                        },
                        "timezone": {
                            "type": "string",
                            "description": "Optional timezone filter"
                        },
                        "address_line1": {
                            "type": "string",
                            "description": "Optional filter for address line1"
                        },
                        "address_city": {
                            "type": "string",
                            "description": "Optional filter for address city"
                        },
                        "address_zip": {
                            "type": "string",
                            "description": "Optional filter for address zip"
                        }
                    },
                    "required": []
                }
            }
        }
