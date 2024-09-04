from typing import Optional

from .objects import *
from .utils import call_with_filtered_kwargs


class ViewObject(object):
    """ ViewObject: parent object to all view-related objects """

    def __init__(self, view: dict) -> None:
        self._view = view
        self.parse()


class LocalUserView(ViewObject):
    local_user: LocalUser = None
    local_user_vote_display_mode: LocalUserVoteDisplayMode = None
    person: Person = None
    counts: PersonAggregates = None

    def parse(self) -> None:
        self.local_user = call_with_filtered_kwargs(LocalUser, self._view["local_user"])
        self.local_user_vote_display_mode = call_with_filtered_kwargs(LocalUserVoteDisplayMode, self._view["local_user_vote_display_mode"])
        self.person = call_with_filtered_kwargs(Person, self._view["person"])
        self.counts = call_with_filtered_kwargs(PersonAggregates, self._view["counts"])


class CommentReplyView(ViewObject):
    comment_reply: CommentReply = None
    comment: Comment = None
    creator: Person = None
    post: Post = None
    community: Community = None
    recipient: Person = None
    counts: CommentAggregates = None
    creator_banned_from_community: bool = None
    banned_from_community: bool = None
    creator_is_moderator: bool = None
    creator_is_admin: bool = None
    subscribed: str = None
    saved: bool = None
    creator_blocked: bool = None
    my_vote: Optional[int] = None

    def parse(self) -> None:
        self.comment_reply = call_with_filtered_kwargs(CommentReply, self._view["comment_reply"])
        self.comment = call_with_filtered_kwargs(Comment, self._view["comment"])
        self.creator = call_with_filtered_kwargs(Person, self._view["creator"])
        self.post = call_with_filtered_kwargs(Post, self._view["post"])
        self.community = call_with_filtered_kwargs(Community, self._view["community"])
        self.recipient = call_with_filtered_kwargs(Person, self._view["recipient"])
        self.counts = call_with_filtered_kwargs(CommentAggregates, self._view["counts"])
        self.creator_banned_from_community = self._view["creator_banned_from_community"]
        self.banned_from_community = self._view["banned_from_community"]
        self.creator_is_moderator = self._view["creator_is_moderator"]
        self.creator_is_admin = self._view["creator_is_admin"]
        self.subscribed = self._view["subscribed"]
        self.saved = self._view["saved"]
        self.creator_blocked = self._view["creator_blocked"]
        if "my_vote" in self._view.keys():
            self.my_vote = self._view["my_vote"]
        else:
            self.my_vote = None


class CommunityFollowerView(ViewObject):
    community: Community = None
    follower: Person = None

    def parse(self) -> None:
        self.community = call_with_filtered_kwargs(Community, self._view["community"])
        self.follower = call_with_filtered_kwargs(Person, self._view["follower"])


class VoteView(ViewObject):
    creator: Person = None
    creator_banned_from_community: bool = None
    score: int = None

    def parse(self) -> None:
        self.creator = call_with_filtered_kwargs(Person, self._view["creator"])
        self.creator_banned_from_community = self._view["creator_banned_from_community"]
        self.score = self._view["score"]


class PrivateMessageReportView(ViewObject):
    private_message_report: PrivateMessageReport = None
    private_message: PrivateMessage = None
    private_message_creator: Person = None
    creator: Person = None
    resolver: Optional[Person] = None

    def parse(self) -> None:
        self.private_message_report = call_with_filtered_kwargs(PrivateMessageReport, self._view["private_message_report"])
        self.private_message = call_with_filtered_kwargs(PrivateMessage, self._view["private_message"])
        self.private_message_creator = call_with_filtered_kwargs(Person, self._view["private_message_creator"])
        self.creator = call_with_filtered_kwargs(Person, self._view["creator"])
        if "resolver" in self._view.keys():
            self.resolver = call_with_filtered_kwargs(Person, self._view["resolver"])
        else:
            self.resolver = None


class ModAddView(ViewObject):
    mod_add: ModAdd = None
    moderator: Optional[Person] = None
    modded_person: Person = None

    def parse(self) -> None:
        self.mod_add = call_with_filtered_kwargs(ModAdd, self._view["mod_add"])
        if "moderator" in self._view.keys():
            self.moderator = call_with_filtered_kwargs(Person, self._view["moderator"])
        else:
            self.moderator = None
        self.modded_person = call_with_filtered_kwargs(Person, self._view["modded_person"])


