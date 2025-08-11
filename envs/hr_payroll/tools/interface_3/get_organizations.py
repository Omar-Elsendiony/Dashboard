import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetOrganizations(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        organization_id: str = None,
        name: str = None,
        country: str = None,
        timezone: str = None,
        city: str = None,
        zip: str = None,
        line1: str = None
    ) -> str:
        organizations = data.get("organizations", {})

        def matches(org_id: str, org: Dict[str, Any]) -> bool:
            if organization_id and org_id != organization_id:
                return False
            if name and name.lower() not in org.get("name", "").lower():
                return False
            if country and org.get("country") != country:
                return False
            if timezone and org.get("timezone") != timezone:
                return False
            if city and org.get("address", {}).get("city") != city:
                return False
            if zip and org.get("address", {}).get("zip") != zip:
                return False
            if line1 and line1.lower() not in org.get("address", {}).get("line1", "").lower():
                return False
            return True

        results = [
            {**org, "organization_id": org_id}
            for org_id, org in organizations.items()
            if matches(org_id, org)
        ]

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_organizations",
                "description": (
                    "Returns organizations matching any provided filter fields. "
                    "organization_id is the only unique field; all other filters allow partial or exact matching."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "organization_id": {
                            "type": "string",
                            "description": "Filter by exact organization ID"
                        },
                        "name": {
                            "type": "string",
                            "description": "Case-insensitive partial match for organization name"
                        },
                        "country": {
                            "type": "string",
                            "description": "Exact country name"
                        },
                        "timezone": {
                            "type": "string",
                            "description": "Exact timezone string"
                        },
                        "city": {
                            "type": "string",
                            "description": "Exact match for city name"
                        },
                        "zip": {
                            "type": "string",
                            "description": "Exact match for ZIP code"
                        },
                        "line1": {
                            "type": "string",
                            "description": "Case-insensitive partial match for address line1"
                        }
                    },
                    "required": []
                }
            }
        }
