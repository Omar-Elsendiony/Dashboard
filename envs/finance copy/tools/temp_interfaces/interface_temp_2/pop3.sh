#!/bin/bash

# Create directory for tools
mkdir -p fund_management_tools
cd fund_management_tools

# Generate generate_report.py
cat > generate_report.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GenerateReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, report_type: str = "performance", 
               investor_id: Optional[str] = None, generated_by: str = "",
               export_period_end: str = "") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        users = data.get("users", {})
        investors = data.get("investors", {})
        reports = data.get("reports", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate user exists
        if str(generated_by) not in users:
            raise ValueError(f"User {generated_by} not found")
        
        # Validate investor if provided
        if investor_id and str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate report type
        valid_types = ["performance", "holding", "financial"]
        if report_type not in valid_types:
            raise ValueError(f"Invalid report type. Must be one of {valid_types}")
        
        report_id = generate_id(reports)
        timestamp = "2025-10-01T00:00:00"
        
        new_report = {
            "report_id": report_id,
            "fund_id": fund_id,
            "investor_id": investor_id,
            "report_date": "2025-10-01",
            "report_type": report_type,
            "generated_by": generated_by,
            "status": "pending",
            "created_at": timestamp,
            "export_period_end": export_period_end or "2025-10-01"
        }
        
        reports[str(report_id)] = new_report
        return json.dumps({"report_id": report_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "generate_report",
                "description": "Generate a new report for regulatory filings or client statements",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "report_type": {"type": "string", "description": "Type of report (performance, holding, financial), defaults to performance"},
                        "investor_id": {"type": "string", "description": "ID of specific investor (optional)"},
                        "generated_by": {"type": "string", "description": "ID of the user generating the report"},
                        "export_period_end": {"type": "string", "description": "End date for the report period"}
                    },
                    "required": ["fund_id", "generated_by", "export_period_end"]
                }
            }
        }
EOF

# Generate get_reports.py
cat > get_reports.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetReports(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None, 
               investor_id: Optional[str] = None, report_type: Optional[str] = None,
               status: Optional[str] = None) -> str:
        reports = data.get("reports", {})
        results = []
        
        for report in reports.values():
            if fund_id and report.get("fund_id") != fund_id:
                continue
            if investor_id and report.get("investor_id") != investor_id:
                continue
            if report_type and report.get("report_type") != report_type:
                continue
            if status and report.get("status") != status:
                continue
            results.append(report)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_reports",
                "description": "Get reports with optional filters for distribution and access",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "report_type": {"type": "string", "description": "Filter by report type (performance, holding, financial)"},
                        "status": {"type": "string", "description": "Filter by status (pending, completed, failed)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Generate create_report.py
cat > create_report.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, generated_by: str, 
               export_period_end: str, report_type: str = "performance",
               investor_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        users = data.get("users", {})
        investors = data.get("investors", {})
        reports = data.get("reports", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate user exists
        if str(generated_by) not in users:
            raise ValueError(f"User {generated_by} not found")
        
        # Validate investor if provided
        if investor_id and str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate report type
        valid_types = ["performance", "holding", "financial"]
        if report_type not in valid_types:
            raise ValueError(f"Invalid report type. Must be one of {valid_types}")
        
        report_id = generate_id(reports)
        timestamp = "2025-10-01T00:00:00"
        
        new_report = {
            "report_id": report_id,
            "fund_id": fund_id,
            "investor_id": investor_id,
            "report_date": "2025-10-01",
            "report_type": report_type,
            "generated_by": generated_by,
            "status": "pending",
            "created_at": timestamp,
            "export_period_end": export_period_end
        }
        
        reports[str(report_id)] = new_report
        return json.dumps(new_report)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_report",
                "description": "Create a custom report for specific needs",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "generated_by": {"type": "string", "description": "ID of the user creating the report"},
                        "export_period_end": {"type": "string", "description": "End date for the report period"},
                        "report_type": {"type": "string", "description": "Type of report (performance, holding, financial), defaults to performance"},
                        "investor_id": {"type": "string", "description": "ID of specific investor (optional)"}
                    },
                    "required": ["fund_id", "generated_by", "export_period_end"]
                }
            }
        }
EOF

