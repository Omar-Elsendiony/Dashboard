#!/bin/bash

# Create directory for tools if it doesn't exist
mkdir -p database_tools

# 1. onboard_new_investor.py
cat > database_tools/onboard_new_investor.py << 'EOF'
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
EOF

# 2. get_investors.py
cat > database_tools/get_investors.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetInvestors(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        investors = data.get("investors", {})
        results = list(investors.values())
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investors",
                "description": "Get all investors for client relationship management",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
EOF

# 3. update_investor_details.py
cat > database_tools/update_investor_details.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateInvestorDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, name: Optional[str] = None,
               contact_email: Optional[str] = None, accreditation_status: Optional[str] = None,
               registration_number: Optional[int] = None, date_of_incorporation: Optional[str] = None,
               country: Optional[str] = None, address: Optional[str] = None,
               tax_id: Optional[str] = None, source_of_funds: Optional[str] = None,
               status: Optional[str] = None) -> str:
        
        investors = data.get("investors", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        investor = investors[str(investor_id)]
        
        # Validate accreditation status if provided
        if accreditation_status:
            valid_accreditation = ["accredited", "non_accredited"]
            if accreditation_status not in valid_accreditation:
                raise ValueError(f"Invalid accreditation status. Must be one of {valid_accreditation}")
            investor["accreditation_status"] = accreditation_status
        
        # Validate status if provided
        if status:
            valid_statuses = ["onboarded", "offboarded"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            investor["status"] = status
        
        # Validate source of funds if provided
        if source_of_funds:
            valid_sources = ["retained_earnings", "shareholder_capital", "asset_sale", "loan_facility", 
                            "external_investment", "government_grant", "merger_or_acquisition_proceeds",
                            "royalty_or_licensing_income", "dividend_income", "other"]
            if source_of_funds not in valid_sources:
                raise ValueError(f"Invalid source of funds. Must be one of {valid_sources}")
            investor["source_of_funds"] = source_of_funds
        
        # Update fields if provided
        if name is not None:
            investor["name"] = name
        if contact_email is not None:
            investor["contact_email"] = contact_email
        if registration_number is not None:
            investor["registration_number"] = registration_number
        if date_of_incorporation is not None:
            investor["date_of_incorporation"] = date_of_incorporation
        if country is not None:
            investor["country"] = country
        if address is not None:
            investor["address"] = address
        if tax_id is not None:
            investor["tax_id"] = tax_id
        
        return json.dumps(investor)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_investor_details",
                "description": "Update investor details for regulatory updates and address changes",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "name": {"type": "string", "description": "Investor name (optional)"},
                        "contact_email": {"type": "string", "description": "Contact email address (optional)"},
                        "accreditation_status": {"type": "string", "description": "Accreditation status (optional)"},
                        "registration_number": {"type": "integer", "description": "Registration number (optional)"},
                        "date_of_incorporation": {"type": "string", "description": "Date of incorporation (optional)"},
                        "country": {"type": "string", "description": "Country (optional)"},
                        "address": {"type": "string", "description": "Address (optional)"},
                        "tax_id": {"type": "string", "description": "Tax ID (optional)"},
                        "source_of_funds": {"type": "string", "description": "Source of funds (optional)"},
                        "status": {"type": "string", "description": "Status (optional)"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
EOF

# 4. get_filtered_investors.py
cat > database_tools/get_filtered_investors.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFilteredInvestors(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], accreditation_status: Optional[str] = None,
               status: Optional[str] = None, country: Optional[str] = None,
               source_of_funds: Optional[str] = None) -> str:
        
        investors = data.get("investors", {})
        results = []
        
        for investor in investors.values():
            if accreditation_status and investor.get("accreditation_status") != accreditation_status:
                continue
            if status and investor.get("status") != status:
                continue
            if country and investor.get("country") != country:
                continue
            if source_of_funds and investor.get("source_of_funds") != source_of_funds:
                continue
            results.append(investor)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_filtered_investors",
                "description": "Get filtered investors for CRM and marketing segmentation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "accreditation_status": {"type": "string", "description": "Filter by accreditation status"},
                        "status": {"type": "string", "description": "Filter by status"},
                        "country": {"type": "string", "description": "Filter by country"},
                        "source_of_funds": {"type": "string", "description": "Filter by source of funds"}
                    },
                    "required": []
                }
            }
        }
EOF

