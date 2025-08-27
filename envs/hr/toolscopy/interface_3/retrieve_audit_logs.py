import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetAuditLogs(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: Optional[str] = None,
               action: Optional[str] = None, reference_type: Optional[str] = None,
               reference_id: Optional[str] = None, start_date: Optional[str] = None,
               end_date: Optional[str] = None) -> str:
        audit_logs = data.get("audit_logs", {})
        results = []
        
        for log in audit_logs.values():
            if user_id and log.get("user_id") != user_id:
                continue
            if action and log.get("action") != action:
                continue
            if reference_type and log.get("reference_type") != reference_type:
                continue
            if reference_id and log.get("reference_id") != reference_id:
                continue
            if start_date and log.get("timestamp", "") < start_date:
                continue
            if end_date and log.get("timestamp", "") > end_date:
                continue
            results.append(log)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_audit_logs",
                "description": "Get audit logs with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "Filter by user ID"},
                        "action": {"type": "string", "description": "Filter by action type (create, read, update, delete, approve, reject)"},
                        "reference_type": {"type": "string", "description": "Filter by reference type"},
                        "reference_id": {"type": "string", "description": "Filter by reference ID"},
                        "start_date": {"type": "string", "description": "Filter by start date (ISO format)"},
                        "end_date": {"type": "string", "description": "Filter by end date (ISO format)"}
                    },
                    "required": []
                }
            }
        }
