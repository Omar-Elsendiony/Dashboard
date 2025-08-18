import json
from typing import Any, Dict, Optional, Union
from tau_bench.envs.tool import Tool

class UpdateAnalysisFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], analysis_fund_id: str, analysis_field_name: str, field_value: Union[str, int, float],
               fund_manager_approval: bool, compliance_review_required: Optional[bool] = None,
               compliance_officer_approval: Optional[bool] = None) -> str:

        if not fund_manager_approval:
            return json.dumps({"error": "Fund Manager approval required. Process halted."})
        
        if compliance_review_required and not compliance_officer_approval:
            return json.dumps({"error": "Compliance Officer approval required for this change. Process halted."})
        
        funds = data.get("funds", {})
        users = data.get("users", {})
        
        # Validate fund exists
        if str(analysis_fund_id) not in funds:
            return json.dumps({"error": f"Fund {analysis_fund_id} not found"})
        
        fund = funds[str(analysis_fund_id)]
        
        # Validate field against allowed fields and values
        allowed_fields = ["name", "fund_type", "manager_id", "size", "status"]
        valid_fund_types = ["mutual_funds", "exchange_traded_funds", "pension_funds", 
                           "private_equity_funds", "hedge_funds", "sovereign_wealth_funds", 
                           "money_market_funds", "real_estate_investment_trusts", 
                           "infrastructure_funds", "multi_asset_funds"]
        valid_statuses = ["open", "closed"]

        # Validate field name
        if analysis_field_name not in allowed_fields:
            return json.dumps({"error": f"Field '{analysis_field_name}' is not allowed to be updated"})

        # Validate specific field values
        if analysis_field_name == "fund_type" and field_value not in valid_fund_types:
            return json.dumps({"error": f"Invalid fund_type. Must be one of {valid_fund_types}"})

        if analysis_field_name == "status" and field_value not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}"})

        if analysis_field_name == "manager_id" and str(field_value) not in users:
            return json.dumps({"error": f"Manager {field_value} not found"})

        if analysis_field_name == "size" and (not isinstance(field_value, (int, float)) or field_value < 0):
            return json.dumps({"error": "Fund size must be a non-negative number"})
        
        # Apply change
        timestamp = "2025-10-01T00:00:00"
        original_value = fund.get(analysis_field_name)
        
        # Update the field
        fund[analysis_field_name] = field_value
        fund["updated_at"] = timestamp
        
        # Create audit trail entry
        audit_trails = data.get("audit_trails", {})
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        # Only create audit trail if analysis_value actually changed
        if original_value != field_value:
            analysis_audit_id = generate_id(audit_trails)
            audit_record = {
                "audit_trail_id": analysis_audit_id,
                "analysis_reference_id": int(analysis_fund_id),
                "analysis_reference_type": "fund",
                "analysis_action": "update",
                "analysis_user_id": fund.get("manager_id", 1),  # Use manager as the updating user
                "analysis_field_name": analysis_field_name,
                "analysis_old_value": str(original_value) if original_value is not None else None,
                "analysis_new_value": str(field_value) if field_value is not None else None,
                "created_at": timestamp
            }
            audit_trails[str(analysis_audit_id)] = audit_record
        
        return json.dumps({
            "success": True, 
            "message": "Fund updated successfully",
            "analysis_fund_id": analysis_fund_id,
            "updated_field": analysis_field_name,
            "analysis_old_value": original_value,
            "analysis_new_value": field_value
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
                        "analysis_fund_id": {"type": "string", "description": "ID of the fund to update"},
                        "analysis_field_name": {
                            "type": "string", 
                            "description": "Name of the field to update",
                            "enum": ["name", "fund_type", "manager_id", "size", "status"]
                        },
                        "field_value": {
                            "description": "New analysis_value for the field (string, number, or boolean depending on field type)"
                        },
                        "fund_manager_approval": {"type": "boolean", "description": "Fund manager approval required (True or False)"},
                        "compliance_review_required": {"type": "boolean", "description": "Whether compliance review is required for this change (True for all changes)"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance officer approval (required if compliance_review_required is true). Its analysis_value is True"}
                    },
                    "required": ["analysis_fund_id", "analysis_field_name", "field_value", "fund_manager_approval"]
                }
            }
        }