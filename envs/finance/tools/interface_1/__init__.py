from .add_fund_audit_trail import AddFundAuditTrail
from .add_fund_trade import AddFundTrade
from .calculate_fund_future_value import CalculateFundFutureValue
from .calculate_fund_liabilities import CalculateFundLiabilities
from .calculate_fund_nav import CalculateFundNav
from .create_fund import CreateFund
from .close_fund import CloseFund
from .execute_fund_trade import ExecuteFundTrade
from .validate_fund_manager_approval import ValidateFundManagerApproval
from .get_available_funds import GetAvailableFunds
from .get_fund_daily_pnl import GetFundDailyPnL
from .get_fund_instruments import GetFundInstruments
from .get_fund_nav_history import GetFundNavHistory
from .get_fund_trade_details import GetFundTradeDetails
from .get_fund_growth_rate import GetFundGrowthRate
from .get_tradable_instruments import GetTradableInstruments
from .get_instruments_prices import GetInstrumentsPrices
from .get_nav_records import GetNavRecords
from .search_funds import SearchFunds
from .update_fund import UpdateFund
from .update_instrument import UpdateInstrument
from .update_instrument_price import UpdateInstrumentPrice
from .update_nav_record_value import UpdateNavRecordValue
from .update_trade import UpdateTrade

ALL_TOOLS_INTERFACE_1 = [
    AddFundAuditTrail,
    AddFundTrade,
    CalculateFundFutureValue,
    CalculateFundLiabilities,
    CalculateFundNav,
    CreateFund,
    CloseFund,
    ExecuteFundTrade,
    ValidateFundManagerApproval,
    GetAvailableFunds,
    GetFundDailyPnL,
    GetFundInstruments,
    GetFundNavHistory,
    GetFundTradeDetails,
    GetFundGrowthRate,
    GetTradableInstruments,
    GetInstrumentsPrices,
    GetNavRecords,
    SearchFunds,
    UpdateFund,
    UpdateInstrument,
    UpdateInstrumentPrice,
    UpdateNavRecordValue,
    UpdateTrade
]
