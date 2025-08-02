from .add_page_label import AddPageLabel
from .create_attachment import CreateAttachment
from .create_comment import CreateComment
from .create_label import CreateLabel
from .create_page import CreatePage
from .create_space import CreateSpace
from .delete_label import DeleteLabel
from .delete_space import DeleteSpace
from .get_attachment_info import GetAttachmentInfo
from .get_global_templates import GetGlobalTemplates
from .get_pages_by_filters import GetPagesByFilters
from .get_space_activity_log import GetSpaceActivityLog
from .get_space_labels import GetSpaceLabels
from .get_space_permissions import GetSpacePermissions
from .get_spaces_by_type import GetSpacesByType
from .get_templates_by_category import GetTemplatesByCategory
from .get_user_by_email import GetUserByEmail
from .get_user_spaces import GetUserSpaces
from .increment_label_usage_count import IncrementLabelUsageCount
from .update_page import UpdatePage

ALL_TOOLS_INTERFACE_4 = [
    AddPageLabel,
    CreateAttachment,
    CreateComment,
    CreateLabel,
    CreatePage,
    CreateSpace,
    DeleteLabel,
    DeleteSpace,
    GetAttachmentInfo,
    GetGlobalTemplates,
    GetPagesByFilters,
    GetSpaceActivityLog,
    GetSpaceLabels,
    GetSpacePermissions,
    GetSpacesByType,
    GetTemplatesByCategory,
    GetUserByEmail,
    GetUserSpaces,
    IncrementLabelUsageCount,
    UpdatePage,
]