class PersonView(ViewObject):
    person: Person = None
    counts: PersonAggregates = None
    is_admin: bool = None

    def parse(self) -> None:
        self.person = call_with_filtered_kwargs(Person, self._view["person"])
        self.counts = call_with_filtered_kwargs(PersonAggregates, self._view["counts"])
        self.is_admin = self._view["is_admin"]


class ModBanView(ViewObject):
    mod_ban: ModBan = None
    moderator: Optional[Person] = None
    banned_person: Person = None

    def parse(self) -> None:
        self.mod_ban = call_with_filtered_kwargs(ModBan, self._view["mod_ban"])
        if "moderator" in self._view.keys():
            self.moderator = call_with_filtered_kwargs(Person, self._view["moderator"])
        else:
            self.moderator = None
        self.banned_person = call_with_filtered_kwargs(Person, self._view["banned_person"])


class RegistrationApplicationView(ViewObject):
    registration_application: RegistrationApplication = None
    creator_local_user: LocalUser = None
    creator: Person = None
    admin: Optional[Person] = None

    def parse(self) -> None:
        self.registration_application = call_with_filtered_kwargs(RegistrationApplication, self._view["registration_application"])
        self.creator_local_user = call_with_filtered_kwargs(LocalUser, self._view["creator_local_user"])
        self.creator = call_with_filtered_kwargs(Person, self._view["creator"])
        if "admin" in self._view.keys():
            self.admin = call_with_filtered_kwargs(Person, self._view["admin"])
        else:
            self.admin = None


class CommunityBlockView(ViewObject):
    person: Person = None
    community: Community = None

    def parse(self) -> None:
        self.person = call_with_filtered_kwargs(Person, self._view["person"])
        self.community = call_with_filtered_kwargs(Community, self._view["community"])


class ModBanFromCommunityView(ViewObject):
    mod_ban_from_community: ModBanFromCommunity = None
    moderator: Optional[Person] = None
    community: Community = None
    banned_person: Person = None

    def parse(self) -> None:
        self.mod_ban_from_community = call_with_filtered_kwargs(ModBanFromCommunity, self._view["mod_ban_from_community"])
        if "moderator" in self._view.keys():
            self.moderator = call_with_filtered_kwargs(Person, self._view["moderator"])
        else:
            self.moderator = None
        self.community = call_with_filtered_kwargs(Community, self._view["community"])
        self.banned_person = call_with_filtered_kwargs(Person, self._view["banned_person"])


class PostView(ViewObject):
    post: Post = None
    creator: Person = None
    community: Community = None
    image_details: Optional[ImageDetails] = None
    creator_banned_from_community: bool = None
    banned_from_community: bool = None
    creator_is_moderator: bool = None
    creator_is_admin: bool = None
    counts: PostAggregates = None
    subscribed: str = None
    saved: bool = None
    read: bool = None
    hidden: bool = None
    creator_blocked: bool = None
    my_vote: Optional[int] = None
    unread_comments: int = None

    def parse(self) -> None:
        self.post = call_with_filtered_kwargs(Post, self._view["post"])
        self.creator = call_with_filtered_kwargs(Person, self._view["creator"])
        self.community = call_with_filtered_kwargs(Community, self._view["community"])
        if "image_details" in self._view.keys():
            self.image_details = call_with_filtered_kwargs(ImageDetails, self._view["image_details"])
        else:
            self.image_details = None
        self.creator_banned_from_community = self._view["creator_banned_from_community"]
        self.banned_from_community = self._view["banned_from_community"]
        self.creator_is_moderator = self._view["creator_is_moderator"]
        self.creator_is_admin = self._view["creator_is_admin"]
        self.counts = call_with_filtered_kwargs(PostAggregates, self._view["counts"])
        self.subscribed = self._view["subscribed"]
        self.saved = self._view["saved"]
        self.read = self._view["read"]
        self.hidden = self._view["hidden"]
        self.creator_blocked = self._view["creator_blocked"]
        if "my_vote" in self._view.keys():
            self.my_vote = self._view["my_vote"]
        else:
            self.my_vote = None
        self.unread_comments = self._view["unread_comments"]


class InstanceBlockView(ViewObject):
    person: Person = None
    instance: Instance = None
    site: Optional[Site] = None

    def parse(self) -> None:
        self.person = call_with_filtered_kwargs(Person, self._view["person"])
        self.instance = call_with_filtered_kwargs(Instance, self._view["instance"])
        if "site" in self._view.keys():
            self.site = call_with_filtered_kwargs(Site, self._view["site"])
        else:
            self.site = None


