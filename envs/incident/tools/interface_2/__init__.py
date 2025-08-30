#interface_2/__init__.py

from .list_products import ListProducts
from .list_components import ListComponents
from .list_client_subscriptions import ListClientSubscriptions
from .list_sla_agreements import ListSlaAgreements
from .list_clients import ListClients
from .list_users import ListUsers
from .list_vendors import ListVendors
from .list_incidents import ListIncidents
from .list_workarounds import ListWorkarounds
from .list_change_requests import ListChangeRequests
from .list_knowledge_base_articles import ListKnowledgeBaseArticles

from .create_product import CreateProduct
from .update_product import UpdateProduct
from .create_component import CreateComponent
from .update_component import UpdateComponent
from .create_client_subscription import CreateClientSubscription
from .update_client_subscription import UpdateClientSubscription
from .create_sla_agreement import CreateSlaAgreement
from .update_sla_agreement import UpdateSlaAgreement
from .create_knowledge_base_article import CreateKnowledgeBaseArticle
from .create_change_request import CreateChangeRequest
from .create_workaround import CreateWorkaround


ALL_TOOLS_INTERFACE_2 = [
    # GET
    ListProducts,
    ListComponents,
    ListClientSubscriptions,
    ListSlaAgreements,
    ListClients,
    ListUsers,
    ListVendors,
    ListIncidents,
    ListWorkarounds,
    ListChangeRequests,
    ListKnowledgeBaseArticles,
    # SET
    CreateProduct,
    UpdateProduct,
    CreateComponent,
    UpdateComponent,
    CreateClientSubscription,
    UpdateClientSubscription,
    CreateSlaAgreement,
    UpdateSlaAgreement,
    CreateKnowledgeBaseArticle,
    CreateChangeRequest,
    CreateWorkaround,
]
