from .address_exports import AddressExports
from .address_group_memberships import AddressGroupMemberships
from .address_groups import AddressGroups
from .address_page_versions import AddressPageVersions
from .address_pages import AddressPages
from .address_permissions import AddressPermissions
from .address_space_features import AddressSpaceFeatures
from .address_spaces import AddressSpaces
from .address_users import AddressUsers
from .address_watchers import AddressWatchers
from .capture_config_change import CaptureConfigChange
from .deliver_notification import DeliverNotification
from .establish_approval_request import EstablishApprovalRequest
from .execute_approval_step import ExecuteApprovalStep
from .handover_to_human import HandOverToHuman
from .lookup_approval_request import LookupApprovalRequest
from .lookup_config_history import LookupConfigHistory
from .lookup_group import LookupGroup
from .lookup_notifications import LookupNotifications
from .lookup_page import LookupPage
from .lookup_permissions import LookupPermissions
from .lookup_space import LookupSpace
from .lookup_user import LookupUser
from .lookup_watchers import LookupWatchers
from .record_new_audit_trail import RecordNewAuditTrail

ALL_TOOLS_INTERFACE_4 = [
    AddressExports,
    AddressGroupMemberships,
    AddressGroups,
    AddressPageVersions,
    AddressPages,
    AddressPermissions,
    AddressSpaceFeatures,
    AddressSpaces,
    AddressUsers,
    AddressWatchers,
    CaptureConfigChange,
    DeliverNotification,
    EstablishApprovalRequest,
    ExecuteApprovalStep,
    HandOverToHuman,
    LookupApprovalRequest,
    LookupConfigHistory,
    LookupGroup,
    LookupNotifications,
    LookupPage,
    LookupPermissions,
    LookupSpace,
    LookupUser,
    LookupWatchers,
    RecordNewAuditTrail,
]
