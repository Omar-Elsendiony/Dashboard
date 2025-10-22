from .create_approval_request import CreateApprovalRequest
from .decide_approval_step import DecideApprovalStep
from .get_approval_request import GetApprovalRequest
from .get_config_history import GetConfigHistory
from .get_group import GetGroup
from .get_notifications import GetNotifications
from .get_page import GetPage
from .get_permissions import GetPermissions
from .get_space import GetSpace
from .get_user import GetUser
from .get_watchers import GetWatchers
from .manage_exports import ManageExports
from .manage_group_memberships import ManageGroupMemberships
from .manage_groups import ManageGroups
from .manage_page_versions import ManagePageVersions
from .manage_pages import ManagePages
from .manage_permissions import ManagePermissions
from .manage_space_features import ManageSpaceFeatures
from .manage_spaces import ManageSpaces
from .manage_users import ManageUsers
from .manage_watchers import ManageWatchers
from .record_audit_log import RecordAuditLog
from .record_config_change import RecordConfigChange
from .send_notification import SendNotification
from .transfer_to_human import TransferToHuman

ALL_TOOLS_INTERFACE_1 = [
    CreateApprovalRequest,
    DecideApprovalStep,
    GetApprovalRequest,
    GetConfigHistory,
    GetGroup,
    GetNotifications,
    GetPage,
    GetPermissions,
    GetSpace,
    GetUser,
    GetWatchers,
    ManageExports,
    ManageGroupMemberships,
    ManageGroups,
    ManagePageVersions,
    ManagePages,
    ManagePermissions,
    ManageSpaceFeatures,
    ManageSpaces,
    ManageUsers,
    ManageWatchers,
    RecordAuditLog,
    RecordConfigChange,
    SendNotification,
    TransferToHuman
]
