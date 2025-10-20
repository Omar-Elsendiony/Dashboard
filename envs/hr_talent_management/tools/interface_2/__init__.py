from .add_audit_entry import AddAuditEntry
from .administer_application_operations import AdministerApplicationOperations
from .administer_benefit_enrollment_operations import AdministerBenefitEnrollmentOperations
from .administer_benefit_plan_operations import AdministerBenefitPlanOperations
from .administer_candidate_operations import AdministerCandidateOperations
from .administer_department_operations import AdministerDepartmentOperations
from .administer_document_operations import AdministerDocumentOperations
from .administer_employee_exit_operations import AdministerEmployeeExitOperations
from .administer_employee_operations import AdministerEmployeeOperations
from .administer_interview_operations import AdministerInterviewOperations
from .administer_it_provisioning_operations import AdministerItProvisioningOperations
from .administer_job_operations import AdministerJobOperations
from .administer_location_operations import AdministerLocationOperations
from .administer_notification_operations import AdministerNotificationOperations
from .administer_offer_operations import AdministerOfferOperations
from .administer_onboarding_operations import AdministerOnboardingOperations
from .administer_payment_operations import AdministerPaymentOperations
from .administer_payroll_cycle_operations import AdministerPayrollCycleOperations
from .administer_payroll_earning_operations import AdministerPayrollEarningOperations
from .administer_payroll_input_operations import AdministerPayrollInputOperations
from .administer_payslip_operations import AdministerPayslipOperations
from .administer_user_operations import AdministerUserOperations
from .fetch_benefit_entities import FetchBenefitEntities
from .fetch_candidate_entities import FetchCandidateEntities
from .fetch_document_task_entities import FetchDocumentTaskEntities
from .fetch_employee_entities import FetchEmployeeEntities
from .fetch_interview_offer_entities import FetchInterviewOfferEntities
from .fetch_job_entities import FetchJobEntities
from .fetch_payment_entities import FetchPaymentEntities
from .fetch_payroll_entities import FetchPayrollEntities
from .fetch_reference_entities import FetchReferenceEntities
from .fetch_system_entities import FetchSystemEntities
from .switch_to_human import SwitchToHuman

ALL_TOOLS_INTERFACE_2 = [
    AddAuditEntry,
    AdministerApplicationOperations,
    AdministerBenefitEnrollmentOperations,
    AdministerBenefitPlanOperations,
    AdministerCandidateOperations,
    AdministerDepartmentOperations,
    AdministerDocumentOperations,
    AdministerEmployeeExitOperations,
    AdministerEmployeeOperations,
    AdministerInterviewOperations,
    AdministerItProvisioningOperations,
    AdministerJobOperations,
    AdministerLocationOperations,
    AdministerNotificationOperations,
    AdministerOfferOperations,
    AdministerOnboardingOperations,
    AdministerPaymentOperations,
    AdministerPayrollCycleOperations,
    AdministerPayrollEarningOperations,
    AdministerPayrollInputOperations,
    AdministerPayslipOperations,
    AdministerUserOperations,
    FetchBenefitEntities,
    FetchCandidateEntities,
    FetchDocumentTaskEntities,
    FetchEmployeeEntities,
    FetchInterviewOfferEntities,
    FetchJobEntities,
    FetchPaymentEntities,
    FetchPayrollEntities,
    FetchReferenceEntities,
    FetchSystemEntities,
    SwitchToHuman
]
