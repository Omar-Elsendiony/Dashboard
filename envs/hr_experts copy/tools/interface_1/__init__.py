from .check_approval import CheckApproval
from .discover_benefits_entities import DiscoverBenefitsEntities
from .discover_department_entities import DiscoverDepartmentEntities
from .discover_document_entities import DiscoverDocumentEntities
# from .discover_employee_entities import DiscoverEmployeeEntities
from .discover_expense_entities import DiscoverExpenseEntities
from .discover_job_entities import DiscoverJobEntities
from .discover_leave_entities import DiscoverLeaveEntities
from .discover_payroll_entities import DiscoverPayrollEntities
from .discover_performance_entities import DiscoverPerformanceEntities
from .discover_recruitment_entities import DiscoverRecruitmentEntities
from .discover_timesheet_entities import DiscoverTimesheetEntities
from .discover_training_entities import DiscoverTrainingEntities
# from .discover_user_entities import DiscoverUserEntities
from .manage_audit_logs import ManageAuditLogs
from .manage_benefits_plan import ManageBenefitsPlan
from .manage_candidate import ManageCandidate
from .manage_department import ManageDepartment
from .manage_document_storage import ManageDocumentStorage
from .manage_employee import ManageEmployee
from .manage_employee_benefits import ManageEmployeeBenefits
from .manage_employee_training import ManageEmployeeTraining
from .manage_expense_reimbursements import ManageExpenseReimbursements
from .manage_interview import ManageInterview
from .manage_job_application import ManageJobApplication
from .manage_job_position import ManageJobPosition
from .manage_job_position_skills import ManageJobPositionSkills
from .manage_leave_requests import ManageLeaveRequests
from .manage_payroll_deduction import ManagePayrollDeduction
from .manage_payroll_record import ManagePayrollRecord
from .manage_performance_review import ManagePerformanceReview
from .manage_skill import ManageSkill
from .manage_training_programs import ManageTrainingPrograms
from .manage_user import ManageUser
from .transfer_to_human import TransferToHuman
from .discover_user_employee_entities import DiscoverUserEmployeeEntities
from .manage_timesheet_entries import ManageTimesheetEntries

ALL_TOOLS_INTERFACE_1 = [
    CheckApproval,
    DiscoverBenefitsEntities,
    DiscoverDepartmentEntities,
    DiscoverDocumentEntities,
    # DiscoverEmployeeEntities,
    DiscoverExpenseEntities,
    DiscoverJobEntities,
    DiscoverLeaveEntities,
    DiscoverPayrollEntities,
    DiscoverPerformanceEntities,
    DiscoverRecruitmentEntities,
    DiscoverTimesheetEntities,
    DiscoverTrainingEntities,
    # DiscoverUserEntities,
    ManageAuditLogs,
    ManageBenefitsPlan,
    ManageCandidate,
    ManageDepartment,
    ManageDocumentStorage,
    ManageEmployee,
    ManageEmployeeBenefits,
    ManageEmployeeTraining,
    ManageExpenseReimbursements,
    ManageInterview,
    ManageJobApplication,
    ManageJobPosition,
    ManageJobPositionSkills,
    ManageLeaveRequests,
    ManagePayrollDeduction,
    ManagePayrollRecord,
    ManagePerformanceReview,
    ManageSkill,
    ManageTrainingPrograms,
    ManageUser,
    TransferToHuman,
    DiscoverUserEmployeeEntities,
    ManageTimesheetEntries,
]

