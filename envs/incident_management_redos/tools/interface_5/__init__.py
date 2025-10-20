from .process_attachments import ProcessAttachments
from .determine_incident_severity import DetermineIncidentSeverity
from .process_change_control import ProcessChangeControl
from .confirm_authorization import ConfirmAuthorization
from .process_clients import ProcessClients
from .get_assets import GetAssets
from .process_communications import ProcessCommunications
from .get_audit import GetAudit
from .process_contracts import ProcessContracts
from .get_change_control import GetChangeControl
from .process_coordinations import ProcessCoordinations
from .get_contracts import GetContracts
from .process_escalations import ProcessEscalations
from .get_coordination import GetCoordination
from .process_improvements import ProcessImprovements
from .get_improvement import GetImprovement
from .process_incident_reports import ProcessIncidentReports
from .get_incident_tracking import GetIncidentTracking
from .process_incidents import ProcessIncidents
from .get_parties import GetParties
from .process_incidents_problems_configuration_items import ProcessIncidentsProblemsConfigurationItems
from .get_workflows import GetWorkflows
from .process_problem_tickets import ProcessProblemTickets
from .fetch_sla_breach_incidents import FetchSlaBreachIncidents
from .process_users import ProcessUsers
from .insert_audit_records import InsertAuditRecords
from .process_work_notes import ProcessWorkNotes
from .process_approval_requests import ProcessApprovalRequests
from .process_work_orders import ProcessWorkOrders
from .process_assets import ProcessAssets
from .switch_to_human import SwitchToHuman

ALL_TOOLS_INTERFACE_5 = [
    ProcessAttachments,
    DetermineIncidentSeverity,
    ProcessChangeControl,
    ConfirmAuthorization,
    ProcessClients,
    GetAssets,
    ProcessCommunications,
    GetAudit,
    ProcessContracts,
    GetChangeControl,
    ProcessCoordinations,
    GetContracts,
    ProcessEscalations,
    GetCoordination,
    ProcessImprovements,
    GetImprovement,
    ProcessIncidentReports,
    GetIncidentTracking,
    ProcessIncidents,
    GetParties,
    ProcessIncidentsProblemsConfigurationItems,
    GetWorkflows,
    ProcessProblemTickets,
    FetchSlaBreachIncidents,
    ProcessUsers,
    InsertAuditRecords,
    ProcessWorkNotes,
    ProcessApprovalRequests,
    ProcessWorkOrders,
    ProcessAssets,
    SwitchToHuman
]
