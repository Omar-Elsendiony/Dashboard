from .find_clients import FindClients
from .find_vendors import FindVendors
from .find_users import FindUsers
from .find_products import FindProducts
from .find_components import FindComponents
from .find_subscription_agreements import FindSubscriptionAgreements
from .find_escalation_entities import FindEscalations
from .find_incident_entities import FindIncidentEntities
from .find_workaround_entities import FindWorkaroundEntities
from .find_root_cause_analysis_entities import FindRootCauseAnalysisEntities
from .find_change_entities import FindChangeEntities
from .find_metrics_entities import FindMetricsEntities
from .find_knowledge_article_entities import FindKnowledgeArticleEntities

from .handle_clients import HandleClients
from .handle_vendors import HandleVendors
from .handle_users import HandleUsers
from .handle_products import HandleProducts
from .handle_components import HandleComponents
from .handle_client_subscriptions import HandleClientSubscriptions
from .handle_sla_agreements import HandleSlaAgreements
from .handle_incidents import HandleIncidents
from .add_audit_records import AddAuditRecords
from .handle_work_arounds import HandleWorkArounds
from .handle_root_cause_analysis import HandleRootCauseAnalysis
from .handle_communications import HandleCommunications
from .handle_escalations import HandleEscalations
from .handle_change_requests import HandleChangeRequests
from .handle_rollback_requests import HandleRollbackRequests
from .handle_metrics import HandleMetrics
from .handle_incident_reports import HandleIncidentReports
from .handle_kb_articles import HandleKbArticles
from .handle_post_incident_reviews import HandlePostIncidentReviews

from .assign_to_human import AssignToHuman

ALL_TOOLS_INTERFACE_2 = [
    FindClients,
    FindVendors,
    FindUsers,
    FindProducts,
    FindComponents,
    FindSubscriptionAgreements,
    FindEscalations,
    FindIncidentEntities,
    FindWorkaroundEntities,
    FindRootCauseAnalysisEntities,
    FindChangeEntities,
    FindMetricsEntities,
    FindKnowledgeArticleEntities,
    HandleClients,
    HandleVendors,
    HandleUsers,
    HandleProducts,
    HandleComponents,
    HandleClientSubscriptions,
    HandleSlaAgreements,
    HandleIncidents,
    AddAuditRecords,
    HandleWorkArounds,
    HandleRootCauseAnalysis,
    HandleCommunications,
    HandleEscalations,
    HandleChangeRequests,
    HandleRollbackRequests,
    HandleMetrics,
    HandleIncidentReports,
    HandleKbArticles,
    HandlePostIncidentReviews,
    AssignToHuman,
]
