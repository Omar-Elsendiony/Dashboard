from .escalate_to_human import EscalateToHuman
from .find_benefits_entities import FindBenefitsEntities
from .find_department_entities import FindDepartmentEntities
from .find_document_entities import FindDocumentEntities
# from .find_employee_entities import FindEmployeeEntities
from .find_expense_entities import FindExpenseEntities
from .find_job_entities import FindJobEntities
from .find_leave_entities import FindLeaveEntities
from .find_payroll_entities import FindPayrollEntities
from .find_performance_entities import FindPerformanceEntities
from .find_recruitment_entities import FindRecruitmentEntities
from .find_timesheet_entities import FindTimesheetEntities
from .find_training_entities import FindTrainingEntities
# from .find_user_entities import FindUserEntities
from .process_audit_logs import ProcessAuditLogs
from .process_benefits_plan import ProcessBenefitsPlan
from .process_candidate import ProcessCandidate
from .process_department import ProcessDepartment
from .process_document_storage import ProcessDocumentStorage
from .process_employee import ProcessEmployee
from .process_employee_benefits import ProcessEmployeeBenefits
from .process_employee_training import ProcessEmployeeTraining
from .process_expense_reimbursements import ProcessExpenseReimbursements
from .process_interview import ProcessInterview
from .process_job_application import ProcessJobApplication
from .process_job_position import ProcessJobPosition
from .process_job_position_skills import ProcessJobPositionSkills
from .process_leave_requests import ProcessLeaveRequests
from .process_payroll_deduction import ProcessPayrollDeduction
from .process_payroll_record import ProcessPayrollRecord
from .process_performance_review import ProcessPerformanceReview
from .process_skill import ProcessSkill
from .process_training_programs import ProcessTrainingPrograms
from .process_user import ProcessUser
from .verify_approval import VerifyApproval
from .find_user_employee_entities import FindUserEmployeeEntities
from .process_timesheet_entries import ProcessTimesheetEntries

ALL_TOOLS_INTERFACE_3 = [
    EscalateToHuman,
    FindBenefitsEntities,
    FindDepartmentEntities,
    FindDocumentEntities,
    # FindEmployeeEntities,
    FindExpenseEntities,
    FindJobEntities,
    FindLeaveEntities,
    FindPayrollEntities,
    FindPerformanceEntities,
    FindRecruitmentEntities,
    FindTimesheetEntities,
    FindTrainingEntities,
    # FindUserEntities,
    ProcessAuditLogs,
    ProcessBenefitsPlan,
    ProcessCandidate,
    ProcessDepartment,
    ProcessDocumentStorage,
    ProcessEmployee,
    ProcessEmployeeBenefits,
    ProcessEmployeeTraining,
    ProcessExpenseReimbursements,
    ProcessInterview,
    ProcessJobApplication,
    ProcessJobPosition,
    ProcessJobPositionSkills,
    ProcessLeaveRequests,
    ProcessPayrollDeduction,
    ProcessPayrollRecord,
    ProcessPerformanceReview,
    ProcessSkill,
    ProcessTrainingPrograms,
    ProcessUser,
    VerifyApproval,
    FindUserEmployeeEntities,
    ProcessTimesheetEntries,
]
