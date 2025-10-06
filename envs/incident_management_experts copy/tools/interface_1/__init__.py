from .discover_clients import DiscoverClients
from .discover_vendors import DiscoverVendors
from .discover_users import DiscoverUsers
from .discover_products import DiscoverProducts
from .discover_components import DiscoverComponents
from .discover_subscription_agreements import DiscoverSubscriptionAgreements
from .discover_change_entities import DiscoverChangeEntities
from .discover_incident_entities import DiscoverIncidentEntities
from .discover_knowledge_article_entities import DiscoverKnowledgeArticleEntities
from .discover_metrics_entities import DiscoverMetricsEntities
from .discover_root_cause_analysis_entities import DiscoverRootCauseAnalysisEntities
from .discover_workaround_entities import DiscoverWorkaroundEntities

from .manage_clients import ManageClients
from .manage_vendors import ManageVendors
from .manage_users import ManageUsers
from .manage_products import ManageProducts
from .manage_components import ManageComponents
from .manage_client_subscriptions import ManageClientSubscriptions
from .manage_sla_agreements import ManageSlaAgreements
from .manage_change_requests import ManageChangeRequests
from .manage_communications import ManageCommunications
from .manage_escalations import ManageEscalations
from .manage_incident_reports import ManageIncidentReports
from .manage_kb_articles import ManageKbArticles
from .manage_metrics import ManageMetrics
from .manage_post_incident_reviews import ManagePostIncidentReviews
from .manage_rollback_requests import ManageRollbackRequests
from .log_audit_records import LogAuditRecords
from .manage_incidents import ManageIncidents
from .manage_root_cause_analysis import ManageRootCauseAnalysis
from .manage_work_arounds import ManageWorkArounds

ALL_TOOLS_INTERFACE_1 = [
    DiscoverClients,
    DiscoverVendors,
    DiscoverUsers,
    DiscoverProducts,
    DiscoverComponents,
    DiscoverSubscriptionAgreements,
    DiscoverChangeEntities,
    DiscoverIncidentEntities,
    DiscoverKnowledgeArticleEntities,
    DiscoverMetricsEntities,
    DiscoverRootCauseAnalysisEntities,
    DiscoverWorkaroundEntities,
    ManageClients,
    ManageVendors,
    ManageUsers,
    ManageProducts,
    ManageComponents,
    ManageClientSubscriptions,
    ManageSlaAgreements,
    ManageChangeRequests,
    ManageCommunications,
    ManageEscalations,
    ManageIncidentReports,
    ManageKbArticles,
    ManageMetrics,
    ManagePostIncidentReviews,
    ManageRollbackRequests,
    LogAuditRecords,
    ManageIncidents,
    ManageRootCauseAnalysis,
    ManageWorkArounds,
]
