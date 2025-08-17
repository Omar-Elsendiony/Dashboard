#!/bin/bash

# Create directory for tools
mkdir -p fund_management_tools
cd fund_management_tools

# Tool 1: investor_onboarding.py
cat > investor_onboarding.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class InvestorOnboarding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], legal_entity_name: str, incorporation_registration_number: str,
               date_of_incorporation: str, country_of_incorporation: str, registered_business_address: str,
               tax_identification_number: str, source_of_funds_declaration: str, 
               aml_screening_results: Dict[str, Any], compliance_officer_approval: bool) -> str:
        
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
        
        investor_id = generate_id(investors)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_investor = {
            "investor_id": investor_id,
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
        
        investors[str(investor_id)] = new_investor
        return json.dumps({"investor_id": str(investor_id), "success": True})

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
                        "date_of_incorporation": {"type": "string", "description": "Date of incorporation"},
                        "country_of_incorporation": {"type": "string", "description": "Country of incorporation"},
                        "registered_business_address": {"type": "string", "description": "Registered business address"},
                        "tax_identification_number": {"type": "string", "description": "Tax identification number"},
                        "source_of_funds_declaration": {"type": "string", "description": "Source of funds declaration"},
                        "aml_screening_results": {"type": "object", "description": "AML screening results"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval flag"}
                    },
                    "required": ["legal_entity_name", "incorporation_registration_number", "date_of_incorporation", 
                               "country_of_incorporation", "registered_business_address", "tax_identification_number",
                               "source_of_funds_declaration", "aml_screening_results", "compliance_officer_approval"]
                }
            }
        }
EOF

# Tool 2: investor_offboarding.py
cat > investor_offboarding.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class InvestorOffboarding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, reason_code: str, 
               compliance_officer_approval: bool) -> str:
        
        if not compliance_officer_approval:
            return json.dumps({"error": "Compliance Officer approval required. Process halted."})
        
        investors = data.get("investors", {})
        subscriptions = data.get("subscriptions", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        
        # Check for active subscriptions
        active_subscriptions = [s for s in subscriptions.values() 
                              if s.get("investor_id") == int(investor_id) and s.get("status") == "approved"]
        
        if active_subscriptions:
            return json.dumps({"error": "Cannot offboard investor with active subscriptions. Process halted."})
        
        # Remove investor (in practice, might just mark as inactive)
        del investors[str(investor_id)]
        
        return json.dumps({"success": True, "message": "Offboarding complete"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "investor_offboarding",
                "description": "Offboard an investor after compliance approval",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor to offboard"},
                        "reason_code": {"type": "string", "description": "Reason code for offboarding"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval for offboarding"}
                    },
                    "required": ["investor_id", "reason_code", "compliance_officer_approval"]
                }
            }
        }
EOF

# Tool 3: create_fund.py
cat > create_fund.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_name: str, fund_type: str, base_currency: str,
               initial_size: float, manager_id: str, strategy_outline: str,
               compliance_officer_review: bool, fund_manager_approval: bool) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if not compliance_officer_review:
            return json.dumps({"error": "Compliance Officer review required. Process halted."})
        
        if not fund_manager_approval:
            return json.dumps({"error": "Fund Manager approval required. Process halted."})
        
        funds = data.get("funds", {})
        users = data.get("users", {})
        
        # Validate manager exists
        if str(manager_id) not in users:
            return json.dumps({"error": f"Manager {manager_id} not found"})
        
        # Validate fund type
        valid_types = ["mutual_funds", "exchange_traded_funds", "pension_funds", "private_equity_funds",
                      "hedge_funds", "sovereign_wealth_funds", "money_market_funds", 
                      "real_estate_investment_trusts", "infrastructure_funds", "multi_asset_funds"]
        if fund_type not in valid_types:
            return json.dumps({"error": f"Invalid fund type. Must be one of {valid_types}"})
        
        fund_id = generate_id(funds)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_fund = {
            "fund_id": fund_id,
            "name": fund_name,
            "fund_type": fund_type,
            "manager_id": int(manager_id),
            "size": initial_size,
            "status": "open",
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        funds[str(fund_id)] = new_fund
        return json.dumps({"fund_id": str(fund_id), "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_fund",
                "description": "Create a new fund after approvals",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_name": {"type": "string", "description": "Name of the fund"},
                        "fund_type": {"type": "string", "description": "Type of fund"},
                        "base_currency": {"type": "string", "description": "Base currency of the fund"},
                        "initial_size": {"type": "number", "description": "Initial size of the fund"},
                        "manager_id": {"type": "string", "description": "ID of the fund manager"},
                        "strategy_outline": {"type": "string", "description": "Strategy outline"},
                        "compliance_officer_review": {"type": "boolean", "description": "Compliance Officer review flag"},
                        "fund_manager_approval": {"type": "boolean", "description": "Fund Manager approval flag"}
                    },
                    "required": ["fund_name", "fund_type", "base_currency", "initial_size", "manager_id", 
                               "strategy_outline", "compliance_officer_review", "fund_manager_approval"]
                }
            }
        }
EOF

# Tool 4: update_fund.py
cat > update_fund.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, changes: Dict[str, Any],
               fund_manager_approval: bool, compliance_review_required: Optional[bool] = None,
               compliance_officer_approval: Optional[bool] = None) -> str:
        
        if not fund_manager_approval:
            return json.dumps({"error": "Fund Manager approval required. Process halted."})
        
        if compliance_review_required and not compliance_officer_approval:
            return json.dumps({"error": "Compliance Officer approval required for this change. Process halted."})
        
        funds = data.get("funds", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        # Find active subscription
        active_subscription = None
        for sub in subscriptions.values():
            if (sub.get("investor_id") == int(investor_id) and 
                sub.get("fund_id") == int(fund_id) and 
                sub.get("status") == "approved"):
                active_subscription = sub
                break
        
        if not active_subscription:
            return json.dumps({"error": "No active subscription found for this investor in the fund"})
        
        if active_subscription.get("amount", 0) < amount_or_units:
            return json.dumps({"error": "Insufficient balance for redemption"})
        
        timestamp = "2025-10-01T00:00:00ZZ"
        
        # Create redemption record
        redemption_id = generate_id(redemptions)
        new_redemption = {
            "redemption_id": redemption_id,
            "subscription_id": active_subscription["subscription_id"],
            "request_date": timestamp.split("T")[0],
            "redemption_amount": amount_or_units,
            "status": "processed",
            "processed_date": timestamp.split("T")[0],
            "updated_at": timestamp,
            "redemption_fee": amount_or_units * 0.01  # 1% redemption fee
        }
        redemptions[str(redemption_id)] = new_redemption
        
        # Update subscription amount
        active_subscription["amount"] -= amount_or_units
        active_subscription["updated_at"] = timestamp
        
        return json.dumps({"success": True, "message": "Redemption processed"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_redemption",
                "description": "Process investor redemption with required approvals",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "amount_or_units": {"type": "number", "description": "Amount or units to redeem"},
                        "reason": {"type": "string", "description": "Reason for redemption"},
                        "compliance_approval": {"type": "boolean", "description": "Compliance approval flag"},
                        "finance_approval": {"type": "boolean", "description": "Finance approval flag"}
                    },
                    "required": ["investor_id", "fund_id", "amount_or_units", "reason", "compliance_approval", "finance_approval"]
                }
            }
        }
