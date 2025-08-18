import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddAnalysisAuditTrail(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], analysis_reference_id: str, analysis_reference_type: str,
               analysis_action: str, analysis_field_name: Optional[str] = None,
               analysis_old_value: Optional[str] = None, analysis_new_value: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        audit_trails = data.get("audit_trails", {})        
        
        # Validate analysis_reference_type
        valid_reference_types = [
            "user", "fund", "investor", "subscription", "commitment", "redemption",
            "trade", "portfolio", "holding", "instrument", "invoice", "payment",
            "document", "report", "nav", "notification"
        ]
        if analysis_reference_type not in valid_reference_types:
            raise ValueError(f"Invalid analysis_reference_type. Must be one of {valid_reference_types}")
        
        # Validate analysis_action
        valid_actions = ["create", "update", "delete", "approve", "cancel", "process"]
        if analysis_action not in valid_actions:
            raise ValueError(f"Invalid analysis_action. Must be one of {valid_actions}")
        
        # Business rule validation
        if analysis_action in ["create", "delete"] and analysis_field_name is not None:
            raise ValueError(f"analysis_field_name should be null for {analysis_action} actions")
        
        if analysis_action == "create" and analysis_old_value is not None:
            raise ValueError("analysis_old_value should be null for create actions")
        
        if analysis_action == "delete" and analysis_new_value is not None:
            raise ValueError("analysis_new_value should be null for delete actions")
        
        # Validate that the referenced entity exists based on analysis_reference_type
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
        
        reference_table = reference_tables.get(analysis_reference_type)
        if reference_table and reference_table in data:
            if str(analysis_reference_id) not in data[reference_table]:
                raise ValueError(f"{analysis_reference_type.title()} {analysis_reference_id} not found")
        
        audit_trail_id = generate_id(audit_trails)
        timestamp = "2025-10-01T00:00:00"
        
        new_audit_trail = {
            "audit_trail_id": audit_trail_id,
            "analysis_reference_id": analysis_reference_id,
            "analysis_reference_type": analysis_reference_type,
            "analysis_action": analysis_action,
            "analysis_field_name": analysis_field_name,
            "analysis_old_value": analysis_old_value,
            "analysis_new_value": analysis_new_value,
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
                        "analysis_reference_id": {"type": "string", "description": "ID of the record that was changed"},
                        "analysis_reference_type": {"type": "string", "description": "Type of record being audited (user, fund, investor, subscription, commitment, redemption, trade, portfolio, holding, instrument, invoice, payment, document, report, nav, notification)"},
                        "analysis_action": {"type": "string", "description": "Action performed (create, update, delete, approve, cancel, process)"},
                        "analysis_field_name": {"type": "string", "description": "Name of the field that was changed (null for create/delete actions)"},
                        "analysis_old_value": {"type": "string", "description": "Previous analysis_value of the field (null for create actions)"},
                        "analysis_new_value": {"type": "string", "description": "New analysis_value of the field (null for delete actions)"}
                    },
                    "required": ["analysis_reference_id", "analysis_reference_type", "analysis_action"]
                }
            }
        }