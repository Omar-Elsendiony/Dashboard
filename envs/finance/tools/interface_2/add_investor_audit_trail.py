import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddInvestorAuditTrail(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_reference_id: str, investor_reference_type: str,
               investor_action: str, investor_field_name: Optional[str] = None,
               investor_old_value: Optional[str] = None, investor_new_value: Optional[str] = None) -> str:
        
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
        if investor_reference_type not in valid_reference_types:
            raise ValueError(f"Invalid reference_type '{investor_reference_type}'. Valid types: {valid_reference_types}")
        
        # Validate action is among allowed actions
        valid_actions = ["create", "update", "delete"]
        if investor_action not in valid_actions:
            raise ValueError(f"Invalid action '{investor_action}'. Valid actions: {valid_actions}")
        
        # Validate parameter consistency
        if investor_action in ["create", "delete"] and investor_field_name is not None:
            raise ValueError(f"field_name should be null for {investor_action} actions")
        
        if investor_action == "create" and investor_old_value is not None:
            raise ValueError("old_value should be null for create actions")
        
        if investor_action == "delete" and investor_new_value is not None:
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
        
        reference_table = reference_tables.get(investor_reference_type)
        if reference_table:
            if str(investor_reference_id) not in data[reference_table]:
                raise ValueError(f"{investor_reference_type.title()} {investor_reference_id} not found")
        
        audit_trail_id = generate_id(audit_trails)
        timestamp = "2025-10-01T00:00:00"
        
        new_audit_trail = {
            "audit_trail_id": audit_trail_id,
            "reference_id": investor_reference_id,
            "reference_type": investor_reference_type,
            "action": investor_action,
            "field_name": investor_field_name,
            "old_value": investor_old_value,
            "new_value": investor_new_value,
            "created_at": timestamp
        }
        
        audit_trails[str(audit_trail_id)] = new_audit_trail
        return json.dumps(new_audit_trail)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "AddInvestorAuditTrail",
                "description": "Add an audit trail record to track changes made to database records",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reference_id": {"type": "string", "description": "ID of the record that was changed"},
                        "reference_type": {"type": "string", "description": "Type of record being audited (user, fund, investor, subscription, commitment, redemption, trade, portfolio, holding, instrument, invoice, payment, document, report, nav, notification)"},
                        "action": {"type": "string", "description": "Action performed (create, update, delete, approve, cancel, process)"},
                        "field_name": {"type": "string", "description": "Name of the field that was changed (null for create/delete actions)"},
                        "old_value": {"type": "string", "description": "Previous value of the field (null for create actions)"},
                        "new_value": {"type": "string", "description": "New value of the field (null for delete actions)"}
                    },
                    "required": ["reference_id", "reference_type", "action"]
                }
            }
        }