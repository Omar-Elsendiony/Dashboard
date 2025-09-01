# interface_2/__init__.py

from .fetch_clients import FetchClients
from .fetch_users import FetchUsers
from .fetch_vendors import FetchVendors
from .fetch_products import FetchProducts
from .fetch_components import FetchComponents
from .fetch_client_subscriptions import FetchClientSubscriptions
from .fetch_sla_agreements import FetchSlaAgreements
from .fetch_incidents import FetchIncidents
from .fetch_change_requests import FetchChangeRequests
from .fetch_workarounds import FetchWorkarounds
from .fetch_knowledge_base_articles import FetchKnowledgeBaseArticles

from .add_change_request import AddChangeRequest
from .add_client_subscription import AddClientSubscription
from .add_component import AddComponent
from .add_knowledge_base_article import AddKnowledgeBaseArticle
from .add_product import AddProduct
from .add_sla_agreement import AddSlaAgreement
from .add_workaround import AddWorkaround
from .modify_client_subscription import ModifyClientSubscription
from .modify_component import ModifyComponent
from .modify_product import ModifyProduct
from .modify_sla_agreement import ModifySlaAgreement
from .log_incident import LogIncident
ALL_TOOLS_INTERFACE_2 = [
    # GET
    FetchClients,
    FetchUsers,
    FetchVendors,
    FetchProducts,
    FetchComponents,
    FetchClientSubscriptions,
    FetchSlaAgreements,
    FetchIncidents,
    FetchChangeRequests,
    FetchWorkarounds,
    FetchKnowledgeBaseArticles,
    # SET
    AddChangeRequest,
    AddClientSubscription,
    AddComponent,
    AddKnowledgeBaseArticle,
    AddProduct,
    AddSlaAgreement,
    AddWorkaround,
    ModifyClientSubscription,
    ModifyComponent,
    ModifyProduct,
    ModifySlaAgreement,
    LogIncident
]
