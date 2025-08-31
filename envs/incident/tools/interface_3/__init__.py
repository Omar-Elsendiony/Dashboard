#interface_3/__init__.py

from .list_incidents import ListIncidents
from .list_escalations import ListEscalations
from .list_users import ListUsers
from .list_clients import ListClients
from .list_components import ListComponents
from .list_communications import ListCommunications
from .list_workarounds import ListWorkarounds
from .list_root_cause_analyses import ListRootCauseAnalyses
from .list_change_requests import ListChangeRequests
from .list_incident_reports import ListIncidentReports
from .list_sla_agreements import ListSlaAgreements

from .create_incident import CreateIncident
from .update_incident import UpdateIncident
from .create_escalation import CreateEscalation
from .update_escalation import UpdateEscalation
from .create_communication import CreateCommunication
from .update_communication import UpdateCommunication
from .create_workaround import CreateWorkaround
from .update_workaround import UpdateWorkaround
from .create_root_cause_analysis import CreateRootCauseAnalysis
from .update_root_cause_analysis import UpdateRootCauseAnalysis
from .create_change_request import CreateChangeRequest
from .create_incident_record import CreateIncidentRecord

ALL_TOOLS_INTERFACE_3 = [
    # GET
    ListIncidents,
    ListEscalations,
    ListUsers,
    ListClients,
    ListComponents,
    ListCommunications,
    ListWorkarounds,
    ListRootCauseAnalyses,
    ListChangeRequests,
    ListIncidentReports,
    ListSlaAgreements,
    # SET
    CreateIncident,
    UpdateIncident,
    CreateEscalation,
    UpdateEscalation,
    CreateCommunication,
    UpdateCommunication,
    CreateWorkaround,
    UpdateWorkaround,
    CreateRootCauseAnalysis,
    UpdateRootCauseAnalysis,
    CreateChangeRequest,
    CreateIncidentRecord,
]
