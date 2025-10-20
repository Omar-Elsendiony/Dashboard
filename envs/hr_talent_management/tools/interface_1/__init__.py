# interface_1/tool_registry.py
from .discover_candidate_entities import DiscoverCandidateEntities
from .discover_interview_offer_entities import DiscoverInterviewOfferEntities
from .manage_job_operations import ManageJobOperations
from .manage_candidate_operations import ManageCandidateOperations
from .manage_application_operations import ManageApplicationOperations
from .manage_interview_operations import ManageInterviewOperations
from .manage_employee_operations import ManageEmployeeOperations
from .manage_it_provisioning_operations import ManageItProvisioningOperations
from .manage_offer_operations import ManageOfferOperations
from .manage_onboarding_operations import ManageOnboardingOperations
from .manage_payroll_cycle_operations import ManagePayrollCycleOperations
from .manage_payroll_input_operations import ManagePayrollInputOperations
from .manage_payroll_earning_operations import ManagePayrollEarningOperations
from .manage_payslip_operations import ManagePayslipOperations
from .discover_payroll_entities import DiscoverPayrollEntities
from .discover_benefit_entities import DiscoverBenefitEntities
from .discover_reference_entities import DiscoverReferenceEntities
from .discover_job_entities import DiscoverJobEntities
from .discover_employee_entities import DiscoverEmployeeEntities
from .discover_document_task_entities import DiscoverDocumentTaskEntities
from .manage_document_operations import ManageDocumentOperations
from .manage_notification_operations import ManageNotificationOperations
from .create_audit_entry import CreateAuditEntry
from .manage_employee_exit_operations import ManageEmployeeExitOperations
from .manage_benefit_enrollment_operations import ManageBenefitEnrollmentOperations
from .manage_benefit_plan_operations import ManageBenefitPlanOperations
from .discover_payment_entities import DiscoverPaymentEntities
from .discover_system_entities import DiscoverSystemEntities
from .manage_payment_operations import ManagePaymentOperations
from .manage_user_operations import ManageUserOperations
from .manage_location_operations import ManageLocationOperations
from .manage_department_operations import ManageDepartmentOperations
from .transfer_to_human import TransferToHuman

ALL_TOOLS_INTERFACE_1 = [
    DiscoverReferenceEntities,
    DiscoverJobEntities,
    DiscoverCandidateEntities,
    DiscoverInterviewOfferEntities,
    ManageJobOperations,
    ManageCandidateOperations,
    ManageApplicationOperations,
    ManageInterviewOperations,
    ManageEmployeeOperations,
    ManageItProvisioningOperations,
    ManageOfferOperations,
    ManageOnboardingOperations,
    ManagePayrollCycleOperations,
    ManagePayrollInputOperations,
    ManagePayrollEarningOperations,
    ManagePayslipOperations,
    DiscoverPayrollEntities,
    DiscoverBenefitEntities,
    DiscoverEmployeeEntities,
    DiscoverDocumentTaskEntities,
    ManageDocumentOperations,
    ManageNotificationOperations,
    CreateAuditEntry,
    ManageEmployeeExitOperations,
    ManageBenefitEnrollmentOperations,
    ManageBenefitPlanOperations,
    DiscoverPaymentEntities,
    DiscoverSystemEntities,
    ManagePaymentOperations,
    ManageUserOperations,
    ManageLocationOperations,
    ManageDepartmentOperations,
    TransferToHuman
]

