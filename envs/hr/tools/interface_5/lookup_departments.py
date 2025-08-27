import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class LookupDepartments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], department_id: Optional[str] = None,
               manager_id: Optional[str] = None, status: Optional[str] = None) -> str:
        
        departments = data.get("departments", {})
        results = []
        
        for department in departments.values():
            if department_id and department.get("department_id") != department_id:
                continue
            if manager_id and department.get("manager_id") != manager_id:
                continue
            if status and department.get("status") != status:
                continue
            results.append(department)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "lookup_departments",
                "description": "Get departments with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "department_id": {"type": "string", "description": "Filter by department ID"},
                        "manager_id": {"type": "string", "description": "Filter by manager ID"},
                        "status": {"type": "string", "description": "Filter by status"}
                    },
                    "required": []
                }
            }
        }
