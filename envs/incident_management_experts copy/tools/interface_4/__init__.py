from .register_clients import RegisterClients
from .register_vendors import RegisterVendors
from .register_users import RegisterUsers
from .register_products import RegisterProducts
from .register_components import RegisterComponents
from .register_subscription_agreements import RegisterSubscriptionAgreements
from .register_change_entities import RegisterChangeEntities
from .register_incident_entities import RegisterIncidentEntities
from .register_knowledge_article_entities import RegisterKnowledgeArticleEntities
from .register_metrics_entities import RegisterMetricsEntities
from .register_root_cause_analysis_entities import RegisterRootCauseAnalysisEntities
from .register_workaround_entities import RegisterWorkaroundEntities

from .create_clients import CreateClients
from .create_vendors import CreateVendors
from .create_users import CreateUsers
from .create_products import CreateProducts
from .create_components import CreateComponents
from .create_client_subscriptions import CreateClientSubscriptions
from .create_sla_agreements import CreateSlaAgreements
from .create_change_requests import CreateChangeRequests
from .create_communications import CreateCommunications
from .create_escalations import CreateEscalations
from .create_incident_reports import CreateIncidentReports
from .create_kb_articles import CreateKbArticles
from .create_metrics import CreateMetrics
from .create_post_incident_reviews import CreatePostIncidentReviews
from .create_rollback_requests import CreateRollbackRequests
from .log_audit_records import LogAuditRecords
from .create_incidents import CreateIncidents
from .create_root_cause_analysis import CreateRootCauseAnalysis
from .create_work_arounds import CreateWorkArounds

ALL_TOOLS_INTERFACE_1 = [
    RegisterClients,
    RegisterVendors,
    RegisterUsers,
    RegisterProducts,
    RegisterComponents,
    RegisterSubscriptionAgreements,
    RegisterChangeEntities,
    RegisterIncidentEntities,
    RegisterKnowledgeArticleEntities,
    RegisterMetricsEntities,
    RegisterRootCauseAnalysisEntities,
    RegisterWorkaroundEntities,
    CreateClients,
    CreateVendors,
    CreateUsers,
    CreateProducts,
    CreateComponents,
    CreateClientSubscriptions,
    CreateSlaAgreements,
    CreateChangeRequests,
    CreateCommunications,
    CreateEscalations,
    CreateIncidentReports,
    CreateKbArticles,
    CreateMetrics,
    CreatePostIncidentReviews,
    CreateRollbackRequests,
    LogAuditRecords,
    CreateIncidents,
    CreateRootCauseAnalysis,
    CreateWorkArounds,
]
