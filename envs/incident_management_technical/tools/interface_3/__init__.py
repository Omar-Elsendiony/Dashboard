from .manipulate_attachments import ManipulateAttachments
from .evaluate_incident_severity import EvaluateIncidentSeverity
from .manipulate_change_control import ManipulateChangeControl
from .find_assets import FindAssets
from .manipulate_communications import ManipulateCommunications
from .find_change_control import FindChangeControl
from .manipulate_coordinations import ManipulateCoordinations
from .manipulate_escalations import ManipulateEscalations
from .find_coordination import FindCoordination
from .manipulate_improvements import ManipulateImprovements
from .find_improvement import FindImprovement
from .manipulate_incident_reports import ManipulateIncidentReports
from .find_incident_tracking import FindIncidentTracking
from .manipulate_incidents import ManipulateIncidents
from .find_parties import FindParties
from .manipulate_incidents_problems_configuration_items import ManipulateIncidentsProblemsConfigurationItems
from .find_workflows import FindWorkflows
from .manipulate_problem_tickets import ManipulateProblemTickets
from .retrieve_sla_breach_incidents import RetrieveSlaBreachIncidents
from .manipulate_users import ManipulateUsers
# from .add_audit_records import AddAuditRecords
from .manipulate_work_notes import ManipulateWorkNotes
from .manipulate_approval_requests import ManipulateApprovalRequests
from .route_to_human import RouteToHuman

ALL_TOOLS_INTERFACE_3 = [
    ManipulateAttachments,
    EvaluateIncidentSeverity,
    ManipulateChangeControl,
    FindAssets,
    ManipulateCommunications,
    FindChangeControl,
    ManipulateCoordinations,
    ManipulateEscalations,
    FindCoordination,
    ManipulateImprovements,
    FindImprovement,
    ManipulateIncidentReports,
    FindIncidentTracking,
    ManipulateIncidents,
    FindParties,
    ManipulateIncidentsProblemsConfigurationItems,
    FindWorkflows,
    ManipulateProblemTickets,
    RetrieveSlaBreachIncidents,
    ManipulateUsers,
    # AddAuditRecords,
    ManipulateWorkNotes,
    ManipulateApprovalRequests,
    RouteToHuman
]