EOF

# Tool 12: create_upload_document.py
cat > create_upload_document.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateUploadDocument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, document_type: str, size_bytes: int,
               confidentiality_level: str, file_name: str, file_format: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        documents = data.get("documents", {})
        
        # Validate user exists
        if str(user_id) not in users:
            return json.dumps({"error": f"User {user_id} not found"})
        
        # Validate file format
        valid_formats = ["pdf", "xlsx", "docx", "csv", "other"]
        if file_format.lower() not in valid_formats:
            return json.dumps({"error": f"Invalid file format. Must be one of {valid_formats}"})
        
        document_id = generate_id(documents)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_document = {
            "document_id": document_id,
            "name": file_name,
            "type": file_format.lower(),
            "uploaded_by": int(user_id),
            "upload_date": timestamp,
            "report_id": None,
            "size_bytes": size_bytes,
            "status": "available"
        }
        
        documents[str(document_id)] = new_document
        
        return json.dumps({"doc_id": str(document_id), "success": True, "status": "available"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_upload_document",
                "description": "Upload and create a document record",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user uploading the document"},
                        "document_type": {"type": "string", "description": "Type of document"},
                        "size_bytes": {"type": "integer", "description": "Size of document in bytes"},
                        "confidentiality_level": {"type": "string", "description": "Confidentiality level"},
                        "file_name": {"type": "string", "description": "Name of the file"},
                        "file_format": {"type": "string", "description": "File format (PDF, DOCX, XLSX, CSV)"}
                    },
                    "required": ["user_id", "document_type", "size_bytes", "confidentiality_level", "file_name", "file_format"]
                }
            }
        }
EOF

# Tool 13: create_commitment.py
cat > create_commitment.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateCommitment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, fund_id: str, amount: float,
               due_date: str, compliance_officer_approval: bool) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if not compliance_officer_approval:
            return json.dumps({"error": "Compliance Officer approval required. Process halted."})
        
        investors = data.get("investors", {})
        funds = data.get("funds", {})
        commitments = data.get("commitments", {})
        
        # Validate entities exist
        if str(investor_id) not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        commitment_id = generate_id(commitments)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_commitment = {
            "commitment_id": commitment_id,
            "fund_id": int(fund_id),
            "investor_id": int(investor_id),
            "commitment_amount": amount,
            "commitment_date": due_date,
            "status": "pending",
            "updated_at": timestamp
        }
        
        commitments[str(commitment_id)] = new_commitment
        
        return json.dumps({"commitment_id": str(commitment_id), "success": True, "status": "Pending"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_commitment",
                "description": "Create a new investment commitment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "amount": {"type": "number", "description": "Commitment amount"},
                        "due_date": {"type": "string", "description": "Due date for the commitment"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval flag"}
                    },
                    "required": ["investor_id", "fund_id", "amount", "due_date", "compliance_officer_approval"]
                }
            }
        }
EOF

# Tool 14: fulfill_commitment.py
cat > fulfill_commitment.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FulfillCommitment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str, payment_receipt_amount: float,
               payment_date: str, payment_method: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        commitments = data.get("commitments", {})
        invoices = data.get("invoices", {})
        payments = data.get("payments", {})
        
        # Validate commitment exists
        if str(commitment_id) not in commitments:
            return json.dumps({"error": f"Commitment {commitment_id} not found"})
        
        commitment = commitments[str(commitment_id)]
        timestamp = "2025-10-01T00:00:00ZZ"
        
        # Validate payment method
        valid_methods = ["wire", "cheque", "credit_card", "bank_transfer"]
        if payment_method not in valid_methods:
            return json.dumps({"error": f"Invalid payment method. Must be one of {valid_methods}"})
        
        # Create invoice if not exists
        invoice_id = None
        for inv_id, invoice in invoices.items():
            if invoice.get("commitment_id") == int(commitment_id):
                invoice_id = int(inv_id)
                break
        
        if invoice_id is None:
            invoice_id = generate_id(invoices)
            new_invoice = {
                "invoice_id": invoice_id,
                "commitment_id": int(commitment_id),
                "invoice_date": payment_date,
                "due_date": payment_date,
                "amount": commitment["commitment_amount"],
                "status": "paid",
                "updated_at": timestamp
            }
            invoices[str(invoice_id)] = new_invoice
        
        # Create payment record
        payment_id = generate_id(payments)
        new_payment = {
            "payment_id": payment_id,
            "invoice_id": invoice_id,
            "payment_date": timestamp,
            "amount": payment_receipt_amount,
            "payment_method": payment_method,
            "status": "completed",
            "created_at": timestamp
        }
        payments[str(payment_id)] = new_payment
        
        # Update commitment status
        if payment_receipt_amount >= commitment["commitment_amount"]:
            commitment["status"] = "fulfilled"
            status = "Fulfilled"
        else:
            status = "Pending"
        
        commitment["updated_at"] = timestamp
        
        return json.dumps({
            "commitment_id": str(commitment_id), 
            "success": True, 
            "status": status,
            "amount": payment_receipt_amount
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fulfill_commitment",
                "description": "Process payment to fulfill a commitment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "ID of the commitment"},
                        "payment_receipt_amount": {"type": "number", "description": "Amount received"},
                        "payment_date": {"type": "string", "description": "Date of payment"},
                        "payment_method": {"type": "string", "description": "Method of payment (wire, cheque, credit_card, bank_transfer)"}
                    },
                    "required": ["commitment_id", "payment_receipt_amount", "payment_date", "payment_method"]
                }
            }
        }
EOF

