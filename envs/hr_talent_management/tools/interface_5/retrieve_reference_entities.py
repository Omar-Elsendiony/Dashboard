import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool


class RetrieveReferenceEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Optional[Dict[str, Any]] = None) -> str:
        """
        Discover and retrieve reference entities including users, locations, and departments.

        entity_type: "users" | "locations" | "departments"
        filters: optional dict with exact-match filtering
        Returns: {"entities": list, "count": int, "message": str}
        """

        if entity_type not in ["users", "locations", "departments"]:
            return json.dumps({
                "entities": [],
                "count": 0,
                "message": f"Invalid entity_type '{entity_type}'. Must be 'users', 'locations', or 'departments'"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "entities": [],
                "count": 0,
                "message": f"Invalid data format for {entity_type}"
            })

        def apply_exact_filters(record: Dict[str, Any], exact_filter_keys: List[str], filters_obj: Dict[str, Any]) -> bool:
            for key in exact_filter_keys:
                if key in filters_obj:
                    if record.get(key) != filters_obj[key]:
                        return False
            return True

        results: List[Dict[str, Any]] = []

        if entity_type == "users":
            users = data.get("users", {})

            # Supported user filters
            user_exact_keys = [
                "user_id", "first_name", "last_name", "email", "phone_number",
                "role", "employment_status"
            ]

            for user_id, user in users.items():
                record = {**user}

                if filters:
                    if not apply_exact_filters(record, user_exact_keys, filters):
                        continue

                # ensure id present as string
                record["user_id"] = str(user_id)
                results.append(record)

            return json.dumps({
                "success": True,
                "entity_type": "users",
                "count": len(results),
                "entities": results,
                "filters_applied": filters or {}
            })

        if entity_type == "locations":
            locations = data.get("locations", {})

            # Supported location filters
            location_exact_keys = [
                "location_id", "city_name", "country", "status"
            ]

            for location_id, location in locations.items():
                record = {**location}

                if filters:
                    if not apply_exact_filters(record, location_exact_keys, filters):
                        continue

                # ensure id present as string
                record["location_id"] = str(location_id)
                results.append(record)

            return json.dumps({
                "success": True,
                "entity_type": "locations",
                "count": len(results),
                "entities": results,
                "filters_applied": filters or {}
            })

        if entity_type == "departments":
            departments = data.get("departments", {})

            # Supported department filters
            department_exact_keys = [
                "department_id", "name", "manager_id", "status"
            ]

            for department_id, department in departments.items():
                record = {**department}

                if filters:
                    if not apply_exact_filters(record, department_exact_keys, filters):
                        continue

                # ensure id present as string
                record["department_id"] = str(department_id)
                results.append(record)

            return json.dumps({
                "success": True,
                "entity_type": "departments",
                "count": len(results),
                "entities": results,
                "filters_applied": filters or {}
            })

        return json.dumps({
            "success": False,
            "error": "Halt: Missing entity_type or invalid entity_type"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_reference_entities",
                "description": "Discover and retrieve reference entities including users, locations, and departments.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of reference entity to discover. Valid values: 'users', 'locations', 'departments'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters for discovery. For users: user_id, first_name, last_name, email, phone_number, role, employment_status. For locations: location_id, city_name, country, status. For departments: department_id, name, manager_id, status"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }

