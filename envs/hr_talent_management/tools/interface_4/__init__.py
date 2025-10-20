from .build_audit_entry import BuildAuditEntry
from .get_benefit_entities import GetBenefitEntities
from .get_candidate_entities import GetCandidateEntities
from .get_document_task_entities import GetDocumentTaskEntities
from .get_employee_entities import GetEmployeeEntities
from .get_interview_offer_entities import GetInterviewOfferEntities
from .get_job_entities import GetJobEntities
from .get_payment_entities import GetPaymentEntities
from .get_payroll_entities import GetPayrollEntities
from .get_reference_entities import GetReferenceEntities
from .get_system_entities import GetSystemEntities
from .handover_to_human import HandOverToHuman
from .process_application_operations import ProcessApplicationOperations
from .process_benefit_enrollment_operations import ProcessBenefitEnrollmentOperations
from .process_benefit_plan_operations import ProcessBenefitPlanOperations
from .process_candidate_operations import ProcessCandidateOperations
from .process_department_operations import ProcessDepartmentOperations
from .process_document_operations import ProcessDocumentOperations
from .process_employee_exit_operations import ProcessEmployeeExitOperations
from .process_employee_operations import ProcessEmployeeOperations
from .process_interview_operations import ProcessInterviewOperations
from .process_it_provisioning_operations import ProcessItProvisioningOperations
from .process_job_operations import ProcessJobOperations
from .process_location_operations import ProcessLocationOperations
from .process_notification_operations import ProcessNotificationOperations
from .process_offer_operations import ProcessOfferOperations
from .process_onboarding_operations import ProcessOnboardingOperations
from .process_payment_operations import ProcessPaymentOperations
from .process_payroll_cycle_operations import ProcessPayrollCycleOperations
from .process_payroll_earning_operations import ProcessPayrollEarningOperations
from .process_payroll_input_operations import ProcessPayrollInputOperations
from .process_payslip_operations import ProcessPayslipOperations
from .process_user_operations import ProcessUserOperations

ALL_TOOLS_INTERFACE_4 = [
    BuildAuditEntry,
    GetBenefitEntities,
    GetCandidateEntities,
    GetDocumentTaskEntities,
    GetEmployeeEntities,
    GetInterviewOfferEntities,
    GetJobEntities,
    GetPaymentEntities,
    GetPayrollEntities,
    GetReferenceEntities,
    GetSystemEntities,
    HandOverToHuman,
    ProcessApplicationOperations,
    ProcessBenefitEnrollmentOperations,
    ProcessBenefitPlanOperations,
    ProcessCandidateOperations,
    ProcessDepartmentOperations,
    ProcessDocumentOperations,
    ProcessEmployeeExitOperations,
    ProcessEmployeeOperations,
    ProcessInterviewOperations,
    ProcessItProvisioningOperations,
    ProcessJobOperations,
    ProcessLocationOperations,
    ProcessNotificationOperations,
    ProcessOfferOperations,
    ProcessOnboardingOperations,
    ProcessPaymentOperations,
    ProcessPayrollCycleOperations,
    ProcessPayrollEarningOperations,
    ProcessPayrollInputOperations,
    ProcessPayslipOperations,
    ProcessUserOperations
]