# Tool 15: calculate_nav.py
cat > calculate_nav.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CalculateNav(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, calculation_date: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        nav_records = data.get("nav_records", {})
        trades = data.get("trades", {})
        instrument_prices = data.get("instrument_prices", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        fund = funds[str(fund_id)]
        
        # Simple NAV calculation based on fund size and recent trades
        base_nav = fund.get("size", 1000000.0)  # Default to initial size
        
        # Get recent trades for this fund
        fund_trades = [t for t in trades.values() if t.get("fund_id") == int(fund_id)]
        
        # Calculate portfolio value (simplified)
        portfolio_value = base_nav
        for trade in fund_trades:
            if trade.get("side") == "buy":
                portfolio_value += trade.get("quantity", 0) * trade.get("price", 0) * 0.01  # 1% impact
            else:
                portfolio_value -= trade.get("quantity", 0) * trade.get("price", 0) * 0.01
        
        # Apply market movement (simplified random walk)
        import hashlib
        seed = int(hashlib.md5(f"{fund_id}{calculation_date}".encode()).hexdigest()[:8], 16)
        market_factor = 1 + (seed % 200 - 100) / 10000.0  # -1% to +1% movement
        nav_value = portfolio_value * market_factor
        
        # Create NAV record
        nav_id = generate_id(nav_records)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_nav_record = {
            "nav_id": nav_id,
            "fund_id": int(fund_id),
            "nav_date": calculation_date,
            "nav_value": round(nav_value, 4),
            "updated_at": timestamp
        }
        
        nav_records[str(nav_id)] = new_nav_record
        
        return json.dumps({"nav_value": round(nav_value, 4), "success": True, "message": "NAV updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_nav",
                "description": "Calculate and update Net Asset Value for a fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "calculation_date": {"type": "string", "description": "Date for NAV calculation"}
                    },
                    "required": ["fund_id", "calculation_date"]
                }
            }
        }
EOF

# Tool 16: generate_report.py
cat > generate_report.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GenerateReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], report_type: str, period: str, requester_role: str,
               fund_id: Optional[str] = None, investor_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        reports = data.get("reports", {})
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        
        # Validate report type
        valid_types = ["performance", "financial", "holding"]
        if report_type not in valid_types:
            return json.dumps({"error": f"Invalid report type. Must be one of {valid_types}"})
        
        # Validate entities if provided
        if fund_id and str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        if investor_id and str(investor_id) not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        
        # Check authorization based on role
        if requester_role not in ["admin", "employee"]:
            return json.dumps({"error": "Insufficient permissions to generate reports"})
        
        report_id = generate_id(reports)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_report = {
            "report_id": report_id,
            "fund_id": int(fund_id) if fund_id else None,
            "investor_id": int(investor_id) if investor_id else None,
            "report_date": timestamp.split("T")[0],
            "report_type": report_type,
            "generated_by": 1,  # Default admin user
            "status": "completed",
            "created_at": timestamp,
            "export_period_end": timestamp.split("T")[0]
        }
        
        reports[str(report_id)] = new_report
        
        return json.dumps({"report_id": str(report_id), "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "generate_report",
                "description": "Generate various types of reports",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "report_type": {"type": "string", "description": "Type of report (performance, financial, holding)"},
                        "fund_id": {"type": "string", "description": "ID of the fund (optional)"},
                        "investor_id": {"type": "string", "description": "ID of the investor (optional)"},
                        "period": {"type": "string", "description": "Reporting period"},
                        "requester_role": {"type": "string", "description": "Role of the person requesting the report"}
                    },
                    "required": ["report_type", "period", "requester_role"]
                }
            }
        }
EOF

# Tool 17: resolve_dispute.py
cat > resolve_dispute.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class ResolveDispute(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], involved_ids: List[str], description: str,
               evidence: Dict[str, Any]) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        investors = data.get("investors", {})
        users = data.get("users", {})
        audit_trails = data.get("audit_trails", {})
        
        # Validate all involved parties exist
        for party_id in involved_ids:
            if str(party_id) not in investors and str(party_id) not in users:
                return json.dumps({"error": f"Party {party_id} not found"})
        
        # Create audit trail entry for dispute resolution
        audit_id = generate_id(audit_trails)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_audit_entry = {
            "audit_trail_id": audit_id,
            "reference_id": int(involved_ids[0]) if involved_ids else 1,
            "reference_type": "investor",
            "action": "update",
            "user_id": 1,  # Default admin user
            "field_name": "dispute_resolution",
            "old_value": "dispute_pending",
            "new_value": "dispute_resolved",
            "created_at": timestamp
        }
        
        audit_trails[str(audit_id)] = new_audit_entry
        
        return json.dumps({"success": True, "message": "Dispute resolved"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "resolve_dispute",
                "description": "Resolve disputes between parties",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "involved_ids": {"type": "array", "items": {"type": "string"}, "description": "IDs of involved parties"},
                        "description": {"type": "string", "description": "Description of the dispute"},
                        "evidence": {"type": "object", "description": "Evidence related to the dispute"}
                    },
                    "required": ["involved_ids", "description", "evidence"]
                }
            }
        }
EOF

# Tool 18: update_instrument.py
cat > update_instrument.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateInstrument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: str, proposed_changes: Dict[str, Any],
               user_authorization: bool, compliance_review_required: Optional[bool] = None) -> str:
        
        if not user_authorization:
            return json.dumps({"error": "User authorization required. Process halted."})
        
        if compliance_review_required and not proposed_changes.get("compliance_approved", False):
            return json.dumps({"error": "Compliance review required but not approved. Process halted."})
        
        instruments = data.get("instruments", {})
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            return json.dumps({"error": f"Instrument {instrument_id} not found"})
        
        instrument = instruments[str(instrument_id)]
        
        # Apply changes
        for key, value in proposed_changes.items():
            if key in ["name", "status", "growth_rate"]:
                instrument[key] = value
        
        return json.dumps({"success": True, "message": "Instrument updated successfully"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_instrument",
                "description": "Update instrument details with authorization",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "ID of the instrument to update"},
                        "proposed_changes": {"type": "object", "description": "Dictionary of proposed changes"},
                        "user_authorization": {"type": "boolean", "description": "User authorization flag"},
                        "compliance_review_required": {"type": "boolean", "description": "Whether compliance review is required"}
                    },
                    "required": ["instrument_id", "proposed_changes", "user_authorization"]
                }
            }
        }
EOF