class ModRemoveCommunityView(ViewObject):
    mod_remove_community: ModRemoveCommunity = None
    moderator: Optional[Person] = None
    community: Community = None

    def parse(self) -> None:
        self.mod_remove_community = call_with_filtered_kwargs(ModRemoveCommunity, self._view["mod_remove_community"])
        if "moderator" in self._view.keys():
            self.moderator = call_with_filtered_kwargs(Person, self._view["moderator"])
        else:
            self.moderator = None
        self.community = call_with_filtered_kwargs(Community, self._view["community"])


class ModHideCommunityView(ViewObject):
    mod_hide_community: ModHideCommunity = None
    admin: Optional[Person] = None
    community: Community = None

    def parse(self) -> None:
        self.mod_hide_community = call_with_filtered_kwargs(ModHideCommunity, self._view["mod_hide_community"])
        if "admin" in self._view.keys():
            self.admin = call_with_filtered_kwargs(Person, self._view["admin"])
        else:
            self.admin = None
        self.community = call_with_filtered_kwargs(Community, self._view["community"])


class ModRemoveCommentView(ViewObject):
    mod_remove_comment: ModRemoveComment = None
    moderator: Optional[Person] = None
    comment: Comment = None
    commenter: Person = None
    post: Post = None
    community: Community = None

    def parse(self) -> None:
        self.mod_remove_comment = call_with_filtered_kwargs(ModRemoveComment, self._view["mod_remove_comment"])
        if "moderator" in self._view.keys():
            self.moderator = call_with_filtered_kwargs(Person, self._view["moderator"])
        else:
            self.moderator = None
        self.comment = call_with_filtered_kwargs(Comment, self._view["comment"])
        self.commenter = call_with_filtered_kwargs(Person, self._view["commenter"])
        self.post = call_with_filtered_kwargs(Post, self._view["post"])
        self.community = call_with_filtered_kwargs(Community, self._view["community"])


class AdminPurgeCommentView(ViewObject):
    admin_purge_comment: AdminPurgeComment = None
    admin: Optional[Person] = None
    post: Post = None

    def parse(self) -> None:
        self.admin_purge_comment = call_with_filtered_kwargs(AdminPurgeComment, self._view["admin_purge_comment"])
        if "admin" in self._view.keys():
            self.admin = call_with_filtered_kwargs(Person, self._view["admin"])
        else:
            self.admin = None
        self.post = call_with_filtered_kwargs(Post, self._view["post"])


class ModAddCommunityView(ViewObject):
    mod_add_community: ModAddCommunity = None
    moderator: Optional[Person] = None
    community: Community = None
    modded_person: Person = None

    def parse(self) -> None:
        self.mod_add_community = call_with_filtered_kwargs(ModAddCommunity, self._view["mod_add_community"])
        if "moderator" in self._view.keys():
            self.moderator = call_with_filtered_kwargs(Person, self._view["moderator"])
        else:
            self.moderator = None
        self.community = call_with_filtered_kwargs(Community, self._view["community"])
        self.modded_person = call_with_filtered_kwargs(Person, self._view["modded_person"])


class PersonBlockView(ViewObject):
    person: Person = None
    target: Person = None

    def parse(self) -> None:
        self.person = call_with_filtered_kwargs(Person, self._view["person"])
        self.target = call_with_filtered_kwargs(Person, self._view["target"])


class CommunityModeratorView(ViewObject):
    community: Community = None
    moderator: Person = None

    def parse(self) -> None:
        self.community = call_with_filtered_kwargs(Community, self._view["community"])
        self.moderator = call_with_filtered_kwargs(Person, self._view["moderator"])


class ModFeaturePostView(ViewObject):
    mod_feature_post: ModFeaturePost = None
    moderator: Optional[Person] = None
    post: Post = None
    community: Community = None

    def parse(self) -> None:
        self.mod_feature_post = call_with_filtered_kwargs(ModFeaturePost, self._view["mod_feature_post"])
        if "moderator" in self._view.keys():
            self.moderator = call_with_filtered_kwargs(Person, self._view["moderator"])
        else:
            self.moderator = None
        self.post = call_with_filtered_kwargs(Post, self._view["post"])
        self.community = call_with_filtered_kwargs(Community, self._view["community"])


