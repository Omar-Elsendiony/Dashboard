from .process_attachments import ProcessAttachments
from .determine_incident_severity import DetermineIncidentSeverity
from .process_change_control import ProcessChangeControl
from .get_assets import GetAssets
from .process_communications import ProcessCommunications
from .get_change_control import GetChangeControl
from .process_coordinations import ProcessCoordinations
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
# from .insert_audit_records import InsertAuditRecords
from .process_work_notes import ProcessWorkNotes
from .process_approval_requests import ProcessApprovalRequests
from .switch_to_human import SwitchToHuman

ALL_TOOLS_INTERFACE_5 = [
    ProcessAttachments,
    DetermineIncidentSeverity,
    ProcessChangeControl,
    GetAssets,
    ProcessCommunications,
    GetChangeControl,
    ProcessCoordinations,
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
    # InsertAuditRecords,
    ProcessWorkNotes,
    ProcessApprovalRequests,
    SwitchToHuman
]
