# Auto-generated — DO NOT EDIT BY HAND
import json
from datetime import datetime, timezone, date
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


def _parse_mmddyyyy(s: str) -> date:
    try:
        return datetime.strptime(s.strip(), "%m-%d-%Y").date()
    except Exception as e:
        raise ValueError(f"Invalid date format '{s}'. Expected MM-DD-YYYY.") from e


def _now_utc_dt(data: Dict[str, Any]) -> datetime:
    # Use injected clock for determinism if provided; else real UTC
    injected = data.get("_now_utc")
    if isinstance(injected, str) and injected.strip():
        try:
            return datetime.fromisoformat(injected.replace("Z", "+00:00"))
        except Exception:
            pass
    return datetime.now(timezone.utc)


def _iso_date(d: date) -> str:
    return d.isoformat()  # YYYY-MM-DD


def _require_user(data: Dict[str, Any], user_id: Optional[str]) -> Dict[str, Any]:
    uid = user_id or data.get("_caller_user_id")
    if not uid or not isinstance(uid, str) or not uid.strip():
        raise ValueError("Missing user context: user_id/_caller_user_id is required.")
    users = data.get("users", {})
    user = None
    for _, u in users.items():
        if u.get("user_id") == uid:
            user = u
            break
    if not user:
        raise ValueError(f"User '{uid}' not found.")
    if str(user.get("employment_status", "")).lower() != "active":
        raise ValueError(f"User '{uid}' is not active.")
    return user


def _enforce_role(user: Dict[str, Any], allowed_roles: set, action_name: str):
    role = str(user.get("role", "")).lower()
    if role not in allowed_roles:
        raise ValueError(f"User '{user.get('user_id')}' not authorized to {action_name} (role '{role}' not allowed).")


def _related_entity_exists(data: Dict[str, Any], related_entity_type: str, related_entity_id: str):
    # Map related_entity_type -> in-memory table key
    table_map = {
        "employee": "employees",
        "candidate": "candidates",
        "offer": "offers",
        "onboarding": "onboarding_checklists",
        "job_requisition": "job_requisitions",
        "job_posting": "job_postings",
        "application": "applications",
    }
    table_key = table_map.get(related_entity_type)
    if not table_key:
        raise ValueError(f"Invalid related_entity_type '{related_entity_type}'.")
    table = data.get(table_key, {})
    for _, rec in table.items():
        if related_entity_type == "offer" and rec.get("offer_id") == related_entity_id:
            return
        if related_entity_type == "job_requisition" and rec.get("requisition_id") == related_entity_id:
            return
        if related_entity_type == "job_posting" and rec.get("posting_id") == related_entity_id:
            return
        if related_entity_type == "application" and rec.get("application_id") == related_entity_id:
            return
        if related_entity_type == "employee" and rec.get("employee_id") == related_entity_id:
            return
        if related_entity_type == "candidate" and rec.get("candidate_id") == related_entity_id:
            return
        if related_entity_type == "onboarding" and rec.get("checklist_id") == related_entity_id:
            return
    raise ValueError(f"Related entity '{related_entity_type}:{related_entity_id}' not found.")


def _maybe_audit(
    data: Dict[str, Any],
    reference_id: str,
    action: str,
    field_name: Optional[str] = None,
    old_value: Optional[str] = None,
    new_value: Optional[str] = None,
):
    """Create an audit entry if auto-audit is enabled. Halt on failure (SOP)."""
    if not data.get("_auto_audit"):
        return
    try:
        # Prefer the dedicated tool if available
        from create_audit_entry import create_audit_entry  # type: ignore
    except Exception as e:
        raise ValueError(f"Audit integration unavailable: {e}")

    try:
        create_audit_entry(
            data,
            reference_id=reference_id,
            reference_type="document",
            action=action,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
        )
    except Exception as e:
        raise ValueError(f"Audit failed: {e}")


