import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class OnboardNewInvestor(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, contact_email: str, 
               accreditation_status: str, registration_number: Optional[int] = None,
               date_of_incorporation: Optional[str] = None, country: Optional[str] = None,
               address: Optional[str] = None, tax_id: Optional[str] = None,
               source_of_funds: Optional[str] = None, status: str = "onboarded") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        investors = data.get("investors", {})
        
        # Validate accreditation status
        valid_accreditation = ["accredited", "non_accredited"]
        if accreditation_status not in valid_accreditation:
            raise ValueError(f"Invalid accreditation status. Must be one of {valid_accreditation}")
        
        # Validate status
        valid_statuses = ["onboarded", "offboarded"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Validate source of funds if provided
        valid_sources = ["retained_earnings", "shareholder_capital", "asset_sale", "loan_facility", 
                        "external_investment", "government_grant", "merger_or_acquisition_proceeds",
                        "royalty_or_licensing_income", "dividend_income", "other"]
        if source_of_funds and source_of_funds not in valid_sources:
            raise ValueError(f"Invalid source of funds. Must be one of {valid_sources}")
        
        investor_id = generate_id(investors)
        timestamp = "2025-10-01T00:00:00"
        
        new_investor = {
            "investor_id": str(investor_id),
            "name": name,
            "registration_number": registration_number,
            "date_of_incorporation": date_of_incorporation,
            "country": country,
            "address": address,
            "tax_id": tax_id,
            "source_of_funds": source_of_funds,
            "status": status,
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
                "name": "onboard_new_investor",
                "description": "Onboard a new investor with KYC compliance and regulatory requirements",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Investor name"},
                        "contact_email": {"type": "string", "description": "Contact email address"},
                        "accreditation_status": {"type": "string", "description": "Accreditation status (accredited, non_accredited)"},
                        "registration_number": {"type": "integer", "description": "Registration number (optional)"},
                        "date_of_incorporation": {"type": "string", "description": "Date of incorporation in YYYY-MM-DD format (optional)"},
                        "country": {"type": "string", "description": "Country (optional)"},
                        "address": {"type": "string", "description": "Address (optional)"},
                        "tax_id": {"type": "string", "description": "Tax ID (optional)"},
                        "source_of_funds": {"type": "string", "description": "Source of funds (optional)"},
                        "status": {"type": "string", "description": "Status (onboarded, offboarded), defaults to onboarded"}
                    },
                    "required": ["name", "contact_email", "accreditation_status"]
                }
            }
        }
