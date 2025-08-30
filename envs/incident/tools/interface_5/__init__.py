#interface_5/__init__.py

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

from .create_metric import CreateMetric
from .update_metric import UpdateMetric
from .create_incident_report import CreateIncidentReport
from .update_incident_report import UpdateIncidentReport
from .create_knowledge_base_article import CreateKnowledgeBaseArticle
from .update_knowledge_base_article import UpdateKnowledgeBaseArticle
from .create_post_incident_review import CreatePostIncidentReview
from .update_post_incident_review import UpdatePostIncidentReview
from .create_communication import CreateCommunication
from .create_root_cause_analysis import CreateRootCauseAnalysis
from .create_workaround import CreateWorkaround


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
    # SET
    CreateMetric,
    UpdateMetric,
    CreateIncidentReport,
    UpdateIncidentReport,
    CreateKnowledgeBaseArticle,
    UpdateKnowledgeBaseArticle,
    CreatePostIncidentReview,
    UpdatePostIncidentReview,
    CreateCommunication,
    CreateRootCauseAnalysis,
    CreateWorkaround,
]