# Tool 19: deactivate_reactivate_instrument.py
cat > deactivate_reactivate_instrument.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeactivateReactivateInstrument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: str, action: str, reason: str,
               fund_manager_approval: bool, compliance_officer_approval: bool) -> str:
        
        if not fund_manager_approval:
            return json.dumps({"error": "Fund Manager approval required. Process halted."})
        
        if not compliance_officer_approval:
            return json.dumps({"error": "Compliance Officer approval required. Process halted."})
        
        instruments = data.get("instruments", {})
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            return json.dumps({"error": f"Instrument {instrument_id} not found"})
        
        # Validate action
        if action not in ["deactivate", "reactivate"]:
            return json.dumps({"error": "Action must be 'deactivate' or 'reactivate'"})
        
        instrument = instruments[str(instrument_id)]
        
        # Update instrument status
        if action == "deactivate":
            instrument["status"] = "inactive"
            message = "Instrument Deactivated"
        else:
            instrument["status"] = "active"
            message = "Instrument Reactivated"
        
        return json.dumps({
            "success": True, 
            "message": message,
            "instrument_id": str(instrument_id)
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "deactivate_reactivate_instrument",
                "description": "Deactivate or reactivate an instrument",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "action": {"type": "string", "description": "Action to perform (deactivate or reactivate)"},
                        "reason": {"type": "string", "description": "Reason for the action"},
                        "fund_manager_approval": {"type": "boolean", "description": "Fund Manager approval flag"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval flag"}
                    },
                    "required": ["instrument_id", "action", "reason", "fund_manager_approval", "compliance_officer_approval"]
                }
            }
        }
EOF

# Tool 20: calculate_liabilities.py
cat > calculate_liabilities.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CalculateLiabilities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_closing_price: float) -> str:
        
        # Calculate liabilities as 1.5% of closing price
        liabilities = instrument_closing_price * 0.015
        
        return json.dumps({"liabilities": round(liabilities, 4)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_liabilities",
                "description": "Calculate liabilities based on instrument closing price",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_closing_price": {"type": "number", "description": "Closing price of the instrument"}
                    },
                    "required": ["instrument_closing_price"]
                }
            }
        }
EOF

# Tool 21: calculate_future_value.py
cat > calculate_future_value.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CalculateFutureValue(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], closing_price_or_nav: float, growth_rate: float, 
               number_of_years: int) -> str:
        
        # Calculate future value using compound interest formula: PV * (1 + r)^n
        future_value = closing_price_or_nav * ((1 + growth_rate) ** number_of_years)
        
        return json.dumps({"future_value": round(future_value, 4)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_future_value",
                "description": "Calculate future value using compound growth",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "closing_price_or_nav": {"type": "number", "description": "Closing price of fund or NAV"},
                        "growth_rate": {"type": "number", "description": "Growth rate (as decimal, e.g., 0.05 for 5%)"},
                        "number_of_years": {"type": "integer", "description": "Number of years"}
                    },
                    "required": ["closing_price_or_nav", "growth_rate", "number_of_years"]
                }
            }
        }
EOF


# Tool 5: delete_fund.py
cat > delete_fund.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, compliance_officer_approval: bool,
               fund_manager_approval: bool) -> str:
        
        if not compliance_officer_approval:
            return json.dumps({"error": "Compliance Officer approval required. Process halted."})
        
        if not fund_manager_approval:
            return json.dumps({"error": "Fund Manager approval required. Process halted."})
        
        funds = data.get("funds", {})
        subscriptions = data.get("subscriptions", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        # Check for active subscriptions
        active_subscriptions = [s for s in subscriptions.values() 
                              if s.get("fund_id") == int(fund_id) and s.get("status") == "approved"]
        
        if active_subscriptions:
            return json.dumps({"error": "Cannot delete fund with active subscriptions. Process halted."})
        
        # Delete fund
        del funds[str(fund_id)]
        
        return json.dumps({"success": True, "message": "Fund deleted"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_fund",
                "description": "Delete a fund after required approvals",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund to delete"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval flag"},
                        "fund_manager_approval": {"type": "boolean", "description": "Fund Manager approval flag"}
                    },
                    "required": ["fund_id", "compliance_officer_approval", "fund_manager_approval"]
                }
            }
        }
EOF

# Tool 6: switch_funds.py
cat > switch_funds.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SwitchFunds(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, current_fund_id: str,
               target_fund_id: str, switch_amount: float) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        subscriptions = data.get("subscriptions", {})
        redemptions = data.get("redemptions", {})
        
        # Validate entities exist
        if str(investor_id) not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        if str(current_fund_id) not in funds:
            return json.dumps({"error": f"Current fund {current_fund_id} not found"})
        if str(target_fund_id) not in funds:
            return json.dumps({"error": f"Target fund {target_fund_id} not found"})
        
        # Find current subscription
        current_subscription = None
        for sub in subscriptions.values():
            if (sub.get("investor_id") == int(investor_id) and 
                sub.get("fund_id") == int(current_fund_id) and 
                sub.get("status") == "approved"):
                current_subscription = sub
                break
        
        if not current_subscription:
            return json.dumps({"error": "No active subscription found in current fund"})
        
        if current_subscription.get("amount", 0) < switch_amount:
            return json.dumps({"error": "Insufficient balance in current fund"})
        
        timestamp = "2025-10-01T00:00:00ZZ"
        
        # Create redemption from current fund
        redemption_id = generate_id(redemptions)
        new_redemption = {
            "redemption_id": redemption_id,
            "subscription_id": current_subscription["subscription_id"],
            "request_date": timestamp.split("T")[0],
            "redemption_amount": switch_amount,
            "status": "processed",
            "processed_date": timestamp.split("T")[0],
            "updated_at": timestamp,
            "redemption_fee": 0.0
        }
        redemptions[str(redemption_id)] = new_redemption
        
        # Update current subscription
        current_subscription["amount"] -= switch_amount
        current_subscription["updated_at"] = timestamp
        
        # Create new subscription in target fund
        subscription_id = generate_id(subscriptions)
        new_subscription = {
            "subscription_id": subscription_id,
            "fund_id": int(target_fund_id),
            "investor_id": int(investor_id),
            "amount": switch_amount,
            "status": "approved",
            "request_assigned_to": 1,  # Default admin
            "request_date": timestamp.split("T")[0],
            "approval_date": timestamp.split("T")[0],
            "updated_at": timestamp
        }
        subscriptions[str(subscription_id)] = new_subscription
        
        return json.dumps({"success": True, "message": "Switch complete"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "switch_funds",
                "description": "Switch investor funds between two funds",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "current_fund_id": {"type": "string", "description": "ID of the current fund"},
                        "target_fund_id": {"type": "string", "description": "ID of the target fund"},
                        "switch_amount": {"type": "number", "description": "Amount to switch"}
                    },
                    "required": ["investor_id", "current_fund_id", "target_fund_id", "switch_amount"]
                }
            }
        }
EOF

