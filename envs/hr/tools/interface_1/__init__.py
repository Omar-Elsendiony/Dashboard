from .get_users import GetUsers
from .get_departments import GetDepartments
from .get_job_positions import GetJobPositions
from .get_job_position_skills import GetJobPositionSkills
from .get_candidates import GetCandidates
from .get_job_applications import GetJobApplications
from .get_interviews import GetInterviews
from .get_documents import GetDocuments
from .get_audit_logs import GetAuditLogs
from .get_skills import GetSkills
from .get_department_summary_report import GetDepartmentSummaryReport
from .create_candidate import CreateCandidate
from .upload_document import UploadDocument
from .create_job_application import CreateJobApplication
from .schedule_interview import ScheduleInterview
from .update_application_stage import UpdateApplicationStage
from .record_interview_outcome import RecordInterviewOutcome
from .create_job_position import CreateJobPosition
from .update_job_position import UpdateJobPosition
from .assign_skill_to_position import AssignSkillToPosition
from .post_job_opening import PostJobOpening
from .close_job_opening import CloseJobOpening
from .create_audit_log import CreateAuditLog

ALL_TOOLS_INTERFACE_1 = [
    GetUsers,
    GetDepartments,
    GetJobPositions,
    GetJobPositionSkills,
    GetCandidates,
    GetJobApplications,
    GetInterviews,
    GetDocuments,
    GetAuditLogs,
    GetSkills,
    GetDepartmentSummaryReport,
    CreateCandidate,
    UploadDocument,
    CreateJobApplication,
    ScheduleInterview,
    UpdateApplicationStage,
    RecordInterviewOutcome,
    CreateJobPosition,
    UpdateJobPosition,
    AssignSkillToPosition,
    PostJobOpening,
    CloseJobOpening,
    CreateAuditLog,
]
