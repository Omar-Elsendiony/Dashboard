from .administer_audit_logs import AdministerAuditLogs
from .administer_benefits_plan import AdministerBenefitsPlan
from .administer_candidate import AdministerCandidate
from .administer_department import AdministerDepartment
from .administer_document_storage import AdministerDocumentStorage
from .administer_employee import AdministerEmployee
from .administer_employee_benefits import AdministerEmployeeBenefits
from .administer_employee_training import AdministerEmployeeTraining
from .administer_expense_reimbursements import AdministerExpenseReimbursements
from .administer_interview import AdministerInterview
from .administer_job_application import AdministerJobApplication
from .administer_job_position import AdministerJobPosition
from .administer_job_position_skills import AdministerJobPositionSkills
from .administer_leave_requests import AdministerLeaveRequests
from .administer_payroll_deduction import AdministerPayrollDeduction
from .administer_payroll_record import AdministerPayrollRecord
from .administer_performance_review import AdministerPerformanceReview
from .administer_skill import AdministerSkill
from .administer_training_programs import AdministerTrainingPrograms
from .administer_user import AdministerUser
from .confirm_approval import ConfirmApproval
from .handover_to_human import HandOverToHuman
from .lookup_benefits_entities import LookupBenefitsEntities
from .lookup_department_entities import LookupDepartmentEntities
from .lookup_document_entities import LookupDocumentEntities
# from .lookup_employee_entities import LookupEmployeeEntities
from .lookup_expense_entities import LookupExpenseEntities
from .lookup_job_entities import LookupJobEntities
from .lookup_leave_entities import LookupLeaveEntities
from .lookup_payroll_entities import LookupPayrollEntities
from .lookup_performance_entities import LookupPerformanceEntities
from .lookup_recruitment_entities import LookupRecruitmentEntities
from .lookup_timesheet_entities import LookupTimesheetEntities
from .lookup_training_entities import LookupTrainingEntities
# from .lookup_user_entities import LookupUserEntities
from .lookup_user_employee_entities import LookupUserEmployeeEntities
from .administer_timesheet_entries import AdministerTimesheetEntries

ALL_TOOLS_INTERFACE_4 = [
    AdministerAuditLogs,
    AdministerBenefitsPlan,
    AdministerCandidate,
    AdministerDepartment,
    AdministerDocumentStorage,
    AdministerEmployee,
    AdministerEmployeeBenefits,
    AdministerEmployeeTraining,
    AdministerExpenseReimbursements,
    AdministerInterview,
    AdministerJobApplication,
    AdministerJobPosition,
    AdministerJobPositionSkills,
    AdministerLeaveRequests,
    AdministerPayrollDeduction,
    AdministerPayrollRecord,
    AdministerPerformanceReview,
    AdministerSkill,
    AdministerTrainingPrograms,
    AdministerUser,
    ConfirmApproval,
    HandOverToHuman,
    LookupBenefitsEntities,
    LookupDepartmentEntities,
    LookupDocumentEntities,
    # LookupEmployeeEntities,
    LookupExpenseEntities,
    LookupJobEntities,
    LookupLeaveEntities,
    LookupPayrollEntities,
    LookupPerformanceEntities,
    LookupRecruitmentEntities,
    LookupTimesheetEntities,
    LookupTrainingEntities,
    # LookupUserEntities,
    LookupUserEmployeeEntities,
    AdministerTimesheetEntries,
]
