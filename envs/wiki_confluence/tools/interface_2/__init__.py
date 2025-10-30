from .set_approval_request import SetApprovalRequest
from .set_approval_decision import SetApprovalDecision
from .fetch_approval_request import FetchApprovalRequest
from .fetch_config_history import FetchConfigHistory
from .fetch_group import FetchGroup
from .fetch_notifications import FetchNotifications
from .fetch_page import FetchPage
from .fetch_permissions import FetchPermissions
from .fetch_space import FetchSpace
from .fetch_user import FetchUser
from .fetch_watchers import FetchWatchers
from .set_exports import SetExports
from .set_group_memberships import SetGroupMemberships
from .set_groups import SetGroups
from .set_page_versions import SetPageVersions
from .set_pages import SetPages
from .set_permissions import SetPermissions
from .set_space_features import SetSpaceFeatures
from .set_spaces import SetSpaces
from .set_users import SetUsers
from .set_watchers import SetWatchers
from .create_new_audit_trail import CreateNewAuditTrail
from .log_config_change import LogConfigChange
from .dispatch_notification import DispatchNotification
from .switch_to_human import SwitchToHuman

ALL_TOOLS_INTERFACE_2 = [
    SetApprovalRequest,
    SetApprovalDecision,
    FetchApprovalRequest,
    FetchConfigHistory,
    FetchGroup,
    FetchNotifications,
    FetchPage,
    FetchPermissions,
    FetchSpace,
    FetchUser,
    FetchWatchers,
    SetExports,
    SetGroupMemberships,
    SetGroups,
    SetPageVersions,
    SetPages,
    SetPermissions,
    SetSpaceFeatures,
    SetSpaces,
    SetUsers,
    SetWatchers,
    CreateNewAuditTrail,
    LogConfigChange,
    DispatchNotification,
    SwitchToHuman
]
