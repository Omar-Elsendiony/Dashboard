# Auto-generated — DO NOT EDIT BY HAND
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool


def _parse_date_sop_mmddyyyy(s: str) -> datetime:
    """Parse input dates per SOP (MM-DD-YYYY)."""
    try:
        return datetime.strptime(s.strip(), "%m-%d-%Y")
    except Exception as e:
        raise ValueError(f"Invalid date format '{s}'. Expected MM-DD-YYYY.") from e


def _parse_record_dt_flexible(s: Optional[str]) -> Optional[datetime]:
    """
    Parse record-side timestamps/dates flexibly:
    - ISO 8601 (YYYY-MM-DD or with time, with optional Z)
    - SOP MM-DD-YYYY
    - Common fallbacks
    Returns None if empty or unparseable.
    """
    if not s or not isinstance(s, str) or not s.strip():
        return None
    txt = s.strip()
    try:
        return datetime.fromisoformat(txt.replace("Z", "+00:00"))
    except Exception:
        pass
    for fmt in ("%m-%d-%Y", "%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(txt, fmt)
        except Exception:
            continue
    return None


def _range_match(rec_value: Optional[str], start: Optional[datetime], end: Optional[datetime]) -> bool:
    """Generic date window check with flexible record parsing."""
    if start is None and end is None:
        return True
    rv = _parse_record_dt_flexible(rec_value)
    if rv is None:
        return False
    if start is not None and rv < start:
        return False
    if end is not None and rv > end:
        return False
    return True


def _paginate(items: List[Dict[str, Any]], limit: int, offset: int) -> Dict[str, Any]:
    end = offset + limit
    sliced = items[offset:end]
    next_offset = end if end < len(items) else None
    return {"items": sliced, "next_offset": next_offset}


class GetEmployeeEntities(Tool):
    """
    SOP discovery for:
      - employees
      - onboarding_checklists
    Returns masked employee records (no tax_id/bank/routing).
    """

    # --- ENUMS FROM DB SCHEMA ---
    EMPLOYEE_TYPES = {"full_time", "part_time", "contractor", "intern"}
    EMPLOYMENT_STATUS = {"active", "inactive", "on_leave", "suspended", "terminated"}
    TAX_FILING_STATUS = {
        "single", "married_filing_joint", "married_filing_separate",
        "head_of_household", "surviving_spouse"
    }

    PRE_ONBOARDING_STATUS = {"pending", "in_progress", "completed"}
    BACKGROUND_CHECK_STATUS = {"pending", "in_progress", "passed", "failed"}
    DOC_VERIF_STATUS = {"pending", "verified", "failed"}
    IT_PROVISIONING_STATUS = {"pending", "in_progress", "completed"}
    BENEFITS_ENROLLMENT_STATUS = {"pending", "in_progress", "completed"}
    OVERALL_STATUS = {"not_started", "in_progress", "completed", "on_hold"}

    # --- ALLOWED FILTERS PER SOP/DB ---
    EMP_ALLOWED_FILTERS = {
        "employee_id",
        "candidate_id",
        "first_name",
        "last_name",
        "employee_type",
        "department_id",
        "location_id",
        "job_title",
        "start_date_from",
        "start_date_to",
        "tax_id",          # filterable, but never returned
        "work_email",
        "phone_number",
        "manager_id",
        "tax_filing_status",
        "employment_status",
    }

    ONB_ALLOWED_FILTERS = {
        "checklist_id",
        "employee_id",
        "start_date_from",
        "start_date_to",
        "position",
        "hiring_manager_id",
        "pre_onboarding_status",
        "background_check_status",
        "document_verification_status",
        "it_provisioning_status",
        "orientation_completed",  # boolean-ish truthy/falsey
        "benefits_enrollment_status",
        "overall_status",
        # NOTE: SOP text mentions candidate_name, but DB schema does not have it.
        # We intentionally do NOT allow 'candidate_name' to avoid silent no-ops.
    }

    @staticmethod
    def _mask_employee(rec: Dict[str, Any]) -> Dict[str, Any]:
        out = dict(rec)
        out.pop("tax_id", None)
        out.pop("bank_account_number", None)
        out.pop("routing_number", None)
        return out

    @staticmethod
    def _normalize_bool_like(v: Any) -> Optional[bool]:
        if v is None:
            return None
        if isinstance(v, bool):
            return v
        txt = str(v).strip().lower()
        if txt in {"true", "1", "yes", "y"}:
            return True
        if txt in {"false", "0", "no", "n"}:
            return False
        raise ValueError("orientation_completed must be boolean (true/false).")

    @staticmethod
    def _validate_filters(entity_type: str, filters: Dict[str, Any]) -> Dict[str, Any]:
        if entity_type == "employees":
            allowed = DiscoverEmployeeEntities.EMP_ALLOWED_FILTERS
        elif entity_type == "onboarding_checklists":
            allowed = DiscoverEmployeeEntities.ONB_ALLOWED_FILTERS
        else:
            raise ValueError("Invalid entity_type. Must be one of {'employees','onboarding_checklists'}.")

        unknown = set(filters.keys()) - allowed
        if unknown:
            raise ValueError(f"Unknown filters for {entity_type}: {sorted(unknown)}")

        f = dict(filters)

        if entity_type == "employees":
            # Normalize enums
            if "employee_type" in f and f["employee_type"] is not None:
                v = str(f["employee_type"]).lower().strip()
                if v not in DiscoverEmployeeEntities.EMPLOYEE_TYPES:
                    raise ValueError(f"Invalid employee_type. Allowed: {sorted(DiscoverEmployeeEntities.EMPLOYEE_TYPES)}")
                f["employee_type"] = v

            if "employment_status" in f and f["employment_status"] is not None:
                v = str(f["employment_status"]).lower().strip()
                if v not in DiscoverEmployeeEntities.EMPLOYMENT_STATUS:
                    raise ValueError(f"Invalid employment_status. Allowed: {sorted(DiscoverEmployeeEntities.EMPLOYMENT_STATUS)}")
                f["employment_status"] = v

            if "tax_filing_status" in f and f["tax_filing_status"] is not None:
                v = str(f["tax_filing_status"]).lower().strip()
                if v not in DiscoverEmployeeEntities.TAX_FILING_STATUS:
                    raise ValueError(f"Invalid tax_filing_status. Allowed: {sorted(DiscoverEmployeeEntities.TAX_FILING_STATUS)}")
                f["tax_filing_status"] = v

            # Date ranges
            for k in ("start_date_from", "start_date_to"):
                if k in f and f[k] is not None:
                    f[k] = _parse_date_sop_mmddyyyy(str(f[k]))

        else:  # onboarding_checklists
            # Normalize enums
            if "pre_onboarding_status" in f and f["pre_onboarding_status"] is not None:
                v = str(f["pre_onboarding_status"]).lower().strip()
                if v not in DiscoverEmployeeEntities.PRE_ONBOARDING_STATUS:
                    raise ValueError(f"Invalid pre_onboarding_status. Allowed: {sorted(DiscoverEmployeeEntities.PRE_ONBOARDING_STATUS)}")
                f["pre_onboarding_status"] = v

            if "background_check_status" in f and f["background_check_status"] is not None:
                v = str(f["background_check_status"]).lower().strip()
                if v not in DiscoverEmployeeEntities.BACKGROUND_CHECK_STATUS:
                    raise ValueError(f"Invalid background_check_status. Allowed: {sorted(DiscoverEmployeeEntities.BACKGROUND_CHECK_STATUS)}")
                f["background_check_status"] = v

            if "document_verification_status" in f and f["document_verification_status"] is not None:
                v = str(f["document_verification_status"]).lower().strip()
                if v not in DiscoverEmployeeEntities.DOC_VERIF_STATUS:
                    raise ValueError(f"Invalid document_verification_status. Allowed: {sorted(DiscoverEmployeeEntities.DOC_VERIF_STATUS)}")
                f["document_verification_status"] = v

            if "it_provisioning_status" in f and f["it_provisioning_status"] is not None:
                v = str(f["it_provisioning_status"]).lower().strip()
                if v not in DiscoverEmployeeEntities.IT_PROVISIONING_STATUS:
                    raise ValueError(f"Invalid it_provisioning_status. Allowed: {sorted(DiscoverEmployeeEntities.IT_PROVISIONING_STATUS)}")
                f["it_provisioning_status"] = v

            if "benefits_enrollment_status" in f and f["benefits_enrollment_status"] is not None:
                v = str(f["benefits_enrollment_status"]).lower().strip()
                if v not in DiscoverEmployeeEntities.BENEFITS_ENROLLMENT_STATUS:
                    raise ValueError(f"Invalid benefits_enrollment_status. Allowed: {sorted(DiscoverEmployeeEntities.BENEFITS_ENROLLMENT_STATUS)}")
                f["benefits_enrollment_status"] = v

            if "overall_status" in f and f["overall_status"] is not None:
                v = str(f["overall_status"]).lower().strip()
                if v not in DiscoverEmployeeEntities.OVERALL_STATUS:
                    raise ValueError(f"Invalid overall_status. Allowed: {sorted(DiscoverEmployeeEntities.OVERALL_STATUS)}")
                f["overall_status"] = v

            if "orientation_completed" in f and f["orientation_completed"] is not None:
                f["orientation_completed"] = DiscoverEmployeeEntities._normalize_bool_like(f["orientation_completed"])

            # Date ranges
            for k in ("start_date_from", "start_date_to"):
                if k in f and f[k] is not None:
                    f[k] = _parse_date_sop_mmddyyyy(str(f[k]))

        return f

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        entity_type: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> str:
        entity_type = (entity_type or "").strip().lower()
        if entity_type not in {"employees", "onboarding_checklists"}:
            raise ValueError("Invalid entity_type. Must be one of {'employees','onboarding_checklists'}.")

        limit = int(limit or 50)
        offset = int(offset or 0)
        if limit <= 0:
            raise ValueError("limit must be > 0.")
        if offset < 0:
            raise ValueError("offset must be >= 0.")

        filters = filters or {}
        if not isinstance(filters, dict):
            raise ValueError("filters must be an object/dict.")

        f = DiscoverEmployeeEntities._validate_filters(entity_type, filters)

        items: List[Dict[str, Any]] = []

        if entity_type == "employees":
            emps = data.get("employees", {})
            for _, rec in emps.items():
                # equals filters
                if "employee_id" in f and f["employee_id"] and rec.get("employee_id") != f["employee_id"]:
                    continue
                if "candidate_id" in f and f["candidate_id"] and rec.get("candidate_id") != f["candidate_id"]:
                    continue
                if "first_name" in f and f["first_name"] and rec.get("first_name") != f["first_name"]:
                    continue
                if "last_name" in f and f["last_name"] and rec.get("last_name") != f["last_name"]:
                    continue
                if "employee_type" in f and f["employee_type"] and str(rec.get("employee_type", "")).lower() != f["employee_type"]:
                    continue
                if "department_id" in f and f["department_id"] and rec.get("department_id") != f["department_id"]:
                    continue
                if "location_id" in f and f["location_id"] and rec.get("location_id") != f["location_id"]:
                    continue
                if "job_title" in f and f["job_title"] and rec.get("job_title") != f["job_title"]:
                    continue
                if "tax_id" in f and f["tax_id"] and rec.get("tax_id") != f["tax_id"]:
                    continue
                if "work_email" in f and f["work_email"] and rec.get("work_email") != f["work_email"]:
                    continue
                if "phone_number" in f and f["phone_number"] and rec.get("phone_number") != f["phone_number"]:
                    continue
                if "manager_id" in f and f["manager_id"] and rec.get("manager_id") != f["manager_id"]:
                    continue
                if "tax_filing_status" in f and f["tax_filing_status"] and str(rec.get("tax_filing_status", "")).lower() != f["tax_filing_status"]:
                    continue
                if "employment_status" in f and f["employment_status"] and str(rec.get("employment_status", "")).lower() != f["employment_status"]:
                    continue
                # date ranges
                if not _range_match(rec.get("start_date"), f.get("start_date_from"), f.get("start_date_to")):
                    continue
                items.append(DiscoverEmployeeEntities._mask_employee(rec))

        else:  # onboarding_checklists
            onb = data.get("onboarding_checklists", {})
            for _, rec in onb.items():
                if "checklist_id" in f and f["checklist_id"] and rec.get("checklist_id") != f["checklist_id"]:
                    continue
                if "employee_id" in f and f["employee_id"] and rec.get("employee_id") != f["employee_id"]:
                    continue
                if "position" in f and f["position"] and rec.get("position") != f["position"]:
                    continue
                if "hiring_manager_id" in f and f["hiring_manager_id"] and rec.get("hiring_manager_id") != f["hiring_manager_id"]:
                    continue
                if "pre_onboarding_status" in f and f["pre_onboarding_status"] and \
                        str(rec.get("pre_onboarding_status", "")).lower() != f["pre_onboarding_status"]:
                    continue
                if "background_check_status" in f and f["background_check_status"] and \
                        str(rec.get("background_check_status", "")).lower() != f["background_check_status"]:
                    continue
                if "document_verification_status" in f and f["document_verification_status"] and \
                        str(rec.get("document_verification_status", "")).lower() != f["document_verification_status"]:
                    continue
                if "it_provisioning_status" in f and f["it_provisioning_status"] and \
                        str(rec.get("it_provisioning_status", "")).lower() != f["it_provisioning_status"]:
                    continue
                if "benefits_enrollment_status" in f and f["benefits_enrollment_status"] and \
                        str(rec.get("benefits_enrollment_status", "")).lower() != f["benefits_enrollment_status"]:
                    continue
                if "overall_status" in f and f["overall_status"] and \
                        str(rec.get("overall_status", "")).lower() != f["overall_status"]:
                    continue
                if "orientation_completed" in f and f["orientation_completed"] is not None:
                    # record may be boolean or string
                    rec_val = rec.get("orientation_completed")
                    if isinstance(rec_val, str):
                        rv = DiscoverEmployeeEntities._normalize_bool_like(rec_val)
                    else:
                        rv = bool(rec_val) if rec_val is not None else None
                    if rv is None or rv != f["orientation_completed"]:
                        continue
                # date ranges
                if not _range_match(rec.get("start_date"), f.get("start_date_from"), f.get("start_date_to")):
                    continue
                items.append(rec)

        return json.dumps(_paginate(items, limit, offset))

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_employee_entities",
                "description": "Discover employees (masked) or onboarding_checklists using SOP/DB-compliant filters.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "enum": ["employees", "onboarding_checklists"]
                        },
                        "filters": {
                            "type": "object",
                            "description": "Allowed keys depend on entity_type.",
                            "properties": {
                                # employees
                                "employee_id": {"type": "string"},
                                "candidate_id": {"type": "string"},
                                "first_name": {"type": "string"},
                                "last_name": {"type": "string"},
                                "employee_type": {"type": "string"},
                                "department_id": {"type": "string"},
                                "location_id": {"type": "string"},
                                "job_title": {"type": "string"},
                                "start_date_from": {"type": "string", "description": "MM-DD-YYYY"},
                                "start_date_to": {"type": "string", "description": "MM-DD-YYYY"},
                                "tax_id": {"type": "string"},
                                "work_email": {"type": "string"},
                                "phone_number": {"type": "string"},
                                "manager_id": {"type": "string"},
                                "tax_filing_status": {"type": "string"},
                                "employment_status": {"type": "string"},

                                # onboarding_checklists
                                "checklist_id": {"type": "string"},
                                "employee_id": {"type": "string"},
                                "start_date_from": {"type": "string", "description": "MM-DD-YYYY"},
                                "start_date_to": {"type": "string", "description": "MM-DD-YYYY"},
                                "position": {"type": "string"},
                                "hiring_manager_id": {"type": "string"},
                                "pre_onboarding_status": {"type": "string"},
                                "background_check_status": {"type": "string"},
                                "document_verification_status": {"type": "string"},
                                "it_provisioning_status": {"type": "string"},
                                "orientation_completed": {"type": "boolean"},
                                "benefits_enrollment_status": {"type": "string"},
                                "overall_status": {"type": "string"},
                            },
                            "additionalProperties": False
                        },
                        "limit": {"type": "integer", "minimum": 1, "default": 50},
                        "offset": {"type": "integer", "minimum": 0, "default": 0},
                    },
                    "required": ["entity_type"]
                }
            }
        }


def discover_employee_entities(data: Dict[str, Any], **kwargs) -> str:
    return DiscoverEmployeeEntities.invoke(data, **kwargs)
