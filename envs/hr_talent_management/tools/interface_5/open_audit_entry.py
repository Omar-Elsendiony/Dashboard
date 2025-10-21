import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class OpenAuditEntry(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], reference_id: str, reference_type: str, action: str, user_id: str, field_name: Optional[str] = None, old_value: Optional[str] = None, new_value: Optional[str] = None) -> str:
        """
        Create an audit trail entry to track changes and actions in the HR system.
        
        Args:
            reference_id: ID of the entity being audited
            reference_type: Type of entity (user, location, department, job_requisition, etc.)
            action: Action performed (create, update, delete, approve, reject, etc.)
            user_id: ID of the user performing the action
            field_name: Optional field name being changed
            old_value: Optional old value of the field
            new_value: Optional new value of the field
        """
        
        def generate_audit_id(audit_trails: Dict[str, Any]) -> int:
            if not audit_trails:
                return 1
            return max(int(k) for k in audit_trails.keys()) + 1
        
        # Validate required fields
        required_values = {
            "reference_id": reference_id,
            "reference_type": reference_type,
            "action": action,
            "user_id": user_id
        }
        missing_fields = [field for field, value in required_values.items() if not value]
        if missing_fields:
            return json.dumps({
                "success": False,
                "audit_id": None,
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            })
        
        # Access related data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "audit_id": None,
                "message": "Invalid data format for audit operations"
            })
        
        users = data.get("users", {})
        audit_trails = data.get("audit_trails", {})
        
        # Validate user exists and is active
        user_str = str(user_id)
        if user_str not in users:
            return json.dumps({
                "success": False,
                "audit_id": None,
                "message": f"User {user_id} not found"
            })
        
        user = users[user_str]
        if user.get("employment_status") != "active":
            return json.dumps({
                "success": False,
                "audit_id": None,
                "message": f"User {user_id} is not active"
            })
        
        # Validate reference_type enum
        valid_reference_types = [
            "user", "location", "department", "job_requisition", "job_posting", 
            "candidate", "application", "interview", "interview_panel_member", 
            "offer", "offer_benefit", "employee", "onboarding_checklist", 
            "document", "it_provisioning_task", "payroll_cycle", "payroll_input", 
            "payroll_earning", "benefit_plan", "benefit_enrollment", "payslip", 
            "payment", "employee_exit", "notification"
        ]
        
        if reference_type not in valid_reference_types:
            return json.dumps({
                "success": False,
                "audit_id": None,
                "message": f"Invalid reference_type '{reference_type}'. Must be one of: {', '.join(valid_reference_types)}"
            })
        
        # Validate action enum
        valid_actions = [
            "create", "update", "delete", "approve", "reject", "lock", 
            "unlock", "submit", "verify"
        ]
        
        if action not in valid_actions:
            return json.dumps({
                "success": False,
                "audit_id": None,
                "message": f"Invalid action '{action}'. Must be one of: {', '.join(valid_actions)}"
            })
        
        # Generate new audit ID and create record
        new_audit_id = generate_audit_id(audit_trails)
        timestamp = "2025-10-10T12:00:00"
        
        new_audit_entry = {
            "audit_id": str(new_audit_id),
            "reference_id": reference_id,
            "reference_type": reference_type,
            "action": action,
            "user_id": user_id,
            "field_name": field_name,
            "old_value": old_value,
            "new_value": new_value,
            "created_at": timestamp
        }
        
        audit_trails[str(new_audit_id)] = new_audit_entry
        
        return json.dumps({
            "success": True,
            "audit_id": str(new_audit_id),
            "message": f"Audit entry {new_audit_id} created successfully",
            "audit_log": new_audit_entry
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "open_audit_entry",
                "description": "Create an audit trail entry to track changes and actions in the HR system. This tool logs all system activities for compliance and audit purposes. The requesting user must be active in the system. Use this tool after any create, update, delete, approve, reject, or other system operations to maintain a complete audit trail.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reference_id": {
                            "type": "string",
                            "description": "ID of the entity being audited (e.g., '123' for user_id, '1' for requisition_id, etc.)"
                        },
                        "reference_type": {
                            "type": "string",
                            "description": "Type of entity being audited. MUST be one of these exact values: 'user', 'location', 'department', 'job_requisition', 'job_posting', 'candidate', 'application', 'interview', 'interview_panel_member', 'offer', 'offer_benefit', 'employee', 'onboarding_checklist', 'document', 'it_provisioning_task', 'payroll_cycle', 'payroll_input', 'payroll_earning', 'benefit_plan', 'benefit_enrollment', 'payslip', 'payment', 'employee_exit', 'notification'"
                        },
                        "action": {
                            "type": "string",
                            "description": "Action performed on the entity. MUST be one of these exact values: 'create' (for new records), 'update' (for modifications), 'delete' (for removals), 'approve' (for approvals), 'reject' (for rejections), 'lock' (for locking records), 'unlock' (for unlocking records), 'submit' (for submissions), 'verify' (for verifications)"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "ID of the user performing the action. The user MUST exist in the system and have employment_status = 'active'"
                        },
                        "field_name": {
                            "type": "string",
                            "description": "Optional: Name of the specific field being changed (e.g., 'status', 'salary', 'department_id'). Only required for field-level change tracking."
                        },
                        "old_value": {
                            "type": "string",
                            "description": "Optional: Previous value of the field before the change. Only used when tracking specific field changes."
                        },
                        "new_value": {
                            "type": "string",
                            "description": "Optional: New value of the field after the change. Only used when tracking specific field changes."
                        }
                    },
                    "required": ["reference_id", "reference_type", "action", "user_id"]
                }
            }
        }
