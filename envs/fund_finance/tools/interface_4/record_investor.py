import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RecordInvestor(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], legal_name: str, source_of_funds: str, 
               contact_email: str, accreditation_status: str,
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
        
        # Validate required fields
        if not legal_name or not legal_name.strip():
            return json.dumps({"error": "Legal name is required"})
        
        if not contact_email or not contact_email.strip():
            return json.dumps({"error": "Contact email is required"})
        
        # Validate source_of_funds
        valid_sources = ['retained_earnings', 'shareholder_capital', 'asset_sale', 'loan_facility', 'external_investment', 'government_grant', 'merger_or_acquisition_proceeds', 'royalty_or_licensing_income', 'dividend_income', 'other']
        if source_of_funds not in valid_sources:
            return json.dumps({"error": f"Invalid source_of_funds. Must be one of {valid_sources}"})
        
        # Validate accreditation_status
        valid_accreditation = ["accredited", "non_accredited"]
        if accreditation_status not in valid_accreditation:
            return json.dumps({"error": f"Invalid accreditation_status. Must be one of {valid_accreditation}"})
        
        # Check if investor with same email already exists
        for investor in investors.values():
            if investor.get("contact_email") == contact_email:
                return json.dumps({"error": "An investor with this email already exists"})
        

        
        investor_id = generate_id(investors)
        timestamp = "2025-10-01T00:00:00"
        
        new_investor = {
            "investor_id": str(investor_id),
            "name": legal_name,
            "registration_number": registration_number,
            "date_of_incorporation": date_of_incorporation,
            "country": country_of_incorporation,
            "address": registered_address,
            "tax_id": tax_id,
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
                "name": "record_investor",
                "description": "Create a new investor profile for onboarding",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "legal_name": {"type": "string", "description": "Legal name of the investor"},
                        "registration_number": {"type": "string", "description": "Registration number (optional)"},
                        "date_of_incorporation": {"type": "string", "description": "Date of incorporation in YYYY-MM-DD format (optional)"},
                        "country_of_incorporation": {"type": "string", "description": "Country of incorporation (optional)"},
                        "registered_address": {"type": "string", "description": "Registered address (optional)"},
                        "tax_id": {"type": "string", "description": "Tax identification number (optional)"},
                        "source_of_funds": {"type": "string", "description": "Source of funds ('retained_earnings', 'shareholder_capital', 'asset_sale', 'loan_facility', 'external_investment', 'government_grant', 'merger_or_acquisition_proceeds', 'royalty_or_licensing_income', 'dividend_income', 'other')"},
                        "contact_email": {"type": "string", "description": "Contact email address"},
                        "accreditation_status": {"type": "string", "description": "Accreditation status (accredited, non_accredited)"}
                    },
                    "required": ["legal_name", "source_of_funds", "contact_email", "accreditation_status"]
                }
            }
        }