# Tool 7: create_subscription.py
cat > create_subscription.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, fund_id: str, amount: float,
               payment_details: Dict[str, Any], compliance_officer_approval: bool) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if not compliance_officer_approval:
            return json.dumps({"error": "Compliance Officer approval required. Process halted."})
        
        investors = data.get("investors", {})
        funds = data.get("funds", {})
        subscriptions = data.get("subscriptions", {})
        
        # Validate entities exist
        if str(investor_id) not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        # Check if fund is open
        if funds[str(fund_id)].get("status") != "open":
            return json.dumps({"error": "Fund is not open for subscriptions"})
        
        subscription_id = generate_id(subscriptions)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        # Determine status based on payment details
        status = "approved" if payment_details.get("confirmed", False) else "pending"
        
        new_subscription = {
            "subscription_id": subscription_id,
            "fund_id": int(fund_id),
            "investor_id": int(investor_id),
            "amount": amount,
            "status": status,
            "request_assigned_to": 1,  # Default admin
            "request_date": timestamp.split("T")[0],
            "approval_date": timestamp.split("T")[0] if status == "approved" else None,
            "updated_at": timestamp
        }
        
        subscriptions[str(subscription_id)] = new_subscription
        
        return_status = "active" if status == "approved" else "funds_pending"
        return json.dumps({"subscription_id": str(subscription_id), "success": True, "status": return_status})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_subscription",
                "description": "Create a new fund subscription",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "amount": {"type": "number", "description": "Subscription amount"},
                        "payment_details": {"type": "object", "description": "Payment details"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval flag"}
                    },
                    "required": ["investor_id", "fund_id", "amount", "payment_details", "compliance_officer_approval"]
                }
            }
        }
EOF

# Tool 8: update_subscription.py
cat > update_subscription.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: str, changes: Dict[str, Any],
               compliance_officer_approval: bool, finance_officer_approval: bool) -> str:
        
        if not compliance_officer_approval:
            return json.dumps({"error": "Compliance Officer approval required. Process halted."})
        
        if not finance_officer_approval:
            return json.dumps({"error": "Finance Officer approval required. Process halted."})
        
        subscriptions = data.get("subscriptions", {})
        
        # Validate subscription exists
        if str(subscription_id) not in subscriptions:
            return json.dumps({"error": f"Subscription {subscription_id} not found"})
        
        subscription = subscriptions[str(subscription_id)]
        timestamp = "2025-10-01T00:00:00ZZ"
        
        # Apply changes
        for key, value in changes.items():
            if key in ["amount", "status"]:
                subscription[key] = value
        
        subscription["updated_at"] = timestamp
        
        return json.dumps({"success": True, "message": "Subscription updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_subscription",
                "description": "Update subscription details with required approvals",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "ID of the subscription to update"},
                        "changes": {"type": "object", "description": "Dictionary of changes"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval flag"},
                        "finance_officer_approval": {"type": "boolean", "description": "Finance Officer approval flag"}
                    },
                    "required": ["subscription_id", "changes", "compliance_officer_approval", "finance_officer_approval"]
                }
            }
        }
EOF

# Tool 9: cancel_subscription.py
cat > cancel_subscription.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CancelSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: str, reason: str) -> str:
        
        subscriptions = data.get("subscriptions", {})
        
        # Validate subscription exists
        if str(subscription_id) not in subscriptions:
            return json.dumps({"error": f"Subscription {subscription_id} not found"})
        
        subscription = subscriptions[str(subscription_id)]
        timestamp = "2025-10-01T00:00:00ZZ"
        
        # Update subscription status
        subscription["status"] = "cancelled"
        subscription["updated_at"] = timestamp
        
        return json.dumps({"success": True, "message": "Cancellation complete"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "cancel_subscription",
                "description": "Cancel a subscription",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "ID of the subscription to cancel"},
                        "reason": {"type": "string", "description": "Reason for cancellation"}
                    },
                    "required": ["subscription_id", "reason"]
                }
            }
        }
EOF

# Tool 10: execute_trade.py
cat > execute_trade.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ExecuteTrade(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, asset_details: Dict[str, Any],
               quantity: float, price_limit: float, trader_id: str,
               fund_manager_approval: bool, risk_manager_clearance: bool) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if not fund_manager_approval:
            return json.dumps({"error": "Fund Manager approval required. Process halted."})
        
        if not risk_manager_clearance:
            return json.dumps({"error": "Risk Manager clearance required. Process halted."})
        
        funds = data.get("funds", {})
        users = data.get("users", {})
        trades = data.get("trades", {})
        instruments = data.get("instruments", {})
        
        # Validate entities exist
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        if str(trader_id) not in users:
            return json.dumps({"error": f"Trader {trader_id} not found"})
        
        # Find or create instrument
        instrument_id = None
        ticker = asset_details.get("ticker")
        for inst_id, inst in instruments.items():
            if inst.get("ticker") == ticker:
                instrument_id = int(inst_id)
                break
        
        if instrument_id is None:
            return json.dumps({"error": f"Instrument with ticker {ticker} not found"})
        
        trade_id = generate_id(trades)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        # Determine trade side
        side = "buy" if quantity > 0 else "sell"
        
        new_trade = {
            "trade_id": trade_id,
            "fund_id": int(fund_id),
            "instrument_id": instrument_id,
            "trade_date": timestamp,
            "quantity": abs(quantity),
            "price": price_limit,
            "side": side,
            "status": "executed",
            "created_at": timestamp
        }
        
        trades[str(trade_id)] = new_trade
        
        return json.dumps({"trade_id": str(trade_id), "success": True, "message": "Trade executed"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "execute_trade",
                "description": "Execute a trade after required approvals",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "asset_details": {"type": "object", "description": "Asset details including ticker"},
                        "quantity": {"type": "number", "description": "Trade quantity: positive for buy, negative for sell"},
                        "price_limit": {"type": "number", "description": "Price limit"},
                        "trader_id": {"type": "string", "description": "ID of the trader"},
                        "fund_manager_approval": {"type": "boolean", "description": "Fund Manager approval flag"},
                        "risk_manager_clearance": {"type": "boolean", "description": "Risk Manager clearance flag"}
                    },
                    "required": ["fund_id", "asset_details", "quantity", "price_limit", "trader_id", 
                               "fund_manager_approval", "risk_manager_clearance"]
                }
            }
        }
EOF

#!/bin/bash

