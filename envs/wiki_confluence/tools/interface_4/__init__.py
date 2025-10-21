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
from .create_approval_request import CreateApprovalRequest
from .decide_approval_step import DecideApprovalStep
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
from .record_config_change import RecordConfigChange
from .record_new_audit_trail import RecordNewAuditTrail
from .send_notification import SendNotification

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
    CreateApprovalRequest,
    DecideApprovalStep,
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
    RecordConfigChange,
    RecordNewAuditTrail,
    SendNotification
]
