from .create_new_audit_trail import CreateNewAuditTrail
from .add_new_user import AddNewUser
from .assess_future_value import AssessFutureValue
from .evaluate_liabilities import EvaluateLiabilities
from .calculate_nav import CalculateNav
from .create_commitment import CreateCommitment
from .create_invoice import CreateInvoice
from .create_upload_document import CreateUploadDocument
from .delete_invoice import DeleteInvoice
from .fulfill_commitment import FulfillCommitment
from .generate_report import GenerateReport
from .confirm_approval import ConfirmApproval
from .get_available_funds import GetAvailableFunds
from .get_commitments import GetCommitments
from .get_filtered_investors import GetFilteredInvestors
from .get_investor_commitments import GetInvestorCommitments
from .get_investor_profile import GetInvestorProfile
from .get_invoices import GetInvoices
from .get_notifications import GetNotifications
from .get_payment_history import GetPaymentHistory
from .acquire_reports import AcquireReports
from .register_payment import RegisterPayment
from .retrieve_invoices import RetrieveInvoices
from .send_email_notification import SendEmailNotification
from .update_invoice import UpdateInvoice

ALL_TOOLS_INTERFACE_3 = [
    CreateNewAuditTrail,
    AddNewUser,
    AssessFutureValue,
    EvaluateLiabilities,
    CalculateNav,
    CreateCommitment,
    CreateInvoice,
    CreateUploadDocument,
    DeleteInvoice,
    FulfillCommitment,
    GenerateReport,
    ConfirmApproval,
    GetAvailableFunds,
    GetCommitments,
    GetFilteredInvestors,
    GetInvestorCommitments,
    GetInvestorProfile,
    GetInvoices,
    GetNotifications,
    GetPaymentHistory,
    AcquireReports,
    RegisterPayment,
    RetrieveInvoices,
    SendEmailNotification,
    UpdateInvoice
]
