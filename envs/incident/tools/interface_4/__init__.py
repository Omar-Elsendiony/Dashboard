#interface_4/__init__.py

from .list_change_requests import ListChangeRequests
from .list_rollback_requests import ListRollbackRequests
from .list_workarounds import ListWorkarounds
from .list_root_cause_analyses import ListRootCauseAnalyses
from .list_communications import ListCommunications
from .list_incidents import ListIncidents
from .list_users import ListUsers
from .list_components import ListComponents
from .list_post_incident_reviews import ListPostIncidentReviews
from .list_incident_reports import ListIncidentReports
from .list_knowledge_base_articles import ListKnowledgeBaseArticles

from .create_change_request import CreateChangeRequest
from .update_change_request import UpdateChangeRequest
from .create_rollback_request import CreateRollbackRequest
from .update_rollback_request import UpdateRollbackRequest
from .create_workaround import CreateWorkaround
from .update_workaround import UpdateWorkaround
from .create_root_cause_analysis import CreateRootCauseAnalysis
from .update_root_cause_analysis import UpdateRootCauseAnalysis
from .create_communication import CreateCommunication
from .update_communication import UpdateCommunication
from .create_post_incident_review import CreatePostIncidentReview


ALL_TOOLS_INTERFACE_4 = [
    # GET
    ListChangeRequests,
    ListRollbackRequests,
    ListWorkarounds,
    ListRootCauseAnalyses,
    ListCommunications,
    ListIncidents,
    ListUsers,
    ListComponents,
    ListPostIncidentReviews,
    ListIncidentReports,
    ListKnowledgeBaseArticles,
    # SET
    CreateChangeRequest,
    UpdateChangeRequest,
    CreateRollbackRequest,
    UpdateRollbackRequest,
    CreateWorkaround,
    UpdateWorkaround,
    CreateRootCauseAnalysis,
    UpdateRootCauseAnalysis,
    CreateCommunication,
    UpdateCommunication,
    CreatePostIncidentReview,
]
