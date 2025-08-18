from .add_commitment import AddCommitment
from .append_audit_trail import AppendAuditTrail
from .authenticate_approval import AuthenticateApproval
from .deactivate_reactivate_instrument import DeactivateReactivateInstrument
from .dispatch_email_notification import DispatchEmailNotification
from .query_investors import QueryInvestors
from .fetch_investor_documents import FetchInvestorDocuments
from .fetch_investor_portfolio import FetchInvestorPortfolio
from .fetch_investor_portfolio_holdings import FetchInvestorPortfolioHoldings
from .fetch_investor_profile import FetchInvestorProfile
from .fetch_investor_statements import FetchInvestorStatements
from .fetch_investor_transactions_history import FetchInvestorTransactionsHistory
from .fetch_notifications import FetchNotifications
from .fetch_payment_history import FetchPaymentHistory
from .fetch_portfolio_holdings import FetchPortfolioHoldings
from .fetch_subscriptions import FetchSubscriptions
from .generate_invoice import GenerateInvoice
from .get_reports import GetReports
from .investor_offboarding import InvestorOffboarding
from .investor_onboarding import InvestorOnboarding
from .locate_user import LocateUser
from .modify_invoice_config import ModifyInvoiceConfig
from .register_subscription import RegisterSubscription
from .remove_invoice import RemoveInvoice
from .revise_investor_details import ReviseInvestorDetails
from .revise_subscription import ReviseSubscription
from .terminate_subscription import TerminateSubscription
from .get_funds import GetFunds
from .search_investors import SearchInvestors


ALL_TOOLS_INTERFACE_5 = [
    AddCommitment,
    AppendAuditTrail,
    AuthenticateApproval,
    DeactivateReactivateInstrument,
    DispatchEmailNotification,
    QueryInvestors,
    FetchInvestorDocuments,
    FetchInvestorPortfolio,
    FetchInvestorPortfolioHoldings,
    FetchInvestorProfile,
    FetchInvestorStatements,
    FetchInvestorTransactionsHistory,
    FetchNotifications,
    FetchPaymentHistory,
    FetchPortfolioHoldings,
    FetchSubscriptions,
    GenerateInvoice,
    GetReports,
    InvestorOffboarding,
    InvestorOnboarding,
    LocateUser,
    ModifyInvoiceConfig,
    RegisterSubscription,
    RemoveInvoice,
    ReviseInvestorDetails,
    ReviseSubscription,
    TerminateSubscription,
    GetFunds,
    SearchInvestors
]
