# manage_attachments.py
import json
import os
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageAttachments(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        attachment_id: Optional[str] = None,
        attachment_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_ROOT = os.path.dirname(TOOL_DIR)
        DATA_DIR = os.path.join(PROJECT_ROOT, "data")
        ATTACHMENTS_FP = os.path.join(DATA_DIR, "attachments.json")

        def ensure_dirs() -> None:
            os.makedirs(DATA_DIR, exist_ok=True)

        def load_attachments() -> Dict[str, Any]:
            if os.path.exists(ATTACHMENTS_FP):
                try:
                    with open(ATTACHMENTS_FP, "r") as f:
                        return json.load(f)
                except Exception:
                    return {}
            return {}

        def save_attachments(attachments_dict: Dict[str, Any]) -> None:
            ensure_dirs()
            with open(ATTACHMENTS_FP, "w") as f:
                json.dump(attachments_dict, f, indent=2)

        timestamp = "2025-11-01T00:00:00"
        attachments = data.setdefault("attachments", {})
        users = data.setdefault("users", {})
        incidents = data.setdefault("incidents", {})
        change_requests = data.setdefault("change_requests", {})
        root_cause_analyses = data.setdefault("root_cause_analyses", {})
        incident_reports = data.setdefault("incident_reports", {})
        post_incident_reviews = data.setdefault("post_incident_reviews", {})
        communications = data.setdefault("communications", {})
        work_orders = data.setdefault("work_orders", {})
        problem_tickets = data.setdefault("problem_tickets", {})

        if not attachments:
            loaded = load_attachments()
            if loaded:
                attachments.update(loaded)

        reference_tables = {
            "incident": incidents,
            "change": change_requests,
            "rca": root_cause_analyses,
            "report": incident_reports,
            "pir": post_incident_reviews,
            "communication": communications,
            "work_order": work_orders,
            "problem": problem_tickets
        }
        valid_reference_types = list(reference_tables.keys())

        if action not in ["create", "update"]:
            return json.dumps({"success": False, "error": f"Invalid action '{action}'. Must be 'create' or 'update'"})

        if action == "create":
            if not attachment_data:
                return json.dumps({"success": False, "error": "attachment_data is required for create action"})
            required_fields = ["reference_id", "reference_type", "file_name", "file_url", "uploaded_by"]
            missing_fields = [f for f in required_fields if f not in attachment_data]
            if missing_fields:
                return json.dumps({"success": False, "error": f"Missing required fields: {', '.join(missing_fields)}"})
            reference_type = attachment_data["reference_type"]
            if reference_type not in valid_reference_types:
                return json.dumps({"success": False, "error": f"Invalid reference_type. Must be one of: {', '.join(valid_reference_types)}"})
            reference_id = str(attachment_data["reference_id"])
            reference_table = reference_tables[reference_type]
            if reference_id not in reference_table:
                return json.dumps({"success": False, "error": f"Reference {reference_type} with ID '{reference_id}' not found"})
            uploaded_by = str(attachment_data["uploaded_by"])
            if uploaded_by not in users:
                return json.dumps({"success": False, "error": f"User with ID '{uploaded_by}' not found"})
            file_size_bytes = attachment_data.get("file_size_bytes")
            if file_size_bytes is not None:
                try:
                    file_size_bytes = int(file_size_bytes)
                    if file_size_bytes < 0:
                        raise ValueError
                except Exception:
                    return json.dumps({"success": False, "error": "file_size_bytes must be a non-negative integer"})
            new_attachment_id = generate_id(attachments)
            new_attachment = {
                "attachment_id": new_attachment_id,
                "reference_id": reference_id,
                "reference_type": reference_type,
                "file_name": attachment_data["file_name"],
                "file_url": attachment_data["file_url"],
                "file_type": attachment_data.get("file_type"),
                "file_size_bytes": file_size_bytes,
                "uploaded_by": uploaded_by,
                "uploaded_at": timestamp,
                "created_at": timestamp,
                "updated_at": timestamp
            }
            attachments[new_attachment_id] = new_attachment
            save_attachments(attachments)
            return json.dumps(new_attachment)

        if not attachment_id:
            return json.dumps({"success": False, "error": "attachment_id is required for update action"})
        if attachment_id not in attachments:
            return json.dumps({"success": False, "error": f"Attachment with ID '{attachment_id}' not found"})
        if not attachment_data:
            return json.dumps({"success": False, "error": "attachment_data is required for update action"})

        current_attachment = attachments[attachment_id]
        updated_attachment = current_attachment.copy()
        effective_reference_type = attachment_data.get("reference_type", current_attachment.get("reference_type"))
        effective_reference_id = str(attachment_data.get("reference_id", current_attachment.get("reference_id", "")))
        if effective_reference_type not in valid_reference_types:
            return json.dumps({"success": False, "error": f"Invalid reference_type. Must be one of: {', '.join(valid_reference_types)}"})
        ref_table = reference_tables[effective_reference_type]
        if effective_reference_id not in ref_table:
            return json.dumps({"success": False, "error": f"Reference {effective_reference_type} with ID '{effective_reference_id}' not found"})
        if "uploaded_by" in attachment_data:
            new_uploader = str(attachment_data["uploaded_by"])
            if new_uploader not in users:
                return json.dumps({"success": False, "error": f"User with ID '{new_uploader}' not found"})
        if "file_size_bytes" in attachment_data and attachment_data["file_size_bytes"] is not None:
            try:
                fs_int = int(attachment_data["file_size_bytes"])
                if fs_int < 0:
                    raise ValueError
                attachment_data["file_size_bytes"] = fs_int
            except Exception:
                return json.dumps({"success": False, "error": "file_size_bytes must be a non-negative integer"})
        allowed_fields = {"reference_id","reference_type","file_name","file_url","file_type","file_size_bytes","uploaded_by"}
        for key, value in attachment_data.items():
            if key not in allowed_fields:
                continue
            if key in {"reference_id", "uploaded_by"} and value is not None:
                updated_attachment[key] = str(value)
            else:
                updated_attachment[key] = value
        updated_attachment["reference_type"] = effective_reference_type
        updated_attachment["reference_id"] = effective_reference_id
        updated_attachment["updated_at"] = timestamp
        attachments[attachment_id] = updated_attachment
        save_attachments(attachments)
        return json.dumps(updated_attachment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_attachments",
                "description": "Create or update attachment records with file persistence to data/attachments.json.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string","enum": ["create", "update"]},
                        "attachment_id": {"type": "string"},
                        "attachment_data": {
                            "type": "object",
                            "properties": {
                                "reference_id": {"type": "string"},
                                "reference_type": {"type": "string"},
                                "file_name": {"type": "string"},
                                "file_url": {"type": "string"},
                                "file_type": {"type": "string"},
                                "file_size_bytes": {"type": "integer"},
                                "uploaded_by": {"type": "string"}
                            }
                        }
                    },
                    "required": ["action"]
                }
            }
        }