class AdministerDocumentOperations(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        operation_type: str,
        document_category: str = None,
        related_entity_type: str = None,
        related_entity_id: str = None,
        file_name: str = None,
        file_format: str = None,
        uploaded_by: str = None,
        upload_date: str = None,
        document_id: str = None,
        expiry_date: str = None,
        verification_status: str = None,
        verified_date: str = None,
        user_id: str = None,
        document_status: str = None
    ) -> str:

        documents = data.setdefault("documents", {})

        op = (operation_type or "").strip().lower()
        if op not in {"upload_document", "verify_document", "update_document_status"}:
            raise ValueError("operation_type must be one of 'upload_document' | 'verify_document' | 'update_document_status'.")

        valid_categories = {
            'verification_id_proof', 'verification_address_proof', 'verification_educational_certificate',
            'verification_experience_letter', 'verification_work_visa', 'verification_pr_card',
            'verification_bank_proof', 'offer_letter', 'contract', 'policy_acknowledgment', 'tax_form',
            'insurance_form', 'nda', 'resume', 'cover_letter', 'job_description', 'budget_justification',
            'budget_approval', 'workforce_plan', 'recruitment_checklist', 'promotion_letter',
            'transfer_memo', 'other'
        }
        valid_related = {'employee', 'candidate', 'offer', 'onboarding', 'job_requisition', 'job_posting', 'application'}
        valid_doc_status = {'active', 'archived', 'expired'}
        valid_verif_status = {'pending', 'verified', 'failed'}

        # Normalize enums
        if document_category is not None:
            document_category = str(document_category).lower().strip()
        if related_entity_type is not None:
            related_entity_type = str(related_entity_type).lower().strip()
        if document_status is not None:
            document_status = str(document_status).lower().strip()
        if verification_status is not None:
            verification_status = str(verification_status).lower().strip()

        now_dt = _now_utc_dt(data)
        today = now_dt.date()

        # ---------- UPLOAD ----------
        if op == "upload_document":
            required_vals = [document_category, related_entity_type, related_entity_id, file_name, file_format, uploaded_by, upload_date]
            if any(v in (None, "") for v in required_vals):
                raise ValueError("Missing required fields for upload_document (document_category, related_entity_type, related_entity_id, file_name, file_format, uploaded_by, upload_date).")

            uploader = _require_user(data, uploaded_by)
            _enforce_role(
                uploader,
                {"hr_recruiter", "hr_admin", "hr_manager", "compliance_officer", "employee"},
                "upload documents"
            )

            if document_category not in valid_categories:
                raise ValueError(f"Invalid document_category. Allowed: {sorted(valid_categories)}")
            if related_entity_type not in valid_related:
                raise ValueError(f"Invalid related_entity_type. Allowed: {sorted(valid_related)}")

            _related_entity_exists(data, related_entity_type, related_entity_id)

            if not isinstance(file_format, str) or not file_format.strip() or len(file_format.strip()) > 10:
                raise ValueError("file_format must be a non-empty string up to 10 characters.")

            if any(d.get("file_name") == file_name for d in documents.values()):
                raise ValueError(f"file_name '{file_name}' already exists (must be unique).")

            upload_date_d = _parse_mmddyyyy(upload_date)
            if upload_date_d > today:
                raise ValueError("Upload date cannot be in the future.")

            expiry_date_iso = None
            if expiry_date not in (None, ""):
                exp_d = _parse_mmddyyyy(expiry_date)
                if exp_d < upload_date_d:
                    raise ValueError("expiry_date cannot be earlier than upload_date.")
                expiry_date_iso = _iso_date(exp_d)

            ver_status = verification_status or "pending"
            ver_status = str(ver_status).lower().strip()
            if ver_status not in valid_verif_status:
                raise ValueError("verification_status must be one of 'pending','verified','failed'.")

            new_id = str(max([int(k) for k in documents.keys()] + [0]) + 1)
            rec = {
                "document_id": new_id,
                "document_category": document_category,
                "related_entity_type": related_entity_type,
                "related_entity_id": related_entity_id,
                "file_name": file_name,
                "file_format": file_format.strip(),
                "upload_date": _iso_date(upload_date_d),
                "uploaded_by": uploader.get("user_id"),
                "document_status": "active",
                "expiry_date": expiry_date_iso,
                "verification_status": ver_status,
                "created_at": now_dt.isoformat(),
            }
            documents[new_id] = rec

            # Auto-audit (create)
            _maybe_audit(
                data,
                reference_id=new_id,
                action="create",
                field_name="file_name",
                old_value=None,
                new_value=file_name,
            )
            return json.dumps(rec)

        # document_id must be provided for the other ops
        if not document_id:
            raise ValueError("document_id is required.")
        rec = documents.get(document_id)
        if not rec:
            raise ValueError(f"Document {document_id} not found.")

        # ---------- VERIFY ----------
        if op == "verify_document":
            if verification_status not in valid_verif_status:
                raise ValueError("verification_status must be one of 'pending','verified','failed'.")
            if str(rec.get("document_status", "")).lower() != "active":
                raise ValueError("Only active documents can be verified.")

            verifier = _require_user(data, user_id)
            _enforce_role(
                verifier,
                {"compliance_officer", "finance_manager", "hr_manager"},
                "verify documents"
            )

            if not verified_date:
                raise ValueError("verified_date is required (MM-DD-YYYY).")
            ver_dt = _parse_mmddyyyy(verified_date)
            if ver_dt > today:
                raise ValueError("Verification date cannot be in the future.")

            old = str(rec.get("verification_status", "pending")).lower()
            rec["verification_status"] = verification_status
            rec["verified_by"] = verifier.get("user_id")
            rec["verified_date"] = _iso_date(ver_dt)

            # Auto-audit (verify)
            _maybe_audit(
                data,
                reference_id=document_id,
                action="verify",
                field_name="verification_status",
                old_value=old,
                new_value=verification_status,
            )
            return json.dumps(rec)

        # ---------- UPDATE STATUS ----------
        if op == "update_document_status":
            if document_status not in valid_doc_status:
                raise ValueError("document_status must be one of 'active','archived','expired'.")

            actor = _require_user(data, user_id)
            _enforce_role(
                actor,
                {"hr_admin", "hr_manager", "hr_director"},
                "update document status"
            )

            current_status = str(rec.get("document_status", "")).lower()
            target_status = document_status

            allowed_transitions = {
                "active": {"archived", "expired"},
                "archived": {"active"},
                "expired": set(),
            }
            if target_status not in allowed_transitions.get(current_status, set()):
                raise ValueError(f"Invalid status transition: {current_status} -> {target_status}.")

            if target_status == "expired":
                exp = rec.get("expiry_date")
                if not exp:
                    raise ValueError("Cannot set status to 'expired' without an expiry_date on the document.")
                try:
                    exp_dt = datetime.fromisoformat(exp).date()
                except Exception:
                    exp_dt = _parse_mmddyyyy(exp)
                if exp_dt > today:
                    raise ValueError("Document cannot be set to 'expired' before its expiry_date.")

            old = current_status
            rec["document_status"] = target_status

            # Auto-audit (update)
            _maybe_audit(
                data,
                reference_id=document_id,
                action="update",
                field_name="document_status",
                old_value=old,
                new_value=target_status,
            )
            return json.dumps(rec)

        raise ValueError("Unsupported operation_type.")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "administer_document_operations",
                "description": "Upload, verify, or update status of documents per SOP and DB schema (auto-audits when enabled).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "enum": ["upload_document", "verify_document", "update_document_status"]
                        },
                        # Common
                        "document_id": {"type": "string"},
                        "user_id": {"type": "string"},

                        # Upload
                        "document_category": {"type": "string"},
                        "related_entity_type": {
                            "type": "string",
                            "enum": ["employee", "candidate", "offer", "onboarding", "job_requisition", "job_posting", "application"]
                        },
                        "related_entity_id": {"type": "string"},
                        "file_name": {"type": "string"},
                        "file_format": {"type": "string"},
                        "uploaded_by": {"type": "string"},
                        "upload_date": {"type": "string", "description": "MM-DD-YYYY"},
                        "expiry_date": {"type": "string", "description": "MM-DD-YYYY"},
                        "verification_status": {"type": "string", "description": "pending|verified|failed"},

                        # Verify
                        "verified_date": {"type": "string", "description": "MM-DD-YYYY"},

                        # Update status
                        "document_status": {"type": "string", "description": "active|archived|expired"}
                    },
                    "required": ["operation_type"]
                }
            }
        }


def manage_document_operations(data: Dict[str, Any], **kwargs) -> str:
    return ManageDocumentOperations.invoke(data, **kwargs)
