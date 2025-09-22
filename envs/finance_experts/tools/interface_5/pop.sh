#!/bin/bash

# Create directory for discovery functions
mkdir -p discovery_functions
cd discovery_functions

# Function 1: DiscoverUserEntities
cat > discover_user_entities.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverUserEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover user entities.
        
        Supported entities:
        - users: User records by user_id, first_name, last_name, email, role, timezone, status
        """
        if entity_type not in ["users"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'users'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("users", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "user_id": entity_id})
            else:
                results.append({**entity_data, "user_id": entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_user_entities",
                "description": "Discover user entities. Entity types: 'users' (user records; filterable by user_id (string), first_name (string), last_name (string), email (string), role (enum: 'system_administrator', 'fund_manager', 'compliance_officer', 'finance_officer', 'trader'), timezone (string), status (enum: 'active', 'inactive', 'suspended'), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'users'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For users, filters are: user_id (string), first_name (string), last_name (string), email (string), role (enum: 'system_administrator', 'fund_manager', 'compliance_officer', 'finance_officer', 'trader'), timezone (string), status (enum: 'active', 'inactive', 'suspended'), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

# Function 2: DiscoverInvestorEntities
cat > discover_investor_entities.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverInvestorEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover investor entities.
        
        Supported entities:
        - investors: Investor records by investor_id, name, registration_number, date_of_incorporation, country, address, tax_id, source_of_funds, status, contact_email, accreditation_status
        """
        if entity_type not in ["investors"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'investors'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("investors", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "investor_id": entity_id})
            else:
                results.append({**entity_data, "investor_id": entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_investor_entities",
                "description": "Discover investor entities. Entity types: 'investors' (investor records; filterable by investor_id (string), name (string), registration_number (string), date_of_incorporation (date), country (string), address (string), tax_id (string), source_of_funds (enum: 'retained_earnings', 'shareholder_capital', 'asset_sale', 'loan_facility', 'external_investment', 'government_grant', 'merger_or_acquisition_proceeds', 'royalty_or_licensing_income', 'dividend_income', 'other'), status (enum: 'onboarded', 'offboarded'), contact_email (string), accreditation_status (enum: 'accredited', 'non_accredited'), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'investors'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For investors, filters are: investor_id (string), name (string), registration_number (string), date_of_incorporation (date), country (string), address (string), tax_id (string), source_of_funds (enum: 'retained_earnings', 'shareholder_capital', 'asset_sale', 'loan_facility', 'external_investment', 'government_grant', 'merger_or_acquisition_proceeds', 'royalty_or_licensing_income', 'dividend_income', 'other'), status (enum: 'onboarded', 'offboarded'), contact_email (string), accreditation_status (enum: 'accredited', 'non_accredited'), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

# Function 3: DiscoverFundEntities
cat > discover_fund_entities.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverFundEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover fund entities.
        
        Supported entities:
        - funds: Fund records by fund_id, name, fund_type, manager_id, size, status
        """
        if entity_type not in ["funds"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'funds'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("funds", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "fund_id": entity_id})
            else:
                results.append({**entity_data, "fund_id": entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_fund_entities",
                "description": "Discover fund entities. Entity types: 'funds' (fund records; filterable by fund_id (string), name (string), fund_type (enum: 'mutual_funds', 'exchange_traded_funds', 'pension_funds', 'private_equity_funds', 'hedge_funds', 'sovereign_wealth_funds', 'money_market_funds', 'real_estate_investment_trusts', 'infrastructure_funds', 'multi_asset_funds'), manager_id (string), size (decimal), status (enum: 'open', 'closed'), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'funds'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For funds, filters are: fund_id (string), name (string), fund_type (enum: 'mutual_funds', 'exchange_traded_funds', 'pension_funds', 'private_equity_funds', 'hedge_funds', 'sovereign_wealth_funds', 'money_market_funds', 'real_estate_investment_trusts', 'infrastructure_funds', 'multi_asset_funds'), manager_id (string), size (decimal), status (enum: 'open', 'closed'), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

# Function 4: DiscoverInstrumentEntities
cat > discover_instrument_entities.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverInstrumentEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover instrument entities.
        
        Supported entities:
        - instruments: Instrument records by instrument_id, ticker, name, status, instrument_type
        """
        if entity_type not in ["instruments"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'instruments'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("instruments", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "instrument_id": entity_id})
            else:
                results.append({**entity_data, "instrument_id": entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_instrument_entities",
                "description": "Discover instrument entities. Entity types: 'instruments' (instrument records; filterable by instrument_id (string), ticker (string), name (string), status (enum: 'active', 'inactive'), instrument_type (enum: 'equities_common_shares', 'equities_preferred_shares', 'equities_indexed', 'equities_domestic', 'equities_international', 'bonds_corporate', 'bonds_municipal', 'bonds_government', 'bonds_inflation_linked', 'bonds_high_yield', 'bonds_distressed', 'money_market_treasury_bills', 'money_market_commercial_paper', 'certificates_of_deposit', 'repurchase_agreements', 'short_term_municipal_notes', 'bankers_acceptances', 'commodities_gold_oil_futures', 'commodities_spot', 'commodities_futures', 'derivatives_options', 'derivatives_futures', 'derivatives_swaps', 'real_estate_direct_property', 'real_estate_reits', 'mortgage_backed_securities', 'property_development_loans', 'private_equity', 'equity_stakes_private_companies', 'equity_stakes_infrastructure_assets', 'mezzanine_financing', 'convertible_preferred_stock', 'leveraged_buyout_debt', 'distressed_debt', 'project_finance_debt', 'infrastructure_bonds', 'ppp_investments', 'infrastructure_debt_equity', 'infrastructure_projects', 'alternative_assets_hedge_funds', 'alternative_assets_commodities')).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'instruments'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For instruments, filters are: instrument_id (string), ticker (string), name (string), status (enum: 'active', 'inactive'), instrument_type (enum: 'equities_common_shares', 'equities_preferred_shares', 'equities_indexed', 'equities_domestic', 'equities_international', 'bonds_corporate', 'bonds_municipal', 'bonds_government', 'bonds_inflation_linked', 'bonds_high_yield', 'bonds_distressed', 'money_market_treasury_bills', 'money_market_commercial_paper', 'certificates_of_deposit', 'repurchase_agreements', 'short_term_municipal_notes', 'bankers_acceptances', 'commodities_gold_oil_futures', 'commodities_spot', 'commodities_futures', 'derivatives_options', 'derivatives_futures', 'derivatives_swaps', 'real_estate_direct_property', 'real_estate_reits', 'mortgage_backed_securities', 'property_development_loans', 'private_equity', 'equity_stakes_private_companies', 'equity_stakes_infrastructure_assets', 'mezzanine_financing', 'convertible_preferred_stock', 'leveraged_buyout_debt', 'distressed_debt', 'project_finance_debt', 'infrastructure_bonds', 'ppp_investments', 'infrastructure_debt_equity', 'infrastructure_projects', 'alternative_assets_hedge_funds', 'alternative_assets_commodities')"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

# Function 5: DiscoverPortfolioEntities
cat > discover_portfolio_entities.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverPortfolioEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover portfolio entities: portfolios and portfolio holdings.
        
        Supported entities:
        - portfolios: Portfolio records by portfolio_id, investor_id, status
        - portfolio_holdings: Portfolio holding records by holding_id, portfolio_id, fund_id, quantity, cost_basis
        """
        if entity_type not in ["portfolios", "portfolio_holdings"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'portfolios' or 'portfolio_holdings'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        id_field = {
            "portfolios": "portfolio_id",
            "portfolio_holdings": "holding_id"
        }[entity_type]
        
        entities = data.get(entity_type, {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_portfolio_entities",
                "description": "Discover portfolio entities including portfolios and portfolio holdings. Entity types: 'portfolios' (portfolio records; filterable by portfolio_id (string), investor_id (string), status (enum: 'active', 'inactive', 'archived'), created_at (timestamp), updated_at (timestamp)), 'portfolio_holdings' (portfolio holding records; filterable by holding_id (string), portfolio_id (string), fund_id (string), quantity (decimal), cost_basis (decimal), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'portfolios' or 'portfolio_holdings'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For portfolios, filters are: portfolio_id (string), investor_id (string), status (enum: 'active', 'inactive', 'archived'), created_at (timestamp), updated_at (timestamp). For portfolio_holdings, filters are: holding_id (string), portfolio_id (string), fund_id (string), quantity (decimal), cost_basis (decimal), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

# Function 6: DiscoverInvestmentFlowEntities
cat > discover_investment_flow_entities.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverInvestmentFlowEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover investment flow entities: subscriptions, commitments, and redemptions.
        
        Supported entities:
        - subscriptions: Subscription records by subscription_id, fund_id, investor_id, amount, status, request_assigned_to, request_date, approval_date
        - commitments: Commitment records by commitment_id, fund_id, investor_id, commitment_amount, commitment_date, status
        - redemptions: Redemption records by redemption_id, subscription_id, request_date, redemption_amount, status, processed_date, redemption_fee
        """
        if entity_type not in ["subscriptions", "commitments", "redemptions"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'subscriptions', 'commitments', or 'redemptions'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        id_field = {
            "subscriptions": "subscription_id",
            "commitments": "commitment_id",
            "redemptions": "redemption_id"
        }[entity_type]
        
        entities = data.get(entity_type, {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_investment_flow_entities",
                "description": "Discover investment flow entities including subscriptions, commitments, and redemptions. Entity types: 'subscriptions' (subscription records; filterable by subscription_id (string), fund_id (string), investor_id (string), amount (decimal), status (enum: 'pending', 'approved', 'cancelled'), request_assigned_to (string), request_date (date), approval_date (date), updated_at (timestamp)), 'commitments' (commitment records; filterable by commitment_id (string), fund_id (string), investor_id (string), commitment_amount (decimal), commitment_date (date), status (enum: 'pending', 'fulfilled'), updated_at (timestamp)), 'redemptions' (redemption records; filterable by redemption_id (string), subscription_id (string), request_date (date), redemption_amount (decimal), status (enum: 'pending', 'approved', 'processed', 'cancelled'), processed_date (date), redemption_fee (decimal), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'subscriptions', 'commitments', or 'redemptions'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For subscriptions, filters are: subscription_id (string), fund_id (string), investor_id (string), amount (decimal), status (enum: 'pending', 'approved', 'cancelled'), request_assigned_to (string), request_date (date), approval_date (date), updated_at (timestamp). For commitments, filters are: commitment_id (string), fund_id (string), investor_id (string), commitment_amount (decimal), commitment_date (date), status (enum: 'pending', 'fulfilled'), updated_at (timestamp). For redemptions, filters are: redemption_id (string), subscription_id (string), request_date (date), redemption_amount (decimal), status (enum: 'pending', 'approved', 'processed', 'cancelled'), processed_date (date), redemption_fee (decimal), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

# Function 7: DiscoverTradingEntities
cat > discover_trading_entities.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverTradingEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover trading entities.
        
        Supported entities:
        - trades: Trade records by trade_id, fund_id, instrument_id, trade_date, quantity, price, side, status
        """
        if entity_type not in ["trades"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'trades'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("trades", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "trade_id": entity_id})
            else:
                results.append({**entity_data, "trade_id": entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_trading_entities",
                "description": "Discover trading entities. Entity types: 'trades' (trade records; filterable by trade_id (string), fund_id (string), instrument_id (string), trade_date (timestamp), quantity (decimal), price (decimal), side (enum: 'buy', 'sell'), status (enum: 'approved', 'executed', 'pending', 'failed'), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'trades'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For trades, filters are: trade_id (string), fund_id (string), instrument_id (string), trade_date (timestamp), quantity (decimal), price (decimal), side (enum: 'buy', 'sell'), status (enum: 'approved', 'executed', 'pending', 'failed'), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

# Function 8: DiscoverValuationEntities
cat > discover_valuation_entities.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverValuationEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover valuation entities: NAV records and instrument prices.
        
        Supported entities:
        - nav_records: Net Asset Value records by nav_id, fund_id, nav_date, nav_value
        - instrument_prices: Price data by price_id, instrument_id, price_date, open_price, high_price, low_price, close_price
        """
        if entity_type not in ["nav_records", "instrument_prices"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'nav_records' or 'instrument_prices'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        id_field = {
            "nav_records": "nav_id",
            "instrument_prices": "price_id"
        }[entity_type]
        
        entities = data.get(entity_type, {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_valuation_entities",
                "description": "Discover valuation entities including NAV records and instrument prices. Entity types: 'nav_records' (Net Asset Value records; filterable by nav_id (string), fund_id (string), nav_date (date), nav_value (decimal), updated_at (timestamp)), 'instrument_prices' (price data; filterable by price_id (string), instrument_id (string), price_date (date), open_price (decimal), high_price (decimal), low_price (decimal), close_price (decimal)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'nav_records' or 'instrument_prices'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For nav_records, filters are: nav_id (string), fund_id (string), nav_date (date), nav_value (decimal), updated_at (timestamp). For instrument_prices, filters are: price_id (string), instrument_id (string), price_date (date), open_price (decimal), high_price (decimal), low_price (decimal), close_price (decimal)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

# Function 9: DiscoverBillingEntities
cat > discover_billing_entities.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverBillingEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover billing entities: invoices and payments.
        
        Supported entities:
        - invoices: Invoice records by invoice_id, commitment_id, invoice_date, due_date, amount, status
        - payments: Payment records by payment_id, invoice_id, subscription_id, payment_date, amount, payment_method, status
        """
        if entity_type not in ["invoices", "payments"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'invoices' or 'payments'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        id_field = {
            "invoices": "invoice_id",
            "payments": "payment_id"
        }[entity_type]
        
        entities = data.get(entity_type, {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_billing_entities",
                "description": "Discover billing entities including invoices and payments. Entity types: 'invoices' (invoice records; filterable by invoice_id (string), commitment_id (string), invoice_date (date), due_date (date), amount (decimal), status (enum: 'issued', 'paid'), updated_at (timestamp)), 'payments' (payment records; filterable by payment_id (string), invoice_id (string), subscription_id (string), payment_date (timestamp), amount (decimal), payment_method (enum: 'wire', 'cheque', 'credit_card', 'bank_transfer'), status (enum: 'draft', 'completed', 'failed'), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'invoices' or 'payments'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For invoices, filters are: invoice_id (string), commitment_id (string), invoice_date (date), due_date (date), amount (decimal), status (enum: 'issued', 'paid'), updated_at (timestamp). For payments, filters are: payment_id (string), invoice_id (string), subscription_id (string), payment_date (timestamp), amount (decimal), payment_method (enum: 'wire', 'cheque', 'credit_card', 'bank_transfer'), status (enum: 'draft', 'completed', 'failed'), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

# Function 10: DiscoverReportingEntities
cat > discover_reporting_entities.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverReportingEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover reporting entities: reports and documents.
        
        Supported entities:
        - reports: Report records by report_id, fund_id, investor_id, report_date, report_type, generated_by, status, export_period_end
        - documents: Document records by document_id, name, format, uploaded_by, upload_date, report_id, size_bytes, confidentiality_level, status
        """
        if entity_type not in ["reports", "documents"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'reports' or 'documents'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        id_field = {
            "reports": "report_id",
            "documents": "document_id"
        }[entity_type]
        
        entities = data.get(entity_type, {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_reporting_entities",
                "description": "Discover reporting entities including reports and documents. Entity types: 'reports' (report records; filterable by report_id (string), fund_id (string), investor_id (string), report_date (date), report_type (enum: 'performance', 'holding', 'financial'), generated_by (string), status (enum: 'pending', 'completed', 'failed'), created_at (timestamp), export_period_end (date)), 'documents' (document records; filterable by document_id (string), name (string), format (enum: 'pdf', 'xlsx', 'docx', 'csv', 'other'), uploaded_by (string), upload_date (timestamp), report_id (string), size_bytes (bigint), confidentiality_level (enum: 'public', 'internal', 'confidential', 'restricted'), status (enum: 'available', 'archived', 'deleted')).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'reports' or 'documents'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For reports, filters are: report_id (string), fund_id (string), investor_id (string), report_date (date), report_type (enum: 'performance', 'holding', 'financial'), generated_by (string), status (enum: 'pending', 'completed', 'failed'), created_at (timestamp), export_period_end (date). For documents, filters are: document_id (string), name (string), format (enum: 'pdf', 'xlsx', 'docx', 'csv', 'other'), uploaded_by (string), upload_date (timestamp), report_id (string), size_bytes (bigint), confidentiality_level (enum: 'public', 'internal', 'confidential', 'restricted'), status (enum: 'available', 'archived', 'deleted')"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

# Function 11: DiscoverSystemEntities
cat > discover_system_entities.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverSystemEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover system entities: notifications and audit trails.
        
        Supported entities:
        - notifications: Notification records by notification_id, email, type, class, reference_id, status, sent_at
        - audit_trails: Audit trail records by audit_trail_id, reference_id, reference_type, action, user_id, field_name, old_value, new_value
        """
        if entity_type not in ["notifications", "audit_trails"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'notifications' or 'audit_trails'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        id_field = {
            "notifications": "notification_id",
            "audit_trails": "audit_trail_id"
        }[entity_type]
        
        entities = data.get(entity_type, {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_system_entities",
                "description": "Discover system entities including notifications and audit trails. Entity types: 'notifications' (notification records; filterable by notification_id (string), email (string), type (enum: 'alert', 'report', 'reminder', 'subscription_update'), class (enum: 'funds', 'investors', 'portfolios', 'trades', 'invoices', 'reports', 'documents', 'subscriptions', 'commitments'), reference_id (string), status (enum: 'pending', 'sent', 'failed'), sent_at (timestamp), created_at (timestamp)), 'audit_trails' (audit trail records; filterable by audit_trail_id (string), reference_id (string), reference_type (enum: 'user', 'fund', 'investor', 'subscription', 'commitment', 'redemption', 'trade', 'portfolio', 'holding', 'instrument', 'invoice', 'payment', 'document', 'report', 'nav', 'notification'), action (enum: 'create', 'update', 'delete', 'approve', 'cancel', 'process'), user_id (string), field_name (string), old_value (text), new_value (text), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'notifications' or 'audit_trails'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For notifications, filters are: notification_id (string), email (string), type (enum: 'alert', 'report', 'reminder', 'subscription_update'), class (enum: 'funds', 'investors', 'portfolios', 'trades', 'invoices', 'reports', 'documents', 'subscriptions', 'commitments'), reference_id (string), status (enum: 'pending', 'sent', 'failed'), sent_at (timestamp), created_at (timestamp). For audit_trails, filters are: audit_trail_id (string), reference_id (string), reference_type (enum: 'user', 'fund', 'investor', 'subscription', 'commitment', 'redemption', 'trade', 'portfolio', 'holding', 'instrument', 'invoice', 'payment', 'document', 'report', 'nav', 'notification'), action (enum: 'create', 'update', 'delete', 'approve', 'cancel', 'process'), user_id (string), field_name (string), old_value (text), new_value (text), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

# Create __init__.py file to make it a package
cat > __init__.py << 'EOF'
"""
Discovery Functions Package

This package contains 11 discovery functions for B2B finance entities:

1. DiscoverUserEntities - users
2. DiscoverInvestorEntities - investors  
3. DiscoverFundEntities - funds
4. DiscoverInstrumentEntities - instruments
5. DiscoverPortfolioEntities - portfolios, portfolio_holdings
6. DiscoverInvestmentFlowEntities - subscriptions, commitments, redemptions
7. DiscoverTradingEntities - trades
8. DiscoverValuationEntities - nav_records, instrument_prices
9. DiscoverBillingEntities - invoices, payments
10. DiscoverReportingEntities - reports, documents
11. DiscoverSystemEntities - notifications, audit_trails

All functions use string IDs and support filtering with exact matches.
"""

from .discover_user_entities import DiscoverUserEntities
from .discover_investor_entities import DiscoverInvestorEntities
from .discover_fund_entities import DiscoverFundEntities
from .discover_instrument_entities import DiscoverInstrumentEntities
from .discover_portfolio_entities import DiscoverPortfolioEntities
from .discover_investment_flow_entities import DiscoverInvestmentFlowEntities
from .discover_trading_entities import DiscoverTradingEntities
from .discover_valuation_entities import DiscoverValuationEntities
from .discover_billing_entities import DiscoverBillingEntities
from .discover_reporting_entities import DiscoverReportingEntities
from .discover_system_entities import DiscoverSystemEntities

__all__ = [
    'DiscoverUserEntities',
    'DiscoverInvestorEntities', 
    'DiscoverFundEntities',
    'DiscoverInstrumentEntities',
    'DiscoverPortfolioEntities',
    'DiscoverInvestmentFlowEntities',
    'DiscoverTradingEntities',
    'DiscoverValuationEntities',
    'DiscoverBillingEntities',
    'DiscoverReportingEntities',
    'DiscoverSystemEntities'
]
EOF

# Create a registry file for easy access to all functions
cat > function_registry.py << 'EOF'
"""
Function Registry for Discovery Functions

Provides easy access to all discovery functions and their metadata.
"""

from typing import Dict, List, Any
from .discover_user_entities import DiscoverUserEntities
from .discover_investor_entities import DiscoverInvestorEntities
from .discover_fund_entities import DiscoverFundEntities
from .discover_instrument_entities import DiscoverInstrumentEntities
from .discover_portfolio_entities import DiscoverPortfolioEntities
from .discover_investment_flow_entities import DiscoverInvestmentFlowEntities
from .discover_trading_entities import DiscoverTradingEntities
from .discover_valuation_entities import DiscoverValuationEntities
from .discover_billing_entities import DiscoverBillingEntities
from .discover_reporting_entities import DiscoverReportingEntities
from .discover_system_entities import DiscoverSystemEntities


class DiscoveryFunctionRegistry:
    """Registry for all discovery functions"""
    
    FUNCTIONS = {
        'users': DiscoverUserEntities,
        'investors': DiscoverInvestorEntities,
        'funds': DiscoverFundEntities,
        'instruments': DiscoverInstrumentEntities,
        'portfolios': DiscoverPortfolioEntities,
        'portfolio_holdings': DiscoverPortfolioEntities,
        'subscriptions': DiscoverInvestmentFlowEntities,
        'commitments': DiscoverInvestmentFlowEntities,
        'redemptions': DiscoverInvestmentFlowEntities,
        'trades': DiscoverTradingEntities,
        'nav_records': DiscoverValuationEntities,
        'instrument_prices': DiscoverValuationEntities,
        'invoices': DiscoverBillingEntities,
        'payments': DiscoverBillingEntities,
        'reports': DiscoverReportingEntities,
        'documents': DiscoverReportingEntities,
        'notifications': DiscoverSystemEntities,
        'audit_trails': DiscoverSystemEntities
    }
    
    ENTITY_GROUPS = {
        'user_entities': ['users'],
        'investor_entities': ['investors'],
        'fund_entities': ['funds'],
        'instrument_entities': ['instruments'],
        'portfolio_entities': ['portfolios', 'portfolio_holdings'],
        'investment_flow_entities': ['subscriptions', 'commitments', 'redemptions'],
        'trading_entities': ['trades'],
        'valuation_entities': ['nav_records', 'instrument_prices'],
        'billing_entities': ['invoices', 'payments'],
        'reporting_entities': ['reports', 'documents'],
        'system_entities': ['notifications', 'audit_trails']
    }
    
    @classmethod
    def get_function_for_entity(cls, entity_type: str):
        """Get the appropriate discovery function for an entity type"""
        return cls.FUNCTIONS.get(entity_type)
    
    @classmethod
    def get_all_entity_types(cls) -> List[str]:
        """Get list of all supported entity types"""
        return list(cls.FUNCTIONS.keys())
    
    @classmethod
    def get_entity_group(cls, entity_type: str) -> str:
        """Get the group name for an entity type"""
        for group, entities in cls.ENTITY_GROUPS.items():
            if entity_type in entities:
                return group
        return None
    
    @classmethod
    def get_function_info_all(cls) -> Dict[str, Any]:
        """Get info for all discovery functions"""
        info = {}
        for entity_type, function_class in cls.FUNCTIONS.items():
            info[entity_type] = function_class.get_info()
        return info
EOF

# Create a simple test file
cat > test_discovery_functions.py << 'EOF'
"""
Simple test file for discovery functions
"""

import json
from function_registry import DiscoveryFunctionRegistry

def test_sample_data():
    """Test with sample data"""
    
    # Sample test data
    sample_data = {
        "users": {
            "user_001": {
                "first_name": "John",
                "last_name": "Doe", 
                "email": "john.doe@company.com",
                "role": "fund_manager",
                "timezone": "UTC",
                "status": "active",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            },
            "user_002": {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane.smith@company.com", 
                "role": "trader",
                "timezone": "UTC",
                "status": "active",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        },
        "funds": {
            "fund_001": {
                "name": "Growth Fund A",
                "fund_type": "mutual_funds",
                "manager_id": "user_001",
                "size": 1000000.00,
                "status": "open",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }
    }
    
    # Test user discovery
    user_function = DiscoveryFunctionRegistry.get_function_for_entity('users')
    if user_function:
        result = user_function.invoke(sample_data, 'users')
        print("Users discovery result:")
        print(json.dumps(json.loads(result), indent=2))
        
        # Test with filter
        result_filtered = user_function.invoke(sample_data, 'users', {"role": "fund_manager"})
        print("\nFiltered users result:")
        print(json.dumps(json.loads(result_filtered), indent=2))
    
    # Test fund discovery
    fund_function = DiscoveryFunctionRegistry.get_function_for_entity('funds')
    if fund_function:
        result = fund_function.invoke(sample_data, 'funds')
        print("\nFunds discovery result:")
        print(json.dumps(json.loads(result), indent=2))

if __name__ == "__main__":
    test_sample_data()
EOF

# Create README file
cat > README.md << 'EOF'
# Discovery Functions

This package contains 11 discovery functions for B2B finance entities, organized by business logic:

## Functions Overview

1. **DiscoverUserEntities** - `users`
2. **DiscoverInvestorEntities** - `investors`  
3. **DiscoverFundEntities** - `funds`
4. **DiscoverInstrumentEntities** - `instruments`
5. **DiscoverPortfolioEntities** - `portfolios`, `portfolio_holdings`
6. **DiscoverInvestmentFlowEntities** - `subscriptions`, `commitments`, `redemptions`
7. **DiscoverTradingEntities** - `trades`
8. **DiscoverValuationEntities** - `nav_records`, `instrument_prices`
9. **DiscoverBillingEntities** - `invoices`, `payments`
10. **DiscoverReportingEntities** - `reports`, `documents`
11. **DiscoverSystemEntities** - `notifications`, `audit_trails`

## Key Features

- **String IDs**: All entity IDs are treated as strings
- **Type Safety**: Complete type specifications for all parameters
- **Enum Support**: Full enum value definitions for categorical fields
- **Filtering**: Exact match filtering with AND logic for multiple filters
- **Consistent API**: All functions follow the same interface pattern

## Usage Example

```python
from function_registry import DiscoveryFunctionRegistry

# Get function for entity type
user_function = DiscoveryFunctionRegistry.get_function_for_entity('users')

# Discover all users
result = user_function.invoke(data, 'users')

# Discover with filters
result = user_function.invoke(data, 'users', {"status": "active", "role": "fund_manager"})
EOF