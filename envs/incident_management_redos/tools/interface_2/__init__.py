from .handle_attachments import HandleAttachments
from .compute_incident_severity import ComputeIncidentSeverity
from .handle_change_control import HandleChangeControl
from .validate_authorization import ValidateAuthorization
from .handle_clients import HandleClients
from .search_assets import SearchAssets
from .handle_communications import HandleCommunications
from .search_audit import SearchAudit
from .handle_contracts import HandleContracts
from .search_change_control import SearchChangeControl
from .handle_coordinations import HandleCoordinations
from .search_contracts import SearchContracts
from .handle_escalations import HandleEscalations
from .search_coordination import SearchCoordination
from .handle_improvements import HandleImprovements
from .search_improvement import SearchImprovement
from .handle_incident_reports import HandleIncidentReports
from .search_incident_tracking import SearchIncidentTracking
from .handle_incidents import HandleIncidents
from .search_parties import SearchParties
from .handle_incidents_problems_configuration_items import HandleIncidentsProblemsConfigurationItems
from .search_workflows import SearchWorkflows
from .handle_problem_tickets import HandleProblemTickets
from .acquire_sla_breach_incidents import AcquireSlaBreachIncidents
from .handle_users import HandleUsers
from .record_audit_records import RecordAuditRecords
from .handle_work_notes import HandleWorkNotes
from .handle_approval_requests import HandleApprovalRequests
from .handle_work_orders import HandleWorkOrders
from .handle_assets import HandleAssets
from .escalate_to_human import EscalateToHuman

ALL_TOOLS_INTERFACE_2 = [
    HandleAttachments,
    ComputeIncidentSeverity,
    HandleChangeControl,
    ValidateAuthorization,
    HandleClients,
    SearchAssets,
    HandleCommunications,
    SearchAudit,
    HandleContracts,
    SearchChangeControl,
    HandleCoordinations,
    SearchContracts,
    HandleEscalations,
    SearchCoordination,
    HandleImprovements,
    SearchImprovement,
    HandleIncidentReports,
    SearchIncidentTracking,
    HandleIncidents,
    SearchParties,
    HandleIncidentsProblemsConfigurationItems,
    SearchWorkflows,
    HandleProblemTickets,
    AcquireSlaBreachIncidents,
    HandleUsers,
    RecordAuditRecords,
    HandleWorkNotes,
    HandleApprovalRequests,
    HandleWorkOrders,
    HandleAssets,
    EscalateToHuman
]
