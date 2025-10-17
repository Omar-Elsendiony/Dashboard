from .discover_assets import DiscoverAssets
from .discover_contracts import DiscoverContracts
from .discover_coordination import DiscoverCoordination
from .discover_incident_tracking import DiscoverIncidentTracking
from .discover_parties import DiscoverParties
from .manage_assets import ManageAssets
from .manage_change_control import ManageChangeControl
from .manage_client_vendors import ManageClientVendors
from .manage_communications import ManageCommunications
from .manage_contracts import ManageContracts
from .manage_escalations import ManageEscalations
from .manage_root_cause_analyses import ManageRootCauseAnalyses
from .manage_users import ManageUsers
from .manage_performance_metrics import ManagePerformanceMetrics
from .manage_incident_reports import ManageIncidentReports
from .manage_work_orders import ManageWorkOrders
from .manage_post_incident_reviews import ManagePostIncidentReviews
from .manage_approval_requests import ManageApprovalRequests
from .log_audit_records import LogAuditRecords
from .manage_incidents import ManageIncidents
from .manage_work_notes import ManageWorkNotes
from .manage_attachments import ManageAttachments

ALL_TOOLS_INTERFACE_1 = [
    DiscoverAssets,
    DiscoverContracts,
    DiscoverCoordination,
    DiscoverIncidentTracking,
    DiscoverParties,
    ManageAssets,
    ManageChangeControl,
    ManageClientVendors,
    ManageCommunications,
    ManageContracts,
    ManageEscalations,
    ManageRootCauseAnalyses,
    ManageUsers,
    ManagePerformanceMetrics,
    ManageIncidentReports,
    ManageWorkOrders,
    ManagePostIncidentReviews,
    ManageApprovalRequests,
      LogAuditRecords,
    ManageIncidents,
    ManageWorkNotes,
    ManageAttachments
]