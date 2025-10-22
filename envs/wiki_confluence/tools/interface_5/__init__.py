from .create_approval_request import CreateApprovalRequest
from .decide_approval_step import DecideApprovalStep
from .generate_new_audit_trail import GenerateNewAuditTrail
from .get_approval_request import GetApprovalRequest
from .get_config_history import GetConfigHistory
from .get_group import GetGroup
from .get_notifications import GetNotifications
from .get_page import GetPage
from .get_permissions import GetPermissions
from .get_space import GetSpace
from .get_user import GetUser
from .get_watchers import GetWatchers
from .process_exports import ProcessExports
from .process_group_memberships import ProcessGroupMemberships
from .process_groups import ProcessGroups
from .process_page_versions import ProcessPageVersions
from .process_pages import ProcessPages
from .process_permissions import ProcessPermissions
from .process_space_features import ProcessSpaceFeatures
from .process_spaces import ProcessSpaces
from .process_users import ProcessUsers
from .process_watchers import ProcessWatchers
from .record_config_change import RecordConfigChange
from .route_to_human import RouteToHuman
from .send_notification import SendNotification

ALL_TOOLS_INTERFACE_5 = [
    CreateApprovalRequest,
    DecideApprovalStep,
    GenerateNewAuditTrail,
    GetApprovalRequest,
    GetConfigHistory,
    GetGroup,
    GetNotifications,
    GetPage,
    GetPermissions,
    GetSpace,
    GetUser,
    GetWatchers,
    ProcessExports,
    ProcessGroupMemberships,
    ProcessGroups,
    ProcessPageVersions,
    ProcessPages,
    ProcessPermissions,
    ProcessSpaceFeatures,
    ProcessSpaces,
    ProcessUsers,
    ProcessWatchers,
    RecordConfigChange,
    RouteToHuman,
    SendNotification
]