class PrivateMessageView(ViewObject):
    private_message: PrivateMessage = None
    creator: Person = None
    recipient: Person = None

    def parse(self) -> None:
        self.private_message = call_with_filtered_kwargs(PrivateMessage, self._view["private_message"])
        self.creator = call_with_filtered_kwargs(Person, self._view["creator"])
        self.recipient = call_with_filtered_kwargs(Person, self._view["recipient"])


class SiteView(ViewObject):
    site: Site = None
    local_site: LocalSite = None
    local_site_rate_limit: LocalSiteRateLimit = None
    counts: SiteAggregates = None

    def parse(self) -> None:
        self.site = call_with_filtered_kwargs(Site, self._view["site"])
        self.local_site = call_with_filtered_kwargs(LocalSite, self._view["local_site"])
        self.local_site_rate_limit = call_with_filtered_kwargs(LocalSiteRateLimit, self._view["local_site_rate_limit"])
        self.counts = call_with_filtered_kwargs(SiteAggregates, self._view["counts"])


class ModLockPostView(ViewObject):
    mod_lock_post: ModLockPost = None
    moderator: Optional[Person] = None
    post: Post = None
    community: Community = None

    def parse(self) -> None:
        self.mod_lock_post = call_with_filtered_kwargs(ModLockPost, self._view["mod_lock_post"])
        if "moderator" in self._view.keys():
            self.moderator = call_with_filtered_kwargs(Person, self._view["moderator"])
        else:
            self.moderator = None
        self.post = call_with_filtered_kwargs(Post, self._view["post"])
        self.community = call_with_filtered_kwargs(Community, self._view["community"])


class MyUserInfo(ViewObject):
    local_user_view: LocalUserView = None
    follows: list[CommunityFollowerView] = None
    moderates: list[CommunityModeratorView] = None
    community_blocks: list[CommunityBlockView] = None
    instance_blocks: list[InstanceBlockView] = None
    person_blocks: list[PersonBlockView] = None
    discussion_languages: list[int] = None

    def parse(self) -> None:
        self.local_user_view = call_with_filtered_kwargs(LocalUserView, self._view["local_user_view"])
        self.follows = [call_with_filtered_kwargs(CommunityFollowerView, e) for e in self._view["follows"]]
        self.moderates = [call_with_filtered_kwargs(CommunityModeratorView, e) for e in self._view["moderates"]]
        self.community_blocks = [call_with_filtered_kwargs(CommunityBlockView, e) for e in self._view["community_blocks"]]
        self.instance_blocks = [call_with_filtered_kwargs(InstanceBlockView, e) for e in self._view["instance_blocks"]]
        self.person_blocks = [call_with_filtered_kwargs(PersonBlockView, e) for e in self._view["person_blocks"]]
        self.discussion_languages = [call_with_filtered_kwargs(int, e) for e in self._view["discussion_languages"]]


class AdminPurgePersonView(ViewObject):
    admin_purge_person: AdminPurgePerson = None
    admin: Optional[Person] = None

    def parse(self) -> None:
        self.admin_purge_person = call_with_filtered_kwargs(AdminPurgePerson, self._view["admin_purge_person"])
        if "admin" in self._view.keys():
            self.admin = call_with_filtered_kwargs(Person, self._view["admin"])
        else:
            self.admin = None


class CommentReportView(ViewObject):
    comment_report: CommentReport = None
    comment: Comment = None
    post: Post = None
    community: Community = None
    creator: Person = None
    comment_creator: Person = None
    counts: CommentAggregates = None
    creator_banned_from_community: bool = None
    creator_is_moderator: bool = None
    creator_is_admin: bool = None
    creator_blocked: bool = None
    subscribed: str = None
    saved: bool = None
    my_vote: Optional[int] = None
    resolver: Optional[Person] = None

    def parse(self) -> None:
        self.comment_report = call_with_filtered_kwargs(CommentReport, self._view["comment_report"])
        self.comment = call_with_filtered_kwargs(Comment, self._view["comment"])
        self.post = call_with_filtered_kwargs(Post, self._view["post"])
        self.community = call_with_filtered_kwargs(Community, self._view["community"])
        self.creator = call_with_filtered_kwargs(Person, self._view["creator"])
        self.comment_creator = call_with_filtered_kwargs(Person, self._view["comment_creator"])
        self.counts = call_with_filtered_kwargs(CommentAggregates, self._view["counts"])
        self.creator_banned_from_community = self._view["creator_banned_from_community"]
        self.creator_is_moderator = self._view["creator_is_moderator"]
        self.creator_is_admin = self._view["creator_is_admin"]
        self.creator_blocked = self._view["creator_blocked"]
        self.subscribed = self._view["subscribed"]
        self.saved = self._view["saved"]
        if "my_vote" in self._view.keys():
            self.my_vote = self._view["my_vote"]
        else:
            self.my_vote = None
        if "resolver" in self._view.keys():
            self.resolver = call_with_filtered_kwargs(Person, self._view["resolver"])
        else:
            self.resolver = None


