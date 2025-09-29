import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddInvestor(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], legal_name: str, source_of_funds: str, 
               contact_email: str, accreditation_status: str,
               compliance_officer_approval: bool,
               registration_number: Optional[str] = None,
               date_of_incorporation: Optional[str] = None,
               country_of_incorporation: Optional[str] = None,
               registered_address: Optional[str] = None,
               tax_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        investors = data.get("investors", {})
        
        # Validate required approvals first
        if not compliance_officer_approval:
            return json.dumps({
                "success": False,
                "error": "Compliance Officer approval is required for investor onboarding"
            })
        
        # Validate required fields
        if not legal_name or not legal_name.strip():
            return json.dumps({
                "success": False,
                "error": "Legal name is required"
            })
        
        if not contact_email or not contact_email.strip():
            return json.dumps({
                "success": False,
                "error": "Contact email is required"
            })
        
        # Validate source_of_funds
        valid_sources = ['retained_earnings', 'shareholder_capital', 'asset_sale', 'loan_facility', 'external_investment', 'government_grant', 'merger_or_acquisition_proceeds', 'royalty_or_licensing_income', 'dividend_income', 'other']
        if source_of_funds not in valid_sources:
            return json.dumps({
                "success": False,
                "error": f"Invalid source_of_funds. Must be one of {valid_sources}"
            })
        
        # Validate accreditation_status
        valid_accreditation = ["accredited", "non_accredited"]
        if accreditation_status not in valid_accreditation:
            return json.dumps({
                "success": False,
                "error": f"Invalid accreditation_status. Must be one of {valid_accreditation}"
            })
        
        # Check if investor with same email already exists
        for investor in investors.values():
            if investor.get("contact_email") == contact_email:
                return json.dumps({
                    "success": False,
                    "error": "An investor with this email already exists"
                })
        
        investor_id = generate_id(investors)
        timestamp = "2025-10-01T00:00:00"
        
        new_investor = {
            "investor_id": str(investor_id) if investor_id is not None else None,
            "name": legal_name,
            "registration_number": registration_number,
            "date_of_incorporation": date_of_incorporation,
            "country": country_of_incorporation,
            "address": registered_address,
            "tax_id": str(tax_id) if tax_id is not None else None,
            "source_of_funds": source_of_funds,
            "status": "onboarded",
            "contact_email": contact_email,
            "accreditation_status": accreditation_status,
            "created_at": timestamp
        }
        
        investors[str(investor_id)] = new_investor
        
        return json.dumps(new_investor)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_investor",
                "description": "Create a new investor profile for onboarding in the fund management system. This tool establishes investor records with comprehensive validation and regulatory compliance checks. Validates investor details including legal name, contact information, source of funds categorization, and accreditation status according to regulatory requirements. Prevents duplicate investor creation by checking existing email addresses. Requires Compliance Officer approval as mandated by regulatory onboarding procedures. Essential for investor relationship management, compliance tracking, and fund subscription eligibility. Supports the complete investor lifecycle from initial onboarding through ongoing relationship management.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "legal_name": {
                            "type": "string", 
                            "description": "Legal name of the investor (required, cannot be empty or whitespace only)"
                        },
                        "registration_number": {
                            "type": "string", 
                            "description": "Registration number of the investor entity (optional, used for corporate entities)"
                        },
                        "date_of_incorporation": {
                            "type": "string", 
                            "description": "Date of incorporation in YYYY-MM-DD format (optional, used for corporate entities)"
                        },
                        "country_of_incorporation": {
                            "type": "string", 
                            "description": "Country of incorporation (optional, used for corporate entities)"
                        },
                        "registered_address": {
                            "type": "string", 
                            "description": "Registered address of the investor (optional, full address string)"
                        },
                        "tax_id": {
                            "type": "string", 
                            "description": "Tax identification number (optional, jurisdiction-specific format)"
                        },
                        "source_of_funds": {
                            "type": "string", 
                            "description": "Source of investment funds (required). Must be one of: 'retained_earnings', 'shareholder_capital', 'asset_sale', 'loan_facility', 'external_investment', 'government_grant', 'merger_or_acquisition_proceeds', 'royalty_or_licensing_income', 'dividend_income', 'other'"
                        },
                        "contact_email": {
                            "type": "string", 
                            "description": "Contact email address (required, must be unique across all investors, cannot be empty or whitespace only)"
                        },
                        "accreditation_status": {
                            "type": "string", 
                            "description": "Investor accreditation status (required). Must be either 'accredited' or 'non_accredited' according to regulatory definitions"
                        },
                        "compliance_officer_approval": {
                            "type": "boolean",
                            "description": "Compliance Officer approval presence (True/False) (required for investor onboarding as mandated by regulatory procedures)"
                        }
                    },
                    "required": ["legal_name", "source_of_funds", "contact_email", "accreditation_status", "compliance_officer_approval"]
                }
            }
        }