# Generate get_fund_valuation.py
cat > get_fund_valuation.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFundValuation(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, nav_date: Optional[str] = None) -> str:
        nav_records = data.get("nav_records", {})
        funds = data.get("funds", {})
        results = []
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        for nav in nav_records.values():
            if nav.get("fund_id") != fund_id:
                continue
            if nav_date and nav.get("nav_date") != nav_date:
                continue
            results.append(nav)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_fund_valuation",
                "description": "Get fund performance measurement through NAV records",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "nav_date": {"type": "string", "description": "Filter by specific NAV date (optional)"}
                    },
                    "required": ["fund_id"]
                }
            }
        }
EOF

# Generate get_daily_profit_loss_by_fund.py
cat > get_daily_profit_loss_by_fund.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetDailyProfitLossByFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, trade_date: Optional[str] = None) -> str:
        trades = data.get("trades", {})
        funds = data.get("funds", {})
        results = []
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        daily_pnl = {}
        
        for trade in trades.values():
            if trade.get("fund_id") != fund_id:
                continue
            
            # Extract date from timestamp
            trade_timestamp = trade.get("trade_date", "")
            trade_day = trade_timestamp.split("T")[0] if "T" in trade_timestamp else trade_timestamp
            
            if trade_date and trade_day != trade_date:
                continue
            
            if trade_day not in daily_pnl:
                daily_pnl[trade_day] = {
                    "date": trade_day,
                    "fund_id": fund_id,
                    "total_buy_value": 0,
                    "total_sell_value": 0,
                    "net_pnl": 0,
                    "trade_count": 0
                }
            
            quantity = float(trade.get("quantity", 0))
            price = float(trade.get("price", 0))
            value = quantity * price
            
            if trade.get("side") == "buy":
                daily_pnl[trade_day]["total_buy_value"] += value
            elif trade.get("side") == "sell":
                daily_pnl[trade_day]["total_sell_value"] += value
            
            daily_pnl[trade_day]["trade_count"] += 1
        
        # Calculate net P&L
        for day_data in daily_pnl.values():
            day_data["net_pnl"] = day_data["total_sell_value"] - day_data["total_buy_value"]
            results.append(day_data)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_daily_profit_loss_by_fund",
                "description": "Get daily profit and loss for risk monitoring by fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "trade_date": {"type": "string", "description": "Filter by specific trade date (optional)"}
                    },
                    "required": ["fund_id"]
                }
            }
        }
EOF

# Generate get_fund_trade_details.py
cat > get_fund_trade_details.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFundTradeDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, instrument_id: Optional[str] = None,
               status: Optional[str] = None, side: Optional[str] = None) -> str:
        trades = data.get("trades", {})
        funds = data.get("funds", {})
        results = []
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        for trade in trades.values():
            if trade.get("fund_id") != fund_id:
                continue
            if instrument_id and trade.get("instrument_id") != instrument_id:
                continue
            if status and trade.get("status") != status:
                continue
            if side and trade.get("side") != side:
                continue
            
            # Calculate trade value for cost analysis
            trade_copy = trade.copy()
            trade_copy["trade_value"] = float(trade.get("quantity", 0)) * float(trade.get("price", 0))
            results.append(trade_copy)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_fund_trade_details",
                "description": "Get fund trade details for transaction cost analysis",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "instrument_id": {"type": "string", "description": "Filter by instrument ID (optional)"},
                        "status": {"type": "string", "description": "Filter by trade status (approved, executed, pending, failed)"},
                        "side": {"type": "string", "description": "Filter by trade side (buy, sell)"}
                    },
                    "required": ["fund_id"]
                }
            }
        }
EOF

# Generate get_instruments.py
cat > get_instruments.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInstruments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_type: Optional[str] = None,
               status: Optional[str] = None, ticker: Optional[str] = None) -> str:
        instruments = data.get("instruments", {})
        results = []
        
        for instrument in instruments.values():
            if instrument_type and instrument.get("instrument_type") != instrument_type:
                continue
            if status and instrument.get("status") != status:
                continue
            if ticker and instrument.get("ticker") != ticker:
                continue
            results.append(instrument)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_instruments",
                "description": "Get instruments for investment universe management",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_type": {"type": "string", "description": "Filter by instrument type"},
                        "status": {"type": "string", "description": "Filter by status (active, inactive)"},
                        "ticker": {"type": "string", "description": "Filter by ticker symbol"}
                    },
                    "required": []
                }
            }
        }
EOF

