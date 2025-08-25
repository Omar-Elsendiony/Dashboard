import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListOrganizationDepartments(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        department_id: str = None,
        organization_id: str = None,
        manager_user_id: str = None,
        name: str = None
    ) -> str:
        departments = data.get("org_departments", {})

        def matches(dept_id, dept):
            if department_id and dept_id != department_id:
                return False
            if organization_id and dept.get("organization_id") != organization_id:
                return False
            if manager_user_id and dept.get("manager_user_id") != manager_user_id:
                return False
            if name and name.lower() not in dept.get("name", "").lower():
                return False
            return True

        results = [
            {**dept, "department_id": dept_id}
            for dept_id, dept in departments.items()
            if matches(dept_id, dept)
        ]

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_organization_departments",
                "description": (
                    "Lists organization departments with optional filters on department_id (key), "
                    "organization_id, manager_user_id, or name. Only department_id yields a unique result."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "department_id": {
                            "type": "string",
                            "description": "Filter by department ID (matches the dictionary key)"
                        },
                        "organization_id": {
                            "type": "string",
                            "description": "Filter by organization ID"
                        },
                        "manager_user_id": {
                            "type": "string",
                            "description": "Filter by manager's user ID"
                        },
                        "name": {
                            "type": "string",
                            "description": "Filter by name (case-insensitive partial match)"
                        }
                    },
                    "required": []
                }
            }
        }