# Create process_redemption.py
cat > process_redemption.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ProcessRedemption(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, fund_id: str, 
               amount_or_units: float, reason: str, compliance_approval: bool, 
               finance_approval: bool) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        investors = data.get("investors", {})
        funds = data.get("funds", {})
        subscriptions = data.get("subscriptions", {})
        redemptions = data.get("redemptions", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            return json.dumps({"success": False, "message": "Investor not found", "halt": True})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            return json.dumps({"success": False, "message": "Fund not found", "halt": True})
        
        # Check if fund is open
        if funds[str(fund_id)].get("status") != "open":
            return json.dumps({"success": False, "message": "Fund is not open for redemptions", "halt": True})
        
        # Validate approvals
        if not compliance_approval or not finance_approval:
            return json.dumps({"success": False, "message": "Required approvals not obtained", "halt": True})
        
        # Find existing subscription
        subscription_id = None
        for sub_id, sub in subscriptions.items():
            if sub.get("investor_id") == investor_id and sub.get("fund_id") == fund_id:
                subscription_id = sub_id
                break
        
        if not subscription_id:
            return json.dumps({"success": False, "message": "No subscription found for this investor and fund", "halt": True})
        
        redemption_id = generate_id(redemptions)
        timestamp = "2025-10-01T00:00:00"
        
        new_redemption = {
            "redemption_id": redemption_id,
            "subscription_id": subscription_id,
            "request_date": "2025-10-01",
            "redemption_amount": amount_or_units,
            "status": "approved",
            "processed_date": "2025-10-01",
            "updated_at": timestamp,
            "redemption_fee": round(amount_or_units * 0.01, 2)  # 1% fee
        }
        
        redemptions[str(redemption_id)] = new_redemption
        return json.dumps({"success": True, "message": "Redemption processed"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_redemption",
                "description": "Process a redemption request for an investor",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "amount_or_units": {"type": "number", "description": "Amount or units to redeem"},
                        "reason": {"type": "string", "description": "Reason for redemption"},
                        "compliance_approval": {"type": "boolean", "description": "Compliance approval flag"},
                        "finance_approval": {"type": "boolean", "description": "Finance approval flag"}
                    },
                    "required": ["investor_id", "fund_id", "amount_or_units", "reason", "compliance_approval", "finance_approval"]
                }
            }
        }
EOF

# Create create_upload_document.py
cat > create_upload_document.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateUploadDocument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, document_type: str, 
               size_bytes: int, confidentiality_level: str, file_name: str, 
               file_format: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        documents = data.get("documents", {})
        
        # Validate user exists
        if str(user_id) not in users:
            return json.dumps({"success": False, "message": "User not found", "halt": True})
        
        # Validate file format
        valid_formats = ["pdf", "docx", "xlsx", "csv"]
        if file_format.lower() not in valid_formats:
            return json.dumps({"success": False, "message": f"Invalid file format. Must be one of {valid_formats}", "halt": True})
        
        # Validate confidentiality level
        valid_levels = ["public", "internal", "confidential", "restricted"]
        if confidentiality_level.lower() not in valid_levels:
            return json.dumps({"success": False, "message": f"Invalid confidentiality level. Must be one of {valid_levels}", "halt": True})
        
        document_id = generate_id(documents)
        timestamp = "2025-10-01T00:00:00"
        
        new_document = {
            "document_id": document_id,
            "name": file_name,
            "type": file_format.lower(),
            "uploaded_by": user_id,
            "upload_date": timestamp,
            "report_id": None,
            "size_bytes": size_bytes,
            "status": "available"
        }
        
        documents[str(document_id)] = new_document
        return json.dumps({"doc_id": str(document_id), "success": True, "status": "available"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_upload_document",
                "description": "Create and upload a document to the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user uploading the document"},
                        "document_type": {"type": "string", "description": "Type of document"},
                        "size_bytes": {"type": "integer", "description": "Size of document in bytes"},
                        "confidentiality_level": {"type": "string", "description": "Confidentiality level"},
                        "file_name": {"type": "string", "description": "Name of the file"},
                        "file_format": {"type": "string", "description": "File format: PDF, DOCX, XLSX, or CSV"}
                    },
                    "required": ["user_id", "document_type", "size_bytes", "confidentiality_level", "file_name", "file_format"]
                }
            }
        }
EOF

# Create create_commitment.py
cat > create_commitment.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateCommitment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, fund_id: str, 
               amount: float, due_date: str, compliance_officer_approval: bool) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        investors = data.get("investors", {})
        funds = data.get("funds", {})
        commitments = data.get("commitments", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            return json.dumps({"success": False, "message": "Investor not found", "halt": True})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            return json.dumps({"success": False, "message": "Fund not found", "halt": True})
        
        # Validate compliance approval
        if not compliance_officer_approval:
            return json.dumps({"success": False, "message": "Compliance officer approval required", "halt": True})
        
        # Validate amount
        if amount <= 0:
            return json.dumps({"success": False, "message": "Amount must be positive", "halt": True})
        
        commitment_id = generate_id(commitments)
        timestamp = "2025-10-01T00:00:00"
        
        new_commitment = {
            "commitment_id": commitment_id,
            "fund_id": fund_id,
            "investor_id": investor_id,
            "commitment_amount": amount,
            "commitment_date": due_date,
            "status": "pending",
            "updated_at": timestamp
        }
        
        commitments[str(commitment_id)] = new_commitment
        return json.dumps({"commitment_id": str(commitment_id), "success": True, "status": "Pending"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_commitment",
                "description": "Create a new commitment for an investor to a fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "amount": {"type": "number", "description": "Commitment amount"},
                        "due_date": {"type": "string", "description": "Due date for the commitment"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval flag"}
                    },
                    "required": ["investor_id", "fund_id", "amount", "due_date", "compliance_officer_approval"]
                }
            }
        }
EOF

