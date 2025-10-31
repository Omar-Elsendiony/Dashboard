from .address_attachments import AddressAttachments
from .calculate_incident_severity import CalculateIncidentSeverity
from .address_change_control import AddressChangeControl
from .lookup_assets import LookupAssets
from .address_communications import AddressCommunications
from .lookup_change_control import LookupChangeControl
from .address_coordinations import AddressCoordinations
from .address_escalations import AddressEscalations
from .lookup_coordination import LookupCoordination
from .address_improvements import AddressImprovements
from .lookup_improvement import LookupImprovement
from .address_incident_reports import AddressIncidentReports
from .lookup_incident_tracking import LookupIncidentTracking
from .address_incidents import AddressIncidents
from .lookup_parties import LookupParties
from .address_incidents_problems_configuration_items import AddressIncidentsProblemsConfigurationItems
from .lookup_workflows import LookupWorkflows
from .address_problem_tickets import AddressProblemTickets
from .obtain_sla_breach_incidents import ObtainSlaBreachIncidents
from .address_users import AddressUsers
# from .insert_audit_records import InsertAuditRecords
from .address_work_notes import AddressWorkNotes
from .address_approval_requests import AddressApprovalRequests
from .handover_to_human import HandoverToHuman

ALL_TOOLS_INTERFACE_4 = [
    AddressAttachments,
    CalculateIncidentSeverity,
    AddressChangeControl,
    LookupAssets,
    AddressCommunications,
    LookupChangeControl,
    AddressCoordinations,
    AddressEscalations,
    LookupCoordination,
    AddressImprovements,
    LookupImprovement,
    AddressIncidentReports,
    LookupIncidentTracking,
    AddressIncidents,
    LookupParties,
    AddressIncidentsProblemsConfigurationItems,
    LookupWorkflows,
    AddressProblemTickets,
    ObtainSlaBreachIncidents,
    AddressUsers,
    # InsertAuditRecords,
    AddressWorkNotes,
    AddressApprovalRequests,
    HandoverToHuman
]