# 5. create_new_fund.py
cat > database_tools/create_new_fund.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateNewFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, fund_type: str, manager_id: str,
               size: Optional[float] = None, status: str = "open") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        users = data.get("users", {})
        
        # Validate manager exists
        if str(manager_id) not in users:
            raise ValueError(f"Manager {manager_id} not found")
        
        # Validate fund type
        valid_fund_types = ["mutual_funds", "exchange_traded_funds", "pension_funds", 
                           "private_equity_funds", "hedge_funds", "sovereign_wealth_funds",
                           "money_market_funds", "real_estate_investment_trusts", 
                           "infrastructure_funds", "multi_asset_funds"]
        if fund_type not in valid_fund_types:
            raise ValueError(f"Invalid fund type. Must be one of {valid_fund_types}")
        
        # Validate status
        valid_statuses = ["open", "closed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        fund_id = generate_id(funds)
        timestamp = "2025-10-01T00:00:00"
        
        new_fund = {
            "fund_id": str(fund_id),
            "name": name,
            "fund_type": fund_type,
            "manager_id": str(manager_id),
            "size": size,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        funds[str(fund_id)] = new_fund
        return json.dumps(new_fund)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_new_fund",
                "description": "Create a new fund for product launches",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Fund name"},
                        "fund_type": {"type": "string", "description": "Fund type"},
                        "manager_id": {"type": "string", "description": "Manager user ID"},
                        "size": {"type": "number", "description": "Fund size (optional)"},
                        "status": {"type": "string", "description": "Fund status (open, closed), defaults to open"}
                    },
                    "required": ["name", "fund_type", "manager_id"]
                }
            }
        }
EOF

# 6. get_funds.py
cat > database_tools/get_funds.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetFunds(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        funds = data.get("funds", {})
        results = list(funds.values())
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_funds",
                "description": "Get fund catalog for investors and internal use",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
EOF

# 7. update_fund_details.py
cat > database_tools/update_fund_details.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateFundDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, name: Optional[str] = None,
               fund_type: Optional[str] = None, manager_id: Optional[str] = None,
               size: Optional[float] = None, status: Optional[str] = None) -> str:
        
        funds = data.get("funds", {})
        users = data.get("users", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        fund = funds[str(fund_id)]
        
        # Validate manager if provided
        if manager_id and str(manager_id) not in users:
            raise ValueError(f"Manager {manager_id} not found")
        
        # Validate fund type if provided
        if fund_type:
            valid_fund_types = ["mutual_funds", "exchange_traded_funds", "pension_funds", 
                               "private_equity_funds", "hedge_funds", "sovereign_wealth_funds",
                               "money_market_funds", "real_estate_investment_trusts", 
                               "infrastructure_funds", "multi_asset_funds"]
            if fund_type not in valid_fund_types:
                raise ValueError(f"Invalid fund type. Must be one of {valid_fund_types}")
            fund["fund_type"] = fund_type
        
        # Validate status if provided
        if status:
            valid_statuses = ["open", "closed"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            fund["status"] = status
        
        # Update fields if provided
        if name is not None:
            fund["name"] = name
        if manager_id is not None:
            fund["manager_id"] = str(manager_id)
        if size is not None:
            fund["size"] = size
        
        fund["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(fund)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_fund_details",
                "description": "Update fund details for strategy changes and fee updates",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "name": {"type": "string", "description": "Fund name (optional)"},
                        "fund_type": {"type": "string", "description": "Fund type (optional)"},
                        "manager_id": {"type": "string", "description": "Manager user ID (optional)"},
                        "size": {"type": "number", "description": "Fund size (optional)"},
                        "status": {"type": "string", "description": "Fund status (optional)"}
                    },
                    "required": ["fund_id"]
                }
            }
        }
EOF

# 8. list_funds_with_filter.py
cat > database_tools/list_funds_with_filter.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ListFundsWithFilter(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_type: Optional[str] = None,
               manager_id: Optional[str] = None, status: Optional[str] = None,
               min_size: Optional[float] = None, max_size: Optional[float] = None) -> str:
        
        funds = data.get("funds", {})
        results = []
        
        for fund in funds.values():
            if fund_type and fund.get("fund_type") != fund_type:
                continue
            if manager_id and fund.get("manager_id") != str(manager_id):
                continue
            if status and fund.get("status") != status:
                continue
            if min_size is not None and (fund.get("size") is None or fund.get("size") < min_size):
                continue
            if max_size is not None and (fund.get("size") is None or fund.get("size") > max_size):
                continue
            results.append(fund)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_funds_with_filter",
                "description": "List funds with filters for investment screening and selection",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_type": {"type": "string", "description": "Filter by fund type"},
                        "manager_id": {"type": "string", "description": "Filter by manager ID"},
                        "status": {"type": "string", "description": "Filter by status"},
                        "min_size": {"type": "number", "description": "Minimum fund size"},
                        "max_size": {"type": "number", "description": "Maximum fund size"}
                    },
                    "required": []
                }
            }
        }
EOF

# 9. get_investor_portfolio.py
cat > database_tools/get_investor_portfolio.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetInvestorPortfolio(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str) -> str:
        portfolios = data.get("portfolios", {})
        results = []
        
        for portfolio in portfolios.values():
            if portfolio.get("investor_id") == str(investor_id):
                results.append(portfolio)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_portfolio",
                "description": "Get investor portfolio for client servicing and performance tracking",
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