# Create fulfill_commitment.py
cat > fulfill_commitment.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FulfillCommitment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str, payment_receipt_amount: float, 
               payment_date: str, payment_method: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        commitments = data.get("commitments", {})
        invoices = data.get("invoices", {})
        payments = data.get("payments", {})
        
        # Validate commitment exists
        if str(commitment_id) not in commitments:
            return json.dumps({"success": False, "message": "Commitment not found", "halt": True})
        
        commitment = commitments[str(commitment_id)]
        
        # Validate payment method
        valid_methods = ["wire", "cheque", "credit_card", "bank_transfer"]
        if payment_method.lower() not in valid_methods:
            return json.dumps({"success": False, "message": f"Invalid payment method. Must be one of {valid_methods}", "halt": True})
        
        # Validate amount
        if payment_receipt_amount <= 0:
            return json.dumps({"success": False, "message": "Payment amount must be positive", "halt": True})
        
        # Create invoice if not exists
        invoice_id = None
        for inv_id, inv in invoices.items():
            if inv.get("commitment_id") == commitment_id:
                invoice_id = inv_id
                break
        
        if not invoice_id:
            invoice_id = generate_id(invoices)
            new_invoice = {
                "invoice_id": invoice_id,
                "commitment_id": commitment_id,
                "invoice_date": payment_date,
                "due_date": payment_date,
                "amount": commitment["commitment_amount"],
                "status": "issued",
                "updated_at": "2025-10-01T00:00:00"
            }
            invoices[str(invoice_id)] = new_invoice
        
        # Create payment record
        payment_id = generate_id(payments)
        timestamp = "2025-10-01T00:00:00"
        
        new_payment = {
            "payment_id": payment_id,
            "invoice_id": str(invoice_id),
            "payment_date": timestamp,
            "amount": payment_receipt_amount,
            "payment_method": payment_method.lower(),
            "status": "completed",
            "created_at": timestamp
        }
        
        payments[str(payment_id)] = new_payment
        
        # Update commitment status
        if payment_receipt_amount >= commitment["commitment_amount"]:
            commitment["status"] = "fulfilled"
            status = "Fulfilled"
        else:
            status = "Pending"
        
        commitment["updated_at"] = timestamp
        
        # Update invoice status if payment covers full amount
        if payment_receipt_amount >= invoices[str(invoice_id)]["amount"]:
            invoices[str(invoice_id)]["status"] = "paid"
            invoices[str(invoice_id)]["updated_at"] = timestamp
        
        return json.dumps({
            "commitment_id": commitment_id, 
            "success": True, 
            "status": status, 
            "amount": payment_receipt_amount
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fulfill_commitment",
                "description": "Fulfill a commitment by recording payment receipt",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "ID of the commitment"},
                        "payment_receipt_amount": {"type": "number", "description": "Amount received"},
                        "payment_date": {"type": "string", "description": "Date of payment"},
                        "payment_method": {"type": "string", "description": "Method of payment: wire, cheque, credit_card, bank_transfer"}
                    },
                    "required": ["commitment_id", "payment_receipt_amount", "payment_date", "payment_method"]
                }
            }
        }
EOF

# Create calculate_nav.py
cat > calculate_nav.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CalculateNav(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, calculation_date: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        nav_records = data.get("nav_records", {})
        trades = data.get("trades", {})
        instrument_prices = data.get("instrument_prices", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            return json.dumps({"success": False, "message": "Fund not found", "halt": True})
        
        fund = funds[str(fund_id)]
        
        # Calculate NAV based on fund size and recent trades
        base_nav = float(fund.get("size", 1000000))  # Use fund size as base
        
        # Adjust based on recent trades for this fund
        trade_adjustments = 0
        for trade in trades.values():
            if trade.get("fund_id") == fund_id and trade.get("status") == "executed":
                trade_value = float(trade.get("quantity", 0)) * float(trade.get("price", 0))
                if trade.get("side") == "buy":
                    trade_adjustments += trade_value
                else:
                    trade_adjustments -= trade_value
        
        # Simple NAV calculation: base + 5% growth + trade adjustments
        nav_value = round(base_nav * 1.05 + trade_adjustments, 4)
        
        # Create or update NAV record
        nav_id = generate_id(nav_records)
        timestamp = "2025-10-01T00:00:00"
        
        new_nav_record = {
            "nav_id": nav_id,
            "fund_id": fund_id,
            "nav_date": calculation_date,
            "nav_value": nav_value,
            "updated_at": timestamp
        }
        
        nav_records[str(nav_id)] = new_nav_record
        
        return json.dumps({"nav_value": nav_value, "success": True, "message": "NAV updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_nav",
                "description": "Calculate and update the Net Asset Value "NAV" for a fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "calculation_date": {"type": "string", "description": "Date for NAV calculation"}
                    },
                    "required": ["fund_id", "calculation_date"]
                }
            }
        }
EOF

# Create generate_report.py
cat > generate_report.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GenerateReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], report_type: str, period: str, 
               requester_role: str, fund_id: Optional[str] = None, 
               investor_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        reports = data.get("reports", {})
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        users = data.get("users", {})
        
        # Validate report type
        valid_types = ["performance", "financial", "holding"]
        if report_type.lower() not in valid_types:
            return json.dumps({"success": False, "message": f"Invalid report type. Must be one of {valid_types}", "halt": True})
        
        # Validate requester role
        valid_roles = ["admin", "employee"]
        if requester_role.lower() not in valid_roles:
            return json.dumps({"success": False, "message": f"Invalid requester role. Must be one of {valid_roles}", "halt": True})
        
        # If fund_id provided, validate it exists
        if fund_id and str(fund_id) not in funds:
            return json.dumps({"success": False, "message": "Fund not found", "halt": True})
        
        # If investor_id provided, validate it exists
        if investor_id and str(investor_id) not in investors:
            return json.dumps({"success": False, "message": "Investor not found", "halt": True})
        
        # Find a user with the appropriate role to be the generator
        generated_by = None
        for user_id, user in users.items():
            if user.get("role") == requester_role.lower():
                generated_by = user_id
                break
        
        if not generated_by:
            return json.dumps({"success": False, "message": "No authorized user found to generate report", "halt": True})
        
        report_id = generate_id(reports)
        timestamp = "2025-10-01T00:00:00"
        
        # Set fund_id to first available fund if not specified and needed
        if not fund_id and funds:
            fund_id = list(funds.keys())[0]
        
        new_report = {
            "report_id": report_id,
            "fund_id": fund_id,
            "investor_id": investor_id,
            "report_date": "2025-10-01",
            "report_type": report_type.lower(),
            "generated_by": generated_by,
            "status": "completed",
            "created_at": timestamp,
            "export_period_end": "2025-10-01"
        }
        
        reports[str(report_id)] = new_report
        
        return json.dumps({"report_id": str(report_id), "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "generate_report",
                "description": "Generate a report for funds or investors",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "report_type": {"type": "string", "description": "Type of report: performance, financial, holding"},
                        "fund_id": {"type": "string", "description": "ID of the fund 'optional'"},
                        "investor_id": {"type": "string", "description": "ID of the investor 'optional'"},
                        "period": {"type": "string", "description": "Reporting period"},
                        "requester_role": {"type": "string", "description": "Role of the person requesting the report"}
                    },
                    "required": ["report_type", "period", "requester_role"]
                }
            }
        }
EOF

