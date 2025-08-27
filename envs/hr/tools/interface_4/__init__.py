from .query_performance_reviews import QueryPerformanceReviews
from .query_training_programs import QueryTrainingPrograms
from .query_employee_training import QueryEmployeeTraining
from .query_employees import QueryEmployees
from .query_users import QueryUsers
from .query_departments import QueryDepartments
from .query_audit_logs import QueryAuditLogs
from .query_documents import QueryDocuments
from .query_job_positions import QueryJobPositions
from .query_skills import QuerySkills
from .query_training_completion_report import QueryTrainingCompletionReport
from .create_performance_review import CreatePerformanceReview
from .update_performance_review import UpdatePerformanceReview
from .create_training_program import CreateTrainingProgram
from .update_training_program import UpdateTrainingProgram
from .enroll_employee_training import EnrollEmployeeTraining
from .complete_employee_training import CompleteEmployeeTraining
from .map_skill_to_position import MapSkillToPosition
from .add_document import AddDocument
from .edit_document import EditDocument
from .register_audit_entry import RegisterAuditEntry
from .update_employee_profile import UpdateEmployeeProfile

ALL_TOOLS_INTERFACE_4 = [
    QueryPerformanceReviews,
    QueryTrainingPrograms,
    QueryEmployeeTraining,
    QueryEmployees,
    QueryUsers,
    QueryDepartments,
    QueryAuditLogs,
    QueryDocuments,
    QueryJobPositions,
    QuerySkills,
    QueryTrainingCompletionReport,
    CreatePerformanceReview,
    UpdatePerformanceReview,
    CreateTrainingProgram,
    UpdateTrainingProgram,
    EnrollEmployeeTraining,
    CompleteEmployeeTraining,
    MapSkillToPosition,
    AddDocument,
    EditDocument,
    RegisterAuditEntry,
    UpdateEmployeeProfile,
]
