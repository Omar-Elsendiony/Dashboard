from .handle_audit_logs import HandleAuditLogs
from .handle_benefits_plan import HandleBenefitsPlan
from .handle_candidate import HandleCandidate
from .handle_department import HandleDepartment
from .handle_document_storage import HandleDocumentStorage
from .handle_employee import HandleEmployee
from .handle_employee_benefits import HandleEmployeeBenefits
from .handle_employee_training import HandleEmployeeTraining
from .handle_expense_reimbursements import HandleExpenseReimbursements
from .handle_interview import HandleInterview
from .handle_job_application import HandleJobApplication
from .handle_job_position import HandleJobPosition
from .handle_job_position_skills import HandleJobPositionSkills
from .handle_leave_requests import HandleLeaveRequests
from .handle_payroll_deduction import HandlePayrollDeduction
from .handle_payroll_record import HandlePayrollRecord
from .handle_performance_review import HandlePerformanceReview
from .handle_skill import HandleSkill
from .handle_training_programs import HandleTrainingPrograms
from .handle_user import HandleUser
from .search_benefits_entities import SearchBenefitsEntities
from .search_department_entities import SearchDepartmentEntities
from .search_document_entities import SearchDocumentEntities
# from .search_employee_entities import SearchEmployeeEntities
from .search_expense_entities import SearchExpenseEntities
from .search_job_entities import SearchJobEntities
from .search_leave_entities import SearchLeaveEntities
from .search_payroll_entities import SearchPayrollEntities
from .search_performance_entities import SearchPerformanceEntities
from .search_recruitment_entities import SearchRecruitmentEntities
from .search_timesheet_entities import SearchTimesheetEntities
from .search_training_entities import SearchTrainingEntities
# from .search_user_entities import SearchUserEntities
from .switch_to_human import SwitchToHuman
from .validate_approval import ValidateApproval
from .search_user_employee_entities import SearchUserEmployeeEntities
from .handle_timesheet_entries import HandleTimesheetEntries

ALL_TOOLS_INTERFACE_2 = [
    HandleAuditLogs,
    HandleBenefitsPlan,
    HandleCandidate,
    HandleDepartment,
    HandleDocumentStorage,
    HandleEmployee,
    HandleEmployeeBenefits,
    HandleEmployeeTraining,
    HandleExpenseReimbursements,
    HandleInterview,
    HandleJobApplication,
    HandleJobPosition,
    HandleJobPositionSkills,
    HandleLeaveRequests,
    HandlePayrollDeduction,
    HandlePayrollRecord,
    HandlePerformanceReview,
    HandleSkill,
    HandleTrainingPrograms,
    HandleUser,
    SearchBenefitsEntities,
    SearchDepartmentEntities,
    SearchDocumentEntities,
    # SearchEmployeeEntities,
    SearchExpenseEntities,
    SearchJobEntities,
    SearchLeaveEntities,
    SearchPayrollEntities,
    SearchPerformanceEntities,
    SearchRecruitmentEntities,
    SearchTimesheetEntities,
    SearchTrainingEntities,
    # SearchUserEntities,
    ValidateApproval,
    SwitchToHuman,
    SearchUserEmployeeEntities,
    HandleTimesheetEntries,
]
