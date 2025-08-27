from .assign_skill_to_position import AssignSkillToPosition
from .close_job_opening import CloseJobOpening
from .create_audit_log import CreateAuditLog
from .create_candidate import CreateCandidate
from .create_job_application import CreateJobApplication
from .create_job_position import CreateJobPosition
from .get_audit_logs import GetAuditLogs
from .get_candidates import GetCandidates
from .get_department_summary_report import GetDepartmentSummaryReport
from .get_departments import GetDepartments
from .get_documents import GetDocuments
from .get_interviews import GetInterviews
from .get_job_applications import GetJobApplications
from .get_job_position_skills import GetJobPositionSkills
from .get_job_positions import GetJobPositions
from .get_skills import GetSkills
from .get_users import GetUsers
from .post_job_opening import PostJobOpening
from .record_interview_outcome import RecordInterviewOutcome
from .schedule_interview import ScheduleInterview
from .update_application_stage import UpdateApplicationStage
from .update_job_position import UpdateJobPosition
from .upload_document import UploadDocument

ALL_TOOLS_INTERFACE_1 = [
    AssignSkillToPosition,
    CloseJobOpening,
    CreateAuditLog,
    CreateCandidate,
    CreateJobApplication,
    CreateJobPosition,
    GetAuditLogs,
    GetCandidates,
    GetDepartmentSummaryReport,
    GetDepartments,
    GetDocuments,
    GetInterviews,
    GetJobApplications,
    GetJobPositionSkills,
    GetJobPositions,
    GetSkills,
    GetUsers,
    PostJobOpening,
    RecordInterviewOutcome,
    ScheduleInterview,
    UpdateApplicationStage,
    UpdateJobPosition,
    UploadDocument
]
