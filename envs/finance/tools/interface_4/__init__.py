from .adjust_fund import AdjustFund
from .adjust_instrument import AdjustInstrument
from .adjust_instrument_price import AdjustInstrumentPrice
from .adjust_nav_record_value import AdjustNavRecordValue
from .calculate_daily_profit_loss_by_fund import CalculateDailyProfitLossByFund
from .check_approval import CheckApproval
from .compose_document import ComposeDocument
from .compose_fund import ComposeFund
from .construct_audit_trail import ConstructAuditTrail
from .construct_user import ConstructUser
from .create_report import CreateReport
from .evaluate_future_value import EvaluateFutureValue
from .evaluate_nav import EvaluateNav
from .filter_funds_with_criteria import FilterFundsWithCriteria
from .get_growth_rate import GetGrowthRate
from .obtain_available_funds import ObtainAvailableFunds
from .obtain_commitments import ObtainCommitments
from .obtain_fund_instruments import ObtainFundInstruments
from .obtain_fund_trade_details import ObtainFundTradeDetails
from .obtain_instruments import ObtainInstruments
from .obtain_instruments_prices import ObtainInstrumentsPrices
from .obtain_nav_records import ObtainNavRecords
from .obtain_performance_history import ObtainPerformanceHistory
from .remove_fund import RemoveFund
from .summary_of_instrument_types_by_prices import SummaryOfInstrumentTypesByPrices
from .identify_users import IdentifyUsers

ALL_TOOLS_INTERFACE_4 = [
    CalculateDailyProfitLossByFund,
    AdjustFund,
    AdjustInstrument,
    AdjustInstrumentPrice,
    AdjustNavRecordValue,
    CheckApproval,
    ComposeDocument,
    ComposeFund,
    ConstructAuditTrail,
    ConstructUser,
    CreateReport,
    RemoveFund,
    EvaluateFutureValue,
    EvaluateNav,
    FilterFundsWithCriteria,
    GetGrowthRate,
    ObtainAvailableFunds,
    ObtainCommitments,
    ObtainFundInstruments,
    ObtainFundTradeDetails,
    ObtainInstruments,
    ObtainInstrumentsPrices,
    ObtainNavRecords,
    ObtainPerformanceHistory,
    SummaryOfInstrumentTypesByPrices,
    IdentifyUsers
]
