from .get_page_comments import GetPageComments
from .create_comment import CreateComment
from .update_comment_content import UpdateCommentContent
from .update_comment_status import UpdateCommentStatus

from .create_notification import CreateNotification
from .update_notification_delivery_method import UpdateNotificationDeliveryMethod
from .get_user_notifications import GetUserNotifications

from .create_watcher import CreateWatcher
from .delete_watcher import DeleteWatcher
from .update_watcher_settings import UpdateWatcherSettings

from .get_users_by_filters import GetUsersByFilters
from .get_user_by_email import GetUserByEmail
from .get_user_groups import GetUserGroups
from .get_user_watchers import GetUserWatchers
from .update_user_status import UpdateUserStatus

from .get_spaces_by_filters import GetSpacesByFilters
from .get_space_pages import GetSpacePages

from .get_comment_info import GetCommentInfo
from .create_attachment import CreateAttachment
from .update_notification_read_status import UpdateNotificationReadStatus



ALL_TOOLS_INTERFACE_2 = [
    GetPageComments,
    CreateComment,
    UpdateCommentContent,
    UpdateCommentStatus,

    CreateNotification,
    UpdateNotificationDeliveryMethod,
    GetUserNotifications,

    CreateWatcher,
    DeleteWatcher,
    GetUserWatchers,
    UpdateWatcherSettings,

    GetUsersByFilters,
    GetUserByEmail,
    GetUserGroups,
    UpdateUserStatus,

    GetSpacesByFilters,
    GetSpacePages,

    GetCommentInfo,
    CreateAttachment,
    UpdateNotificationReadStatus,

]
