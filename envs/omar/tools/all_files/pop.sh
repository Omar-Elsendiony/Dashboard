#!/bin/bash

# Create get_investor_profile.py
cat > get_investor_profile.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorProfile(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str) -> str:
        investors = data.get("investors", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        investor = investors[str(investor_id)]
        return json.dumps(investor)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_profile",
                "description": "Retrieve complete investor profile information including KYC details, status, and contact information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
EOF

# Create get_investor_portfolio.py
cat > get_investor_portfolio.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorPortfolio(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str) -> str:
        investors = data.get("investors", {})
        portfolios = data.get("portfolios", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Find investor's portfolio
        investor_portfolio = None
        for portfolio in portfolios.values():
            if portfolio.get("investor_id") == investor_id:
                investor_portfolio = portfolio
                break
        
        if not investor_portfolio:
            return json.dumps({"message": "No portfolio found for investor"})
        
        return json.dumps(investor_portfolio)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_portfolio",
                "description": "Get the investor's complete portfolio overview including all holdings and performance metrics",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
EOF

# Create get_investor_portfolio_holdings.py
cat > get_investor_portfolio_holdings.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorPortfolioHoldings(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str) -> str:
        investors = data.get("investors", {})
        portfolios = data.get("portfolios", {})
        portfolio_holdings = data.get("portfolio_holdings", {})
        funds = data.get("funds", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Find investor's portfolio
        investor_portfolio = None
        for portfolio in portfolios.values():
            if portfolio.get("investor_id") == investor_id:
                investor_portfolio = portfolio
                break
        
        if not investor_portfolio:
            return json.dumps([])
        
        # Get holdings for this portfolio
        holdings = []
        for holding in portfolio_holdings.values():
            if holding.get("portfolio_id") == investor_portfolio.get("portfolio_id"):
                # Enrich with fund details
                fund_id = holding.get("fund_id")
                fund_details = funds.get(str(fund_id), {})
                
                enriched_holding = {
                    **holding,
                    "fund_name": fund_details.get("name"),
                    "fund_type": fund_details.get("fund_type"),
                    "fund_status": fund_details.get("status")
                }
                holdings.append(enriched_holding)
        
        return json.dumps(holdings)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_portfolio_holdings",
                "description": "Retrieve detailed breakdown of all fund holdings within the investor's portfolio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
EOF

# Create get_available_funds.py
cat > get_available_funds.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetAvailableFunds(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: Optional[str] = None, 
               fund_type: Optional[str] = None, status: Optional[str] = None) -> str:
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        results = []
        
        # If investor_id is provided, validate it exists
        if investor_id and str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        for fund in funds.values():
            # Filter by fund type if specified
            if fund_type and fund.get("fund_type") != fund_type:
                continue
            
            # Filter by status if specified (default to "open" if not specified)
            if status and fund.get("status") != status:
                continue
            elif not status and fund.get("status") != "open":
                continue
            
            results.append(fund)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_available_funds",
                "description": "List all funds available for investment based on investor's accreditation and eligibility",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor (optional)"},
                        "fund_type": {"type": "string", "description": "Filter by fund type"},
                        "status": {"type": "string", "description": "Filter by fund status (open, closed)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create get_fund_details.py
cat > get_fund_details.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFundDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str) -> str:
        funds = data.get("funds", {})
        users = data.get("users", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        fund = funds[str(fund_id)]
        
        # Enrich with manager details
        manager_id = fund.get("manager_id")
        manager_details = users.get(str(manager_id), {})
        
        enriched_fund = {
            **fund,
            "manager_name": f"{manager_details.get('first_name', '')} {manager_details.get('last_name', '')}".strip(),
            "manager_email": manager_details.get("email")
        }
        
        return json.dumps(enriched_fund)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_fund_details",
                "description": "Get comprehensive information about a specific fund including strategy, fees, and performance",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"}
                    },
                    "required": ["fund_id"]
                }
            }
        }
EOF

