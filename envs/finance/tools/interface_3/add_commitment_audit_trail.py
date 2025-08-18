import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddCommitmentAuditTrail(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_reference_id: str, commitment_reference_type: str,
               commitment_action: str, commitment_field_name: Optional[str] = None,
               commitment_old_value: Optional[str] = None, commitment_new_value: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        audit_trails = data.get("audit_trails", {})        
        
        # Validate commitment_reference_type
        valid_reference_types = [
            "user", "fund", "investor", "subscription", "commitment", "redemption",
            "trade", "portfolio", "holding", "instrument", "invoice", "payment",
            "document", "report", "nav", "notification"
        ]
        if commitment_reference_type not in valid_reference_types:
            raise ValueError(f"Invalid commitment_reference_type. Must be one of {valid_reference_types}")
        
        # Validate commitment_action
        valid_actions = ["create", "update", "delete", "approve", "cancel", "process"]
        if commitment_action not in valid_actions:
            raise ValueError(f"Invalid commitment_action. Must be one of {valid_actions}")
        
        # Business rule validation
        if commitment_action in ["create", "delete"] and commitment_field_name is not None:
            raise ValueError(f"commitment_field_name should be null for {commitment_action} actions")
        
        if commitment_action == "create" and commitment_old_value is not None:
            raise ValueError("commitment_old_value should be null for create actions")
        
        if commitment_action == "delete" and commitment_new_value is not None:
            raise ValueError("commitment_new_value should be null for delete actions")
        
        # Validate that the referenced entity exists based on commitment_reference_type
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
        
        reference_table = reference_tables.get(commitment_reference_type)
        if reference_table and reference_table in data:
            if str(commitment_reference_id) not in data[reference_table]:
                raise ValueError(f"{commitment_reference_type.title()} {commitment_reference_id} not found")
        
        audit_trail_id = generate_id(audit_trails)
        timestamp = "2025-10-01T00:00:00"
        
        new_audit_trail = {
            "audit_trail_id": audit_trail_id,
            "commitment_reference_id": commitment_reference_id,
            "commitment_reference_type": commitment_reference_type,
            "commitment_action": commitment_action,
            "commitment_field_name": commitment_field_name,
            "commitment_old_value": commitment_old_value,
            "commitment_new_value": commitment_new_value,
            "created_at": timestamp
        }
        
        audit_trails[str(audit_trail_id)] = new_audit_trail
        return json.dumps(new_audit_trail)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_audit_trail",
                "description": "Add an audit trail record to track changes made to database records",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_reference_id": {"type": "string", "description": "ID of the record that was changed"},
                        "commitment_reference_type": {"type": "string", "description": "Type of record being audited (user, fund, investor, subscription, commitment, redemption, trade, portfolio, holding, instrument, invoice, payment, document, report, nav, notification)"},
                        "commitment_action": {"type": "string", "description": "Action performed (create, update, delete, approve, cancel, process)"},
                        "commitment_field_name": {"type": "string", "description": "Name of the field that was changed (null for create/delete actions)"},
                        "commitment_old_value": {"type": "string", "description": "Previous value of the field (null for create actions)"},
                        "commitment_new_value": {"type": "string", "description": "New value of the field (null for delete actions)"}
                    },
                    "required": ["commitment_reference_id", "commitment_reference_type", "commitment_action"]
                }
            }
        }