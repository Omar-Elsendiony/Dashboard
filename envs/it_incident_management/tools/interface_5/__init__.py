# interface_5/__init__.py

from .list_metrics import ListMetrics
from .list_incident_reports import ListIncidentReports
from .list_knowledge_base_articles import ListKnowledgeBaseArticles
from .list_post_incident_reviews import ListPostIncidentReviews
from .list_incidents import ListIncidents
from .list_users import ListUsers
from .list_clients import ListClients
from .list_vendors import ListVendors
from .list_root_cause_analyses import ListRootCauseAnalyses
from .list_change_requests import ListChangeRequests
from .list_workarounds import ListWorkarounds
from .list_components import ListComponents
from .list_products import ListProducts
from .list_sla_agreements import ListSlaAgreements

from .log_metric import LogMetric
from .revise_metric import ReviseMetric
from .log_incident_report import LogIncidentReport
from .revise_incident_report import ReviseIncidentReport
from .log_knowledge_base_article import LogKnowledgeBaseArticle
from .revise_knowledge_base_article import ReviseKnowledgeBaseArticle
from .log_post_incident_review import LogPostIncidentReview
from .revise_post_incident_review import RevisePostIncidentReview
from .log_communication import LogCommunication
from .log_root_cause_analysis import LogRootCauseAnalysis
from .log_workaround import LogWorkaround
from .add_incident import AddIncident
from .revise_incident import ReviseIncident
from .log_incident_update_record import LogIncidentUpdateRecord


ALL_TOOLS_INTERFACE_5 = [
    # GET
    ListMetrics,
    ListIncidentReports,
    ListKnowledgeBaseArticles,
    ListPostIncidentReviews,
    ListIncidents,
    ListUsers,
    ListClients,
    ListVendors,
    ListRootCauseAnalyses,
    ListChangeRequests,
    ListWorkarounds,
    ListComponents,
    ListProducts,
    ListSlaAgreements,
    # SET
    LogMetric,
    ReviseMetric,
    LogIncidentReport,
    ReviseIncidentReport,
    LogKnowledgeBaseArticle,
    ReviseKnowledgeBaseArticle,
    LogPostIncidentReview,
    RevisePostIncidentReview,
    LogCommunication,
    LogRootCauseAnalysis,
    LogWorkaround,
    AddIncident,
    ReviseIncident,
    LogIncidentUpdateRecord
]
