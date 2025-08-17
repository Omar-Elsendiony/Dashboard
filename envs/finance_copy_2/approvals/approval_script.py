import json
import random
from typing import Dict, List

def generate_fund_approvals():
    """Generate realistic fund management approval documents for 175 investors across 17 action types."""
    
    # User roles mapping
    users = {
        "1": "compliance_officer", "2": "trader", "3": "trader", "4": "fund_manager", "5": "finance_officer",
        "6": "system_administrator", "7": "trader", "8": "finance_officer", "9": "trader", "10": "compliance_officer",
        "11": "finance_officer", "12": "fund_manager", "13": "trader", "14": "finance_officer", "15": "compliance_officer",
        "16": "finance_officer", "17": "fund_manager", "18": "compliance_officer", "19": "trader", "20": "fund_manager",
        "21": "fund_manager", "22": "finance_officer", "23": "trader", "24": "compliance_officer", "25": "compliance_officer",
        "26": "compliance_officer", "27": "fund_manager", "28": "trader", "29": "compliance_officer", "30": "system_administrator",
        "31": "fund_manager", "32": "trader", "33": "compliance_officer", "34": "trader", "35": "system_administrator",
        "36": "system_administrator", "37": "compliance_officer", "38": "fund_manager", "39": "fund_manager", "40": "finance_officer",
        "41": "system_administrator", "42": "fund_manager", "43": "fund_manager", "44": "system_administrator", "45": "fund_manager",
        "46": "system_administrator", "47": "compliance_officer", "48": "fund_manager", "49": "compliance_officer", "50": "system_administrator",
        "51": "fund_manager", "52": "trader", "53": "compliance_officer", "54": "finance_officer", "55": "system_administrator",
        "56": "trader", "57": "system_administrator", "58": "trader", "59": "system_administrator", "60": "compliance_officer",
        "61": "compliance_officer", "62": "compliance_officer", "63": "fund_manager", "64": "system_administrator", "65": "trader",
        "66": "finance_officer", "67": "compliance_officer", "68": "trader", "69": "fund_manager", "70": "finance_officer",
        "71": "system_administrator", "72": "finance_officer", "73": "fund_manager", "74": "compliance_officer", "75": "system_administrator",
        "76": "system_administrator", "77": "finance_officer", "78": "compliance_officer", "79": "compliance_officer", "80": "trader",
        "81": "trader", "82": "trader", "83": "fund_manager", "84": "compliance_officer", "85": "finance_officer",
        "86": "fund_manager", "87": "system_administrator", "88": "fund_manager", "89": "finance_officer", "90": "finance_officer",
        "91": "system_administrator", "92": "system_administrator", "93": "finance_officer", "94": "finance_officer", "95": "fund_manager",
        "96": "compliance_officer", "97": "system_administrator", "98": "trader", "99": "fund_manager", "100": "finance_officer",
        "101": "trader", "102": "finance_officer", "103": "finance_officer", "104": "compliance_officer", "105": "finance_officer",
        "106": "trader", "107": "fund_manager", "108": "fund_manager", "109": "compliance_officer", "110": "compliance_officer",
        "111": "fund_manager", "112": "fund_manager", "113": "finance_officer", "114": "fund_manager", "115": "trader",
        "116": "system_administrator", "117": "compliance_officer", "118": "compliance_officer", "119": "system_administrator", "120": "finance_officer",
        "121": "trader", "122": "compliance_officer", "123": "fund_manager", "124": "system_administrator", "125": "compliance_officer"
    }
    
    # Approval action definitions with their required roles
    approval_actions = {
        "COMMIT": {
            "name": "Investment Commitment",
            "required_roles": ["compliance_officer"],
            "content": "This document certifies that the investment commitment request has been reviewed and meets all regulatory compliance requirements. The investor's source of funds, accreditation status, and risk profile have been verified in accordance with applicable securities laws and internal policies."
        },
        "FUNDC": {
            "name": "Fund Creation",
            "required_roles": ["compliance_officer"],
            "content": "Compliance approval granted for fund establishment. All regulatory filings, prospectus documentation, and risk disclosures have been reviewed and found compliant with securities regulations. The fund structure meets applicable investment company requirements."
        },
        "SUBCR": {
            "name": "Subscription Creation",
            "required_roles": ["compliance_officer"],
            "content": "Investment subscription approved following comprehensive compliance review. Investor eligibility, anti-money laundering checks, and suitability assessments have been completed satisfactorily. All required disclosure documents have been provided to the investor."
        },
        "INSTD": {
            "name": "Instrument Deactivation",
            "required_roles": ["compliance_officer"],
            "content": "Compliance approval for instrument deactivation. Risk assessment completed and no regulatory impediments identified. All outstanding positions and settlement obligations have been reviewed and are in compliance with market regulations."
        },
        "INSTR": {
            "name": "Instrument Reactivation", 
            "required_roles": ["compliance_officer"],
            "content": "Instrument reactivation approved following compliance review. Market conditions, regulatory status, and risk parameters have been assessed. The instrument meets all current trading and compliance requirements for active status."
        },
        "FUNDD": {
            "name": "Fund Deletion",
            "required_roles": ["compliance_officer"],
            "content": "Compliance approval for fund termination. All regulatory notifications have been filed, investor redemptions processed, and final reporting requirements satisfied. The fund dissolution complies with all applicable regulations and contractual obligations."
        },
        "INVON": {
            "name": "Investor Onboarding",
            "required_roles": ["compliance_officer"],
            "content": "New investor onboarding approved. Know Your Customer (KYC) procedures completed, beneficial ownership verified, and anti-money laundering screening passed. The investor meets all accreditation and eligibility requirements for participation in our investment products."
        },
        "INVOF": {
            "name": "Investor Offboarding",
            "required_roles": ["compliance_officer"],
            "content": "Investor offboarding approved following compliance review. All positions have been liquidated, final distributions processed, and required tax reporting completed. The termination of the investor relationship complies with all regulatory and contractual requirements."
        },
        "REDMC": {
            "name": "Redemption Compliance",
            "required_roles": ["compliance_officer"],
            "content": "Compliance approval for redemption request. Investor eligibility verified, lock-up periods confirmed expired, and all regulatory requirements for redemption processing have been satisfied. No compliance impediments to redemption identified."
        },
        "SUBUP": {
            "name": "Subscription Update",
            "required_roles": ["compliance_officer"],
            "content": "Subscription modification approved following compliance review. Updated terms comply with applicable regulations and fund documentation. All necessary investor notifications and regulatory filings have been completed or scheduled."
        },
        "TRADE": {
            "name": "Trade Execution",
            "required_roles": ["fund_manager"],
            "content": "Trade execution authorized by Fund Manager. Investment decision aligns with fund objectives, risk parameters, and investment mandate. Position sizing and market impact assessment completed. Trade is within approved risk limits and portfolio guidelines."
        },
        "FUNDU": {
            "name": "Fund Update",
            "required_roles": ["fund_manager"],
            "content": "Fund parameter update approved by Fund Manager. The proposed changes are consistent with the fund's investment strategy and will not adversely impact existing investors. Updated documentation and investor notifications will be processed accordingly."
        },
        "REDMF": {
            "name": "Redemption Finance",
            "required_roles": ["finance_officer"],
            "content": "Finance approval for redemption processing. Liquidity analysis completed, cash flow impact assessed, and fund accounting verified. Sufficient liquid assets available to meet redemption without compromising fund operations or other investors' interests."
        },
        "SUBUF": {
            "name": "Subscription Update Finance",
            "required_roles": ["finance_officer"],
            "content": "Finance approval for subscription modification. Impact on fund accounting, fee calculations, and capital structure assessed. Updated terms are financially sound and will not create adverse effects on fund operations or existing investor positions."
        },
        "RPTPF": {
            "name": "Performance Report",
            "required_roles": ["fund_manager"],
            "content": "Performance report generation authorized by Fund Manager. Report parameters align with fund objectives and investor reporting requirements. Performance calculations and benchmarking methodologies have been verified for accuracy."
        },
        "RPTFF": {
            "name": "Financial Report",
            "required_roles": ["finance_officer"],
            "content": "Financial report generation authorized by Finance Officer. All financial data has been reconciled and validated. Report complies with applicable accounting standards and regulatory reporting requirements."
        },
        "RPTHF": {
            "name": "Holdings Report",
            "required_roles": ["finance_officer"],
            "content": "Holdings report generation authorized by Finance Officer. Portfolio positions have been verified against custodial records and all valuations updated to current market prices. Report accurately reflects fund composition as of the specified date."
        }
    }
    
    def get_eligible_approvers(required_roles: List[str]) -> List[str]:
        """Get list of user IDs who can approve based on required roles."""
        eligible = []
        for user_id, role in users.items():
            if role in required_roles:
                eligible.append(user_id)
        return eligible
    
    # Generate approvals
    approvals = {}
    approval_id = 1
    
    # For each investor (1-175)
    for investor_id in range(1, 176):
        # For each action type
        for action_code, action_info in approval_actions.items():
            # Get eligible approvers for this action
            eligible_approvers = get_eligible_approvers(action_info["required_roles"])
            
            if not eligible_approvers:
                continue  # Skip if no eligible approvers
            
            # Randomly select an approver
            approver_id = random.choice(eligible_approvers)
            
            # Create approval document
            approval = {
                "id": str(approval_id),
                "code": f"{investor_id}-{action_code}-{approver_id}",
                "content": action_info["content"],
                "approved_by": approver_id,
                "action_name": action_info["name"],
                "investor_id": str(investor_id),
                "approver_role": users[approver_id]
            }
            
            approvals[str(approval_id)] = approval
            approval_id += 1
    
    return approvals

