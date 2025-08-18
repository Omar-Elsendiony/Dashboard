from .add_portfolio_holding import AddPortfolioHolding
from .cancel_investor_subscription import CancelInvestorSubscription
from .create_investor_subscription import CreateInvestorSubscription
from .create_new_user import CreateNewUser
from .filter_funds import FilterFunds
from .find_user import FindUser
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
from .insert_audit_trail import InsertAuditTrail
from .investor_withdrawal import InvestorWithdrawal
from .investor_enrollment import InvestorEnrollment
from .process_investor_redemption import ProcessInvestorRedemption
from .remove_portfolio_holding import RemovePortfolioHolding
from .switch_investor_funds import SwitchInvestorFunds
from .update_investor_details import UpdateInvestorDetails
from .update_investor_portfolio_holding import UpdateInvestorPortfolioHolding
from .update_investor_subscription import UpdateInvestorSubscription
from .approval_lookup import ApprovalLookup

ALL_TOOLS_INTERFACE_2 = [
    AddPortfolioHolding,
    CancelInvestorSubscription,
    CreateInvestorSubscription,
    CreateNewUser,
    FilterFunds,
    FindUser,
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
    InsertAuditTrail,
    InvestorEnrollment,
    InvestorWithdrawal,
    ProcessInvestorRedemption,
    RemovePortfolioHolding,
    SwitchInvestorFunds,
    UpdateInvestorDetails,
    UpdateInvestorPortfolioHolding,
    UpdateInvestorSubscription,
    ApprovalLookup
]
