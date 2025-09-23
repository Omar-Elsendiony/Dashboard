from .approval_lookup import ApprovalLookup
from .create_commitment import CreateCommitment
from .create_investor import CreateInvestor
from .create_new_audit_trail import CreateNewAuditTrail
from .discover_billing_entities import DiscoverBillingEntities
from .discover_fund_entities import DiscoverFundEntities
from .discover_instrument_entities import DiscoverInstrumentEntities
from .discover_investment_flow_entities import DiscoverInvestmentFlowEntities
from .discover_investor_entities import DiscoverInvestorEntities
from .discover_portfolio_entities import DiscoverPortfolioEntities
from .discover_reporting_entities import DiscoverReportingEntities
from .discover_system_entities import DiscoverSystemEntities
from .discover_trading_entities import DiscoverTradingEntities
from .discover_user_entities import DiscoverUserEntities
from .discover_valuation_entities import DiscoverValuationEntities
from .execute_trade import ExecuteTrade
from .fulfill_commitment import FulfillCommitment
from .generate_report import GenerateReport
from .manage_fund import ManageFund
from .manage_instrument import ManageInstrument
from .manage_instrument_price import ManageInstrumentPrice
from .manage_invoice import ManageInvoice
from .manage_nav_record import ManageNavRecord
from .manage_notifications import ManageNotifications
from .manage_payment import ManagePayment
from .manage_portfolio import ManagePortfolio
from .manage_portfolio_holdings import ManagePortfolioHoldings
from .manage_subscription import ManageSubscription
from .offboard_investor import OffboardInvestor
from .process_redemption import ProcessRedemption
from .transfer_to_human import TransferToHuman
from .upload_document import UploadDocument

ALL_TOOLS_INTERFACE_1 = [
    ApprovalLookup,
    CreateCommitment,
    CreateInvestor,
    CreateNewAuditTrail,
    DiscoverBillingEntities,
    DiscoverFundEntities,
    DiscoverInstrumentEntities,
    DiscoverInvestmentFlowEntities,
    DiscoverInvestorEntities,
    DiscoverPortfolioEntities,
    DiscoverReportingEntities,
    DiscoverSystemEntities,
    DiscoverTradingEntities,
    DiscoverUserEntities,
    DiscoverValuationEntities,
    ExecuteTrade,
    FulfillCommitment,
    GenerateReport,
    ManageFund,
    ManageInstrument,
    ManageInstrumentPrice,
    ManageInvoice,
    ManageNavRecord,
    ManageNotifications,
    ManagePayment,
    ManagePortfolio,
    ManagePortfolioHoldings,
    ManageSubscription,
    OffboardInvestor,
    ProcessRedemption,
    TransferToHuman,
    UploadDocument
]
