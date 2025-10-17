import json
import os
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class LogAuditRecords(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        audit_id: Optional[str] = None,
        audit_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        # Resolve correct data directory dynamically
        TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
        ENV_DIR = os.path.dirname(TOOL_DIR)
        DATA_DIR = os.path.join(ENV_DIR, "data")
        AUDIT_FP = os.path.join(DATA_DIR, "audit_trails.json")

        def ensure_dirs() -> None:
            os.makedirs(DATA_DIR, exist_ok=True)

        def load_audit_trails() -> Dict[str, Any]:
            if os.path.exists(AUDIT_FP):
                try:
                    with open(AUDIT_FP, "r") as f:
                        return json.load(f)
                except Exception:
                    return {}
            return {}

        def save_audit_trails(audit_dict: Dict[str, Any]) -> None:
            ensure_dirs()
            with open(AUDIT_FP, "w") as f:
                json.dump(audit_dict, f, indent=2)

        timestamp = "2025-11-01T00:00:00"
        audit_trails = data.setdefault("audit_trails", {})
        users = data.setdefault("users", {})

        if not audit_trails:
            loaded = load_audit_trails()
            if loaded:
                audit_trails.update(loaded)

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

        # ---------- CREATE ----------
        if action == "create":
            if not audit_data:
                return json.dumps({
                    "success": False,
                    "error": "audit_data is required for create action"
                })

            required_fields = [
                "reference_id", "reference_type", "action",
                "user_id", "field_name", "old_value", "new_value"
            ]
            missing_fields = [f for f in required_fields if f not in audit_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                })

            user_id = str(audit_data["user_id"])
            if user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User with ID '{user_id}' not found"
                })

            new_audit_id = generate_id(audit_trails)
            new_entry = {
                "audit_id": new_audit_id,
                "reference_id": str(audit_data["reference_id"]),
                "reference_type": audit_data["reference_type"],
                "action": audit_data["action"],
                "user_id": user_id,
                "field_name": audit_data["field_name"],
                "old_value": audit_data["old_value"],
                "new_value": audit_data["new_value"],
                "created_at": timestamp
            }

            audit_trails[new_audit_id] = new_entry
            save_audit_trails(audit_trails)
            return json.dumps(new_entry)

        # ---------- UPDATE ----------
        if action == "update":
            if not audit_id:
                return json.dumps({
                    "success": False,
                    "error": "audit_id is required for update action"
                })

            if audit_id not in audit_trails:
                return json.dumps({
                    "success": False,
                    "error": f"Audit record with ID '{audit_id}' not found"
                })

            if not audit_data:
                return json.dumps({
                    "success": False,
                    "error": "audit_data is required for update action"
                })

            updated_audit = audit_trails[audit_id].copy()
            for key, value in audit_data.items():
                if key in updated_audit and value is not None:
                    updated_audit[key] = value

            updated_audit["created_at"] = timestamp
            audit_trails[audit_id] = updated_audit
            save_audit_trails(audit_trails)
            return json.dumps(updated_audit)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "log_audit_records",
                "description": (
                    "Create or update audit trail records. "
                    "This API reads from and writes to data/audit_trails.json, maintaining a record of all field changes. "
                    "Each record tracks reference_id, reference_type, action, user_id, field_name, old_value, new_value, and timestamp."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": (
                                "Action to perform:\n"
                                "- 'create': Add a new audit entry (requires audit_data)\n"
                                "- 'update': Modify an existing entry (requires audit_id and audit_data)"
                            ),
                            "enum": ["create", "update"]
                        },
                        "audit_id": {
                            "type": "string",
                            "description": "Unique audit record ID (required for update action only)"
                        },
                        "audit_data": {
                            "type": "object",
                            "description": (
                                "Audit record data object containing reference details and field changes.\n\n"
                                "For 'create': requires reference_id, reference_type, action, user_id, field_name, old_value, new_value.\n"
                                "For 'update': any of these fields can be modified.\n\n"
                                "Example Create:\n"
                                "{\n"
                                "  \"reference_id\": \"56\",\n"
                                "  \"reference_type\": \"escalation\",\n"
                                "  \"action\": \"create\",\n"
                                "  \"user_id\": \"15\",\n"
                                "  \"field_name\": \"priority\",\n"
                                "  \"old_value\": \"building\",\n"
                                "  \"new_value\": \"star\"\n"
                                "}\n\n"
                                "Example Update:\n"
                                "{ \"new_value\": \"critical\" }"
                            ),
                            "properties": {
                                "reference_id": {"type": "string"},
                                "reference_type": {"type": "string"},
                                "action": {"type": "string"},
                                "user_id": {"type": "string"},
                                "field_name": {"type": "string"},
                                "old_value": {"type": "string"},
                                "new_value": {"type": "string"}
                            }
                        }
                    },
                    "required": ["action"]
                }
            }
        }
