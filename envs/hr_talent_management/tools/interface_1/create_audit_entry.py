# Auto-generated — DO NOT EDIT BY HAND
import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateAuditEntry(Tool):
    """
    Create an audit trail record consistent with the HR SOP and DB schema.
    - Enforces valid reference_type and action enums (DB-aligned).
    - Accepts common aliases for reference_type and normalizes to canonical DB values.
    - Requires a caller user id for traceability (SOP: auditable, role-bound actions).
    - Uses UTC ISO8601 timestamps for created_at (DB: timestamp).
    - For 'update' actions, requires field_name and at least one of old_value/new_value.
    - Normalizes enums to lowercase to reduce caller error, while validating against allowed sets.
    """

    # Canonical enums (must match DB schema exactly)
    VALID_REFERENCE_TYPES = {
        "requisition", "application", "offer", "employee", "payroll",
        "benefit", "exit", "document", "shortlist"
    }

    VALID_ACTIONS = {
        "create", "update", "delete", "approve", "reject",
        "lock", "unlock", "submit", "verify"
    }

    # Friendly aliases → canonical reference_type
    REFERENCE_TYPE_ALIASES = {
        "job_requisition": "requisition",
        "requisitions": "requisition",
        "jobreq": "requisition",

        "applications": "application",
        "app": "application",

        "offers": "offer",

        "employees": "employee",
        "worker": "employee",
        "workers": "employee",

        "payroll_cycle": "payroll",
        "payroll_cycles": "payroll",
        "payrun": "payroll",

        "benefits": "benefit",

        "employee_exit": "exit",
        "employee_exits": "exit",
        "termination": "exit",

        "doc": "document",
        "documents": "document",

        "short_list": "shortlist",
        "short_listed": "shortlist",
        "shortlists": "shortlist",
    }

    @staticmethod
    def _now_utc_iso(data: Dict[str, Any]) -> str:
        injected = data.get("_now_utc")
        if isinstance(injected, str) and injected.strip():
            return injected
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _require_caller_user_id(data: Dict[str, Any]) -> str:
        caller = data.get("_caller_user_id")
        if not caller or not isinstance(caller, str) or not caller.strip():
            # SOP: halt with explicit error if we cannot attribute the action
            raise ValueError("Missing _caller_user_id for audit attribution.")
        return caller

    @staticmethod
    def _next_numeric_id_str(store: Dict[str, Any]) -> str:
        numeric_keys = [int(k) for k in store.keys() if str(k).isdigit()]
        return str((max(numeric_keys) if numeric_keys else 0) + 1)

    @classmethod
    def _normalize_reference_type(cls, value: str) -> str:
        v = (value or "").strip().lower()
        if v in cls.VALID_REFERENCE_TYPES:
            return v
        if v in cls.REFERENCE_TYPE_ALIASES:
            return cls.REFERENCE_TYPE_ALIASES[v]
        return v  # return as-is; will be validated later

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reference_id: str,
        reference_type: str,
        action: str,
        field_name: Optional[str] = None,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None,
    ) -> str:
        # -------- Input normalization --------
        if not isinstance(reference_id, str) or not reference_id.strip():
            raise ValueError("Invalid reference_id. Must be a non-empty string.")

        ref_type_norm = CreateAuditEntry._normalize_reference_type(reference_type)
        action_norm = action.lower().strip() if isinstance(action, str) else ""

        if ref_type_norm not in CreateAuditEntry.VALID_REFERENCE_TYPES:
            allowed = ", ".join(sorted(CreateAuditEntry.VALID_REFERENCE_TYPES))
            raise ValueError(
                f"Invalid reference_type '{reference_type}'. Must be one of [{allowed}] "
                f"(aliases accepted: {', '.join(sorted(CreateAuditEntry.REFERENCE_TYPE_ALIASES.keys()))})."
            )
        if action_norm not in CreateAuditEntry.VALID_ACTIONS:
            allowed = ", ".join(sorted(CreateAuditEntry.VALID_ACTIONS))
            raise ValueError(
                f"Invalid action '{action}'. Must be one of [{allowed}]."
            )

        # For 'update', require field_name and at least one of old/new
        if action_norm == "update":
            if not field_name or not isinstance(field_name, str) or not field_name.strip():
                raise ValueError("For action 'update', field_name is required.")
            if (old_value is None) and (new_value is None):
                raise ValueError("For action 'update', at least one of old_value or new_value must be provided.")

        # -------- Caller + time --------
        caller_user_id = CreateAuditEntry._require_caller_user_id(data)
        created_at_iso = CreateAuditEntry._now_utc_iso(data)

        # -------- Storage --------
        audit_trails = data.setdefault("audit_trails", {})
        new_id = CreateAuditEntry._next_numeric_id_str(audit_trails)

        rec = {
            "audit_id": new_id,
            "reference_id": reference_id,
            "reference_type": ref_type_norm,
            "action": action_norm,
            "user_id": caller_user_id,
            "field_name": field_name,
            "old_value": old_value,
            "new_value": new_value,
            "created_at": created_at_iso,
        }

        audit_trails[new_id] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        # Provide explicit enums for clarity + short descriptions for each reference_type.
        return {
            "type": "function",
            "function": {
                "name": "create_audit_entry",
                "description": (
                    "Append a record to audit_trails adhering to HR audit policy. "
                    "Valid reference_type values mirror the DB enum. Common aliases are accepted and normalized."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reference_id": {"type": "string", "description": "Primary key of the referenced record."},
                        "reference_type": {
                            "type": "string",
                            "description": (
                                "Entity type for the reference. "
                                "Allowed: requisition (job requisitions), application (candidate applications), "
                                "offer (candidate offers), employee (employee records), payroll (payroll cycles/ops), "
                                "benefit (benefit plans/enrollments), exit (employee exits), document (uploaded docs), "
                                "shortlist (shortlisting decisions). "
                                "Aliases accepted: job_requisition→requisition, payroll_cycle→payroll, employee_exit→exit, doc→document, etc."
                            ),
                            "enum": [
                                "requisition","application","offer","employee","payroll",
                                "benefit","exit","document","shortlist"
                            ],
                        },
                        "action": {
                            "type": "string",
                            "description": "Audit action verb.",
                            "enum": ["create","update","delete","approve","reject","lock","unlock","submit","verify"],
                        },
                        "field_name": {"type": "string", "description": "Required for 'update' actions."},
                        "old_value": {"type": "string", "description": "Optional; recommended for 'update' actions."},
                        "new_value": {"type": "string", "description": "Optional; recommended for 'update' actions."},
                    },
                    "required": ["reference_id", "reference_type", "action"],
                },
            },
        }


def create_audit_entry(data: Dict[str, Any], **kwargs) -> str:
    return CreateAuditEntry.invoke(data, **kwargs)
