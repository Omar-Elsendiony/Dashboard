import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RegisterNewOrganization(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        name: str,
        timezone: str,
        region: str,
        address: Dict[str, str]
    ) -> str:
        orgs = data.setdefault("organizations", {})

        # Prevent duplicate name + region + address
        for org in orgs.values():
            if (
                org.get("name", "").lower() == name.lower() and
                org.get("country", "").lower() == region.lower() and
                org.get("address", {}) == address
            ):
                raise ValueError("Organization with same name, region, and address already exists")

        org_id = str(uuid.uuid4())
        orgs[org_id] = {
            "name": name,
            "country": region,
            "timezone": timezone,
            "address": {
                "line1": address.get("line1", ""),
                "city": address.get("city", ""),
                "zip": address.get("zip", "")
            }
        }

        return json.dumps({
            "organization_id": org_id,
            **orgs[org_id]
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "register_new_organization",
                "description": "Registers a new organization with timezone, region, and detailed address",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Organization name"
                        },
                        "timezone": {
                            "type": "string",
                            "description": "Timezone of the organization"
                        },
                        "region": {
                            "type": "string",
                            "description": "Region or country of operation"
                        },
                        "address": {
                            "type": "object",
                            "description": "Address of the organization",
                            "properties": {
                                "line1": {"type": "string"},
                                "city": {"type": "string"},
                                "zip": {"type": "string"}
                            },
                            "required": ["line1", "city", "zip"]
                        }
                    },
                    "required": ["name", "timezone", "region", "address"]
                }
            }
        }