# Generate get_instruments_prices.py
cat > get_instruments_prices.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInstrumentsPrices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: Optional[str] = None,
               price_date: Optional[str] = None) -> str:
        instrument_prices = data.get("instrument_prices", {})
        instruments = data.get("instruments", {})
        results = []
        
        # Validate instrument if provided
        if instrument_id and str(instrument_id) not in instruments:
            raise ValueError(f"Instrument {instrument_id} not found")
        
        for price in instrument_prices.values():
            if instrument_id and price.get("instrument_id") != instrument_id:
                continue
            if price_date and price.get("price_date") != price_date:
                continue
            results.append(price)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_instruments_prices",
                "description": "Get instrument prices for pricing and valuation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "Filter by instrument ID (optional)"},
                        "price_date": {"type": "string", "description": "Filter by price date (optional)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Generate update_instrument_price.py
cat > update_instrument_price.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateInstrumentPrice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: str, price_date: str,
               open_price: float, high_price: float, low_price: float, 
               close_price: float) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        instruments = data.get("instruments", {})
        instrument_prices = data.get("instrument_prices", {})
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument {instrument_id} not found")
        
        # Check if price record already exists for this instrument and date
        existing_price_id = None
        for price_id, price_record in instrument_prices.items():
            if (price_record.get("instrument_id") == instrument_id and 
                price_record.get("price_date") == price_date):
                existing_price_id = price_id
                break
        
        price_record = {
            "instrument_id": instrument_id,
            "price_date": price_date,
            "open_price": open_price,
            "high_price": high_price,
            "low_price": low_price,
            "close_price": close_price
        }
        
        if existing_price_id:
            # Update existing record
            price_record["price_id"] = int(existing_price_id)
            instrument_prices[existing_price_id] = price_record
            return json.dumps({"status": "updated", "price_id": int(existing_price_id)})
        else:
            # Create new record
            price_id = generate_id(instrument_prices)
            price_record["price_id"] = price_id
            instrument_prices[str(price_id)] = price_record
            return json.dumps({"status": "created", "price_id": price_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_instrument_price",
                "description": "Update daily price data for instruments",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "price_date": {"type": "string", "description": "Date of the price data"},
                        "open_price": {"type": "number", "description": "Opening price"},
                        "high_price": {"type": "number", "description": "Highest price"},
                        "low_price": {"type": "number", "description": "Lowest price"},
                        "close_price": {"type": "number", "description": "Closing price"}
                    },
                    "required": ["instrument_id", "price_date", "open_price", "high_price", "low_price", "close_price"]
                }
            }
        }
EOF

# Generate add_new_trade_for_fund.py
cat > add_new_trade_for_fund.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddNewTradeForFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, instrument_id: str,
               quantity: float, price: float, side: str, status: str = "pending") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        instruments = data.get("instruments", {})
        trades = data.get("trades", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument {instrument_id} not found")
        
        # Validate side
        valid_sides = ["buy", "sell"]
        if side not in valid_sides:
            raise ValueError(f"Invalid side. Must be one of {valid_sides}")
        
        # Validate status
        valid_statuses = ["approved", "executed", "pending", "failed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        trade_id = generate_id(trades)
        timestamp = "2025-10-01T00:00:00"
        
        new_trade = {
            "trade_id": trade_id,
            "fund_id": fund_id,
            "instrument_id": instrument_id,
            "trade_date": timestamp,
            "quantity": quantity,
            "price": price,
            "side": side,
            "status": status,
            "created_at": timestamp
        }
        
        trades[str(trade_id)] = new_trade
        return json.dumps({"trade_id": trade_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_new_trade_for_fund",
                "description": "Add a new trade for investment execution",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "quantity": {"type": "number", "description": "Trade quantity"},
                        "price": {"type": "number", "description": "Trade price"},
                        "side": {"type": "string", "description": "Trade side (buy, sell)"},
                        "status": {"type": "string", "description": "Trade status (approved, executed, pending, failed), defaults to pending"}
                    },
                    "required": ["fund_id", "instrument_id", "quantity", "price", "side"]
                }
            }
        }
EOF

