from .add_page_label import AddPageLabel
from .create_attachment import CreateAttachment
from .create_comment import CreateComment
from .create_page_version import CreatePageVersion
from .delete_attachment import DeleteAttachment
from .delete_comment import DeleteComment
from .get_attachment_info import GetAttachmentInfo
from .get_comment_info import GetCommentInfo
from .get_label_info import GetLabelInfo
from .get_page_attachments import GetPageAttachments
from .get_page_comments_by_thread_level import GetPageCommentsByThreadLevel
from .get_page_versions import GetPageVersions
from .get_space_pages import GetSpacePages
from .get_spaces_by_filters import GetSpacesByFilters
from .get_user_attachments import GetUserAttachments
from .get_user_by_email import GetUserByEmail
from .get_user_comments import GetUserComments
from .get_user_notifications_by_type import GetUserNotificationsByType
from .get_user_watchers import GetUserWatchers
from .remove_page_label import RemovePageLabel
from .update_comment_content import UpdateCommentContent
from .update_watcher_settings import UpdateWatcherSettings

ALL_TOOLS_INTERFACE_5 = [
    AddPageLabel,
    CreateAttachment,
    CreateComment,
    CreatePageVersion,
    DeleteAttachment,
    DeleteComment,
    GetAttachmentInfo,
    GetCommentInfo,
    GetLabelInfo,
    GetPageAttachments,
    GetPageCommentsByThreadLevel,
    GetPageVersions,
    GetSpacePages,
    GetSpacesByFilters,
    GetUserAttachments,
    GetUserByEmail,
    GetUserComments,
    GetUserNotificationsByType,
    GetUserWatchers,
    RemovePageLabel,
    UpdateCommentContent,
    UpdateWatcherSettings
]