def save_approvals_to_file(approvals: Dict, filename: str = "fund_approvals.json"):
    """Save approvals to JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(approvals, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(approvals)} approval documents saved to {filename}")

def generate_summary_stats(approvals: Dict):
    """Generate summary statistics of the approvals."""
    stats = {
        "total_approvals": len(approvals),
        "by_action": {},
        "by_role": {},
        "by_approver": {}
    }
    
    for approval in approvals.values():
        # Count by action type
        action = approval["code"].split("-")[1]
        stats["by_action"][action] = stats["by_action"].get(action, 0) + 1
        
        # Count by role
        role = approval["approver_role"]
        stats["by_role"][role] = stats["by_role"].get(role, 0) + 1
        
        # Count by approver
        approver = approval["approved_by"]
        stats["by_approver"][approver] = stats["by_approver"].get(approver, 0) + 1
    
    return stats

if __name__ == "__main__":
    print("Generating fund management approval documents...")
    
    # Generate all approvals
    all_approvals = generate_fund_approvals()
    
    # Save to file
    save_approvals_to_file(all_approvals)
    
    # Generate and display summary statistics
    stats = generate_summary_stats(all_approvals)
    
    print(f"\n=== SUMMARY STATISTICS ===")
    print(f"Total approvals generated: {stats['total_approvals']}")
    
    print(f"\nApprovals by Action Type:")
    for action, count in sorted(stats['by_action'].items()):
        print(f"  {action}: {count}")
    
    print(f"\nApprovals by Role:")
    for role, count in sorted(stats['by_role'].items()):
        print(f"  {role}: {count}")
    
    print(f"\nTop 10 Most Active Approvers:")
    top_approvers = sorted(stats['by_approver'].items(), key=lambda x: x[1], reverse=True)[:10]
    for approver_id, count in top_approvers:
        role = next(role for uid, role in {
            "1": "compliance_officer", "10": "compliance_officer", "15": "compliance_officer", 
            "18": "compliance_officer", "24": "compliance_officer", "25": "compliance_officer",
            "26": "compliance_officer", "29": "compliance_officer", "33": "compliance_officer", 
            "37": "compliance_officer", "47": "compliance_officer", "49": "compliance_officer",
            "53": "compliance_officer", "60": "compliance_officer", "61": "compliance_officer", 
            "62": "compliance_officer", "67": "compliance_officer", "74": "compliance_officer",
            "78": "compliance_officer", "79": "compliance_officer", "84": "compliance_officer", 
            "96": "compliance_officer", "104": "compliance_officer", "109": "compliance_officer",
            "110": "compliance_officer", "117": "compliance_officer", "118": "compliance_officer", 
            "122": "compliance_officer", "125": "compliance_officer",
            "4": "fund_manager", "12": "fund_manager", "17": "fund_manager", "20": "fund_manager",
            "21": "fund_manager", "27": "fund_manager", "31": "fund_manager", "38": "fund_manager",
            "39": "fund_manager", "42": "fund_manager", "43": "fund_manager", "45": "fund_manager",
            "48": "fund_manager", "51": "fund_manager", "63": "fund_manager", "69": "fund_manager",
            "73": "fund_manager", "83": "fund_manager", "86": "fund_manager", "88": "fund_manager",
            "95": "fund_manager", "99": "fund_manager", "107": "fund_manager", "108": "fund_manager",
            "111": "fund_manager", "112": "fund_manager", "114": "fund_manager", "123": "fund_manager",
            "5": "finance_officer", "8": "finance_officer", "11": "finance_officer", "14": "finance_officer",
            "16": "finance_officer", "22": "finance_officer", "40": "finance_officer", "54": "finance_officer",
            "66": "finance_officer", "70": "finance_officer", "72": "finance_officer", "77": "finance_officer",
            "85": "finance_officer", "89": "finance_officer", "90": "finance_officer", "93": "finance_officer",
            "94": "finance_officer", "100": "finance_officer", "102": "finance_officer", "103": "finance_officer",
            "105": "finance_officer", "113": "finance_officer", "120": "finance_officer"
        }.items() if uid == approver_id)
        print(f"  User {approver_id} ({role}): {count} approvals")
    
    print(f"\nSample approval documents saved to 'fund_approvals.json'")
    print("Each investor (1-175) has 17 different approval types generated.")