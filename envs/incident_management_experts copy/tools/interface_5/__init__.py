from .get_clients import DiscoverClients
from .get_vendors import DiscoverVendors
from .get_users import DiscoverUsers
from .get_products import DiscoverProducts
from .get_components import DiscoverComponents
from .get_subscription_agreements import DiscoverSubscriptionAgreements
from .get_change_entities import DiscoverChangeEntities
from .get_incident_entities import DiscoverIncidentEntities
from .get_knowledge_article_entities import DiscoverKnowledgeArticleEntities
from .get_metrics_entities import DiscoverMetricsEntities
from .get_root_cause_analysis_entities import DiscoverRootCauseAnalysisEntities
from .get_workaround_entities import DiscoverWorkaroundEntities

from .process_clients import ManageClients
from .process_vendors import ManageVendors
from .process_users import ManageUsers
from .process_products import ManageProducts
from .process_components import ManageComponents
from .process_client_subscriptions import ManageClientSubscriptions
from .process_sla_agreements import ManageSlaAgreements
from .process_change_requests import ManageChangeRequests
from .process_communications import ManageCommunications
from .process_escalations import ManageEscalations
from .process_incident_reports import ManageIncidentReports
from .process_kb_articles import ManageKbArticles
from .process_metrics import ManageMetrics
from .process_post_incident_reviews import ManagePostIncidentReviews
from .process_rollback_requests import ManageRollbackRequests
from .capture_audit_records import LogAuditRecords
from .process_incidents import ManageIncidents
from .process_root_cause_analysis import ManageRootCauseAnalysis
from .process_work_arounds import ManageWorkArounds

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
