from .handle_application_operations import HandleApplicationOperations
from .handle_benefit_enrollment_operations import HandleBenefitEnrollmentOperations
from .handle_benefit_plan_operations import HandleBenefitPlanOperations
from .handle_candidate_operations import HandleCandidateOperations
from .handle_department_operations import HandleDepartmentOperations
from .handle_document_operations import HandleDocumentOperations
from .handle_employee_exit_operations import HandleEmployeeExitOperations
from .handle_employee_operations import HandleEmployeeOperations
from .handle_interview_operations import HandleInterviewOperations
from .handle_it_provisioning_operations import HandleItProvisioningOperations
from .handle_job_operations import HandleJobOperations
from .handle_location_operations import HandleLocationOperations
from .handle_notification_operations import HandleNotificationOperations
from .handle_offer_operations import HandleOfferOperations
from .handle_onboarding_operations import HandleOnboardingOperations
from .handle_payment_operations import HandlePaymentOperations
from .handle_payroll_cycle_operations import HandlePayrollCycleOperations
from .handle_payroll_earning_operations import HandlePayrollEarningOperations
from .handle_payroll_input_operations import HandlePayrollInputOperations
from .handle_payslip_operations import HandlePayslipOperations
from .handle_user_operations import HandleUserOperations
from .open_audit_entry import OpenAuditEntry
from .retrieve_benefit_entities import RetrieveBenefitEntities
from .retrieve_candidate_entities import RetrieveCandidateEntities
from .retrieve_document_task_entities import RetrieveDocumentTaskEntities
from .retrieve_employee_entities import RetrieveEmployeeEntities
from .retrieve_interview_offer_entities import RetrieveInterviewOfferEntities
from .retrieve_job_entities import RetrieveJobEntities
from .retrieve_payment_entities import RetrievePaymentEntities
from .retrieve_payroll_entities import RetrievePayrollEntities
from .retrieve_reference_entities import RetrieveReferenceEntities
from .retrieve_system_entities import RetrieveSystemEntities
from .route_to_human import RouteToHuman

ALL_TOOLS_INTERFACE_5 = [
    HandleApplicationOperations,
    HandleBenefitEnrollmentOperations,
    HandleBenefitPlanOperations,
    HandleCandidateOperations,
    HandleDepartmentOperations,
    HandleDocumentOperations,
    HandleEmployeeExitOperations,
    HandleEmployeeOperations,
    HandleInterviewOperations,
    HandleItProvisioningOperations,
    HandleJobOperations,
    HandleLocationOperations,
    HandleNotificationOperations,
    HandleOfferOperations,
    HandleOnboardingOperations,
    HandlePaymentOperations,
    HandlePayrollCycleOperations,
    HandlePayrollEarningOperations,
    HandlePayrollInputOperations,
    HandlePayslipOperations,
    HandleUserOperations,
    OpenAuditEntry,
    RetrieveBenefitEntities,
    RetrieveCandidateEntities,
    RetrieveDocumentTaskEntities,
    RetrieveEmployeeEntities,
    RetrieveInterviewOfferEntities,
    RetrieveJobEntities,
    RetrievePaymentEntities,
    RetrievePayrollEntities,
    RetrieveReferenceEntities,
    RetrieveSystemEntities,
    RouteToHuman
]