# 10. get_portfolio_holdings.py
cat > database_tools/get_portfolio_holdings.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPortfolioHoldings(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], portfolio_id: str) -> str:
        portfolio_holdings = data.get("portfolio_holdings", {})
        results = []
        
        for holding in portfolio_holdings.values():
            if holding.get("portfolio_id") == str(portfolio_id):
                results.append(holding)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_portfolio_holdings",
                "description": "Get portfolio holdings for holdings analysis and risk management",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string", "description": "ID of the portfolio"}
                    },
                    "required": ["portfolio_id"]
                }
            }
        }
EOF

# Continue with remaining tools...
# 11. add_new_holding.py
cat > database_tools/add_new_holding.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddNewHolding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], portfolio_id: str, fund_id: str,
               quantity: float, cost_basis: float) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        portfolio_holdings = data.get("portfolio_holdings", {})
        portfolios = data.get("portfolios", {})
        funds = data.get("funds", {})
        
        # Validate portfolio exists
        if str(portfolio_id) not in portfolios:
            raise ValueError(f"Portfolio {portfolio_id} not found")
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        holding_id = generate_id(portfolio_holdings)
        timestamp = "2025-10-01T00:00:00"
        
        new_holding = {
            "holding_id": str(holding_id),
            "portfolio_id": str(portfolio_id),
            "fund_id": str(fund_id),
            "quantity": quantity,
            "cost_basis": cost_basis,
            "created_at": timestamp
        }
        
        portfolio_holdings[str(holding_id)] = new_holding
        return json.dumps(new_holding)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_new_holding",
                "description": "Add new holding for investment execution",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string", "description": "ID of the portfolio"},
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "quantity": {"type": "number", "description": "Quantity of holding"},
                        "cost_basis": {"type": "number", "description": "Cost basis of holding"}
                    },
                    "required": ["portfolio_id", "fund_id", "quantity", "cost_basis"]
                }
            }
        }
EOF

# 12. update_investor_portfolio_holding.py
cat > database_tools/update_investor_portfolio_holding.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateInvestorPortfolioHolding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], holding_id: str, quantity: Optional[float] = None,
               cost_basis: Optional[float] = None) -> str:
        
        portfolio_holdings = data.get("portfolio_holdings", {})
        
        # Validate holding exists
        if str(holding_id) not in portfolio_holdings:
            raise ValueError(f"Holding {holding_id} not found")
        
        holding = portfolio_holdings[str(holding_id)]
        
        # Update fields if provided
        if quantity is not None:
            holding["quantity"] = quantity
        if cost_basis is not None:
            holding["cost_basis"] = cost_basis
        
        return json.dumps(holding)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_investor_portfolio_holding",
                "description": "Update investor portfolio holding for position adjustments",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "holding_id": {"type": "string", "description": "ID of the holding"},
                        "quantity": {"type": "number", "description": "New quantity (optional)"},
                        "cost_basis": {"type": "number", "description": "New cost basis (optional)"}
                    },
                    "required": ["holding_id"]
                }
            }
        }
EOF

# 13. subscribe_investor_to_fund.py
cat > database_tools/subscribe_investor_to_fund.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SubscribeInvestorToFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, investor_id: str, amount: float,
               request_assigned_to: str, request_date: str, payment_id: Optional[str] = None,
               status: str = "pending") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        subscriptions = data.get("subscriptions", {})
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        users = data.get("users", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate assigned user exists
        if str(request_assigned_to) not in users:
            raise ValueError(f"Assigned user {request_assigned_to} not found")
        
        # Validate status
        valid_statuses = ["pending", "approved", "cancelled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        subscription_id = generate_id(subscriptions)
        timestamp = "2025-10-01T00:00:00"
        
        new_subscription = {
            "subscription_id": str(subscription_id),
            "fund_id": str(fund_id),
            "investor_id": str(investor_id),
            "payment_id": str(payment_id) if payment_id else None,
            "amount": amount,
            "status": status,
            "request_assigned_to": str(request_assigned_to),
            "request_date": request_date,
            "approval_date": None,
            "updated_at": timestamp
        }
        
        subscriptions[str(subscription_id)] = new_subscription
        return json.dumps(new_subscription)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "subscribe_investor_to_fund",
                "description": "Subscribe investor to fund for core revenue generation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "amount": {"type": "number", "description": "Subscription amount"},
                        "request_assigned_to": {"type": "string", "description": "ID of assigned user"},
                        "request_date": {"type": "string", "description": "Request date in YYYY-MM-DD format"},
                        "payment_id": {"type": "string", "description": "Payment ID (optional)"},
                        "status": {"type": "string", "description": "Status (pending, approved, cancelled), defaults to pending"}
                    },
                    "required": ["fund_id", "investor_id", "amount", "request_assigned_to", "request_date"]
                }
            }
        }
EOF