class ModRemovePostView(ViewObject):
    mod_remove_post: ModRemovePost = None
    moderator: Optional[Person] = None
    post: Post = None
    community: Community = None

    def parse(self) -> None:
        self.mod_remove_post = call_with_filtered_kwargs(ModRemovePost, self._view["mod_remove_post"])
        if "moderator" in self._view.keys():
            self.moderator = call_with_filtered_kwargs(Person, self._view["moderator"])
        else:
            self.moderator = None
        self.post = call_with_filtered_kwargs(Post, self._view["post"])
        self.community = call_with_filtered_kwargs(Community, self._view["community"])


class CommunityView(ViewObject):
    community: Community = None
    subscribed: str = None
    blocked: bool = None
    counts: CommunityAggregates = None
    banned_from_community: bool = None

    def parse(self) -> None:
        self.community = call_with_filtered_kwargs(Community, self._view["community"])
        self.subscribed = self._view["subscribed"]
        self.blocked = self._view["blocked"]
        self.counts = call_with_filtered_kwargs(CommunityAggregates, self._view["counts"])
        self.banned_from_community = self._view["banned_from_community"]


class AdminPurgeCommunityView(ViewObject):
    admin_purge_community: AdminPurgeCommunity = None
    admin: Optional[Person] = None

    def parse(self) -> None:
        self.admin_purge_community = call_with_filtered_kwargs(AdminPurgeCommunity, self._view["admin_purge_community"])
        if "admin" in self._view.keys():
            self.admin = call_with_filtered_kwargs(Person, self._view["admin"])
        else:
            self.admin = None


class AdminPurgePostView(ViewObject):
    admin_purge_post: AdminPurgePost = None
    admin: Optional[Person] = None
    community: Community = None

    def parse(self) -> None:
        self.admin_purge_post = call_with_filtered_kwargs(AdminPurgePost, self._view["admin_purge_post"])
        if "admin" in self._view.keys():
            self.admin = call_with_filtered_kwargs(Person, self._view["admin"])
        else:
            self.admin = None
        self.community = call_with_filtered_kwargs(Community, self._view["community"])


class ModTransferCommunityView(ViewObject):
    mod_transfer_community: ModTransferCommunity = None
    moderator: Optional[Person] = None
    community: Community = None
    modded_person: Person = None

    def parse(self) -> None:
        self.mod_transfer_community = call_with_filtered_kwargs(ModTransferCommunity, self._view["mod_transfer_community"])
        if "moderator" in self._view.keys():
            self.moderator = call_with_filtered_kwargs(Person, self._view["moderator"])
        else:
            self.moderator = None
        self.community = call_with_filtered_kwargs(Community, self._view["community"])
        self.modded_person = call_with_filtered_kwargs(Person, self._view["modded_person"])


class LocalImageView(ViewObject):
    local_image: LocalImage = None
    person: Person = None

    def parse(self) -> None:
        self.local_image = call_with_filtered_kwargs(LocalImage, self._view["local_image"])
        self.person = call_with_filtered_kwargs(Person, self._view["person"])


