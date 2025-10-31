from .manage_attachments import ManageAttachments
from .assess_incident_severity import AssessIncidentSeverity
from .manage_change_control import ManageChangeControl
from .discover_assets import DiscoverAssets
from .manage_communications import ManageCommunications
from .discover_change_control import DiscoverChangeControl
from .manage_coordinations import ManageCoordinations
from .manage_escalations import ManageEscalations
from .discover_coordination import DiscoverCoordination
from .manage_improvements import ManageImprovements
from .discover_improvement import DiscoverImprovement
from .manage_incident_reports import ManageIncidentReports
from .discover_incident_tracking import DiscoverIncidentTracking
from .manage_incidents import ManageIncidents
from .discover_parties import DiscoverParties
from .manage_incidents_problems_configuration_items import ManageIncidentsProblemsConfigurationItems
from .discover_workflows import DiscoverWorkflows
from .manage_problem_tickets import ManageProblemTickets
from .get_sla_breach_incidents import GetSlaBreachIncidents
from .manage_users import ManageUsers
# from .log_audit_records import LogAuditRecords
from .manage_work_notes import ManageWorkNotes
from .manage_approval_requests import ManageApprovalRequests
from .transfer_to_human import TransferToHuman

ALL_TOOLS_INTERFACE_1 = [
    ManageAttachments,
    AssessIncidentSeverity,
    ManageChangeControl,
    DiscoverAssets,
    ManageCommunications,
    DiscoverChangeControl,
    ManageCoordinations,
    ManageEscalations,
    DiscoverCoordination,
    ManageImprovements,
    DiscoverImprovement,
    ManageIncidentReports,
    DiscoverIncidentTracking,
    ManageIncidents,
    DiscoverParties,
    ManageIncidentsProblemsConfigurationItems,
    DiscoverWorkflows,
    ManageProblemTickets,
    GetSlaBreachIncidents,
    ManageUsers,
    # LogAuditRecords,
    ManageWorkNotes,
    ManageApprovalRequests,
    TransferToHuman
]
