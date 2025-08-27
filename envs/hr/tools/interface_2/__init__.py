from .fetch_users import FetchUsers
from .fetch_employees import FetchEmployees
from .fetch_departments import FetchDepartments
from .fetch_job_positions import FetchJobPositions
from .fetch_documents import FetchDocuments
from .fetch_audit_logs import FetchAuditLogs
from .fetch_payroll_records import FetchPayrollRecords
from .fetch_employee_benefits import FetchEmployeeBenefits
from .fetch_employee_training import FetchEmployeeTraining
from .fetch_job_position_skills import FetchJobPositionSkills
from .fetch_skills import FetchSkills
from .create_user import CreateUser
from .update_user import UpdateUser
from .onboard_employee import OnboardEmployee
from .update_employee_profile import UpdateEmployeeProfile
from .create_department import CreateDepartment
from .update_department import UpdateDepartment
from .update_job_position import UpdateJobPosition
from .submit_document import SubmitDocument
from .modify_document import ModifyDocument
from .log_audit_entry import LogAuditEntry
from .offboard_employee import OffboardEmployee
from .bulk_update_employee_status import BulkUpdateEmployeeStatus
from .approval_lookup import ApprovalLookup
ALL_TOOLS_INTERFACE_2 = [
    FetchUsers,
    FetchEmployees,
    FetchDepartments,
    FetchJobPositions,
    FetchDocuments,
    FetchAuditLogs,
    FetchPayrollRecords,
    FetchEmployeeBenefits,
    FetchEmployeeTraining,
    FetchJobPositionSkills,
    FetchSkills,
    CreateUser,
    UpdateUser,
    OnboardEmployee,
    UpdateEmployeeProfile,
    CreateDepartment,
    UpdateDepartment,
    UpdateJobPosition,
    SubmitDocument,
    ModifyDocument,
    LogAuditEntry,
    OffboardEmployee,
    BulkUpdateEmployeeStatus,
    ApprovalLookup
]
