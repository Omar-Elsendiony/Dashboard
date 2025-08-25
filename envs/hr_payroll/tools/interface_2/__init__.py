from .get_pending_reimbursements import GetPendingReimbursements
from .fetch_time_summary_by_team import FetchTimeSummaryByTeam
from .retrieve_worker_contracts_with_organization import RetrieveWorkerContractsWithOrganization
from .get_payroll_run_details import GetPayrollRunDetails
from .check_user_virtual_cards import CheckUserVirtualCards
from .block_suspicious_payment import BlockSuspiciousPayment
from .extend_contract_period import ExtendContractPeriod
from .approve_overtime_entry import ApproveOvertimeEntry
from .create_new_contract import CreateNewContract
from .update_document_status import UpdateDocumentStatus
from .block_virtual_card import BlockVirtualCard
from .get_contracts import GetContracts
from .get_documents import GetDocuments
from .get_payments import GetPayments
from .upload_document import UploadDocument
from .create_payment import CreatePayment
from .start_new_engagement import StartNewEngagement
from .find_user import FindUser


ALL_TOOLS_INTERFACE_2 = [
    GetPendingReimbursements,
    FetchTimeSummaryByTeam,
    RetrieveWorkerContractsWithOrganization,
    GetPayrollRunDetails,
    CheckUserVirtualCards,
    BlockSuspiciousPayment,
    ExtendContractPeriod,
    ApproveOvertimeEntry,
    CreateNewContract,
    UpdateDocumentStatus,
    BlockVirtualCard,
    GetContracts,
    GetDocuments,
    UploadDocument,
    GetPayments,
    CreatePayment,
    StartNewEngagement,
    FindUser
]