# Generate update_trade.py
cat > update_trade.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateTrade(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], trade_id: str, status: Optional[str] = None,
               quantity: Optional[float] = None, price: Optional[float] = None) -> str:
        trades = data.get("trades", {})
        
        # Validate trade exists
        if str(trade_id) not in trades:
            raise ValueError(f"Trade {trade_id} not found")
        
        trade = trades[str(trade_id)]
        
        # Validate status if provided
        if status:
            valid_statuses = ["approved", "executed", "pending", "failed"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            trade["status"] = status
        
        # Update other fields if provided
        if quantity is not None:
            trade["quantity"] = quantity
        
        if price is not None:
            trade["price"] = price
        
        trade["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(trade)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_trade",
                "description": "Update trade for settlement and corrections",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "trade_id": {"type": "string", "description": "ID of the trade to update"},
                        "status": {"type": "string", "description": "New status (approved, executed, pending, failed)"},
                        "quantity": {"type": "number", "description": "Updated quantity"},
                        "price": {"type": "number", "description": "Updated price"}
                    },
                    "required": ["trade_id"]
                }
            }
        }
EOF

# Generate add_new_user.py
cat > add_new_user.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddNewUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], first_name: str, last_name: str, 
               email: str, role: str, timezone: str, status: str = "active") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        
        # Check if email already exists
        for user in users.values():
            if user.get("email") == email:
                raise ValueError(f"Email {email} already exists")
        
        # Validate role
        valid_roles = ["system_administrator", "fund_manager", "compliance_officer", 
                      "finance_officer", "trader"]
        if role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of {valid_roles}")
        
        # Validate status
        valid_statuses = ["active", "inactive", "suspended"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        user_id = generate_id(users)
        timestamp = "2025-10-01T00:00:00"
        
        new_user = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "role": role,
            "timezone": timezone,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        users[str(user_id)] = new_user
        return json.dumps({"user_id": user_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_new_user",
                "description": "Add a new user for staff onboarding",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string", "description": "User's first name"},
                        "last_name": {"type": "string", "description": "User's last name"},
                        "email": {"type": "string", "description": "User's email address"},
                        "role": {"type": "string", "description": "User role (system_administrator, fund_manager, compliance_officer, finance_officer, trader)"},
                        "timezone": {"type": "string", "description": "User's timezone"},
                        "status": {"type": "string", "description": "User status (active, inactive, suspended), defaults to active"}
                    },
                    "required": ["first_name", "last_name", "email", "role", "timezone"]
                }
            }
        }
EOF

# Generate get_user_information.py
cat > get_user_information.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserInformation(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str) -> str:
        users = data.get("users", {})
        
        # Validate user exists
        if str(user_id) not in users:
            raise ValueError(f"User {user_id} not found")
        
        user = users[str(user_id)]
        return json.dumps(user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_information",
                "description": "Get user information for access control and permissions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user"}
                    },
                    "required": ["user_id"]
                }
            }
        }
EOF

# Generate find_user.py
cat > find_user.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FindUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: Optional[str] = None,
               role: Optional[str] = None, status: Optional[str] = None,
               first_name: Optional[str] = None, last_name: Optional[str] = None) -> str:
        users = data.get("users", {})
        results = []
        
        for user in users.values():
            if email and user.get("email", "").lower() != email.lower():
                continue
            if role and user.get("role") != role:
                continue
            if status and user.get("status") != status:
                continue
            if first_name and first_name.lower() not in user.get("first_name", "").lower():
                continue
            if last_name and last_name.lower() not in user.get("last_name", "").lower():
                continue
            results.append(user)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_user",
                "description": "Find users for lookup and support",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "description": "Filter by email address"},
                        "role": {"type": "string", "description": "Filter by role (system_administrator, fund_manager, compliance_officer, finance_officer, trader)"},
                        "status": {"type": "string", "description": "Filter by status (active, inactive, suspended)"},
                        "first_name": {"type": "string", "description": "Filter by first name (partial match)"},
                        "last_name": {"type": "string", "description": "Filter by last name (partial match)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Generate send_email_notification.py
cat > send_email_notification.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SendEmailNotification(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: str, notification_type: str, 
               notification_class: str, reference_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        notifications = data.get("notifications", {})
        
        # Validate notification type
        valid_types = ["alert", "report", "reminder", "subscription_update"]
        if notification_type not in valid_types:
            raise ValueError(f"Invalid notification type. Must be one of {valid_types}")
        
        # Validate notification class
        valid_classes = ["funds", "investors", "portfolios", "trades", "invoices", 
                        "reports", "documents", "subscriptions", "commitments"]
        if notification_class not in valid_classes:
            raise ValueError(f"Invalid notification class. Must be one of {valid_classes}")
        
        notification_id = generate_id(notifications)
        timestamp = "2025-10-01T00:00:00"
        
        new_notification = {
            "notification_id": notification_id,
            "email": email,
            "type": notification_type,
            "class": notification_class,
            "reference_id": reference_id,
            "status": "pending",
            "sent_at": None,
            "created_at": timestamp
        }
        
        notifications[str(notification_id)] = new_notification
        return json.dumps({"notification_id": notification_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "send_email_notification",
                "description": "Send email notification for client communication",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "description": "Recipient email address"},
                        "type": {"type": "string", "description": "Notification type (alert, report, reminder, subscription_update)"},
                        "class": {"type": "string", "description": "Notification class (funds, investors, portfolios, trades, invoices, reports, documents, subscriptions, commitments)"},
                        "reference_id": {"type": "string", "description": "Reference ID for related entity (optional)"}
                    },
                    "required": ["email", "type", "class"]
                }
            }
        }
