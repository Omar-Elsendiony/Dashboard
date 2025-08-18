import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddFundAuditTrail(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_reference_id: str, fund_reference_type: str,
               fund_audit_action: str, fund_field_name: Optional[str] = None,
               fund_old_value: Optional[str] = None, fund_new_value: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        audit_trails = data.get("audit_trails", {})        
        
        # Validate reference_type
        valid_reference_types = [
            "user", "fund", "investor", "subscription", "commitment", "redemption",
            "trade", "portfolio", "holding", "instrument", "invoice", "payment",
            "document", "report", "nav", "notification"
        ]
        if fund_reference_type not in valid_reference_types:
            raise ValueError(f"Invalid reference_type. Must be one of {valid_reference_types}")
        
        # Validate action
        valid_actions = ["create", "update", "delete", "approve", "cancel", "process"]
        if fund_audit_action not in valid_actions:
            raise ValueError(f"Invalid action. Must be one of {valid_actions}")
        
        # Business rule validation
        if fund_audit_action in ["create", "delete"] and fund_field_name is not None:
            raise ValueError(f"field_name should be null for {fund_audit_action} actions")
        
        if fund_audit_action == "create" and fund_old_value is not None:
            raise ValueError("old_value should be null for create actions")
        
        if fund_audit_action == "delete" and fund_new_value is not None:
            raise ValueError("new_value should be null for delete actions")
        
        # Validate that the referenced entity exists based on reference_type
        reference_tables = {
            "user": "users",
            "fund": "funds",
            "investor": "investors",
            "subscription": "subscriptions",
            "commitment": "commitments",
            "redemption": "redemptions",
            "trade": "trades",
            "portfolio": "portfolios",
            "holding": "portfolio_holdings",
            "instrument": "instruments",
            "invoice": "invoices",
            "payment": "payments",
            "document": "documents",
            "report": "reports",
            "nav": "nav_records",
            "notification": "notifications"
        }
        
        reference_table = reference_tables.get(fund_reference_type)
        if reference_table and reference_table in data:
            if str(fund_reference_id) not in data[reference_table]:
                raise ValueError(f"{fund_reference_type.title()} {fund_reference_id} not found")
        
        audit_trail_id = generate_id(audit_trails)
        timestamp = "2025-10-01T00:00:00"
        
        new_audit_trail = {
            "audit_trail_id": audit_trail_id,
            "reference_id": fund_reference_id,
            "reference_type": fund_reference_type,
            "action": fund_audit_action,
            "field_name": fund_field_name,
            "old_value": fund_old_value,
            "new_value": fund_new_value,
            "created_at": timestamp
        }
        
        audit_trails[str(audit_trail_id)] = new_audit_trail
        return json.dumps(new_audit_trail)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_fund_audit_trail",
                "description": "Add an audit trail record for Fund Management & Trading Operations to track changes made to database records",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_reference_id": {"type": "string", "description": "ID of the fund-related record that was changed"},
                        "fund_reference_type": {"type": "string", "description": "Type of record being audited (user, fund, investor, subscription, commitment, redemption, trade, portfolio, holding, instrument, invoice, payment, document, report, nav, notification)"},
                        "fund_audit_action": {"type": "string", "description": "Fund management action performed (create, update, delete, approve, cancel, process)"},
                        "fund_field_name": {"type": "string", "description": "Name of the field that was changed (null for create/delete actions)"},
                        "fund_old_value": {"type": "string", "description": "Previous value of the field (null for create actions)"},
                        "fund_new_value": {"type": "string", "description": "New value of the field (null for delete actions)"}
                    },
                    "required": ["fund_reference_id", "fund_reference_type", "fund_audit_action"]
                }
            }
        }