import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateInvestorDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, investor_name: Optional[str] = None,
               contact_email: Optional[str] = None, accreditation_status: Optional[str] = None,
               registration_number: Optional[int] = None, date_of_incorporation: Optional[str] = None,
               investor_country: Optional[str] = None, investor_address: Optional[str] = None,
               tax_id: Optional[str] = None, source_of_funds: Optional[str] = None,
               investor_status: Optional[str] = None) -> str:
        
        investors = data.get("investors", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        investor = investors[str(investor_id)]
        
        # Validate accreditation investor_status if provided
        if accreditation_status:
            valid_accreditation = ["accredited", "non_accredited"]
            if accreditation_status not in valid_accreditation:
                raise ValueError(f"Invalid accreditation investor_status. Must be one of {valid_accreditation}")
            investor["accreditation_status"] = accreditation_status
        
        # Validate investor_status if provided
        if investor_status:
            valid_statuses = ["onboarded", "offboarded"]
            if investor_status not in valid_statuses:
                raise ValueError(f"Invalid investor_status. Must be one of {valid_statuses}")
            investor["investor_status"] = investor_status
        
        # Validate source of funds if provided
        if source_of_funds:
            valid_sources = ["retained_earnings", "shareholder_capital", "asset_sale", "loan_facility", 
                            "external_investment", "government_grant", "merger_or_acquisition_proceeds",
                            "royalty_or_licensing_income", "dividend_income", "other"]
            if source_of_funds not in valid_sources:
                raise ValueError(f"Invalid source of funds. Must be one of {valid_sources}")
            investor["source_of_funds"] = source_of_funds
        
        # Update fields if provided
        if investor_name is not None:
            investor["investor_name"] = investor_name
        if contact_email is not None:
            investor["contact_email"] = contact_email
        if registration_number is not None:
            investor["registration_number"] = registration_number
        if date_of_incorporation is not None:
            investor["date_of_incorporation"] = date_of_incorporation
        if investor_country is not None:
            investor["investor_country"] = investor_country
        if investor_address is not None:
            investor["investor_address"] = investor_address
        if tax_id is not None:
            investor["tax_id"] = tax_id
        
        return json.dumps(investor)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "investor_name": "update_investor_details",
                "description": "Update investor details for regulatory updates and investor_address changes",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "investor_name": {"type": "string", "description": "Investor investor_name (optional)"},
                        "contact_email": {"type": "string", "description": "Contact investor_email investor_address (optional)"},
                        "accreditation_status": {"type": "string", "description": "Accreditation investor_status (optional)"},
                        "registration_number": {"type": "integer", "description": "Registration number (optional)"},
                        "date_of_incorporation": {"type": "string", "description": "Date of incorporation (optional)"},
                        "investor_country": {"type": "string", "description": "Country (optional)"},
                        "investor_address": {"type": "string", "description": "Address (optional)"},
                        "tax_id": {"type": "string", "description": "Tax ID (optional)"},
                        "source_of_funds": {"type": "string", "description": "Source of funds (optional)"},
                        "investor_status": {"type": "string", "description": "Status (optional)"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
