import json
import random
from datetime import datetime, timedelta

def generate_approvals(users_data, num_approvals=999):
    """
    Generate approval records for incident management actions.
    Approvals serve as fallback authorization for users who lack direct role authorization.
    
    Args:
        users_data: Dictionary of users with their roles
        num_approvals: Number of approval records to generate
    """
    
    # Single source of truth for all actions and their authorized roles
    ACTIONS = {
        "create_client": ["system_administrator", "incident_manager", "account_manager"],
        "update_client": ["system_administrator", "incident_manager", "account_manager"],
        "create_user": ["system_administrator", "incident_manager"],
        "update_user": ["system_administrator", "incident_manager"],
        "create_vendor": ["system_administrator", "incident_manager", "executive"],
        "update_vendor": ["system_administrator", "incident_manager", "executive"],
        "create_product": ["system_administrator", "incident_manager", "executive"],
        "update_product": ["system_administrator", "incident_manager", "executive"],
        "create_component": ["system_administrator", "technical_support", "incident_manager"],
        "update_component": ["system_administrator", "technical_support", "incident_manager"],
        "create_subscription": ["account_manager", "incident_manager", "executive"],
        "update_subscription": ["account_manager", "incident_manager", "executive"],
        "create_sla": ["account_manager", "system_administrator", "executive"],
        "update_sla": ["account_manager", "system_administrator", "executive"],
        "create_incident": ["incident_manager", "technical_support", "system_administrator", "executive"],
        "update_incident": ["incident_manager", "technical_support", "system_administrator", "executive"],
        "resolve_incident": ["incident_manager", "technical_support", "executive"],
        "close_incident": ["incident_manager", "executive"],
        "create_communication": ["incident_manager", "technical_support", "system_administrator", "account_manager"],
        "update_communication": ["incident_manager", "technical_support", "system_administrator", "account_manager"],
        "create_workaround": ["technical_support", "incident_manager", "system_administrator", "executive"],
        "update_workaround": ["technical_support", "incident_manager", "system_administrator", "executive"],
        "conduct_rca": ["technical_support", "incident_manager", "system_administrator", "executive"],
        "update_rca": ["technical_support", "incident_manager", "system_administrator", "executive"],
        "create_escalation": ["incident_manager", "technical_support", "system_administrator", "executive"],
        "update_escalation": ["incident_manager", "technical_support", "system_administrator", "executive"],
        "create_change_request": ["technical_support", "incident_manager", "system_administrator", "executive"],
        "update_change_request": ["technical_support", "incident_manager", "system_administrator", "executive"],
        "create_rollback_request": ["system_administrator", "executive"],
        "update_rollback_request": ["incident_manager", "system_administrator", "executive"],
        "record_metrics": ["incident_manager", "system_administrator"],
        "update_metrics": ["incident_manager", "system_administrator"],
        "generate_report": ["incident_manager", "executive"],
        "update_report": ["incident_manager", "executive"],
        "create_kb_article": ["technical_support", "incident_manager"],
        "update_kb_article": ["technical_support", "incident_manager"],
        "create_pir": ["incident_manager", "executive"],
        "update_pir": ["incident_manager", "executive"]
    }
    
    # All possible roles
    all_roles = [
        "incident_manager", "technical_support", "account_manager", 
        "executive", "vendor_contact", "system_administrator", "client_contact"
    ]
    
    # Filter users by role for easier selection
    users_by_role = {}
    for user_id, user in users_data.items():
        role = user.get("role")
        if role:
            if role not in users_by_role:
                users_by_role[role] = []
            users_by_role[role].append(user)
    
    approvals = {}
    approval_counter = 1
    base_date = datetime(2025, 9, 1)
    
    while len(approvals) < num_approvals:
        # Select random action
        action = random.choice(list(ACTIONS.keys()))
        authorized_roles = ACTIONS[action]
        
        # Select approver role from authorized roles (approver MUST have authorized role)
        approver_role = random.choice(authorized_roles)
        
        # Select requester role from roles NOT authorized
        unauthorized_roles = [r for r in all_roles if r not in authorized_roles]
        
        if not unauthorized_roles or approver_role not in users_by_role:
            continue
        
        requester_role = random.choice(unauthorized_roles)
        
        # Get users with these roles
        if requester_role not in users_by_role:
            continue
            
        approver = random.choice(users_by_role[approver_role])
        requester = random.choice(users_by_role[requester_role])

        # Ensure requester and approver are not the same person
        if approver["email"] == requester["email"]:
            continue
        
        # Generate timestamp (random date within last 60 days)
        days_ago = random.randint(0, 60)
        timestamp = base_date + timedelta(days=days_ago, hours=random.randint(8, 18), 
                                          minutes=random.randint(0, 59))
        
        # Random status (most approved, some pending)
        status = random.choices(["approved", "pending"], weights=[0.85, 0.15])[0]
        
        # Use a simple numeric string for the ID
        approval_id = str(approval_counter)
        
        approvals[approval_id] = {
            "approval_id": approval_id,
            "action_name": action,
            "approver_email": approver["email"],
            "approver_role": approver_role,
            "requester_email": requester["email"],
            "requester_role": requester_role,
            "timestamp": timestamp.isoformat(),
            "status": status
        }
        
        approval_counter += 1
    
    return approvals


def main():
    # Load users from file
    try:
        with open("users.json", "r") as f:
            users_data = json.load(f)
    except FileNotFoundError:
        print("Error: users.json not found. Please ensure the file exists.")
        return
    except json.JSONDecodeError:
        print("Error: users.json is not valid JSON.")
        return
    
    # Generate approvals
    approvals_data = generate_approvals(users_data, num_approvals=999)
    
    # Output as JSON
    output = {
        "approvals": approvals_data
    }
    
    print(f"Generated {len(approvals_data)} approval records")
    
    # Save to file
    with open("approvals.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nApprovals saved to approvals.json")


if __name__ == "__main__":
    main()