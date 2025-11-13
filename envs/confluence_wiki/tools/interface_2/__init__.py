from .new_attachment import NewAttachment
from .new_database import NewDatabase
from .new_label import NewLabel
from .new_page import NewPage
from .new_page_version import NewPageVersion
from .new_permission import NewPermission
from .new_smart_link import NewSmartLink
from .new_whiteboard import NewWhiteboard
from .remove_database import RemoveDatabase
from .remove_page import RemovePage
from .remove_page_version import RemovePageVersion
from .remove_smart_link import RemoveSmartLink
from .remove_whiteboard import RemoveWhiteboard
from .fetch_ancestors import FetchAncestors
from .fetch_descendants import FetchDescendants
from .fetch_direct_children import FetchDirectChildren
from .fetch_entity import FetchEntity
from .fetch_page import FetchPage
from .fetch_permissions import FetchPermissions
from .fetch_space import FetchSpace
from .fetch_user import FetchUser
from .fetch_versions import FetchVersions
from .delete_attachment import DeleteAttachment
from .delete_label import DeleteLabel
from .switch_to_human import SwitchToHuman
from .modify_attachment import ModifyAttachment
from .modify_database import ModifyDatabase
from .modify_label import ModifyLabel
from .modify_page import ModifyPage
from .modify_permission import ModifyPermission
from .modify_smart_link import ModifySmartLink
from .modify_whiteboard import ModifyWhiteboard

ALL_TOOLS_INTERFACE_2 = [
    NewAttachment,
    NewDatabase,
    NewLabel,
    NewPage,
    NewPageVersion,
    NewPermission,
    NewSmartLink,
    NewWhiteboard,
    RemoveDatabase,
    RemovePage,
    RemovePageVersion,
    RemoveSmartLink,
    RemoveWhiteboard,
    FetchAncestors,
    FetchDescendants,
    FetchDirectChildren,
    FetchEntity,
    FetchPage,
    FetchPermissions,
    FetchSpace,
    FetchUser,
    FetchVersions,
    DeleteAttachment,
    DeleteLabel,
    SwitchToHuman,
    ModifyAttachment,
    ModifyDatabase,
    ModifyLabel,
    ModifyPage,
    ModifyPermission,
    ModifySmartLink,
    ModifyWhiteboard,
]
