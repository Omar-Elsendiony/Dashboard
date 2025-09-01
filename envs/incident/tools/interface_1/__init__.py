# interface_1/__init__.py

from .get_clients import GetClients
from .get_users import GetUsers
from .get_vendors import GetVendors
from .get_products import GetProducts
from .get_components import GetComponents
from .get_client_subscriptions import GetClientSubscriptions
from .get_sla_agreements import GetSlaAgreements
from .get_incidents import GetIncidents
from .get_metrics import GetMetrics
from .get_knowledge_base_articles import GetKnowledgeBaseArticles

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
from .record_incident import RecordIncident

ALL_TOOLS_INTERFACE_1 = [
    # GET
    GetClients,
    GetUsers,
    GetVendors,
    GetProducts,
    GetComponents,
    GetClientSubscriptions,
    GetSlaAgreements,
    GetIncidents,
    GetMetrics,
    GetKnowledgeBaseArticles,
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
    RecordIncident
]
