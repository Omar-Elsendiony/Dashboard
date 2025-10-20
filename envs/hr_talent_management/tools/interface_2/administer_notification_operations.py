# Auto-generated — DO NOT EDIT BY HAND
import json
from typing import Any, Dict, Optional
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool


# ---- helpers ---------------------------------------------------------------

def _now_utc_iso(data: Dict[str, Any]) -> str:
    # Use injected clock if present for determinism
    injected = data.get("_now_utc")
    if isinstance(injected, str) and injected.strip():
        try:
            # normalize Z → +00:00 for fromisoformat
            dt = datetime.fromisoformat(injected.replace("Z", "+00:00"))
            return dt.isoformat()
        except Exception:
            pass
    return datetime.now(timezone.utc).isoformat()


def _get_user(data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    users = data.get("users", {})
    for _, u in users.items():
        if u.get("user_id") == user_id:
            return u
    raise ValueError(f"User '{user_id}' not found.")


def _require_active_user(data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    if not user_id:
        raise ValueError("Missing required user id.")
    u = _get_user(data, user_id)
    if str(u.get("employment_status", "")).lower() != "active":
        raise ValueError(f"User '{user_id}' is not active.")
    return u


def _related_entity_exists(data: Dict[str, Any], reference_type: str, reference_id: str) -> None:
    """
    Verify the referenced record exists based on notifications.reference_type enum:
      {'application','interview','offer','employee','payroll','benefit','document','exit'}
    """
    if not reference_type or not reference_id:
        raise ValueError("reference_type and reference_id are required.")
    rt = reference_type

    # Map to table names + primary key field names
    table_map = {
        "application": ("applications", "application_id"),
        "interview": ("interviews", "interview_id"),
        "offer": ("offers", "offer_id"),
        "employee": ("employees", "employee_id"),
        "payroll": ("payslips", "payslip_id"),     # notifications are often about payslips
        "benefit": ("benefit_enrollments", "enrollment_id"),
        "document": ("documents", "document_id"),
        "exit": ("employee_exits", "exit_id"),
    }
    if rt not in table_map:
        raise ValueError(f"Invalid reference_type '{rt}'.")
    table_key, pk = table_map[rt]
    table = data.get(table_key, {})
    for _, rec in table.items():
        if rec.get(pk) == reference_id:
            return
    raise ValueError(f"Reference not found for {rt}:{reference_id}.")


def _maybe_audit_notification(data: Dict[str, Any], reference_type: str, reference_id: str, action: str, field_name: Optional[str] = None, old_value: Optional[str] = None, new_value: Optional[str] = None):
    """
    If auto-audit is enabled, log to audit_trails against the *business object* (not the notification),
    but only when the reference_type exists in audit_trails.reference_type enum:
      ['requisition','application','offer','employee','payroll','benefit','exit','document','shortlist']
    'interview' is NOT supported; skip audit in that case.
    """
    if not data.get("_auto_audit"):
        return
    ref_map = {
        "application": "application",
        "offer": "offer",
        "employee": "employee",
        "payroll": "payroll",
        "benefit": "benefit",
        "document": "document",
        "exit": "exit",
        # 'interview' not present in audit_trails enum — skip
    }
    at_ref_type = ref_map.get(reference_type)
    if not at_ref_type:
        return  # skip unsupported reference types for audit

    try:
        from create_audit_entry import create_audit_entry  # type: ignore
        create_audit_entry(
            data,
            reference_id=reference_id,
            reference_type=at_ref_type,
            action=action,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
        )
    except Exception as e:
        # Per SOP: if external audit fails, halt
        raise ValueError(f"Audit failed: {e}")


# ---- main tool -------------------------------------------------------------

class AdministerNotificationOperations(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        operation_type: str,
        recipient_user_id: str = None,
        sender_user_id: str = None,
        recipient_email: str = None,
        notification_type: str = None,
        reference_type: str = None,
        reference_id: str = None,
        subject: str = None,
        notification_id: str = None,
        failed_reason: str = None
    ) -> str:
        notifications = data.setdefault("notifications", {})
        op = (operation_type or "").strip().lower()

        # Enums from DB
        valid_types = {
            'application_acknowledgment', 'interview_scheduled', 'offer_issued', 'onboarding_welcome',
            'payslip_released', 'payment_processed', 'benefits_enrollment', 'payroll_query_update',
            'exit_confirmation', 'document_request', 'other'
        }
        valid_refs = {'application', 'interview', 'offer', 'employee', 'payroll', 'benefit', 'document', 'exit'}
        valid_status = {'pending', 'sent', 'failed', 'bounced'}

        # Normalize inputs that are enums
        if notification_type is not None:
            notification_type = str(notification_type).lower().strip()
        if reference_type is not None:
            reference_type = str(reference_type).lower().strip()

        now_iso = _now_utc_iso(data)

        # ---------------- create_notification ----------------
        if op == "create_notification":
            # Required: at least one recipient, sender, type, ref type/id, subject
            if not subject or not sender_user_id or not notification_type or not reference_type or not reference_id:
                raise ValueError("Missing required fields for create_notification (subject, sender_user_id, notification_type, reference_type, reference_id).")
            if not (recipient_user_id or recipient_email):
                raise ValueError("At least one recipient is required: recipient_user_id or recipient_email.")

            # Validate enums
            if notification_type not in valid_types:
                raise ValueError(f"Invalid notification_type. Allowed: {sorted(valid_types)}")
            if reference_type not in valid_refs:
                raise ValueError(f"Invalid reference_type. Allowed: {sorted(valid_refs)}")

            # Sender must exist & be active
            _require_active_user(data, sender_user_id)

            # Recipient user (if provided) must exist & be active
            if recipient_user_id:
                _require_active_user(data, recipient_user_id)

            # Reference must exist
            _related_entity_exists(data, reference_type, reference_id)

            # Create record
            new_id = str(max([int(k) for k in notifications.keys()] + [0]) + 1)
            rec = {
                "notification_id": new_id,
                "recipient_user_id": recipient_user_id,
                "sender_user_id": sender_user_id,
                "recipient_email": recipient_email,
                "notification_type": notification_type,
                "reference_type": reference_type,
                "reference_id": reference_id,
                "subject": subject,
                "notification_status": "pending",
                "created_at": now_iso,
                "sent_at": None,
                "failed_reason": None
            }
            notifications[new_id] = rec

            # Optional auto-audit: submitting/queuing a notification against the business object
            _maybe_audit_notification(
                data,
                reference_type=reference_type,
                reference_id=reference_id,
                action="submit",
                field_name="notification_status",
                old_value=None,
                new_value="pending",
            )
            return json.dumps(rec)

        # For updates, require notification_id and record existence
        if not notification_id:
            raise ValueError("notification_id is required for status updates.")
        if notification_id not in notifications:
            raise ValueError(f"Notification {notification_id} not found.")
        rec = notifications[notification_id]
        current_status = rec.get("notification_status", "pending")
        if current_status not in valid_status:
            raise ValueError("Corrupt notification_status on record.")

        # Allowed transitions: pending → sent|failed|bounced; others terminal
        def _ensure_transition(target: str):
            if current_status == "pending" and target in {"sent", "failed", "bounced"}:
                return
            if current_status != "pending":
                raise ValueError(f"Invalid status transition: {current_status} -> {target} (terminal state).")
            raise ValueError(f"Invalid status transition: {current_status} -> {target}.")

        # ---------------- mark_sent ----------------
        if op == "mark_sent":
            _ensure_transition("sent")
            old = current_status
            rec["notification_status"] = "sent"
            rec["sent_at"] = now_iso
            # Auto-audit
            _maybe_audit_notification(
                data,
                reference_type=rec.get("reference_type"),
                reference_id=rec.get("reference_id"),
                action="update",
                field_name="notification_status",
                old_value=old,
                new_value="sent",
            )
            return json.dumps(rec)

        # ---------------- mark_failed ----------------
        if op == "mark_failed":
            if not failed_reason or not str(failed_reason).strip():
                raise ValueError("failed_reason is required for mark_failed.")
            _ensure_transition("failed")
            old = current_status
            rec["notification_status"] = "failed"
            rec["failed_reason"] = str(failed_reason).strip()
            # Auto-audit
            _maybe_audit_notification(
                data,
                reference_type=rec.get("reference_type"),
                reference_id=rec.get("reference_id"),
                action="update",
                field_name="notification_status",
                old_value=old,
                new_value="failed",
            )
            return json.dumps(rec)

        # ---------------- mark_bounced ----------------
        if op == "mark_bounced":
            if not failed_reason or not str(failed_reason).strip():
                raise ValueError("failed_reason (bounce reason) is required for mark_bounced.")
            _ensure_transition("bounced")
            old = current_status
            rec["notification_status"] = "bounced"
            rec["failed_reason"] = str(failed_reason).strip()
            # Auto-audit
            _maybe_audit_notification(
                data,
                reference_type=rec.get("reference_type"),
                reference_id=rec.get("reference_id"),
                action="update",
                field_name="notification_status",
                old_value=old,
                new_value="bounced",
            )
            return json.dumps(rec)

        raise ValueError("operation_type must be one of: create_notification | mark_sent | mark_failed | mark_bounced")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "administer_notification_operations",
                "description": "Create or update notifications per SOP/DB (supports create, mark_sent, mark_failed, mark_bounced).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "enum": ["create_notification", "mark_sent", "mark_failed", "mark_bounced"]
                        },
                        "recipient_user_id": {"type": "string"},
                        "sender_user_id": {"type": "string"},
                        "recipient_email": {"type": "string"},
                        "notification_type": {"type": "string"},
                        "reference_type": {
                            "type": "string",
                            "enum": ["application", "interview", "offer", "employee", "payroll", "benefit", "document", "exit"]
                        },
                        "reference_id": {"type": "string"},
                        "subject": {"type": "string"},
                        "notification_id": {"type": "string"},
                        "failed_reason": {"type": "string"}
                    },
                    "required": ["operation_type"]
                }
            }
        }


def manage_notification_operations(data: Dict[str, Any], **kwargs) -> str:
    return ManageNotificationOperations.invoke(data, **kwargs)
