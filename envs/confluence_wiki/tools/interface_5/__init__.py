from .make_attachment import MakeAttachment
from .make_database import MakeDatabase
from .make_label import MakeLabel
from .make_page import MakePage
from .make_page_version import MakePageVersion
from .make_permission import MakePermission
from .make_smart_link import MakeSmartLink
from .make_whiteboard import MakeWhiteboard
from .erase_database import EraseDatabase
from .erase_page import ErasePage
from .erase_page_version import ErasePageVersion
from .erase_smart_link import EraseSmartLink
from .erase_whiteboard import EraseWhiteboard
from .access_ancestors import AccessAncestors
from .access_descendants import AccessDescendants
from .access_direct_children import AccessDirectChildren
from .access_entity import AccessEntity
from .access_page import AccessPage
from .access_permissions import AccessPermissions
from .access_space import AccessSpace
from .access_user import AccessUser
from .access_versions import AccessVersions
from .discard_attachment import DiscardAttachment
from .discard_label import DiscardLabel
from .route_to_human import RouteToHuman
from .change_attachment import ChangeAttachment
from .change_database import ChangeDatabase
from .change_label import ChangeLabel
from .change_page import ChangePage
from .change_permission import ChangePermission
from .change_smart_link import ChangeSmartLink
from .change_whiteboard import ChangeWhiteboard

ALL_TOOLS_INTERFACE_5 = [
    MakeAttachment,
    MakeDatabase,
    MakeLabel,
    MakePage,
    MakePageVersion,
    MakePermission,
    MakeSmartLink,
    MakeWhiteboard,
    EraseDatabase,
    ErasePage,
    ErasePageVersion,
    EraseSmartLink,
    EraseWhiteboard,
    AccessAncestors,
    AccessDescendants,
    AccessDirectChildren,
    AccessEntity,
    AccessPage,
    AccessPermissions,
    AccessSpace,
    AccessUser,
    AccessVersions,
    DiscardAttachment,
    DiscardLabel,
    RouteToHuman,
    ChangeAttachment,
    ChangeDatabase,
    ChangeLabel,
    ChangePage,
    ChangePermission,
    ChangeSmartLink,
    ChangeWhiteboard,
]
