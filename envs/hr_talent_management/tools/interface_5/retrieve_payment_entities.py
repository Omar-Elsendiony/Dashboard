import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool


class RetrievePaymentEntities(Tool):
    @staticmethod
    def invoke(
            data: Dict[str, Any],
            entity_type: str,
            filters: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Discover payment-related entities with optional filtering.

        Entity Types:
        - payslips: Discover payslips with employee/cycle/status and numeric/date range filters
        - payments: Discover payments with employee/cycle/method/status and amount/date filters
        """

        def matches_filter(entity: Dict[str, Any], filter_key: str, filter_value: Any) -> bool:
            """Check if an entity matches a specific filter key/value."""
            # Range: date (YYYY-MM-DD format comparison)
            if filter_key.endswith("_from") or filter_key.endswith("_to"):
                base_key = filter_key.replace("_from", "").replace("_to", "")
                entity_value = entity.get(base_key)
                if entity_value is None:
                    return False
                if filter_key.endswith("_from"):
                    # Check if entity date is greater than or equal to filter date
                    return entity_value >= filter_value
                # Check if entity date is less than or equal to filter date
                return entity_value <= filter_value

            # Range: numeric (min/max)
            if filter_key.endswith("_min") or filter_key.endswith("_max"):
                base_key = filter_key.replace("_min", "").replace("_max", "")
                entity_value = entity.get(base_key)
                if entity_value is None:
                    return False
                if filter_key.endswith("_min"):
                    # Check if entity value is greater than or equal to filter value
                    return entity_value >= filter_value
                # Check if entity value is less than or equal to filter value
                return entity_value <= filter_value

            # Exact match (case-insensitive for strings)
            entity_value = entity.get(filter_key)
            if isinstance(filter_value, str) and isinstance(entity_value, str):
                return entity_value.lower() == filter_value.lower()
            return entity_value == filter_value

        def validate_filter_conflicts(filters: Dict[str, Any]) -> Optional[str]:
            """Validate that paired range filters are not conflicting."""
            if not filters:
                return None

            conflicts: List[str] = []

            # Date ranges
            for base in [
                "released_date",
                "payment_date",
            ]:
                from_key = f"{base}_from"
                to_key = f"{base}_to"
                if from_key in filters and to_key in filters:
                    if filters[from_key] > filters[to_key]:
                        conflicts.append(f"{base} range: {filters[from_key]} > {filters[to_key]}")

            # Numeric ranges
            for base in [
                "gross_pay",
                "base_salary",
                "total_deductions",
                "net_pay",
                "amount",
            ]:
                min_key = f"{base}_min"
                max_key = f"{base}_max"
                if min_key in filters and max_key in filters:
                    # Note: Numeric values are compared directly
                    if filters[min_key] > filters[max_key]:
                        conflicts.append(f"{base} range: {filters[min_key]} > {filters[max_key]}")

            if conflicts:
                return "Halt: Search parameters result in ambiguous or conflicting results: " + ", ".join(conflicts)
            return None

        def apply_filters(
                entities: Dict[str, Any], valid_filters: List[str], filters: Dict[str, Any]
        ) -> Dict[str, Any]:
            if not filters:
                return entities

            # 1. Validate conflicts first
            conflict_error = validate_filter_conflicts(filters)
            if conflict_error:
                return {"error": conflict_error}

            # 2. Validate filter keys
            invalid = [k for k in filters.keys() if k not in valid_filters]
            if invalid:
                return {
                    "error": (
                            "Halt: Discovery tool execution failed due to system errors - invalid filter keys: "
                            + ", ".join(invalid)
                            + ". Valid filters are: "
                            + ", ".join(valid_filters)
                    )
                }

            # 3. Apply filters
            filtered: Dict[str, Any] = {}
            for entity_id, entity in entities.items():
                include = True
                for k, v in filters.items():
                    if not matches_filter(entity, k, v):
                        include = False
                        break
                if include:
                    filtered[entity_id] = entity
            return filtered

        if not isinstance(data, dict):
            return json.dumps(
                {
                    "success": False,
                    "error": "Halt: Discovery tool execution failed due to system errors - invalid data format",
                }
            )

        if entity_type not in ["payslips", "payments"]:
            return json.dumps(
                {
                    "success": False,
                    "error": "Halt: Missing entity_type or invalid entity_type - must be one of: payslips, payments",
                }
            )

        if entity_type == "payslips":
            entities = data.get("payslips", {})
            valid_filters = [
                "payslip_id",
                "employee_id",
                "cycle_id",
                "gross_pay_min",
                "gross_pay_max",
                "base_salary_min",
                "base_salary_max",
                "total_deductions_min",
                "total_deductions_max",
                "net_pay_min",
                "net_pay_max",
                "proration_status",
                "payslip_status",
                "released_date_from",
                "released_date_to",
            ]

            if filters:
                filtered_entities = apply_filters(entities, valid_filters, filters)
                if "error" in filtered_entities:
                    return json.dumps({"success": False, "error": filtered_entities["error"]})
                entities = filtered_entities

            return json.dumps(
                {
                    "success": True,
                    "entity_type": "payslips",
                    "count": len(entities),
                    "payslips": entities,
                    "filters_applied": filters or {},
                }
            )

        # entity_type == "payments"
        entities = data.get("payments", {})
        valid_filters = [
            "payment_id",
            "employee_id",
            "cycle_id",
            "payslip_id",
            "amount_min",
            "amount_max",
            "payment_date_from",
            "payment_date_to",
            "payment_method",
            "payment_status",
            "transaction_id",
        ]

        if filters:
            filtered_entities = apply_filters(entities, valid_filters, filters)
            if "error" in filtered_entities:
                return json.dumps({"success": False, "error": filtered_entities["error"]})
            entities = filtered_entities

        return json.dumps(
            {
                "success": True,
                "entity_type": "payments",
                "count": len(entities),
                "payments": entities,
                "filters_applied": filters or {},
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_payment_entities",
                "description": "Discover and filter payment-related entities (payslips, payments) in the HR talent management system. Supports exact, numeric range, and date range filters for reporting and analysis. Entity types: 'payslips' (payslip_status: draft, generated, verified, released, archived; proration_status: not_applicable, applied, none), 'payments' (payment_method: bank_transfer, check, cash; payment_status: pending, processed, failed, reversed).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of payment entity to discover",
                            "enum": ["payslips", "payments"],
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters. For payslips: payslip_id, employee_id, cycle_id, gross_pay_min, gross_pay_max, base_salary_min, base_salary_max, total_deductions_min, total_deductions_max, net_pay_min, net_pay_max, proration_status, payslip_status, released_date_from, released_date_to. For payments: payment_id, employee_id, cycle_id, payslip_id, amount_min, amount_max, payment_date_from, payment_date_to, payment_method, payment_status, transaction_id. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                # Payslips filters
                                "payslip_id": {"type": "string", "description": "Exact payslip ID"},
                                "employee_id": {"type": "string", "description": "Employee ID"},
                                "cycle_id": {"type": "string", "description": "Payroll cycle ID"},
                                "gross_pay_min": {"type": "number", "description": "Minimum gross pay"},
                                "gross_pay_max": {"type": "number", "description": "Maximum gross pay"},
                                "base_salary_min": {"type": "number", "description": "Minimum base salary"},
                                "base_salary_max": {"type": "number", "description": "Maximum base salary"},
                                "total_deductions_min": {"type": "number", "description": "Minimum total deductions"},
                                "total_deductions_max": {"type": "number", "description": "Maximum total deductions"},
                                "net_pay_min": {"type": "number", "description": "Minimum net pay"},
                                "net_pay_max": {"type": "number", "description": "Maximum net pay"},
                                "proration_status": {"type": "string", "description": "Proration status", "enum": ["not_applicable", "applied", "none"]},
                                "payslip_status": {"type": "string", "description": "Payslip status", "enum": ["draft", "generated", "verified", "released", "archived"]},
                                "released_date_from": {"type": "string", "description": "Released date from (YYYY-MM-DD)"},
                                "released_date_to": {"type": "string", "description": "Released date to (YYYY-MM-DD)"},

                                # Payments filters
                                "payment_id": {"type": "string", "description": "Exact payment ID"},
                                "payslip_id": {"type": "string", "description": "Payslip ID"},
                                "amount_min": {"type": "number", "description": "Minimum amount"},
                                "amount_max": {"type": "number", "description": "Maximum amount"},
                                "payment_date_from": {"type": "string", "description": "Payment date from (YYYY-MM-DD)"},
                                "payment_date_to": {"type": "string", "description": "Payment date to (YYYY-MM-DD)"},
                                "payment_method": {"type": "string", "description": "Payment method", "enum": ["bank_transfer", "check", "cash"]},
                                "payment_status": {"type": "string", "description": "Payment status", "enum": ["pending", "processed", "failed", "reversed"]},
                                "transaction_id": {"type": "string", "description": "Transaction ID"},
                            },
                        },
                    },
                    "required": ["entity_type"],
                },
            },
        }
