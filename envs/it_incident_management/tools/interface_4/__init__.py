# interface_4/__init__.py

from .query_change_requests import QueryChangeRequests
from .query_rollback_requests import QueryRollbackRequests
from .query_workarounds import QueryWorkarounds
from .query_root_cause_analyses import QueryRootCauseAnalyses
from .query_communications import QueryCommunications
from .query_incidents import QueryIncidents
from .query_users import QueryUsers
from .query_components import QueryComponents
from .query_post_incident_reviews import QueryPostIncidentReviews
from .query_incident_reports import QueryIncidentReports
from .query_knowledge_base_articles import QueryKnowledgeBaseArticles
from .query_products import QueryProducts
from .query_sla_agreements import QuerySlaAgreements

from .record_change_request import RecordChangeRequest
from .edit_change_request import EditChangeRequest
from .record_rollback_request import RecordRollbackRequest
from .edit_rollback_request import EditRollbackRequest
from .record_workaround import RecordWorkaround
from .edit_workaround import EditWorkaround
from .record_root_cause_analysis import RecordRootCauseAnalysis
from .edit_root_cause_analysis import EditRootCauseAnalysis
from .record_communication import RecordCommunication
from .edit_communication import EditCommunication
from .record_post_incident_review import RecordPostIncidentReview
from .create_incident import CreateIncident
from .record_incident_update_record import RecordIncidentUpdateRecord
from .edit_incident import EditIncident
from .query_client_subscriptions import QueryClientSubscriptions
ALL_TOOLS_INTERFACE_4 = [
    # GET
    QueryChangeRequests,
    QueryRollbackRequests,
    QueryWorkarounds,
    QueryRootCauseAnalyses,
    QueryCommunications,
    QueryIncidents,
    QueryUsers,
    QueryComponents,
    QueryPostIncidentReviews,
    QueryIncidentReports,
    QueryKnowledgeBaseArticles,
    QueryProducts,
    QuerySlaAgreements,
    # SET
    RecordChangeRequest,
    EditChangeRequest,
    RecordRollbackRequest,
    EditRollbackRequest,
    RecordWorkaround,
    EditWorkaround,
    RecordRootCauseAnalysis,
    EditRootCauseAnalysis,
    RecordCommunication,
    EditCommunication,
    RecordPostIncidentReview,
    CreateIncident,
    RecordIncidentUpdateRecord,
    EditIncident,
    QueryClientSubscriptions
]