# Create get_fund_nav_history.py
cat > get_fund_nav_history.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFundNavHistory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, 
               start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        funds = data.get("funds", {})
        nav_records = data.get("nav_records", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Get NAV records for this fund
        fund_navs = []
        for nav in nav_records.values():
            if nav.get("fund_id") == fund_id:
                nav_date = nav.get("nav_date")
                
                # Filter by date range if provided
                if start_date and nav_date < start_date:
                    continue
                if end_date and nav_date > end_date:
                    continue
                
                fund_navs.append(nav)
        
        # Sort by date
        fund_navs.sort(key=lambda x: x.get("nav_date", ""))
        
        return json.dumps(fund_navs)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_fund_nav_history",
                "description": "Retrieve historical Net Asset Value data for specific funds over time periods",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "start_date": {"type": "string", "description": "Start date for NAV history (YYYY-MM-DD format)"},
                        "end_date": {"type": "string", "description": "End date for NAV history (YYYY-MM-DD format)"}
                    },
                    "required": ["fund_id"]
                }
            }
        }
EOF

# Create get_investor_subscriptions.py
cat > get_investor_subscriptions.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorSubscriptions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, 
               status: Optional[str] = None, fund_id: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        subscriptions = data.get("subscriptions", {})
        funds = data.get("funds", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Get subscriptions for this investor
        investor_subscriptions = []
        for subscription in subscriptions.values():
            if subscription.get("investor_id") == investor_id:
                # Filter by status if specified
                if status and subscription.get("status") != status:
                    continue
                
                # Filter by fund if specified
                if fund_id and subscription.get("fund_id") != fund_id:
                    continue
                
                # Enrich with fund details
                sub_fund_id = subscription.get("fund_id")
                fund_details = funds.get(str(sub_fund_id), {})
                
                enriched_subscription = {
                    **subscription,
                    "fund_name": fund_details.get("name"),
                    "fund_type": fund_details.get("fund_type")
                }
                investor_subscriptions.append(enriched_subscription)
        
        return json.dumps(investor_subscriptions)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_subscriptions",
                "description": "List all subscription requests and their current status (pending, approved, cancelled)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "status": {"type": "string", "description": "Filter by subscription status (pending, approved, cancelled)"},
                        "fund_id": {"type": "string", "description": "Filter by fund ID"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
EOF

# Create get_investor_commitments.py
cat > get_investor_commitments.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorCommitments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, 
               status: Optional[str] = None, fund_id: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        commitments = data.get("commitments", {})
        funds = data.get("funds", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Get commitments for this investor
        investor_commitments = []
        for commitment in commitments.values():
            if commitment.get("investor_id") == investor_id:
                # Filter by status if specified
                if status and commitment.get("status") != status:
                    continue
                
                # Filter by fund if specified
                if fund_id and commitment.get("fund_id") != fund_id:
                    continue
                
                # Enrich with fund details
                comm_fund_id = commitment.get("fund_id")
                fund_details = funds.get(str(comm_fund_id), {})
                
                enriched_commitment = {
                    **commitment,
                    "fund_name": fund_details.get("name"),
                    "fund_type": fund_details.get("fund_type")
                }
                investor_commitments.append(enriched_commitment)
        
        return json.dumps(investor_commitments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_commitments",
                "description": "Retrieve all capital commitments and their fulfillment status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "status": {"type": "string", "description": "Filter by commitment status (pending, fulfilled)"},
                        "fund_id": {"type": "string", "description": "Filter by fund ID"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
EOF

# Create get_investor_redemptions.py
cat > get_investor_redemptions.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorRedemptions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, 
               status: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        redemptions = data.get("redemptions", {})
        subscriptions = data.get("subscriptions", {})
        funds = data.get("funds", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Get redemptions for this investor
        investor_redemptions = []
        for redemption in redemptions.values():
            # Find the subscription this redemption relates to
            subscription_id = redemption.get("subscription_id")
            subscription = subscriptions.get(str(subscription_id), {})
            
            # Check if this subscription belongs to our investor
            if subscription.get("investor_id") == investor_id:
                # Filter by status if specified
                if status and redemption.get("status") != status:
                    continue
                
                # Enrich with fund details
                fund_id = subscription.get("fund_id")
                fund_details = funds.get(str(fund_id), {})
                
                enriched_redemption = {
                    **redemption,
                    "fund_id": fund_id,
                    "fund_name": fund_details.get("name"),
                    "fund_type": fund_details.get("fund_type"),
                    "original_subscription_amount": subscription.get("amount")
                }
                investor_redemptions.append(enriched_redemption)
        
        return json.dumps(investor_redemptions)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_redemptions",
                "description": "View all redemption requests including pending, approved, and processed transactions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "status": {"type": "string", "description": "Filter by redemption status (pending, approved, processed, cancelled)"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
EOF

# Create get_investor_statements.py
cat > get_investor_statements.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorStatements(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, 
               report_type: Optional[str] = None, start_date: Optional[str] = None, 
               end_date: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        reports = data.get("reports", {})
        documents = data.get("documents", {})
        users = data.get("users", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Get reports for this investor
        investor_statements = []
        for report in reports.values():
            if report.get("investor_id") == investor_id:
                # Filter by report type if specified
                if report_type and report.get("report_type") != report_type:
                    continue
                
                # Filter by date range if provided
                report_date = report.get("report_date")
                if start_date and report_date < start_date:
                    continue
                if end_date and report_date > end_date:
                    continue
                
                # Enrich with generator details
                generated_by = report.get("generated_by")
                generator = users.get(str(generated_by), {})
                
                # Find associated documents
                report_id = report.get("report_id")
                associated_docs = []
                for doc in documents.values():
                    if doc.get("report_id") == report_id:
                        associated_docs.append({
                            "document_id": doc.get("document_id"),
                            "name": doc.get("name"),
                            "format": doc.get("format"),
                            "size_bytes": doc.get("size_bytes"),
                            "upload_date": doc.get("upload_date")
                        })
                
                enriched_report = {
                    **report,
                    "generator_name": f"{generator.get('first_name', '')} {generator.get('last_name', '')}".strip(),
                    "documents": associated_docs
                }
                investor_statements.append(enriched_report)
        
        return json.dumps(investor_statements)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_statements",
                "description": "Access periodic statements including performance, holdings, and transaction summaries",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "report_type": {"type": "string", "description": "Filter by report type (performance, holding, financial)"},
                        "start_date": {"type": "string", "description": "Start date for reports (YYYY-MM-DD format)"},
                        "end_date": {"type": "string", "description": "End date for reports (YYYY-MM-DD format)"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
EOF

# Create get_investor_documents.py
cat > get_investor_documents.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorDocuments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, 
               document_format: Optional[str] = None, confidentiality_level: Optional[str] = None,
               status: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        documents = data.get("documents", {})
        reports = data.get("reports", {})
        users = data.get("users", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Get documents related to this investor through reports
        investor_documents = []
        
        # First, find all reports for this investor
        investor_report_ids = []
        for report in reports.values():
            if report.get("investor_id") == investor_id:
                investor_report_ids.append(report.get("report_id"))
        
        # Then find documents associated with these reports
        for document in documents.values():
            report_id = document.get("report_id")
            
            # Include document if it's associated with investor's reports or if no report_id (general docs)
            if report_id in investor_report_ids or not report_id:
                # Filter by format if specified
                if document_format and document.get("format") != document_format:
                    continue
                
                # Filter by confidentiality level if specified
                if confidentiality_level and document.get("confidentiality_level") != confidentiality_level:
                    continue
                
                # Filter by status if specified
                if status and document.get("status") != status:
                    continue
                
                # Enrich with uploader details
                uploaded_by = document.get("uploaded_by")
                uploader = users.get(str(uploaded_by), {})
                
                enriched_document = {
                    **document,
                    "uploader_name": f"{uploader.get('first_name', '')} {uploader.get('last_name', '')}".strip(),
                    "uploader_email": uploader.get("email")
                }
                investor_documents.append(enriched_document)
        
        return json.dumps(investor_documents)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_documents",
                "description": "Retrieve all documents related to the investor (agreements, reports, correspondence)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "document_format": {"type": "string", "description": "Filter by document format (pdf, xlsx, docx, csv, other)"},
                        "confidentiality_level": {"type": "string", "description": "Filter by confidentiality level (public, internal, confidential, restricted)"},
                        "status": {"type": "string", "description": "Filter by document status (available, archived, deleted)"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
EOF

# Create get_investor_transactions_history.py
cat > get_investor_transactions_history.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorTransactionsHistory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, 
               start_date: Optional[str] = None, end_date: Optional[str] = None,
               transaction_type: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        subscriptions = data.get("subscriptions", {})
        redemptions = data.get("redemptions", {})
        payments = data.get("payments", {})
        commitments = data.get("commitments", {})
        funds = data.get("funds", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        transactions = []
        
        # Get subscriptions
        if not transaction_type or transaction_type == "subscription":
            for subscription in subscriptions.values():
                if subscription.get("investor_id") == investor_id:
                    request_date = subscription.get("request_date")
                    
                    # Date filtering
                    if start_date and request_date < start_date:
                        continue
                    if end_date and request_date > end_date:
                        continue
                    
                    # Enrich with fund details
                    fund_id = subscription.get("fund_id")
                    fund_details = funds.get(str(fund_id), {})
                    
                    transactions.append({
                        "transaction_id": subscription.get("subscription_id"),
                        "transaction_type": "subscription",
                        "fund_id": fund_id,
                        "fund_name": fund_details.get("name"),
                        "amount": subscription.get("amount"),
                        "status": subscription.get("status"),
                        "date": request_date,
                        "approval_date": subscription.get("approval_date")
                    })
        
        # Get redemptions
        if not transaction_type or transaction_type == "redemption":
            for redemption in redemptions.values():
                subscription_id = redemption.get("subscription_id")
                subscription = subscriptions.get(str(subscription_id), {})
                
                if subscription.get("investor_id") == investor_id:
                    request_date = redemption.get("request_date")
                    
                    # Date filtering
                    if start_date and request_date < start_date:
                        continue
                    if end_date and request_date > end_date:
                        continue
                    
                    # Enrich with fund details
                    fund_id = subscription.get("fund_id")
                    fund_details = funds.get(str(fund_id), {})
                    
                    transactions.append({
                        "transaction_id": redemption.get("redemption_id"),
                        "transaction_type": "redemption",
                        "fund_id": fund_id,
                        "fund_name": fund_details.get("name"),
                        "amount": redemption.get("redemption_amount"),
                        "status": redemption.get("status"),
                        "date": request_date,
                        "processed_date": redemption.get("processed_date"),
                        "redemption_fee": redemption.get("redemption_fee")
                    })
        
        # Get commitments
        if not transaction_type or transaction_type == "commitment":
            for commitment in commitments.values():
                if commitment.get("investor_id") == investor_id:
                    commitment_date = commitment.get("commitment_date")
                    
                    # Date filtering
                    if start_date and commitment_date < start_date:
                        continue
                    if end_date and commitment_date > end_date:
                        continue
                    
                    # Enrich with fund details
                    fund_id = commitment.get("fund_id")
                    fund_details = funds.get(str(fund_id), {})
                    
                    transactions.append({
                        "transaction_id": commitment.get("commitment_id"),
                        "transaction_type": "commitment",
                        "fund_id": fund_id,
                        "fund_name": fund_details.get("name"),
                        "amount": commitment.get("commitment_amount"),
                        "status": commitment.get("status"),
                        "date": commitment_date
                    })
        
        # Sort by date (most recent first)
        transactions.sort(key=lambda x: x.get("date", ""), reverse=True)
        
        return json.dumps(transactions)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_transactions_history",
                "description": "Comprehensive transaction history including all subscriptions, redemptions, switches, and payments",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "start_date": {"type": "string", "description": "Start date for transaction history (YYYY-MM-DD format)"},
                        "end_date": {"type": "string", "description": "End date for transaction history (YYYY-MM-DD format)"},
                        "transaction_type": {"type": "string", "description": "Filter by transaction type (subscription, redemption, commitment)"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
EOF

echo "All fund management tools have been created successfully!"
echo "Files generated:"
echo "- get_investor_profile.py"
echo "- get_investor_portfolio.py"
echo "- get_investor_portfolio_holdings.py"
echo "- get_available_funds.py"
echo "- get_fund_details.py"
echo "- get_fund_nav_history.py"
echo "- get_investor_subscriptions.py"
echo "- get_investor_commitments.py"
echo "- get_investor_redemptions.py"
echo "- get_investor_statements.py"
echo "- get_investor_documents.py"
echo "- get_investor_transactions_history.py"