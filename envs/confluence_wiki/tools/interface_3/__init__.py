from .generate_attachment import GenerateAttachment
from .generate_database import GenerateDatabase
from .generate_label import GenerateLabel
from .generate_page import GeneratePage
from .generate_page_version import GeneratePageVersion
from .generate_permission import GeneratePermission
from .generate_smart_link import GenerateSmartLink
from .generate_whiteboard import GenerateWhiteboard
from .destroy_database import DestroyDatabase
from .destroy_page import DestroyPage
from .destroy_page_version import DestroyPageVersion
from .destroy_smart_link import DestroySmartLink
from .destroy_whiteboard import DestroyWhiteboard
from .retrieve_ancestors import RetrieveAncestors
from .retrieve_descendants import RetrieveDescendants
from .retrieve_direct_children import RetrieveDirectChildren
from .retrieve_entity import RetrieveEntity
from .retrieve_page import RetrievePage
from .retrieve_permissions import RetrievePermissions
from .retrieve_space import RetrieveSpace
from .retrieve_user import RetrieveUser
from .retrieve_versions import RetrieveVersions
from .eliminate_attachment import EliminateAttachment
from .eliminate_label import EliminateLabel
from .escalate_to_human import EscalateToHuman
from .alter_attachment import AlterAttachment
from .alter_database import AlterDatabase
from .alter_label import AlterLabel
from .alter_page import AlterPage
from .alter_permission import AlterPermission
from .alter_smart_link import AlterSmartLink
from .alter_whiteboard import AlterWhiteboard

ALL_TOOLS_INTERFACE_3 = [
    GenerateAttachment,
    GenerateDatabase,
    GenerateLabel,
    GeneratePage,
    GeneratePageVersion,
    GeneratePermission,
    GenerateSmartLink,
    GenerateWhiteboard,
    DestroyDatabase,
    DestroyPage,
    DestroyPageVersion,
    DestroySmartLink,
    DestroyWhiteboard,
    RetrieveAncestors,
    RetrieveDescendants,
    RetrieveDirectChildren,
    RetrieveEntity,
    RetrievePage,
    RetrievePermissions,
    RetrieveSpace,
    RetrieveUser,
    RetrieveVersions,
    EliminateAttachment,
    EliminateLabel,
    EscalateToHuman,
    AlterAttachment,
    AlterDatabase,
    AlterLabel,
    AlterPage,
    AlterPermission,
    AlterSmartLink,
    AlterWhiteboard,
]
