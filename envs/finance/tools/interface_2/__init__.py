from .add_investor_audit_trail import AddInvestorAuditTrail
from .add_portfolio_holding import AddPortfolioHolding
from .cancel_investor_subscription import CancelInvestorSubscription
from .create_investor_subscription import CreateInvestorSubscription
from .create_investor_user import CreateInvestorUser
from .find_investor_user import FindInvestorUser
from .get_filtered_investors import GetFilteredInvestors
from .get_investor_documents import GetInvestorDocuments
from .get_investor_portfolio import GetInvestorPortfolio
from .get_investor_portfolio_holdings import GetInvestorPortfolioHoldings
from .get_investor_profile import GetInvestorProfile
from .get_investor_redemptions import GetInvestorRedemptions
from .get_investor_statements import GetInvestorStatements
from .get_investor_subscription_list import GetInvestorSubscriptionList
from .get_investor_subscriptions import GetInvestorSubscriptions
from .get_investor_transactions_history import GetInvestorTransactionsHistory
from .get_portfolio_holdings import GetPortfolioHoldings
from .investor_offboarding import InvestorOffboarding
from .investor_onboarding import InvestorOnboarding
from .process_investor_redemption import ProcessInvestorRedemption
from .remove_portfolio_holding import RemovePortfolioHolding
from .switch_investor_funds import SwitchInvestorFunds
from .update_investor_details import UpdateInvestorDetails
from .update_investor_portfolio_holding import UpdateInvestorPortfolioHolding
from .update_investor_subscription import UpdateInvestorSubscription
from .validate_compliance_approval import ValidateComplianceApproval

ALL_TOOLS_INTERFACE_2 = [
    AddInvestorAuditTrail,
    AddPortfolioHolding,
    CancelInvestorSubscription,
    CreateInvestorSubscription,
    CreateInvestorUser,
    FindInvestorUser,
    GetFilteredInvestors,
    GetInvestorDocuments,
    GetInvestorPortfolio,
    GetInvestorPortfolioHoldings,
    GetInvestorProfile,
    GetInvestorRedemptions,
    GetInvestorStatements,
    GetInvestorSubscriptionList,
    GetInvestorSubscriptions,
    GetInvestorTransactionsHistory,
    GetPortfolioHoldings,
    InvestorOffboarding,
    InvestorOnboarding,
    ProcessInvestorRedemption,
    RemovePortfolioHolding,
    SwitchInvestorFunds,
    UpdateInvestorDetails,
    UpdateInvestorPortfolioHolding,
    UpdateInvestorSubscription,
    ValidateComplianceApproval
]
