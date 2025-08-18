import json
from typing import Any, Dict, Optional, Union
from tau_bench.envs.tool import Tool

class UpdateFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, field_name: str, field_value: Union[str, int, float],
               fund_manager_approval: bool, compliance_review_required: Optional[bool] = None,
               compliance_officer_approval: Optional[bool] = None) -> str:

        if not fund_manager_approval:
            return json.dumps({"error": "Fund Manager approval required. Process halted."})
        
        if compliance_review_required and not compliance_officer_approval:
            return json.dumps({"error": "Compliance Officer approval required for this change. Process halted."})
        
        funds = data.get("funds", {})
        users = data.get("users", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        fund = funds[str(fund_id)]
        
        # Validate field against allowed fields and values
        allowed_fields = ["name", "fund_type", "manager_id", "size", "status"]
        valid_fund_types = ["mutual_funds", "exchange_traded_funds", "pension_funds", 
                           "private_equity_funds", "hedge_funds", "sovereign_wealth_funds", 
                           "money_market_funds", "real_estate_investment_trusts", 
                           "infrastructure_funds", "multi_asset_funds"]
        valid_statuses = ["open", "closed"]

        # Validate field name
        if field_name not in allowed_fields:
            return json.dumps({"error": f"Field '{field_name}' is not allowed to be updated"})

        # Validate specific field values
        if field_name == "fund_type" and field_value not in valid_fund_types:
            return json.dumps({"error": f"Invalid fund_type. Must be one of {valid_fund_types}"})

        if field_name == "status" and field_value not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}"})

        if field_name == "manager_id" and str(field_value) not in users:
            return json.dumps({"error": f"Manager {field_value} not found"})

        if field_name == "size" and (not isinstance(field_value, (int, float)) or field_value < 0):
            return json.dumps({"error": "Fund size must be a non-negative number"})
        
        # Apply change
        timestamp = "2025-10-01T00:00:00"
        original_value = fund.get(field_name)
        
        # Update the field
        fund[field_name] = field_value
        fund["updated_at"] = timestamp
        
        # Create audit trail entry
        audit_trails = data.get("audit_trails", {})
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        # Only create audit trail if value actually changed
        if original_value != field_value:
            audit_id = generate_id(audit_trails)
            audit_record = {
                "audit_trail_id": audit_id,
                "reference_id": int(fund_id),
                "reference_type": "fund",
                "action": "update",
                "user_id": fund.get("manager_id", 1),  # Use manager as the updating user
                "field_name": field_name,
                "old_value": str(original_value) if original_value is not None else None,
                "new_value": str(field_value) if field_value is not None else None,
                "created_at": timestamp
            }
            audit_trails[str(audit_id)] = audit_record
        
        return json.dumps({
            "success": True, 
            "message": "Fund updated successfully",
            "fund_id": fund_id,
            "updated_field": field_name,
            "old_value": original_value,
            "new_value": field_value
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_fund",
                "description": "Update a single fund field with required approvals and audit trail",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund to update"},
                        "field_name": {
                            "type": "string", 
                            "description": "Name of the field to update",
                            "enum": ["name", "fund_type", "manager_id", "size", "status"]
                        },
                        "field_value": {
                            "description": "New value for the field (string, number, or boolean depending on field type)"
                        },
                        "fund_manager_approval": {"type": "boolean", "description": "Fund manager approval required (True or False)"},
                        "compliance_review_required": {"type": "boolean", "description": "Whether compliance review is required for this change (True for all changes)"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance officer approval (required if compliance_review_required is true). Its value is True"}
                    },
                    "required": ["fund_id", "field_name", "field_value", "fund_manager_approval"]
                }
            }
        }