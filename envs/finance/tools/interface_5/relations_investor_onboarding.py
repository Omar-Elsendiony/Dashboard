import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RelationsInvestorOnboarding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], legal_entity_name: str, incorporation_registration_number: str,
               date_of_incorporation: str, country_of_incorporation: str, registered_business_address: str,
               tax_identification_number: str, source_of_funds_declaration: str, compliance_officer_approval: bool) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if not compliance_officer_approval:
            return json.dumps({"error": "Compliance Officer approval required. Process halted."})
        
        investors = data.get("investors", {})
        
        # Validate source of funds
        valid_sources = ["retained_earnings", "shareholder_capital", "asset_sale", "loan_facility", 
                        "external_investment", "government_grant", "merger_or_acquisition_proceeds",
                        "royalty_or_licensing_income", "dividend_income", "other"]
        if source_of_funds_declaration not in valid_sources:
            return json.dumps({"error": f"Invalid source of funds. Must be one of {valid_sources}"})
        
        relations_investor_id = generate_id(investors)
        timestamp = "2025-10-01T00:00:00"
        
        new_investor = {
            "relations_investor_id": relations_investor_id,
            "name": legal_entity_name,
            "registration_number": incorporation_registration_number,
            "date_of_incorporation": date_of_incorporation,
            "country": country_of_incorporation,
            "address": registered_business_address,
            "tax_id": tax_identification_number,
            "source_of_funds": source_of_funds_declaration,
            "contact_email": "",  # Will need to be provided separately
            "accreditation_status": "accredited",  # Default for institutional investors
            "created_at": timestamp
        }
        
        investors[str(relations_investor_id)] = new_investor
        return json.dumps({"relations_investor_id": str(relations_investor_id)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "investor_onboarding",
                "description": "Onboard a new institutional investor after compliance checks",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "legal_entity_name": {"type": "string", "description": "Legal entity name"},
                        "incorporation_registration_number": {"type": "string", "description": "Incorporation/registration number"},
                        "date_of_incorporation": {"type": "string", "description": "Date of incorporation (YYYY-MM-DD)"},
                        "country_of_incorporation": {"type": "string", "description": "Country of incorporation"},
                        "registered_business_address": {"type": "string", "description": "Registered business address"},
                        "tax_identification_number": {"type": "string", "description": "Tax identification number"},
                        "source_of_funds_declaration": {"type": "string", "description": "Source of funds declaration. It should be only one of the following: 'retained_earnings', 'shareholder_capital', 'asset_sale', 'loan_facility', 'external_investment', 'government_grant', 'merger_or_acquisition_proceeds', 'royalty_or_licensing_income', 'dividend_income', 'other'"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval flag (True/False)"}
                    },
                    "required": ["legal_entity_name", "incorporation_registration_number", "date_of_incorporation", 
                               "country_of_incorporation", "registered_business_address", "tax_identification_number",
                               "source_of_funds_declaration", "compliance_officer_approval"]
                }
            }
        }
