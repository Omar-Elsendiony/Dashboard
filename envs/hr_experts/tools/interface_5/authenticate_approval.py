import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AuthenticateApproval(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, requester_email: str) -> str:
        """
        Check approval for HR actions based on SOPs and approval data.
        
        Args:
            data: Environment data containing users and approvals
            action: The HR action being performed
            requester_email: Email of the user requesting the action  
        """
        # Define role authorization mapping based on SOPs
        role_authorizations = {
            "hr_director": [
                "user_provisioning", "create_department", "update_department", 
                "create_benefits_plan", "update_benefits_plan", "create_job_position", 
                "update_job_position", "skills_management", "job_position_skills_management"
            ],
            "hr_manager": [
                "employee_onboarding", "employee_offboarding", "performance_review_final_approval"
            ],
            "it_administrator": [
                "user_provisioning"
            ],
            "finance_officer": [
                "create_benefits_plan", "update_benefits_plan", "process_payroll_run", 
                "payroll_correction"
            ],
            "hiring_manager": [
                "create_job_position", "update_job_position", "job_position_skills_management",
                "manage_application_stage", "timesheet_approval", "timesheet_correction"
            ],
            "recruiter": [
                "manage_application_stage"
            ],
            "payroll_administrator": [
                "timesheet_approval", "timesheet_correction"
            ],
            "compliance_officer": [
                "employee_onboarding", "employee_offboarding"
            ]
        }
        
        # Define actions requiring multiple approvers (AND logic)
        and_approval_actions = {
            "employee_onboarding": ["hr_manager", "compliance_officer"],
            "employee_offboarding": ["hr_manager", "compliance_officer"]
        }
        
        # Define actions allowing alternative approvers (OR logic)  
        or_approval_actions = {
            "user_provisioning": ["hr_director", "it_administrator"],
            "create_benefits_plan": ["hr_director", "finance_officer"],
            "update_benefits_plan": ["hr_director", "finance_officer"],
            "create_job_position": ["hr_director", "hiring_manager"],
            "update_job_position": ["hr_director", "hiring_manager"],
            "job_position_skills_management": ["hr_director", "hiring_manager"],
            "manage_application_stage": ["recruiter", "hiring_manager"],
            "timesheet_approval": ["payroll_administrator", "hiring_manager"],
            "timesheet_correction": ["payroll_administrator", "hiring_manager"]
        }
        
        # Define simplified action to approval keyword mapping
        action_keywords = {
            "user_provisioning": ["user provisioning", "elevated roles"],
            "create_department": ["department creation"],
            "update_department": ["department update", "department manager"],
            "create_benefits_plan": ["benefits plan creation"],
            "update_benefits_plan": ["benefits plan update"],
            "create_job_position": ["job position", "publishable"],
            "update_job_position": ["job position", "publishable"],
            "job_position_skills_management": ["job position", "skills"],
            "manage_application_stage": ["application stage"],
            "employee_onboarding": ["onboarding"],
            "employee_offboarding": ["offboarding"],
            "timesheet_approval": ["timesheet approval"],
            "timesheet_correction": ["timesheet correction"],
            "process_payroll_run": ["payroll run"],
            "payroll_correction": ["payroll correction"],
            "performance_review_final_approval": ["performance review"],
            "skills_management": ["skills management"]
        }
        
        # Find the requester's role
        users = data.get("users", {})
        role_conducting_action = None
        
        for user in users.values():
            if user.get("email") == requester_email:
                role_conducting_action = user.get("role")
                break
        
        if not role_conducting_action:
            return json.dumps({
                "approval_valid": False,
                "error": f"No user found with email: {requester_email}"
            })
        
        # Check if role is directly authorized for the action (single approver actions)
        single_approver_actions = [
            "create_department", "update_department", "skills_management", 
            "process_payroll_run", "payroll_correction", "performance_review_final_approval"
        ]
        
        if action in single_approver_actions:
            authorized_roles = role_authorizations.get(role_conducting_action, [])
            if action in authorized_roles:
                return json.dumps({
                    "approval_valid": True,
                    "message": f"Role '{role_conducting_action}' is directly authorized for action '{action}'"
                })
            else:
                return json.dumps({
                    "approval_valid": False,
                    "error": f"Role '{role_conducting_action}' is not authorized for action '{action}'"
                })
        
        # For approval-based actions, check the approvals data
        approvals = data.get("approvals", {})
        
        # Find matching approvals using keywords
        matching_approvals = []
        keywords = action_keywords.get(action, [action])
        
        for approval in approvals.values():
            action_name = approval.get("action_name", "").lower()
            
            # Check if any keyword matches the approval action name
            for keyword in keywords:
                if keyword.lower() in action_name:
                    matching_approvals.append(approval)
                    break
        
        if not matching_approvals:
            return json.dumps({
                "approval_valid": False,
                "error": f"No approval found for action '{action}'"
            })
        
        # Extract approver roles from matching approvals
        approver_roles = []
        for approval in matching_approvals:
            approver_role = approval.get("approver_role")
            if approver_role:
                approver_roles.append(approver_role)
        
        # Check AND logic actions (require all specified roles)
        if action in and_approval_actions:
            required_roles = set(and_approval_actions[action])
            approved_roles = set(approver_roles)
            
            if required_roles.issubset(approved_roles):
                return json.dumps({
                    "approval_valid": True,
                    "approved_by": list(required_roles),
                    "message": f"All required approvals received from: {', '.join(required_roles)}"
                })
            else:
                missing_roles = required_roles - approved_roles
                return json.dumps({
                    "approval_valid": False,
                    "error": f"Missing required approvals from roles: {', '.join(missing_roles)}"
                })
        
        # Check OR logic actions (any of the specified roles is sufficient)
        elif action in or_approval_actions:
            allowed_roles = set(or_approval_actions[action])
            approved_roles = set(approver_roles)
            
            if allowed_roles.intersection(approved_roles):
                valid_approver = list(allowed_roles.intersection(approved_roles))[0]
                return json.dumps({
                    "approval_valid": True,
                    "approved_by": valid_approver,
                    "message": f"Approved by authorized role: {valid_approver}"
                })
            else:
                return json.dumps({
                    "approval_valid": False,
                    "error": f"No valid approval from authorized roles: {', '.join(allowed_roles)}"
                })
        
        return json.dumps({
            "approval_valid": False,
            "error": f"No valid approval found for action '{action}'"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "authenticate_approval",
                "description": "Authenticates role authorization and approval for HR management actions using requester email and approval codes. Actions include: user_provisioning (creating/updating user accounts with elevated roles), create_department/update_department (department management operations), create_benefits_plan/update_benefits_plan (benefits plan management), create_job_position/update_job_position (job position management), skills_management (managing skills catalog), job_position_skills_management (linking skills to positions), manage_application_stage (moving applications through hiring workflow), employee_onboarding (new employee setup), employee_offboarding (employee departure processing), timesheet_approval/timesheet_correction (timesheet management), process_payroll_run (payroll processing), payroll_correction (payroll adjustments), performance_review_final_approval (performance review finalization). Roles include: hr_director (senior HR leadership with broad permissions), hr_manager (HR operations management), it_administrator (IT system administration), finance_officer (financial operations), hiring_manager (department hiring authority), recruiter (talent acquisition), payroll_administrator (payroll operations), compliance_officer (regulatory compliance). Some actions require single approvers, others allow alternative approvers (OR logic), and some require multiple approvers (AND logic) based on company SOPs.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The HR action being performed: user_provisioning, create_department, update_department, create_benefits_plan, update_benefits_plan, create_job_position, update_job_position, skills_management, job_position_skills_management, manage_application_stage, employee_onboarding, employee_offboarding, timesheet_approval, timesheet_correction, process_payroll_run, payroll_correction, performance_review_final_approval"
                        },
                        "requester_email": {
                            "type": "string",
                            "description": "Email of the user requesting the action"
                        }
                    },
                    "required": ["action", "requester_email"]
                }
            }
        }