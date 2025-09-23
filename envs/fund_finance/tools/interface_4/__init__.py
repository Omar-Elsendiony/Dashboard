from .verify_approval import VerifyApproval
from .record_commitment import RecordCommitment
from .record_investor import RecordInvestor
from .record_new_audit_trail import RecordNewAuditTrail
from .lookup_billing_entities import LookupBillingEntities
from .lookup_fund_entities import LookupFundEntities
from .lookup_instrument_entities import LookupInstrumentEntities
from .lookup_investment_flow_entities import LookupInvestmentFlowEntities
from .lookup_investor_entities import LookupInvestorEntities
from .lookup_portfolio_entities import LookupPortfolioEntities
from .lookup_reporting_entities import LookupReportingEntities
from .lookup_system_entities import LookupSystemEntities
from .lookup_trading_entities import LookupTradingEntities
from .lookup_user_entities import LookupUserEntities
from .lookup_valuation_entities import LookupValuationEntities
from .process_trade import ProcessTrade
from .accomplish_commitment import AccomplishCommitment
from .compile_report import CompileReport
from .address_fund import AddressFund
from .address_instrument import AddressInstrument
from .address_instrument_price import AddressInstrumentPrice
from .address_invoice import AddressInvoice
from .address_nav_record import AddressNavRecord
from .address_notifications import AddressNotifications
from .address_payment import AddressPayment
from .address_portfolio import AddressPortfolio
from .address_portfolio_holdings import AddressPortfolioHoldings
from .address_subscription import AddressSubscription
from .deregister_investor import DeregisterInvestor
from .finalize_redemption import FinalizeRedemption
from .handover_to_human import HandOverToHuman
from .archive_document import ArchiveDocument

ALL_TOOLS_INTERFACE_4 = [
    VerifyApproval,
    RecordCommitment,
    RecordInvestor,
    RecordNewAuditTrail,
    LookupBillingEntities,
    LookupFundEntities,
    LookupInstrumentEntities,
    LookupInvestmentFlowEntities,
    LookupInvestorEntities,
    LookupPortfolioEntities,
    LookupReportingEntities,
    LookupSystemEntities,
    LookupTradingEntities,
    LookupUserEntities,
    LookupValuationEntities,
    ProcessTrade,
    AccomplishCommitment,
    CompileReport,
    AddressFund,
    AddressInstrument,
    AddressInstrumentPrice,
    AddressInvoice,
    AddressNavRecord,
    AddressNotifications,
    AddressPayment,
    AddressPortfolio,
    AddressPortfolioHoldings,
    AddressSubscription,
    DeregisterInvestor,
    FinalizeRedemption,
    HandOverToHuman,
    ArchiveDocument
]
