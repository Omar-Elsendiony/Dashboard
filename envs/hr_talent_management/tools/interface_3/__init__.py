from .escalate_to_human import EscalateToHuman
from .execute_application_operations import ExecuteApplicationOperations
from .execute_benefit_enrollment_operations import ExecuteBenefitEnrollmentOperations
from .execute_benefit_plan_operations import ExecuteBenefitPlanOperations
from .execute_candidate_operations import ExecuteCandidateOperations
from .execute_department_operations import ExecuteDepartmentOperations
from .execute_document_operations import ExecuteDocumentOperations
from .execute_employee_exit_operations import ExecuteEmployeeExitOperations
from .execute_employee_operations import ExecuteEmployeeOperations
from .execute_interview_operations import ExecuteInterviewOperations
from .execute_it_provisioning_operations import ExecuteItProvisioningOperations
from .execute_job_operations import ExecuteJobOperations
from .execute_location_operations import ExecuteLocationOperations
from .execute_notification_operations import ExecuteNotificationOperations
from .execute_offer_operations import ExecuteOfferOperations
from .execute_onboarding_operations import ExecuteOnboardingOperations
from .execute_payment_operations import ExecutePaymentOperations
from .execute_payroll_cycle_operations import ExecutePayrollCycleOperations
from .execute_payroll_earning_operations import ExecutePayrollEarningOperations
from .execute_payroll_input_operations import ExecutePayrollInputOperations
from .execute_payslip_operations import ExecutePayslipOperations
from .execute_user_operations import ExecuteUserOperations
from .lookup_benefit_entities import LookupBenefitEntities
from .lookup_candidate_entities import LookupCandidateEntities
from .lookup_document_task_entities import LookupDocumentTaskEntities
from .lookup_employee_entities import LookupEmployeeEntities
from .lookup_interview_offer_entities import LookupInterviewOfferEntities
from .lookup_job_entities import LookupJobEntities
from .lookup_payment_entities import LookupPaymentEntities
from .lookup_payroll_entities import LookupPayrollEntities
from .lookup_reference_entities import LookupReferenceEntities
from .lookup_system_entities import LookupSystemEntities
from .make_audit_entry import MakeAuditEntry

ALL_TOOLS_INTERFACE_3 = [
    EscalateToHuman,
    ExecuteApplicationOperations,
    ExecuteBenefitEnrollmentOperations,
    ExecuteBenefitPlanOperations,
    ExecuteCandidateOperations,
    ExecuteDepartmentOperations,
    ExecuteDocumentOperations,
    ExecuteEmployeeExitOperations,
    ExecuteEmployeeOperations,
    ExecuteInterviewOperations,
    ExecuteItProvisioningOperations,
    ExecuteJobOperations,
    ExecuteLocationOperations,
    ExecuteNotificationOperations,
    ExecuteOfferOperations,
    ExecuteOnboardingOperations,
    ExecutePaymentOperations,
    ExecutePayrollCycleOperations,
    ExecutePayrollEarningOperations,
    ExecutePayrollInputOperations,
    ExecutePayslipOperations,
    ExecuteUserOperations,
    LookupBenefitEntities,
    LookupCandidateEntities,
    LookupDocumentTaskEntities,
    LookupEmployeeEntities,
    LookupInterviewOfferEntities,
    LookupJobEntities,
    LookupPaymentEntities,
    LookupPayrollEntities,
    LookupReferenceEntities,
    LookupSystemEntities,
    MakeAuditEntry
]
