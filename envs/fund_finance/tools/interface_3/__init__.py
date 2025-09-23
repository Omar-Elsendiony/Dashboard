from .validate_approval import ValidateApproval
from .register_commitment import RegisterCommitment
from .register_investor import RegisterInvestor
from .register_new_audit_trail import RegisterNewAuditTrail
from .find_billing_entities import FindBillingEntities
from .find_fund_entities import FindFundEntities
from .find_instrument_entities import FindInstrumentEntities
from .find_investment_flow_entities import FindInvestmentFlowEntities
from .find_investor_entities import FindInvestorEntities
from .find_portfolio_entities import FindPortfolioEntities
from .find_reporting_entities import FindReportingEntities
from .find_system_entities import FindSystemEntities
from .find_trading_entities import FindTradingEntities
from .find_user_entities import FindUserEntities
from .find_valuation_entities import FindValuationEntities
from .conduct_trade import ConductTrade
from .complete_commitment import CompleteCommitment
from .build_report import BuildReport
from .manipulate_fund import ManipulateFund
from .manipulate_instrument import ManipulateInstrument
from .manipulate_instrument_price import ManipulateInstrumentPrice
from .manipulate_invoice import ManipulateInvoice
from .manipulate_nav_record import ManipulateNavRecord
from .manipulate_notifications import ManipulateNotifications
from .manipulate_payment import ManipulatePayment
from .manipulate_portfolio import ManipulatePortfolio
from .manipulate_portfolio_holdings import ManipulatePortfolioHoldings
from .manipulate_subscription import ManipulateSubscription
from .remove_investor import RemoveInvestor
from .complete_redemption import CompleteRedemption
from .escalate_to_human import EscalateToHuman
from .submit_document import SubmitDocument

ALL_TOOLS_INTERFACE_3 = [
    ValidateApproval,
    RegisterCommitment,
    RegisterInvestor,
    RegisterNewAuditTrail,
    FindBillingEntities,
    FindFundEntities,
    FindInstrumentEntities,
    FindInvestmentFlowEntities,
    FindInvestorEntities,
    FindPortfolioEntities,
    FindReportingEntities,
    FindSystemEntities,
    FindTradingEntities,
    FindUserEntities,
    FindValuationEntities,
    ConductTrade,
    CompleteCommitment,
    BuildReport,
    ManipulateFund,
    ManipulateInstrument,
    ManipulateInstrumentPrice,
    ManipulateInvoice,
    ManipulateNavRecord,
    ManipulateNotifications,
    ManipulatePayment,
    ManipulatePortfolio,
    ManipulatePortfolioHoldings,
    ManipulateSubscription,
    RemoveInvestor,
    CompleteRedemption,
    EscalateToHuman,
    SubmitDocument
]