class PersonMentionView(ViewObject):
    person_mention: PersonMention = None
    comment: Comment = None
    creator: Person = None
    post: Post = None
    community: Community = None
    recipient: Person = None
    counts: CommentAggregates = None
    creator_banned_from_community: bool = None
    banned_from_community: bool = None
    creator_is_moderator: bool = None
    creator_is_admin: bool = None
    subscribed: str = None
    saved: bool = None
    creator_blocked: bool = None
    my_vote: Optional[int] = None

    def parse(self) -> None:
        self.person_mention = call_with_filtered_kwargs(PersonMention, self._view["person_mention"])
        self.comment = call_with_filtered_kwargs(Comment, self._view["comment"])
        self.creator = call_with_filtered_kwargs(Person, self._view["creator"])
        self.post = call_with_filtered_kwargs(Post, self._view["post"])
        self.community = call_with_filtered_kwargs(Community, self._view["community"])
        self.recipient = call_with_filtered_kwargs(Person, self._view["recipient"])
        self.counts = call_with_filtered_kwargs(CommentAggregates, self._view["counts"])
        self.creator_banned_from_community = self._view["creator_banned_from_community"]
        self.banned_from_community = self._view["banned_from_community"]
        self.creator_is_moderator = self._view["creator_is_moderator"]
        self.creator_is_admin = self._view["creator_is_admin"]
        self.subscribed = self._view["subscribed"]
        self.saved = self._view["saved"]
        self.creator_blocked = self._view["creator_blocked"]
        if "my_vote" in self._view.keys():
            self.my_vote = self._view["my_vote"]
        else:
            self.my_vote = None


class CustomEmojiView(ViewObject):
    custom_emoji: CustomEmoji = None
    keywords: list[CustomEmojiKeyword] = None

    def parse(self) -> None:
        self.custom_emoji = call_with_filtered_kwargs(CustomEmoji, self._view["custom_emoji"])
        self.keywords = [call_with_filtered_kwargs(CustomEmojiKeyword, e) for e in self._view["keywords"]]


class CommentView(ViewObject):
    comment: Comment = None
    creator: Person = None
    post: Post = None
    community: Community = None
    counts: CommentAggregates = None
    creator_banned_from_community: bool = None
    banned_from_community: bool = None
    creator_is_moderator: bool = None
    creator_is_admin: bool = None
    subscribed: str = None
    saved: bool = None
    creator_blocked: bool = None
    my_vote: Optional[int] = None

    def parse(self) -> None:
        self.comment = call_with_filtered_kwargs(Comment, self._view["comment"])
        self.creator = call_with_filtered_kwargs(Person, self._view["creator"])
        self.post = call_with_filtered_kwargs(Post, self._view["post"])
        self.community = call_with_filtered_kwargs(Community, self._view["community"])
        self.counts = call_with_filtered_kwargs(CommentAggregates, self._view["counts"])
        self.creator_banned_from_community = self._view["creator_banned_from_community"]
        self.banned_from_community = self._view["banned_from_community"]
        self.creator_is_moderator = self._view["creator_is_moderator"]
        self.creator_is_admin = self._view["creator_is_admin"]
        self.subscribed = self._view["subscribed"]
        self.saved = self._view["saved"]
        self.creator_blocked = self._view["creator_blocked"]
        if "my_vote" in self._view.keys():
            self.my_vote = self._view["my_vote"]
        else:
            self.my_vote = None


class PostReportView(ViewObject):
    post_report: PostReport = None
    post: Post = None
    community: Community = None
    creator: Person = None
    post_creator: Person = None
    creator_banned_from_community: bool = None
    creator_is_moderator: bool = None
    creator_is_admin: bool = None
    subscribed: str = None
    saved: bool = None
    read: bool = None
    hidden: bool = None
    creator_blocked: bool = None
    my_vote: Optional[int] = None
    unread_comments: int = None
    counts: PostAggregates = None
    resolver: Optional[Person] = None

    def parse(self) -> None:
        self.post_report = call_with_filtered_kwargs(PostReport, self._view["post_report"])
        self.post = call_with_filtered_kwargs(Post, self._view["post"])
        self.community = call_with_filtered_kwargs(Community, self._view["community"])
        self.creator = call_with_filtered_kwargs(Person, self._view["creator"])
        self.post_creator = call_with_filtered_kwargs(Person, self._view["post_creator"])
        self.creator_banned_from_community = self._view["creator_banned_from_community"]
        self.creator_is_moderator = self._view["creator_is_moderator"]
        self.creator_is_admin = self._view["creator_is_admin"]
        self.subscribed = self._view["subscribed"]
        self.saved = self._view["saved"]
        self.read = self._view["read"]
        self.hidden = self._view["hidden"]
        self.creator_blocked = self._view["creator_blocked"]
        if "my_vote" in self._view.keys():
            self.my_vote = self._view["my_vote"]
        else:
            self.my_vote = None
        self.unread_comments = self._view["unread_comments"]
        self.counts = call_with_filtered_kwargs(PostAggregates, self._view["counts"])
        if "resolver" in self._view.keys():
            self.resolver = call_with_filtered_kwargs(Person, self._view["resolver"])
        else:
            self.resolver = None
