from .submit_approval_request import SubmitApprovalRequest
from .resolve_approval_step import ResolveApprovalStep
from .access_approval_request import AccessApprovalRequest
from .access_config_history import AccessConfigHistory
from .access_group import AccessGroup
from .access_notifications import AccessNotifications
from .access_page import AccessPage
from .access_permissions import AccessPermissions
from .access_space import AccessSpace
from .access_user import AccessUser
from .access_watchers import AccessWatchers
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
from .generate_new_audit_trail import GenerateNewAuditTrail
from .store_config_change import StoreConfigChange
from .broadcast_notification import BroadcastNotification
from .route_to_human import RouteToHuman

ALL_TOOLS_INTERFACE_5 = [
    SubmitApprovalRequest,
    ResolveApprovalStep,
    AccessApprovalRequest,
    AccessConfigHistory,
    AccessGroup,
    AccessNotifications,
    AccessPage,
    AccessPermissions,
    AccessSpace,
    AccessUser,
    AccessWatchers,
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
    GenerateNewAuditTrail,
    StoreConfigChange,
    BroadcastNotification,
    RouteToHuman
]
