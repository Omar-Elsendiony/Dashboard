from .create_attachment import CreateAttachment
from .create_database import CreateDatabase
from .create_label import CreateLabel
from .create_page import CreatePage
from .create_page_version import CreatePageVersion
from .create_permission import CreatePermission
from .create_smart_link import CreateSmartLink
from .create_whiteboard import CreateWhiteboard
from .delete_database import DeleteDatabase
from .delete_page import DeletePage
from .delete_page_version import DeletePageVersion
from .delete_smart_link import DeleteSmartLink
from .delete_whiteboard import DeleteWhiteboard
from .get_ancestors import GetAncestors
from .get_descendants import GetDescendants
from .get_direct_children import GetDirectChildren
from .get_entity import GetEntity
from .get_page import GetPage
from .get_permissions import GetPermissions
from .get_space import GetSpace
from .get_user import GetUser
from .get_versions import GetVersions
from .remove_attachment import RemoveAttachment
from .remove_label import RemoveLabel
from .transfer_to_human import TransferToHuman
from .update_attachment import UpdateAttachment
from .update_database import UpdateDatabase
from .update_label import UpdateLabel
from .update_page import UpdatePage
from .update_permission import UpdatePermission
from .update_smart_link import UpdateSmartLink
from .update_whiteboard import UpdateWhiteboard

ALL_TOOLS_INTERFACE_1 = [
    CreateAttachment,
    CreateDatabase,
    CreateLabel,
    CreatePage,
    CreatePageVersion,
    CreatePermission,
    CreateSmartLink,
    CreateWhiteboard,
    DeleteDatabase,
    DeletePage,
    DeletePageVersion,
    DeleteSmartLink,
    DeleteWhiteboard,
    GetAncestors,
    GetDescendants,
    GetDirectChildren,
    GetEntity,
    GetPage,
    GetPermissions,
    GetSpace,
    GetUser,
    GetVersions,
    RemoveAttachment,
    RemoveLabel,
    TransferToHuman,
    UpdateAttachment,
    UpdateDatabase,
    UpdateLabel,
    UpdatePage,
    UpdatePermission,
    UpdateSmartLink,
    UpdateWhiteboard,
]
