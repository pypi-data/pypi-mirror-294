from typing import Optional
import requests

from .views import *
from .objects import *


class CaptchaResponse(object):
    """https://join-lemmy.org/api/interfaces/CaptchaResponse.html"""

    png: str = None
    wav: str = None
    uuid: str = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.png = response["png"]
        self.wav = response["wav"]
        self.uuid = response["uuid"]


class BannedPersonsResponse(object):
    """https://join-lemmy.org/api/interfaces/BannedPersonsResponse.html"""

    banned: list[PersonView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.banned = [PersonView(e) for e in response["banned"]]


class ListMediaResponse(object):
    """https://join-lemmy.org/api/interfaces/ListMediaResponse.html"""

    images: list[LocalImageView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.images = [LocalImageView(e) for e in response["images"]]


class UpdateTotpResponse(object):
    """https://join-lemmy.org/api/interfaces/UpdateTotpResponse.html"""

    enabled: bool = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.enabled = response["enabled"]


class CommentReportResponse(object):
    """https://join-lemmy.org/api/interfaces/CommentReportResponse.html"""

    comment_report_view: CommentReportView = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.comment_report_view = CommentReportView(response["comment_report_view"])


class GetCommunityResponse(object):
    """https://join-lemmy.org/api/interfaces/GetCommunityResponse.html"""

    community_view: CommunityView = None
    site: Optional[Site] = None
    moderators: list[CommunityModeratorView] = None
    discussion_languages: list[int] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.community_view = CommunityView(response["community_view"])
        if "site" in response:
            self.site = Site(response["site"])
        else:
            self.site = None
        self.moderators = [CommunityModeratorView(e) for e in response["moderators"]]
        self.discussion_languages = [int(e) for e in response["discussion_languages"]]


class GetPostsResponse(object):
    """https://join-lemmy.org/api/interfaces/GetPostsResponse.html"""

    posts: list[PostView] = None
    next_page: Optional[str] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.posts = [PostView(e) for e in response["posts"]]
        if "next_page" in response:
            self.next_page = response["next_page"]
        else:
            self.next_page = None


class CommunityResponse(object):
    """https://join-lemmy.org/api/interfaces/CommunityResponse.html"""

    community_view: CommunityView = None
    discussion_languages: list[int] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.community_view = CommunityView(response["community_view"])
        self.discussion_languages = [int(e) for e in response["discussion_languages"]]


class GetCommentsResponse(object):
    """https://join-lemmy.org/api/interfaces/GetCommentsResponse.html"""

    comments: list[CommentView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.comments = [CommentView(e) for e in response["comments"]]


class SearchResponse(object):
    """https://join-lemmy.org/api/interfaces/SearchResponse.html"""

    type_: str = None
    comments: list[CommentView] = None
    posts: list[PostView] = None
    communities: list[CommunityView] = None
    users: list[PersonView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.type_ = response["type_"]
        self.comments = [CommentView(e) for e in response["comments"]]
        self.posts = [PostView(e) for e in response["posts"]]
        self.communities = [CommunityView(e) for e in response["communities"]]
        self.users = [PersonView(e) for e in response["users"]]


class PrivateMessageResponse(object):
    """https://join-lemmy.org/api/interfaces/PrivateMessageResponse.html"""

    private_message_view: PrivateMessageView = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.private_message_view = PrivateMessageView(response["private_message_view"])


class AddModToCommunityResponse(object):
    """https://join-lemmy.org/api/interfaces/AddModToCommunityResponse.html"""

    moderators: list[CommunityModeratorView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.moderators = [CommunityModeratorView(e) for e in response["moderators"]]


class GetReportCountResponse(object):
    """https://join-lemmy.org/api/interfaces/GetReportCountResponse.html"""

    community_id: Optional[int] = None
    comment_reports: int = None
    post_reports: int = None
    private_message_reports: Optional[int] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        if "community_id" in response:
            self.community_id = response["community_id"]
        else:
            self.community_id = None
        self.comment_reports = response["comment_reports"]
        self.post_reports = response["post_reports"]
        if "private_message_reports" in response:
            self.private_message_reports = response["private_message_reports"]
        else:
            self.private_message_reports = None


class PostReportResponse(object):
    """https://join-lemmy.org/api/interfaces/PostReportResponse.html"""

    post_report_view: PostReportView = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.post_report_view = PostReportView(response["post_report_view"])


class RegistrationApplicationResponse(object):
    """https://join-lemmy.org/api/interfaces/RegistrationApplicationResponse.html"""

    registration_application: RegistrationApplicationView = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.registration_application = RegistrationApplicationView(response["registration_application"])


class GetSiteResponse(object):
    """https://join-lemmy.org/api/interfaces/GetSiteResponse.html"""

    site_view: SiteView = None
    admins: list[PersonView] = None
    version: str = None
    my_user: Optional[MyUserInfo] = None
    all_languages: list[Language] = None
    discussion_languages: list[int] = None
    taglines: list[Tagline] = None
    custom_emojis: list[CustomEmojiView] = None
    blocked_urls: list[LocalSiteUrlBlocklist] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.site_view = SiteView(response["site_view"])
        self.admins = [PersonView(e) for e in response["admins"]]
        self.version = response["version"]
        if "my_user" in response:
            self.my_user = MyUserInfo(response["my_user"])
        else:
            self.my_user = None
        self.all_languages = [Language(e) for e in response["all_languages"]]
        self.discussion_languages = [int(e) for e in response["discussion_languages"]]
        self.taglines = [Tagline(e) for e in response["taglines"]]
        self.custom_emojis = [CustomEmojiView(e) for e in response["custom_emojis"]]
        self.blocked_urls = [LocalSiteUrlBlocklist(e) for e in response["blocked_urls"]]


class GetCaptchaResponse(object):
    """https://join-lemmy.org/api/interfaces/GetCaptchaResponse.html"""

    ok: Optional[CaptchaResponse] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        if "ok" in response:
            self.ok = CaptchaResponse(response["ok"])
        else:
            self.ok = None


class PersonMentionResponse(object):
    """https://join-lemmy.org/api/interfaces/PersonMentionResponse.html"""

    person_mention_view: PersonMentionView = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.person_mention_view = PersonMentionView(response["person_mention_view"])


class GetModlogResponse(object):
    """https://join-lemmy.org/api/interfaces/GetModlogResponse.html"""

    removed_posts: list[ModRemovePostView] = None
    locked_posts: list[ModLockPostView] = None
    featured_posts: list[ModFeaturePostView] = None
    removed_comments: list[ModRemoveCommentView] = None
    removed_communities: list[ModRemoveCommunityView] = None
    banned_from_community: list[ModBanFromCommunityView] = None
    banned: list[ModBanView] = None
    added_to_community: list[ModAddCommunityView] = None
    transferred_to_community: list[ModTransferCommunityView] = None
    added: list[ModAddView] = None
    admin_purged_persons: list[AdminPurgePersonView] = None
    admin_purged_communities: list[AdminPurgeCommunityView] = None
    admin_purged_posts: list[AdminPurgePostView] = None
    admin_purged_comments: list[AdminPurgeCommentView] = None
    hidden_communities: list[ModHideCommunityView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.removed_posts = [ModRemovePostView(e) for e in response["removed_posts"]]
        self.locked_posts = [ModLockPostView(e) for e in response["locked_posts"]]
        self.featured_posts = [ModFeaturePostView(e) for e in response["featured_posts"]]
        self.removed_comments = [ModRemoveCommentView(e) for e in response["removed_comments"]]
        self.removed_communities = [ModRemoveCommunityView(e) for e in response["removed_communities"]]
        self.banned_from_community = [ModBanFromCommunityView(e) for e in response["banned_from_community"]]
        self.banned = [ModBanView(e) for e in response["banned"]]
        self.added_to_community = [ModAddCommunityView(e) for e in response["added_to_community"]]
        self.transferred_to_community = [ModTransferCommunityView(e) for e in response["transferred_to_community"]]
        self.added = [ModAddView(e) for e in response["added"]]
        self.admin_purged_persons = [AdminPurgePersonView(e) for e in response["admin_purged_persons"]]
        self.admin_purged_communities = [AdminPurgeCommunityView(e) for e in response["admin_purged_communities"]]
        self.admin_purged_posts = [AdminPurgePostView(e) for e in response["admin_purged_posts"]]
        self.admin_purged_comments = [AdminPurgeCommentView(e) for e in response["admin_purged_comments"]]
        self.hidden_communities = [ModHideCommunityView(e) for e in response["hidden_communities"]]


class SuccessResponse(object):
    """https://join-lemmy.org/api/interfaces/SuccessResponse.html"""

    success: bool = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.success = response["success"]


class ListRegistrationApplicationsResponse(object):
    """https://join-lemmy.org/api/interfaces/ListRegistrationApplicationsResponse.html"""

    registration_applications: list[RegistrationApplicationView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.registration_applications = [RegistrationApplicationView(e) for e in response["registration_applications"]]


class BlockInstanceResponse(object):
    """https://join-lemmy.org/api/interfaces/BlockInstanceResponse.html"""

    blocked: bool = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.blocked = response["blocked"]


class ResolveObjectResponse(object):
    """https://join-lemmy.org/api/interfaces/ResolveObjectResponse.html"""

    comment: Optional[CommentView] = None
    post: Optional[PostView] = None
    community: Optional[CommunityView] = None
    person: Optional[PersonView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        if "comment" in response:
            self.comment = CommentView(response["comment"])
        else:
            self.comment = None
        if "post" in response:
            self.post = PostView(response["post"])
        else:
            self.post = None
        if "community" in response:
            self.community = CommunityView(response["community"])
        else:
            self.community = None
        if "person" in response:
            self.person = PersonView(response["person"])
        else:
            self.person = None


class PrivateMessageReportResponse(object):
    """https://join-lemmy.org/api/interfaces/PrivateMessageReportResponse.html"""

    private_message_report_view: PrivateMessageReportView = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.private_message_report_view = PrivateMessageReportView(response["private_message_report_view"])


class SiteResponse(object):
    """https://join-lemmy.org/api/interfaces/SiteResponse.html"""

    site_view: SiteView = None
    taglines: list[Tagline] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.site_view = SiteView(response["site_view"])
        self.taglines = [Tagline(e) for e in response["taglines"]]


class ListPostReportsResponse(object):
    """https://join-lemmy.org/api/interfaces/ListPostReportsResponse.html"""

    post_reports: list[PostReportView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.post_reports = [PostReportView(e) for e in response["post_reports"]]


class BlockCommunityResponse(object):
    """https://join-lemmy.org/api/interfaces/BlockCommunityResponse.html"""

    community_view: CommunityView = None
    blocked: bool = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.community_view = CommunityView(response["community_view"])
        self.blocked = response["blocked"]


class PrivateMessagesResponse(object):
    """https://join-lemmy.org/api/interfaces/PrivateMessagesResponse.html"""

    private_messages: list[PrivateMessageView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.private_messages = [PrivateMessageView(e) for e in response["private_messages"]]


class LoginResponse(object):
    """https://join-lemmy.org/api/interfaces/LoginResponse.html"""

    jwt: Optional[str] = None
    registration_created: bool = None
    verify_email_sent: bool = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        if "jwt" in response:
            self.jwt = response["jwt"]
        else:
            self.jwt = None
        self.registration_created = response["registration_created"]
        self.verify_email_sent = response["verify_email_sent"]


class GetUnreadCountResponse(object):
    """https://join-lemmy.org/api/interfaces/GetUnreadCountResponse.html"""

    replies: int = None
    mentions: int = None
    private_messages: int = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.replies = response["replies"]
        self.mentions = response["mentions"]
        self.private_messages = response["private_messages"]


class BanFromCommunityResponse(object):
    """https://join-lemmy.org/api/interfaces/BanFromCommunityResponse.html"""

    person_view: PersonView = None
    banned: bool = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.person_view = PersonView(response["person_view"])
        self.banned = response["banned"]


class CommentReplyResponse(object):
    """https://join-lemmy.org/api/interfaces/CommentReplyResponse.html"""

    comment_reply_view: CommentReplyView = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.comment_reply_view = CommentReplyView(response["comment_reply_view"])


class ListPostLikesResponse(object):
    """https://join-lemmy.org/api/interfaces/ListPostLikesResponse.html"""

    post_likes: list[VoteView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.post_likes = [VoteView(e) for e in response["post_likes"]]


class ListCommentReportsResponse(object):
    """https://join-lemmy.org/api/interfaces/ListCommentReportsResponse.html"""

    comment_reports: list[CommentReportView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.comment_reports = [CommentReportView(e) for e in response["comment_reports"]]


class GetSiteMetadataResponse(object):
    """https://join-lemmy.org/api/interfaces/GetSiteMetadataResponse.html"""

    metadata: LinkMetadata = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.metadata = LinkMetadata(response["metadata"])


class BanPersonResponse(object):
    """https://join-lemmy.org/api/interfaces/BanPersonResponse.html"""

    person_view: PersonView = None
    banned: bool = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.person_view = PersonView(response["person_view"])
        self.banned = response["banned"]


class CommentResponse(object):
    """https://join-lemmy.org/api/interfaces/CommentResponse.html"""

    comment_view: CommentView = None
    recipient_ids: list[int] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.comment_view = CommentView(response["comment_view"])
        self.recipient_ids = [int(e) for e in response["recipient_ids"]]


class GetRepliesResponse(object):
    """https://join-lemmy.org/api/interfaces/GetRepliesResponse.html"""

    replies: list[CommentReplyView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.replies = [CommentReplyView(e) for e in response["replies"]]


class GetUnreadRegistrationApplicationCountResponse(object):
    """https://join-lemmy.org/api/interfaces/GetUnreadRegistrationApplicationCountResponse.html"""

    registration_applications: int = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.registration_applications = response["registration_applications"]


class CustomEmojiResponse(object):
    """https://join-lemmy.org/api/interfaces/CustomEmojiResponse.html"""

    custom_emoji: CustomEmojiView = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.custom_emoji = CustomEmojiView(response["custom_emoji"])


class GetPersonDetailsResponse(object):
    """https://join-lemmy.org/api/interfaces/GetPersonDetailsResponse.html"""

    person_view: PersonView = None
    site: Optional[Site] = None
    comments: list[CommentView] = None
    posts: list[PostView] = None
    moderates: list[CommunityModeratorView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.person_view = PersonView(response["person_view"])
        if "site" in response:
            self.site = Site(response["site"])
        else:
            self.site = None
        self.comments = [CommentView(e) for e in response["comments"]]
        self.posts = [PostView(e) for e in response["posts"]]
        self.moderates = [CommunityModeratorView(e) for e in response["moderates"]]


class ListCommunitiesResponse(object):
    """https://join-lemmy.org/api/interfaces/ListCommunitiesResponse.html"""

    communities: list[CommunityView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.communities = [CommunityView(e) for e in response["communities"]]


class GetPersonMentionsResponse(object):
    """https://join-lemmy.org/api/interfaces/GetPersonMentionsResponse.html"""

    mentions: list[PersonMentionView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.mentions = [PersonMentionView(e) for e in response["mentions"]]


class AddAdminResponse(object):
    """https://join-lemmy.org/api/interfaces/AddAdminResponse.html"""

    admins: list[PersonView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.admins = [PersonView(e) for e in response["admins"]]


class GetFederatedInstancesResponse(object):
    """https://join-lemmy.org/api/interfaces/GetFederatedInstancesResponse.html"""

    federated_instances: Optional[FederatedInstances] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        if "federated_instances" in response:
            self.federated_instances = FederatedInstances(response["federated_instances"])
        else:
            self.federated_instances = None


class PostResponse(object):
    """https://join-lemmy.org/api/interfaces/PostResponse.html"""

    post_view: PostView = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.post_view = PostView(response["post_view"])


class GenerateTotpSecretResponse(object):
    """https://join-lemmy.org/api/interfaces/GenerateTotpSecretResponse.html"""

    totp_secret_url: str = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.totp_secret_url = response["totp_secret_url"]


class ListPrivateMessageReportsResponse(object):
    """https://join-lemmy.org/api/interfaces/ListPrivateMessageReportsResponse.html"""

    private_message_reports: list[PrivateMessageReportView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.private_message_reports = [PrivateMessageReportView(e) for e in response["private_message_reports"]]


class BlockPersonResponse(object):
    """https://join-lemmy.org/api/interfaces/BlockPersonResponse.html"""

    person_view: PersonView = None
    blocked: bool = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.person_view = PersonView(response["person_view"])
        self.blocked = response["blocked"]


class GetPostResponse(object):
    """https://join-lemmy.org/api/interfaces/GetPostResponse.html"""

    post_view: PostView = None
    community_view: CommunityView = None
    moderators: list[CommunityModeratorView] = None
    cross_posts: list[PostView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.post_view = PostView(response["post_view"])
        self.community_view = CommunityView(response["community_view"])
        self.moderators = [CommunityModeratorView(e) for e in response["moderators"]]
        self.cross_posts = [PostView(e) for e in response["cross_posts"]]


class ListCommentLikesResponse(object):
    """https://join-lemmy.org/api/interfaces/ListCommentLikesResponse.html"""

    comment_likes: list[VoteView] = None

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
        self.comment_likes = [VoteView(e) for e in response["comment_likes"]]
