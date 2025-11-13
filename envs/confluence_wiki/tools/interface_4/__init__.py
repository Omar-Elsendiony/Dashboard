from .establish_attachment import EstablishAttachment
from .establish_database import EstablishDatabase
from .establish_label import EstablishLabel
from .establish_page import EstablishPage
from .establish_page_version import EstablishPageVersion
from .establish_permission import EstablishPermission
from .establish_smart_link import EstablishSmartLink
from .establish_whiteboard import EstablishWhiteboard
from .eliminate_database import EliminateDatabase
from .eliminate_page import EliminatePage
from .eliminate_page_version import EliminatePageVersion
from .eliminate_smart_link import EliminateSmartLink
from .eliminate_whiteboard import EliminateWhiteboard
from .lookup_ancestors import LookupAncestors
from .lookup_descendants import LookupDescendants
from .lookup_direct_children import LookupDirectChildren
from .lookup_entity import LookupEntity
from .lookup_page import LookupPage
from .lookup_permissions import LookupPermissions
from .lookup_space import LookupSpace
from .lookup_user import LookupUser
from .lookup_versions import LookupVersions
from .erase_attachment import EraseAttachment
from .erase_label import EraseLabel
from .handover_to_human import HandoverToHuman
from .edit_attachment import EditAttachment
from .edit_database import EditDatabase
from .edit_label import EditLabel
from .edit_page import EditPage
from .edit_permission import EditPermission
from .edit_smart_link import EditSmartLink
from .edit_whiteboard import EditWhiteboard

ALL_TOOLS_INTERFACE_4 = [
    EstablishAttachment,
    EstablishDatabase,
    EstablishLabel,
    EstablishPage,
    EstablishPageVersion,
    EstablishPermission,
    EstablishSmartLink,
    EstablishWhiteboard,
    EliminateDatabase,
    EliminatePage,
    EliminatePageVersion,
    EliminateSmartLink,
    EliminateWhiteboard,
    LookupAncestors,
    LookupDescendants,
    LookupDirectChildren,
    LookupEntity,
    LookupPage,
    LookupPermissions,
    LookupSpace,
    LookupUser,
    LookupVersions,
    EraseAttachment,
    EraseLabel,
    HandoverToHuman,
    EditAttachment,
    EditDatabase,
    EditLabel,
    EditPage,
    EditPermission,
    EditSmartLink,
    EditWhiteboard,
]