EOF

# Generate get_notifications.py
cat > get_notifications.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetNotifications(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: Optional[str] = None,
               notification_type: Optional[str] = None, status: Optional[str] = None,
               notification_class: Optional[str] = None) -> str:
        notifications = data.get("notifications", {})
        results = []
        
        for notification in notifications.values():
            if email and notification.get("email") != email:
                continue
            if notification_type and notification.get("type") != notification_type:
                continue
            if status and notification.get("status") != status:
                continue
            if notification_class and notification.get("class") != notification_class:
                continue
            results.append(notification)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_notifications",
                "description": "Get notifications for message management",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "description": "Filter by email address"},
                        "type": {"type": "string", "description": "Filter by notification type (alert, report, reminder, subscription_update)"},
                        "status": {"type": "string", "description": "Filter by status (pending, sent, failed)"},
                        "class": {"type": "string", "description": "Filter by notification class"}
                    },
                    "required": []
                }
            }
        }
EOF

# Generate notify_user.py
cat > notify_user.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class NotifyUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, notification_type: str, 
               notification_class: str, reference_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        notifications = data.get("notifications", {})
        
        # Validate user exists
        if str(user_id) not in users:
            raise ValueError(f"User {user_id} not found")
        
        user_email = users[str(user_id)].get("email")
        if not user_email:
            raise ValueError(f"User {user_id} has no email address")
        
        # Validate notification type
        valid_types = ["alert", "report", "reminder", "subscription_update"]
        if notification_type not in valid_types:
            raise ValueError(f"Invalid notification type. Must be one of {valid_types}")
        
        # Validate notification class
        valid_classes = ["funds", "investors", "portfolios", "trades", "invoices", 
                        "reports", "documents", "subscriptions", "commitments"]
        if notification_class not in valid_classes:
            raise ValueError(f"Invalid notification class. Must be one of {valid_classes}")
        
        notification_id = generate_id(notifications)
        timestamp = "2025-10-01T00:00:00"
        
        new_notification = {
            "notification_id": notification_id,
            "email": user_email,
            "type": notification_type,
            "class": notification_class,
            "reference_id": reference_id,
            "status": "pending",
            "sent_at": None,
            "created_at": timestamp
        }
        
        notifications[str(notification_id)] = new_notification
        return json.dumps({"notification_id": notification_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "notify_user",
                "description": "Send system alerts to users",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user to notify"},
                        "type": {"type": "string", "description": "Notification type (alert, report, reminder, subscription_update)"},
                        "class": {"type": "string", "description": "Notification class (funds, investors, portfolios, trades, invoices, reports, documents, subscriptions, commitments)"},
                        "reference_id": {"type": "string", "description": "Reference ID for related entity (optional)"}
                    },
                    "required": ["user_id", "type", "class"]
                }
            }
        }
EOF

echo "All fund management tools have been generated successfully!"
echo ""
echo "Generated tools:"
echo "- Financial Reporting: generate_report.py, get_reports.py, create_report.py"
echo "- Performance Analytics: get_fund_valuation.py, get_daily_profit_loss_by_fund.py, get_fund_trade_details.py"
echo "- Market Data: get_instruments.py, get_instruments_prices.py, update_instrument_price.py"
echo "- Trade Execution: add_new_trade_for_fund.py, update_trade.py"
echo "- User Management: add_new_user.py, get_user_information.py, find_user.py"
echo "- Communication: send_email_notification.py, get_notifications.py, notify_user.py"
echo ""
echo "To use these tools, run: bash $(basename $0)"