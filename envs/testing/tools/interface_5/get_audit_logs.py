import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetAuditLogs(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], log_id: Optional[str] = None, user_id: Optional[str] = None,
               action: Optional[str] = None, reference_type: Optional[str] = None, reference_id: Optional[str] = None) -> str:
        
        audit_logs = data.get("audit_logs", {})
        result = []
        
        for alid, log in audit_logs.items():
            # Apply filters
            if log_id and str(log_id) != alid:
                continue
            if user_id and log.get("user_id") != user_id:
                continue
            if action and log.get("action") != action:
                continue
            if reference_type and log.get("reference_type") != reference_type:
                continue
            if reference_id and log.get("reference_id") != reference_id:
                continue
            
            result.append({
                "log_id": alid,
                "user_id": log.get("user_id"),
                "action": log.get("action"),
                "reference_type": log.get("reference_type"),
                "reference_id": log.get("reference_id"),
                "field_name": log.get("field_name"),
                "old_value": log.get("old_value"),
                "new_value": log.get("new_value"),
                "timestamp": log.get("timestamp")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_audit_logs",
                "description": "Get audit logs matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "log_id": {"type": "string", "description": "ID of the audit log"},
                        "user_id": {"type": "string", "description": "ID of the user who performed the action"},
                        "action": {"type": "string", "description": "Action performed (create, update, delete)"},
                        "reference_type": {"type": "string", "description": "Type of entity that was modified"},
                        "reference_id": {"type": "string", "description": "ID of the entity that was modified"}
                    },
                    "required": []
                }
            }
        }
