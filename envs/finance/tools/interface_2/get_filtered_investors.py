import json
from typing import Any, Dict, Optional, List
from datetime import datetime
from tau_bench.envs.tool import Tool

class GetFilteredInvestors(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], 
               accreditation_status: Optional[str] = None,
               investor_status: Optional[str] = None, 
               investor_country: Optional[str] = None,
               source_of_funds: Optional[str] = None,
               name_contains: Optional[str] = None,
               registration_number: Optional[int] = None,
               incorporation_date_from: Optional[str] = None,
               incorporation_date_to: Optional[str] = None,
               countries: Optional[List[str]] = None,
               has_tax_id: Optional[bool] = None,
               has_registration_number: Optional[bool] = None,
               created_after: Optional[str] = None,
               created_before: Optional[str] = None,
               email_domain: Optional[str] = None,
               address_contains: Optional[str] = None) -> str:
        
        investors = data.get("investors", {})
        results = []
        
        for investor in investors.values():
            # Existing filters
            if accreditation_status and investor.get("accreditation_status") != accreditation_status:
                continue
            if investor_status and investor.get("investor_status") != investor_status:
                continue
            if investor_country and investor.get("investor_country") != investor_country:
                continue
            if source_of_funds and investor.get("source_of_funds") != source_of_funds:
                continue
            
            # New investor_name filter
            if name_contains and name_contains.lower() not in investor.get("investor_name", "").lower():
                continue
            
            # Registration number filter
            if registration_number and investor.get("registration_number") != registration_number:
                continue
            
            # Date of incorporation filters
            if incorporation_date_from or incorporation_date_to:
                inc_date = investor.get("date_of_incorporation")
                if inc_date:
                    try:
                        inc_date_obj = datetime.strptime(inc_date, "%Y-%m-%d").date()
                        if incorporation_date_from:
                            from_date = datetime.strptime(incorporation_date_from, "%Y-%m-%d").date()
                            if inc_date_obj < from_date:
                                continue
                        if incorporation_date_to:
                            to_date = datetime.strptime(incorporation_date_to, "%Y-%m-%d").date()
                            if inc_date_obj > to_date:
                                continue
                    except (ValueError, TypeError):
                        if incorporation_date_from or incorporation_date_to:
                            continue
                elif incorporation_date_from or incorporation_date_to:
                    continue
            
            # Multiple countries filter
            if countries and investor.get("investor_country") not in countries:
                continue
            
            # Tax ID presence filter
            if has_tax_id is not None:
                tax_id = investor.get("tax_id")
                if has_tax_id and (not tax_id or tax_id.strip() == ""):
                    continue
                if not has_tax_id and tax_id and tax_id.strip() != "":
                    continue
            
            # Registration number presence filter
            if has_registration_number is not None:
                reg_num = investor.get("registration_number")
                if has_registration_number and reg_num is None:
                    continue
                if not has_registration_number and reg_num is not None:
                    continue
            
            # Created date filters
            if created_after or created_before:
                created_at = investor.get("created_at")
                if created_at:
                    try:
                        created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        if created_after:
                            after_date = datetime.fromisoformat(created_after.replace('Z', '+00:00'))
                            if created_date < after_date:
                                continue
                        if created_before:
                            before_date = datetime.fromisoformat(created_before.replace('Z', '+00:00'))
                            if created_date > before_date:
                                continue
                    except (ValueError, TypeError):
                        if created_after or created_before:
                            continue
                elif created_after or created_before:
                    continue
            
            # Email domain filter
            if email_domain:
                investor_email = investor.get("contact_email", "")
                if not investor_email or not investor_email.endswith(f"@{email_domain}"):
                    continue
            
            # Address contains filter
            if address_contains:
                investor_address = investor.get("investor_address", "")
                if address_contains.lower() not in investor_address.lower():
                    continue
            
            results.append(investor)
        
        return json.dumps(results, indent=2)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_filtered_investors",
                "description": "Get filtered investors for CRM and marketing segmentation with comprehensive filtering options",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "accreditation_status": {
                            "type": "string", 
                            "description": "Filter by accreditation investor_status (accredited/non_accredited)",
                            "enum": ["accredited", "non_accredited"]
                        },
                        "investor_status": {
                            "type": "string", 
                            "description": "Filter by investor investor_status (onboarded/offboarded)",
                            "enum": ["onboarded", "offboarded"]
                        },
                        "investor_country": {
                            "type": "string", 
                            "description": "Filter by specific investor_country"
                        },
                        "source_of_funds": {
                            "type": "string", 
                            "description": "Filter by specific source of funds",
                            "enum": ["retained_earnings", "shareholder_capital", "asset_sale", "loan_facility", 
                                   "external_investment", "government_grant", "merger_or_acquisition_proceeds", 
                                   "royalty_or_licensing_income", "dividend_income", "other"]
                        },
                        "name_contains": {
                            "type": "string", 
                            "description": "Filter by partial investor_name match (case-insensitive)"
                        },
                        "registration_number": {
                            "type": "integer", 
                            "description": "Filter by specific registration number"
                        },
                        "incorporation_date_from": {
                            "type": "string", 
                            "description": "Filter investors incorporated on or after this date (YYYY-MM-DD format)"
                        },
                        "incorporation_date_to": {
                            "type": "string", 
                            "description": "Filter investors incorporated on or before this date (YYYY-MM-DD format)"
                        },
                        "countries": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Filter by multiple countries (returns investors from any of these countries)"
                        },
                        "has_tax_id": {
                            "type": "boolean", 
                            "description": "Filter by presence of tax ID (true for investors with tax ID, false for those without)"
                        },
                        "has_registration_number": {
                            "type": "boolean", 
                            "description": "Filter by presence of registration number (true for investors with reg number, false for those without)"
                        },
                        "created_after": {
                            "type": "string", 
                            "description": "Filter investors created after this timestamp (ISO format) [ex: 2022-08-17T04:30:00]"
                        },
                        "created_before": {
                            "type": "string", 
                            "description": "Filter investors created before this timestamp (ISO format) [ex: 2022-08-17T04:30:00]"
                        },
                        "email_domain": {
                            "type": "string", 
                            "description": "Filter by investor_email domain (e.g., 'company.com' to find all @company.com emails)"
                        },
                        "address_contains": {
                            "type": "string", 
                            "description": "Filter by partial investor_address match (case-insensitive)"
                        }
                    },
                    "required": []
                }
            }
        }