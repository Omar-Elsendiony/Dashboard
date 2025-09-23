from .check_approval import CheckApproval
from .add_commitment import AddCommitment
from .add_investor import AddInvestor
from .add_new_audit_trail import AddNewAuditTrail
from .search_billing_entities import SearchBillingEntities
from .search_fund_entities import SearchFundEntities
from .search_instrument_entities import SearchInstrumentEntities
from .search_investment_flow_entities import SearchInvestmentFlowEntities
from .search_investor_entities import SearchInvestorEntities
from .search_portfolio_entities import SearchPortfolioEntities
from .search_reporting_entities import SearchReportingEntities
from .search_system_entities import SearchSystemEntities
from .search_trading_entities import SearchTradingEntities
from .search_user_entities import SearchUserEntities
from .search_valuation_entities import SearchValuationEntities
from .perform_trade import PerformTrade
from .settle_commitment import SettleCommitment
from .create_report import CreateReport
from .handle_fund import HandleFund
from .handle_instrument import HandleInstrument
from .handle_instrument_price import HandleInstrumentPrice
from .handle_invoice import HandleInvoice
from .handle_nav_record import HandleNavRecord
from .handle_notifications import HandleNotifications
from .handle_payment import HandlePayment
from .handle_portfolio import HandlePortfolio
from .handle_portfolio_holdings import HandlePortfolioHoldings
from .handle_subscription import HandleSubscription
from .terminate_investor import TerminateInvestor
from .handle_redemption import HandleRedemption
from .switch_to_human import SwitchToHuman  
from .store_document import StoreDocument

ALL_TOOLS_INTERFACE_2 = [
    CheckApproval,
    AddCommitment,
    AddInvestor,
    AddNewAuditTrail,
    SearchBillingEntities,
    SearchFundEntities,
    SearchInstrumentEntities,
    SearchInvestmentFlowEntities,
    SearchInvestorEntities,
    SearchPortfolioEntities,
    SearchReportingEntities,
    SearchSystemEntities,
    SearchTradingEntities,
    SearchUserEntities,
    SearchValuationEntities,
    PerformTrade,
    SettleCommitment,
    CreateReport,
    HandleFund,
    HandleInstrument,
    HandleInstrumentPrice,
    HandleInvoice,
    HandleNavRecord,
    HandleNotifications,
    HandlePayment,
    HandlePortfolio,
    HandlePortfolioHoldings,
    HandleSubscription,
    TerminateInvestor,
    HandleRedemption,
    SwitchToHuman,
    StoreDocument
]
