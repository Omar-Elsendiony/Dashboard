from .authenticate_approval import AuthenticateApproval
from .execute_audit_logs import ExecuteAuditLogs
from .execute_benefits_plan import ExecuteBenefitsPlan
from .execute_candidate import ExecuteCandidate
from .execute_department import ExecuteDepartment
from .execute_document_storage import ExecuteDocumentStorage
from .execute_employee import ExecuteEmployee
from .execute_employee_benefits import ExecuteEmployeeBenefits
from .execute_employee_training import ExecuteEmployeeTraining
from .execute_expense_reimbursements import ExecuteExpenseReimbursements
from .execute_interview import ExecuteInterview
from .execute_job_application import ExecuteJobApplication
from .execute_job_position import ExecuteJobPosition
from .execute_job_position_skills import ExecuteJobPositionSkills
from .execute_leave_requests import ExecuteLeaveRequests
from .execute_payroll_deduction import ExecutePayrollDeduction
from .execute_payroll_record import ExecutePayrollRecord
from .execute_performance_review import ExecutePerformanceReview
from .execute_skill import ExecuteSkill
from .execute_training_programs import ExecuteTrainingPrograms
from .execute_user import ExecuteUser
from .retrieve_benefits_entities import RetrieveBenefitsEntities
from .retrieve_department_entities import RetrieveDepartmentEntities
from .retrieve_document_entities import RetrieveDocumentEntities
# from .retrieve_employee_entities import RetrieveEmployeeEntities
from .retrieve_expense_entities import RetrieveExpenseEntities
from .retrieve_job_entities import RetrieveJobEntities
from .retrieve_leave_entities import RetrieveLeaveEntities
from .retrieve_payroll_entities import RetrievePayrollEntities
from .retrieve_performance_entities import RetrievePerformanceEntities
from .retrieve_recruitment_entities import RetrieveRecruitmentEntities
from .retrieve_timesheet_entities import RetrieveTimesheetEntities
from .retrieve_training_entities import RetrieveTrainingEntities
# from .retrieve_user_entities import RetrieveUserEntities
from .route_to_human import RouteToHuman
from .retrieve_user_employee_entities import RetrieveUserEmployeeEntities
from .execute_timesheet_entries import ExecuteTimesheetEntries

ALL_TOOLS_INTERFACE_5 = [
    AuthenticateApproval,
    ExecuteAuditLogs,
    ExecuteBenefitsPlan,
    ExecuteCandidate,
    ExecuteDepartment,
    ExecuteDocumentStorage,
    ExecuteEmployee,
    ExecuteEmployeeBenefits,
    ExecuteEmployeeTraining,
    ExecuteExpenseReimbursements,
    ExecuteInterview,
    ExecuteJobApplication,
    ExecuteJobPosition,
    ExecuteJobPositionSkills,
    ExecuteLeaveRequests,
    ExecutePayrollDeduction,
    ExecutePayrollRecord,
    ExecutePerformanceReview,
    ExecuteSkill,
    ExecuteTrainingPrograms,
    ExecuteUser,
    RetrieveBenefitsEntities,
    RetrieveDepartmentEntities,
    RetrieveDocumentEntities,
    # RetrieveEmployeeEntities,
    RetrieveExpenseEntities,
    RetrieveJobEntities,
    RetrieveLeaveEntities,
    RetrievePayrollEntities,
    RetrievePerformanceEntities,
    RetrieveRecruitmentEntities,
    RetrieveTimesheetEntities,
    RetrieveTrainingEntities,
    # RetrieveUserEntities,
    RouteToHuman,
    RetrieveUserEmployeeEntities,
    ExecuteTimesheetEntries,
]
