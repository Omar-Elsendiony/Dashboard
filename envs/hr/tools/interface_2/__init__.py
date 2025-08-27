from .bulk_update_employee_status import BulkUpdateEmployeeStatus
from .create_audit_log import CreateAuditLog
from .create_department import CreateDepartment
from .create_user import CreateUser
from .get_audit_logs import GetAuditLogs
from .get_departments import GetDepartments
from .get_documents import GetDocuments
from .get_employee_benefits import GetEmployeeBenefits
from .get_employee_training import GetEmployeeTraining
from .get_employees import GetEmployees
from .get_job_position_skills import GetJobPositionSkills
from .get_job_positions import GetJobPositions
from .get_payroll_records import GetPayrollRecords
from .get_skills import GetSkills
from .get_users import GetUsers
from .offboard_employee import OffboardEmployee
from .onboard_employee import OnboardEmployee
from .update_department import UpdateDepartment
from .update_document import UpdateDocument
from .update_employee_profile import UpdateEmployeeProfile
from .update_job_position import UpdateJobPosition
from .update_user import UpdateUser
from .upload_document import UploadDocument

ALL_TOOLS_INTERFACE_2 = [
    BulkUpdateEmployeeStatus,
    CreateAuditLog,
    CreateDepartment,
    CreateUser,
    GetAuditLogs,
    GetDepartments,
    GetDocuments,
    GetEmployeeBenefits,
    GetEmployeeTraining,
    GetEmployees,
    GetJobPositionSkills,
    GetJobPositions,
    GetPayrollRecords,
    GetSkills,
    GetUsers,
    OffboardEmployee,
    OnboardEmployee,
    UpdateDepartment,
    UpdateDocument,
    UpdateEmployeeProfile,
    UpdateJobPosition,
    UpdateUser,
    UploadDocument
]