# Create resolve_dispute.py
cat > resolve_dispute.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class ResolveDispute(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], involved_ids: List[str], description: str, 
               evidence: Dict[str, Any]) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        investors = data.get("investors", {})
        audit_trails = data.get("audit_trails", {})
        
        # Validate that involved parties exist (check both users and investors)
        valid_parties = []
        for party_id in involved_ids:
            if str(party_id) in users or str(party_id) in investors:
                valid_parties.append(party_id)
            else:
                return json.dumps({"success": False, "message": f"Party {party_id} not found", "halt": True})
        
        # Validate evidence is provided
        if not evidence or not isinstance(evidence, dict):
            return json.dumps({"success": False, "message": "Valid evidence dictionary required", "halt": True})
        
        # Validate description
        if not description or len(description.strip()) == 0:
            return json.dumps({"success": False, "message": "Description is required", "halt": True})
        
        # Find an admin user to log the resolution
        admin_user = None
        for user_id, user in users.items():
            if user.get("role") == "admin":
                admin_user = user_id
                break
        
        if not admin_user:
            return json.dumps({"success": False, "message": "No admin user available to process dispute", "halt": True})
        
        # Create audit trail entry for dispute resolution
        audit_id = generate_id(audit_trails)
        timestamp = "2025-10-01T00:00:00"
        
        audit_entry = {
            "audit_trail_id": audit_id,
            "reference_id": involved_ids[0],  # Use first party as reference
            "reference_type": "user",
            "action": "process",
            "user_id": admin_user,
            "field_name": "dispute_resolution",
            "old_value": "disputed",
            "new_value": f"resolved: {description}",
            "created_at": timestamp
        }
        
        audit_trails[str(audit_id)] = audit_entry
        
        return json.dumps({"success": True, "message": "Dispute resolved"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "resolve_dispute",
                "description": "Resolve a dispute between parties with evidence",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "involved_ids": {"type": "array", "items": {"type": "string"}, "description": "IDs of involved parties"},
                        "description": {"type": "string", "description": "Description of the dispute"},
                        "evidence": {"type": "object", "description": "Evidence related to the dispute"}
                    },
                    "required": ["involved_ids", "description", "evidence"]
                }
            }
        }
EOF

# Create update_instrument.py
cat > update_instrument.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateInstrument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: str, proposed_changes: Dict[str, Any], 
               user_authorization: bool, compliance_review_required: Optional[bool] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        instruments = data.get("instruments", {})
        users = data.get("users", {})
        audit_trails = data.get("audit_trails", {})
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            return json.dumps({"success": False, "message": "Instrument not found", "halt": True})
        
        # Validate user authorization
        if not user_authorization:
            return json.dumps({"success": False, "message": "User authorization required", "halt": True})
        
        # Validate proposed changes
        if not proposed_changes or not isinstance(proposed_changes, dict):
            return json.dumps({"success": False, "message": "Valid proposed changes required", "halt": True})
        
        instrument = instruments[str(instrument_id)]
        
        # Check current status and validate action
        current_status = instrument.get("status", "active")
        if action.lower() == "deactivate" and current_status == "inactive":
            return json.dumps({"success": False, "message": "Instrument is already inactive", "halt": True})
        elif action.lower() == "reactivate" and current_status == "active":
            return json.dumps({"success": False, "message": "Instrument is already active", "halt": True})
        
        # Find an admin user to perform the action
        admin_user = None
        for user_id, user in users.items():
            if user.get("role") == "admin":
                admin_user = user_id
                break
        
        if not admin_user:
            return json.dumps({"success": False, "message": "No authorized user found to perform action", "halt": True})
        
        # Update instrument status
        old_status = instrument.get("status")
        new_status = "inactive" if action.lower() == "deactivate" else "active"
        instrument["status"] = new_status
        
        # Create audit trail entry
        audit_id = generate_id(audit_trails)
        timestamp = "2025-10-01T00:00:00"
        
        audit_entry = {
            "audit_trail_id": audit_id,
            "reference_id": instrument_id,
            "reference_type": "instrument",
            "action": action.lower(),
            "user_id": admin_user,
            "field_name": "status",
            "old_value": old_status,
            "new_value": new_status,
            "created_at": timestamp
        }
        audit_trails[str(audit_id)] = audit_entry
        
        action_past = "Deactivated" if action.lower() == "deactivate" else "Reactivated"
        return json.dumps({
            "success": True, 
            "message": f"Instrument {action_past}", 
            "instrument_id": instrument_id
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "deactivate_reactivate_instrument",
                "description": "Deactivate or reactivate an instrument",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "action": {"type": "string", "description": "Action to perform: deactivate or reactivate"},
                        "reason": {"type": "string", "description": "Reason for the action"},
                        "fund_manager_approval": {"type": "boolean", "description": "Fund Manager approval flag"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval flag"}
                    },
                    "required": ["instrument_id", "action", "reason", "fund_manager_approval", "compliance_officer_approval"]
                }
            }
        }
EOF

# Create calculate_liabilities.py
cat > calculate_liabilities.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CalculateLiabilities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_closing_price: float) -> str:
        
        # Validate closing price
        if instrument_closing_price <= 0:
            return json.dumps({"success": False, "message": "Instrument closing price must be positive", "halt": True})
        
        # Calculate liabilities as 1.5% of closing price
        liabilities = round(instrument_closing_price * 0.015, 4)
        
        return json.dumps({"liabilities": liabilities})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_liabilities",
                "description": "Calculate liabilities as 1.5% of instrument closing price",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_closing_price": {"type": "number", "description": "Closing price of the instrument"}
                    },
                    "required": ["instrument_closing_price"]
                }
            }
        }
EOF

# Create calculate_future_value.py
cat > calculate_future_value.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CalculateFutureValue(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], closing_price_or_nav: float, growth_rate: float, 
               number_of_years: int) -> str:
        
        # Validate inputs
        if closing_price_or_nav <= 0:
            return json.dumps({"success": False, "message": "Closing price or NAV must be positive", "halt": True})
        
        if number_of_years < 0:
            return json.dumps({"success": False, "message": "Number of years must be non-negative", "halt": True})
        
        # Calculate future value using formula: FV = PV * (1 + r)^n
        future_value = round(closing_price_or_nav * ((1 + growth_rate) ** number_of_years), 4)
        
        return json.dumps({"future_value": future_value})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_future_value",
                "description": "Calculate future value using compound interest formula",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "closing_price_or_nav": {"type": "number", "description": "Closing price of fund or NAV"},
                        "growth_rate": {"type": "number", "description": "Growth rate 'r'"},
                        "number_of_years": {"type": "integer", "description": "Number of years 'n'"}
                    },
                    "required": ["closing_price_or_nav", "growth_rate", "number_of_years"]
                }
            }
        }
EOF