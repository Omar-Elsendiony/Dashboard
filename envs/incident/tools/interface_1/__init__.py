#interface_1/__init__.py

from .list_clients import ListClients
from .list_users import ListUsers
from .list_vendors import ListVendors
from .list_products import ListProducts
from .list_components import ListComponents
from .list_client_subscriptions import ListClientSubscriptions
from .list_sla_agreements import ListSlaAgreements
from .list_incidents import ListIncidents
from .list_metrics import ListMetrics
from .list_knowledge_base_articles import ListKnowledgeBaseArticles

from .create_client import CreateClient
from .update_client import UpdateClient
from .create_user import CreateUser
from .update_user import UpdateUser
from .create_vendor import CreateVendor
from .update_vendor import UpdateVendor
from .create_client_subscription import CreateClientSubscription
from .update_client_subscription import UpdateClientSubscription
from .create_sla_agreement import CreateSlaAgreement
from .update_sla_agreement import UpdateSlaAgreement


ALL_TOOLS_INTERFACE_1 = [
    # GET
    ListClients,
    ListUsers,
    ListVendors,
    ListProducts,
    ListComponents,
    ListClientSubscriptions,
    ListSlaAgreements,
    ListIncidents,
    ListMetrics,
    ListKnowledgeBaseArticles,
    # SET
    CreateClient,
    UpdateClient,
    CreateUser,
    UpdateUser,
    CreateVendor,
    UpdateVendor,
    CreateClientSubscription,
    UpdateClientSubscription,
    CreateSlaAgreement,
    UpdateSlaAgreement,
]
