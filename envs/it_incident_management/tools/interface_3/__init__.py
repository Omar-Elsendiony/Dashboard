# interface_3/__init__.py

from .retrieve_incidents import RetrieveIncidents
from .retrieve_escalations import RetrieveEscalations
from .retrieve_users import RetrieveUsers
from .retrieve_clients import RetrieveClients
from .retrieve_components import RetrieveComponents
from .retrieve_communications import RetrieveCommunications
from .retrieve_workarounds import RetrieveWorkarounds
from .retrieve_root_cause_analyses import RetrieveRootCauseAnalyses
from .retrieve_change_requests import RetrieveChangeRequests
from .retrieve_incident_reports import RetrieveIncidentReports
from .retrieve_sla_agreements import RetrieveSlaAgreements
from .retrieve_products import RetrieveProducts

from .register_incident import RegisterIncident
from .amend_incident import AmendIncident
from .register_escalation import RegisterEscalation
from .amend_escalation import AmendEscalation
from .register_communication import RegisterCommunication
from .amend_communication import AmendCommunication
from .register_workaround import RegisterWorkaround
from .amend_workaround import AmendWorkaround
from .register_root_cause_analysis import RegisterRootCauseAnalysis
from .amend_root_cause_analysis import AmendRootCauseAnalysis
from .register_change_request import RegisterChangeRequest
from .register_incident_update_record import RegisterIncidentUpdateRecord

ALL_TOOLS_INTERFACE_3 = [
    # GET
    RetrieveIncidents,
    RetrieveEscalations,
    RetrieveUsers,
    RetrieveClients,
    RetrieveComponents,
    RetrieveCommunications,
    RetrieveWorkarounds,
    RetrieveRootCauseAnalyses,
    RetrieveChangeRequests,
    RetrieveIncidentReports,
    RetrieveSlaAgreements,
    RetrieveProducts,
    # SET
    RegisterIncident,
    AmendIncident,
    RegisterEscalation,
    AmendEscalation,
    RegisterCommunication,
    AmendCommunication,
    RegisterWorkaround,
    AmendWorkaround,
    RegisterRootCauseAnalysis,
    AmendRootCauseAnalysis,
    RegisterChangeRequest,
    RegisterIncidentUpdateRecord,
]
