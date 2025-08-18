from .add_analysis_audit_trail import AddAnalysisAuditTrail
from .add_analysis_user import AddAnalysisUser
from .calculate_fund_future_value import CalculateFundFutureValue
from .calculate_fund_nav import CalculateFundNav
from .create_analysis_fund import CreateAnalysisFund
from .upload_analysis_document import UploadAnalysisDocument
from .delete_analysis_fund import DeleteAnalysisFund
from .generate_analysis_report import GenerateAnalysisReport
from .get_analysis_approval import GetAnalysisApproval
from .get_available_analysis_funds import GetAvailableAnalysisFunds
from .get_fund_commitments import GetFundCommitments
from .get_daily_fund_profit_loss import GetDailyFundProfitLoss
from .get_fund_instrument_analysis import GetFundInstrumentAnalysis
from .get_fund_trade_analysis import GetFundTradeAnalysis
from .get_fund_growth_rate import GetFundGrowthRate
from .get_fund_instruments import GetFundInstruments
from .get_instrument_price_analysis import GetInstrumentPriceAnalysis
from .get_fund_nav_records import GetFundNavRecords
from .get_fund_performance_history import GetFundPerformanceHistory
from .list_funds_for_analysis import ListFundsForAnalysis
from .summarize_instrument_analysis import SummarizeInstrumentAnalysis
from .update_analysis_fund import UpdateAnalysisFund
from .update_analysis_instrument import UpdateAnalysisInstrument
from .update_analysis_instrument_price import UpdateAnalysisInstrumentPrice
from .update_fund_nav_value import UpdateFundNavValue

ALL_TOOLS_INTERFACE_4 = [
    AddAnalysisAuditTrail,
    AddAnalysisUser,
    CalculateFundFutureValue,
    CalculateFundNav,
    CreateAnalysisFund,
    UploadAnalysisDocument,
    DeleteAnalysisFund,
    GenerateAnalysisReport,
    GetAnalysisApproval,
    GetAvailableAnalysisFunds,
    GetFundCommitments,
    GetDailyFundProfitLoss,
    GetFundInstrumentAnalysis,
    GetFundTradeAnalysis,
    GetFundGrowthRate,
    GetFundInstruments,
    GetInstrumentPriceAnalysis,
    GetFundNavRecords,
    GetFundPerformanceHistory,
    ListFundsForAnalysis,
    SummarizeInstrumentAnalysis,
    UpdateAnalysisFund,
    UpdateAnalysisInstrument,
    UpdateAnalysisInstrumentPrice,
    UpdateFundNavValue
]
