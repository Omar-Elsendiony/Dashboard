from .get_group_info import GetGroupInfo
from .get_user_by_email import GetUserByEmail

from .assign_permission_to_group import AssignPermissionToGroup
from .assign_permission_to_user import AssignPermissionToUser
from .remove_permission_from_group import RemovePermissionFromGroup
from .remove_permission_from_user import RemovePermissionFromUser

from .create_group import CreateGroup
from .create_permission import CreatePermission
from .create_user import CreateUser

from .delete_permission import DeletePermission
from .delete_user import DeleteUser

from .get_group_members import GetGroupMembers
from .get_permission_info import GetPermissionInfo
from .get_permissions_by_category import GetPermissionsByCategory
from .get_space_permissions import GetSpacePermissions
from .get_space_statistics import GetSpaceStatistics
from .get_user_groups import GetUserGroups
from .get_user_space_permissions import GetUserSpacePermissions
from .get_user_activity_log import GetUserActivityLog
from .get_spaces_by_filters import GetSpacesByFilters

from .update_permission import UpdatePermission
from .update_user import UpdateUser

from .add_user_to_group import AddUserToGroup
from .remove_user_from_group import RemoveUserFromGroup

ALL_TOOLS_INTERFACE_3 = [
    GetGroupInfo,
    GetUserByEmail,

    AssignPermissionToGroup,
    AssignPermissionToUser,
    RemovePermissionFromGroup,
    RemovePermissionFromUser,

    CreateGroup,
    CreatePermission,
    CreateUser,

    DeletePermission,
    DeleteUser,

    GetGroupMembers,
    GetPermissionInfo,
    GetPermissionsByCategory,
    GetSpacePermissions,
    GetSpaceStatistics,
    GetUserGroups,
    GetUserSpacePermissions,
    GetUserActivityLog,
    GetSpacesByFilters,

    UpdatePermission,
    UpdateUser,
    
    AddUserToGroup,
    RemoveUserFromGroup
]
