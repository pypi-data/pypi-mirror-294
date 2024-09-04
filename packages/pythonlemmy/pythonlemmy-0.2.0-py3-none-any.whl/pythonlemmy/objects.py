from typing import Optional
from dataclasses import dataclass


@dataclass
class ListCommunities:
    """https://join-lemmy.org/api/interfaces/ListCommunities.html"""
    
    type_: Optional[str] = None
    sort: Optional[str] = None
    show_nsfw: Optional[bool] = None
    page: Optional[int] = None
    limit: Optional[int] = None


@dataclass
class RegistrationApplication:
    """https://join-lemmy.org/api/interfaces/RegistrationApplication.html"""
    
    id: int = None
    local_user_id: int = None
    answer: str = None
    admin_id: Optional[int] = None
    deny_reason: Optional[str] = None
    published: str = None


@dataclass
class AdminPurgeComment:
    """https://join-lemmy.org/api/interfaces/AdminPurgeComment.html"""
    
    id: int = None
    admin_person_id: int = None
    post_id: int = None
    reason: Optional[str] = None
    when_: str = None


@dataclass
class CreateSite:
    """https://join-lemmy.org/api/interfaces/CreateSite.html"""
    
    name: str = None
    sidebar: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    banner: Optional[str] = None
    enable_downvotes: Optional[bool] = None
    enable_nsfw: Optional[bool] = None
    community_creation_admin_only: Optional[bool] = None
    require_email_verification: Optional[bool] = None
    application_question: Optional[str] = None
    private_instance: Optional[bool] = None
    default_theme: Optional[str] = None
    default_post_listing_type: Optional[str] = None
    default_sort_type: Optional[str] = None
    legal_information: Optional[str] = None
    application_email_admins: Optional[bool] = None
    hide_modlog_mod_names: Optional[bool] = None
    discussion_languages: Optional[list[int]] = None
    slur_filter_regex: Optional[str] = None
    actor_name_max_length: Optional[int] = None
    rate_limit_message: Optional[int] = None
    rate_limit_message_per_second: Optional[int] = None
    rate_limit_post: Optional[int] = None
    rate_limit_post_per_second: Optional[int] = None
    rate_limit_register: Optional[int] = None
    rate_limit_register_per_second: Optional[int] = None
    rate_limit_image: Optional[int] = None
    rate_limit_image_per_second: Optional[int] = None
    rate_limit_comment: Optional[int] = None
    rate_limit_comment_per_second: Optional[int] = None
    rate_limit_search: Optional[int] = None
    rate_limit_search_per_second: Optional[int] = None
    federation_enabled: Optional[bool] = None
    federation_debug: Optional[bool] = None
    captcha_enabled: Optional[bool] = None
    captcha_difficulty: Optional[str] = None
    allowed_instances: Optional[list[str]] = None
    blocked_instances: Optional[list[str]] = None
    taglines: Optional[list[str]] = None
    registration_mode: Optional[str] = None
    content_warning: Optional[str] = None
    default_post_listing_mode: Optional[str] = None


@dataclass
class DeleteComment:
    """https://join-lemmy.org/api/interfaces/DeleteComment.html"""
    
    comment_id: int = None
    deleted: bool = None


@dataclass
class CreateCommunity:
    """https://join-lemmy.org/api/interfaces/CreateCommunity.html"""
    
    name: str = None
    title: str = None
    description: Optional[str] = None
    icon: Optional[str] = None
    banner: Optional[str] = None
    nsfw: Optional[bool] = None
    posting_restricted_to_mods: Optional[bool] = None
    discussion_languages: Optional[list[int]] = None
    visibility: Optional[str] = None


@dataclass
class AdminPurgeCommunity:
    """https://join-lemmy.org/api/interfaces/AdminPurgeCommunity.html"""
    
    id: int = None
    admin_person_id: int = None
    reason: Optional[str] = None
    when_: str = None


@dataclass
class ModRemoveCommunity:
    """https://join-lemmy.org/api/interfaces/ModRemoveCommunity.html"""
    
    id: int = None
    mod_person_id: int = None
    community_id: int = None
    reason: Optional[str] = None
    removed: bool = None
    when_: str = None


@dataclass
class LocalSiteUrlBlocklist:
    """https://join-lemmy.org/api/interfaces/LocalSiteUrlBlocklist.html"""
    
    id: int = None
    url: str = None
    published: str = None
    updated: Optional[str] = None


@dataclass
class PostReport:
    """https://join-lemmy.org/api/interfaces/PostReport.html"""
    
    id: int = None
    creator_id: int = None
    post_id: int = None
    original_post_name: str = None
    original_post_url: Optional[str] = None
    original_post_body: Optional[str] = None
    reason: str = None
    resolved: bool = None
    resolver_id: Optional[int] = None
    published: str = None
    updated: Optional[str] = None


@dataclass
class CommentAggregates:
    """https://join-lemmy.org/api/interfaces/CommentAggregates.html"""
    
    comment_id: int = None
    score: int = None
    upvotes: int = None
    downvotes: int = None
    published: str = None
    child_count: int = None


@dataclass
class FeaturePost:
    """https://join-lemmy.org/api/interfaces/FeaturePost.html"""
    
    post_id: int = None
    featured: bool = None
    feature_type: str = None


@dataclass
class GetSiteMetadata:
    """https://join-lemmy.org/api/interfaces/GetSiteMetadata.html"""
    
    url: str = None


@dataclass
class ModLockPost:
    """https://join-lemmy.org/api/interfaces/ModLockPost.html"""
    
    id: int = None
    mod_person_id: int = None
    post_id: int = None
    locked: bool = None
    when_: str = None


@dataclass
class ResolveCommentReport:
    """https://join-lemmy.org/api/interfaces/ResolveCommentReport.html"""
    
    report_id: int = None
    resolved: bool = None


@dataclass
class DeleteCommunity:
    """https://join-lemmy.org/api/interfaces/DeleteCommunity.html"""
    
    community_id: int = None
    deleted: bool = None


@dataclass
class GetPersonMentions:
    """https://join-lemmy.org/api/interfaces/GetPersonMentions.html"""
    
    sort: Optional[str] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    unread_only: Optional[bool] = None


@dataclass
class ModHideCommunity:
    """https://join-lemmy.org/api/interfaces/ModHideCommunity.html"""
    
    id: int = None
    community_id: int = None
    mod_person_id: int = None
    when_: str = None
    reason: Optional[str] = None
    hidden: bool = None


@dataclass
class HideCommunity:
    """https://join-lemmy.org/api/interfaces/HideCommunity.html"""
    
    community_id: int = None
    hidden: bool = None
    reason: Optional[str] = None


@dataclass
class RemoveCommunity:
    """https://join-lemmy.org/api/interfaces/RemoveCommunity.html"""
    
    community_id: int = None
    removed: bool = None
    reason: Optional[str] = None


@dataclass
class EditComment:
    """https://join-lemmy.org/api/interfaces/EditComment.html"""
    
    comment_id: int = None
    content: Optional[str] = None
    language_id: Optional[int] = None


@dataclass
class EditCustomEmoji:
    """https://join-lemmy.org/api/interfaces/EditCustomEmoji.html"""
    
    id: int = None
    category: str = None
    image_url: str = None
    alt_text: str = None
    keywords: list[str] = None


@dataclass
class PersonMention:
    """https://join-lemmy.org/api/interfaces/PersonMention.html"""
    
    id: int = None
    recipient_id: int = None
    comment_id: int = None
    read: bool = None
    published: str = None


@dataclass
class HidePost:
    """https://join-lemmy.org/api/interfaces/HidePost.html"""
    
    post_ids: list[int] = None
    hide: bool = None


@dataclass
class CreatePrivateMessageReport:
    """https://join-lemmy.org/api/interfaces/CreatePrivateMessageReport.html"""
    
    private_message_id: int = None
    reason: str = None


@dataclass
class ReadableFederationState:
    """https://join-lemmy.org/api/interfaces/ReadableFederationState.html"""
    
    instance_id: int = None
    last_successful_id: Optional[int] = None
    last_successful_published_time: Optional[str] = None
    fail_count: int = None
    last_retry: Optional[str] = None
    next_retry: Optional[str] = None


@dataclass
class Login:
    """https://join-lemmy.org/api/interfaces/Login.html"""
    
    username_or_email: str = None
    password: str = None
    totp_2fa_token: Optional[str] = None


@dataclass
class BlockInstance:
    """https://join-lemmy.org/api/interfaces/BlockInstance.html"""
    
    instance_id: int = None
    block: bool = None


@dataclass
class LoginToken:
    """https://join-lemmy.org/api/interfaces/LoginToken.html"""
    
    user_id: int = None
    published: str = None
    ip: Optional[str] = None
    user_agent: Optional[str] = None


@dataclass
class PasswordChangeAfterReset:
    """https://join-lemmy.org/api/interfaces/PasswordChangeAfterReset.html"""
    
    token: str = None
    password: str = None
    password_verify: str = None


@dataclass
class LocalUser:
    """https://join-lemmy.org/api/interfaces/LocalUser.html"""
    
    id: int = None
    person_id: int = None
    email: Optional[str] = None
    show_nsfw: bool = None
    theme: str = None
    default_sort_type: str = None
    default_listing_type: str = None
    interface_language: str = None
    show_avatars: bool = None
    send_notifications_to_email: bool = None
    show_scores: bool = None
    show_bot_accounts: bool = None
    show_read_posts: bool = None
    email_verified: bool = None
    accepted_application: bool = None
    open_links_in_new_tab: bool = None
    blur_nsfw: bool = None
    auto_expand: bool = None
    infinite_scroll_enabled: bool = None
    admin: bool = None
    post_listing_mode: str = None
    totp_2fa_enabled: bool = None
    enable_keyboard_navigation: bool = None
    enable_animated_images: bool = None
    collapse_bot_comments: bool = None


@dataclass
class PersonAggregates:
    """https://join-lemmy.org/api/interfaces/PersonAggregates.html"""
    
    person_id: int = None
    post_count: int = None
    comment_count: int = None


@dataclass
class MarkCommentReplyAsRead:
    """https://join-lemmy.org/api/interfaces/MarkCommentReplyAsRead.html"""
    
    comment_reply_id: int = None
    read: bool = None


@dataclass
class Search:
    """https://join-lemmy.org/api/interfaces/Search.html"""
    
    q: str = None
    community_id: Optional[int] = None
    community_name: Optional[str] = None
    creator_id: Optional[int] = None
    type_: Optional[str] = None
    sort: Optional[str] = None
    listing_type: Optional[str] = None
    page: Optional[int] = None
    limit: Optional[int] = None


@dataclass
class LocalUserVoteDisplayMode:
    """https://join-lemmy.org/api/interfaces/LocalUserVoteDisplayMode.html"""
    
    local_user_id: int = None
    score: bool = None
    upvotes: bool = None
    downvotes: bool = None
    upvote_percentage: bool = None


@dataclass
class LockPost:
    """https://join-lemmy.org/api/interfaces/LockPost.html"""
    
    post_id: int = None
    locked: bool = None


@dataclass
class ChangePassword:
    """https://join-lemmy.org/api/interfaces/ChangePassword.html"""
    
    new_password: str = None
    new_password_verify: str = None
    old_password: str = None


@dataclass
class ResolveObject:
    """https://join-lemmy.org/api/interfaces/ResolveObject.html"""
    
    q: str = None


@dataclass
class VerifyEmail:
    """https://join-lemmy.org/api/interfaces/VerifyEmail.html"""
    
    token: str = None


@dataclass
class ModAddCommunity:
    """https://join-lemmy.org/api/interfaces/ModAddCommunity.html"""
    
    id: int = None
    mod_person_id: int = None
    other_person_id: int = None
    community_id: int = None
    removed: bool = None
    when_: str = None


@dataclass
class BlockPerson:
    """https://join-lemmy.org/api/interfaces/BlockPerson.html"""
    
    person_id: int = None
    block: bool = None


@dataclass
class ListPrivateMessageReports:
    """https://join-lemmy.org/api/interfaces/ListPrivateMessageReports.html"""
    
    page: Optional[int] = None
    limit: Optional[int] = None
    unresolved_only: Optional[bool] = None


@dataclass
class SiteAggregates:
    """https://join-lemmy.org/api/interfaces/SiteAggregates.html"""
    
    site_id: int = None
    users: int = None
    posts: int = None
    comments: int = None
    communities: int = None
    users_active_day: int = None
    users_active_week: int = None
    users_active_month: int = None
    users_active_half_year: int = None


@dataclass
class CreatePostReport:
    """https://join-lemmy.org/api/interfaces/CreatePostReport.html"""
    
    post_id: int = None
    reason: str = None


@dataclass
class CustomEmoji:
    """https://join-lemmy.org/api/interfaces/CustomEmoji.html"""
    
    id: int = None
    local_site_id: int = None
    shortcode: str = None
    image_url: str = None
    alt_text: str = None
    category: str = None
    published: str = None
    updated: Optional[str] = None


@dataclass
class PurgePost:
    """https://join-lemmy.org/api/interfaces/PurgePost.html"""
    
    post_id: int = None
    reason: Optional[str] = None


@dataclass
class PostAggregates:
    """https://join-lemmy.org/api/interfaces/PostAggregates.html"""
    
    post_id: int = None
    comments: int = None
    score: int = None
    upvotes: int = None
    downvotes: int = None
    published: str = None
    newest_comment_time: str = None


@dataclass
class Language:
    """https://join-lemmy.org/api/interfaces/Language.html"""
    
    id: int = None
    code: str = None
    name: str = None


@dataclass
class GetReportCount:
    """https://join-lemmy.org/api/interfaces/GetReportCount.html"""
    
    community_id: Optional[int] = None


@dataclass
class DeletePrivateMessage:
    """https://join-lemmy.org/api/interfaces/DeletePrivateMessage.html"""
    
    private_message_id: int = None
    deleted: bool = None


@dataclass
class Community:
    """https://join-lemmy.org/api/interfaces/Community.html"""
    
    id: int = None
    name: str = None
    title: str = None
    description: Optional[str] = None
    removed: bool = None
    published: str = None
    updated: Optional[str] = None
    deleted: bool = None
    nsfw: bool = None
    actor_id: str = None
    local: bool = None
    icon: Optional[str] = None
    banner: Optional[str] = None
    hidden: bool = None
    posting_restricted_to_mods: bool = None
    instance_id: int = None
    visibility: str = None


@dataclass
class ListPostReports:
    """https://join-lemmy.org/api/interfaces/ListPostReports.html"""
    
    page: Optional[int] = None
    limit: Optional[int] = None
    unresolved_only: Optional[bool] = None
    community_id: Optional[int] = None
    post_id: Optional[int] = None


@dataclass
class ModFeaturePost:
    """https://join-lemmy.org/api/interfaces/ModFeaturePost.html"""
    
    id: int = None
    mod_person_id: int = None
    post_id: int = None
    featured: bool = None
    when_: str = None
    is_featured_community: bool = None


@dataclass
class GetPersonDetails:
    """https://join-lemmy.org/api/interfaces/GetPersonDetails.html"""
    
    person_id: Optional[int] = None
    username: Optional[str] = None
    sort: Optional[str] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    community_id: Optional[int] = None
    saved_only: Optional[bool] = None


@dataclass
class AddModToCommunity:
    """https://join-lemmy.org/api/interfaces/AddModToCommunity.html"""
    
    community_id: int = None
    person_id: int = None
    added: bool = None


@dataclass
class Site:
    """https://join-lemmy.org/api/interfaces/Site.html"""
    
    id: int = None
    name: str = None
    sidebar: Optional[str] = None
    published: str = None
    updated: Optional[str] = None
    icon: Optional[str] = None
    banner: Optional[str] = None
    description: Optional[str] = None
    actor_id: str = None
    last_refreshed_at: str = None
    inbox_url: str = None
    public_key: str = None
    instance_id: int = None
    content_warning: Optional[str] = None


@dataclass
class ApproveRegistrationApplication:
    """https://join-lemmy.org/api/interfaces/ApproveRegistrationApplication.html"""
    
    id: int = None
    approve: bool = None
    deny_reason: Optional[str] = None


@dataclass
class EditPost:
    """https://join-lemmy.org/api/interfaces/EditPost.html"""
    
    post_id: int = None
    name: Optional[str] = None
    url: Optional[str] = None
    body: Optional[str] = None
    alt_text: Optional[str] = None
    nsfw: Optional[bool] = None
    language_id: Optional[int] = None
    custom_thumbnail: Optional[str] = None


@dataclass
class GetPost:
    """https://join-lemmy.org/api/interfaces/GetPost.html"""
    
    id: Optional[int] = None
    comment_id: Optional[int] = None


@dataclass
class FollowCommunity:
    """https://join-lemmy.org/api/interfaces/FollowCommunity.html"""
    
    community_id: int = None
    follow: bool = None


@dataclass
class GetPrivateMessages:
    """https://join-lemmy.org/api/interfaces/GetPrivateMessages.html"""
    
    unread_only: Optional[bool] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    creator_id: Optional[int] = None


@dataclass
class ModBan:
    """https://join-lemmy.org/api/interfaces/ModBan.html"""
    
    id: int = None
    mod_person_id: int = None
    other_person_id: int = None
    reason: Optional[str] = None
    banned: bool = None
    expires: Optional[str] = None
    when_: str = None


@dataclass
class Tagline:
    """https://join-lemmy.org/api/interfaces/Tagline.html"""
    
    id: int = None
    local_site_id: int = None
    content: str = None
    published: str = None
    updated: Optional[str] = None


@dataclass
class RemoveComment:
    """https://join-lemmy.org/api/interfaces/RemoveComment.html"""
    
    comment_id: int = None
    removed: bool = None
    reason: Optional[str] = None


@dataclass
class UpdateTotp:
    """https://join-lemmy.org/api/interfaces/UpdateTotp.html"""
    
    totp_token: str = None
    enabled: bool = None


@dataclass
class MarkPostAsRead:
    """https://join-lemmy.org/api/interfaces/MarkPostAsRead.html"""
    
    post_ids: list[int] = None
    read: bool = None


@dataclass
class ResolvePrivateMessageReport:
    """https://join-lemmy.org/api/interfaces/ResolvePrivateMessageReport.html"""
    
    report_id: int = None
    resolved: bool = None


@dataclass
class LinkMetadata:
    """https://join-lemmy.org/api/interfaces/LinkMetadata.html"""
    
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    embed_video_url: Optional[str] = None
    content_type: Optional[str] = None


@dataclass
class PrivateMessage:
    """https://join-lemmy.org/api/interfaces/PrivateMessage.html"""
    
    id: int = None
    creator_id: int = None
    recipient_id: int = None
    content: str = None
    deleted: bool = None
    read: bool = None
    published: str = None
    updated: Optional[str] = None
    ap_id: str = None
    local: bool = None


@dataclass
class DeletePost:
    """https://join-lemmy.org/api/interfaces/DeletePost.html"""
    
    post_id: int = None
    deleted: bool = None


@dataclass
class PurgeComment:
    """https://join-lemmy.org/api/interfaces/PurgeComment.html"""
    
    comment_id: int = None
    reason: Optional[str] = None


@dataclass
class CreatePost:
    """https://join-lemmy.org/api/interfaces/CreatePost.html"""
    
    name: str = None
    community_id: int = None
    url: Optional[str] = None
    body: Optional[str] = None
    alt_text: Optional[str] = None
    honeypot: Optional[str] = None
    nsfw: Optional[bool] = None
    language_id: Optional[int] = None
    custom_thumbnail: Optional[str] = None


@dataclass
class CreateCustomEmoji:
    """https://join-lemmy.org/api/interfaces/CreateCustomEmoji.html"""
    
    category: str = None
    shortcode: str = None
    image_url: str = None
    alt_text: str = None
    keywords: list[str] = None


@dataclass
class InstanceWithFederationState:
    """https://join-lemmy.org/api/interfaces/InstanceWithFederationState.html"""
    
    id: int = None
    domain: str = None
    published: str = None
    updated: Optional[str] = None
    software: Optional[str] = None
    version: Optional[str] = None
    federation_state: Optional[ReadableFederationState] = None


@dataclass
class CommunityAggregates:
    """https://join-lemmy.org/api/interfaces/CommunityAggregates.html"""
    
    community_id: int = None
    subscribers: int = None
    posts: int = None
    comments: int = None
    published: str = None
    users_active_day: int = None
    users_active_week: int = None
    users_active_month: int = None
    users_active_half_year: int = None
    subscribers_local: int = None


@dataclass
class LocalImage:
    """https://join-lemmy.org/api/interfaces/LocalImage.html"""
    
    local_user_id: Optional[int] = None
    pictrs_alias: str = None
    pictrs_delete_token: str = None
    published: str = None


@dataclass
class EditCommunity:
    """https://join-lemmy.org/api/interfaces/EditCommunity.html"""
    
    community_id: int = None
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    banner: Optional[str] = None
    nsfw: Optional[bool] = None
    posting_restricted_to_mods: Optional[bool] = None
    discussion_languages: Optional[list[int]] = None
    visibility: Optional[str] = None


@dataclass
class ListPostLikes:
    """https://join-lemmy.org/api/interfaces/ListPostLikes.html"""
    
    post_id: int = None
    page: Optional[int] = None
    limit: Optional[int] = None


@dataclass
class CommentReply:
    """https://join-lemmy.org/api/interfaces/CommentReply.html"""
    
    id: int = None
    recipient_id: int = None
    comment_id: int = None
    read: bool = None
    published: str = None


@dataclass
class ModRemovePost:
    """https://join-lemmy.org/api/interfaces/ModRemovePost.html"""
    
    id: int = None
    mod_person_id: int = None
    post_id: int = None
    reason: Optional[str] = None
    removed: bool = None
    when_: str = None


@dataclass
class BanFromCommunity:
    """https://join-lemmy.org/api/interfaces/BanFromCommunity.html"""
    
    community_id: int = None
    person_id: int = None
    ban: bool = None
    remove_data: Optional[bool] = None
    reason: Optional[str] = None
    expires: Optional[int] = None


@dataclass
class CreatePostLike:
    """https://join-lemmy.org/api/interfaces/CreatePostLike.html"""
    
    post_id: int = None
    score: int = None


@dataclass
class RemovePost:
    """https://join-lemmy.org/api/interfaces/RemovePost.html"""
    
    post_id: int = None
    removed: bool = None
    reason: Optional[str] = None


@dataclass
class EditPrivateMessage:
    """https://join-lemmy.org/api/interfaces/EditPrivateMessage.html"""
    
    private_message_id: int = None
    content: str = None


@dataclass
class ImageDetails:
    """https://join-lemmy.org/api/interfaces/ImageDetails.html"""
    
    link: str = None
    width: int = None
    height: int = None
    content_type: str = None


@dataclass
class GetModlog:
    """https://join-lemmy.org/api/interfaces/GetModlog.html"""
    
    mod_person_id: Optional[int] = None
    community_id: Optional[int] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    type_: Optional[str] = None
    other_person_id: Optional[int] = None
    post_id: Optional[int] = None
    comment_id: Optional[int] = None


@dataclass
class SaveUserSettings:
    """https://join-lemmy.org/api/interfaces/SaveUserSettings.html"""
    
    show_nsfw: Optional[bool] = None
    blur_nsfw: Optional[bool] = None
    auto_expand: Optional[bool] = None
    theme: Optional[str] = None
    default_sort_type: Optional[str] = None
    default_listing_type: Optional[str] = None
    interface_language: Optional[str] = None
    avatar: Optional[str] = None
    banner: Optional[str] = None
    display_name: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    matrix_user_id: Optional[str] = None
    show_avatars: Optional[bool] = None
    send_notifications_to_email: Optional[bool] = None
    bot_account: Optional[bool] = None
    show_bot_accounts: Optional[bool] = None
    show_read_posts: Optional[bool] = None
    discussion_languages: Optional[list[int]] = None
    open_links_in_new_tab: Optional[bool] = None
    infinite_scroll_enabled: Optional[bool] = None
    post_listing_mode: Optional[str] = None
    enable_keyboard_navigation: Optional[bool] = None
    enable_animated_images: Optional[bool] = None
    collapse_bot_comments: Optional[bool] = None
    show_scores: Optional[bool] = None
    show_upvotes: Optional[bool] = None
    show_downvotes: Optional[bool] = None
    show_upvote_percentage: Optional[bool] = None


@dataclass
class CreatePrivateMessage:
    """https://join-lemmy.org/api/interfaces/CreatePrivateMessage.html"""
    
    content: str = None
    recipient_id: int = None


@dataclass
class LocalSiteRateLimit:
    """https://join-lemmy.org/api/interfaces/LocalSiteRateLimit.html"""
    
    local_site_id: int = None
    message: int = None
    message_per_second: int = None
    post: int = None
    post_per_second: int = None
    register: int = None
    register_per_second: int = None
    image: int = None
    image_per_second: int = None
    comment: int = None
    comment_per_second: int = None
    search: int = None
    search_per_second: int = None
    published: str = None
    updated: Optional[str] = None
    import_user_settings: int = None
    import_user_settings_per_second: int = None


@dataclass
class ListCommentLikes:
    """https://join-lemmy.org/api/interfaces/ListCommentLikes.html"""
    
    comment_id: int = None
    page: Optional[int] = None
    limit: Optional[int] = None


@dataclass
class SaveComment:
    """https://join-lemmy.org/api/interfaces/SaveComment.html"""
    
    comment_id: int = None
    save: bool = None


@dataclass
class ListMedia:
    """https://join-lemmy.org/api/interfaces/ListMedia.html"""
    
    page: Optional[int] = None
    limit: Optional[int] = None


@dataclass
class LocalSite:
    """https://join-lemmy.org/api/interfaces/LocalSite.html"""
    
    id: int = None
    site_id: int = None
    site_setup: bool = None
    enable_downvotes: bool = None
    enable_nsfw: bool = None
    community_creation_admin_only: bool = None
    require_email_verification: bool = None
    application_question: Optional[str] = None
    private_instance: bool = None
    default_theme: str = None
    default_post_listing_type: str = None
    legal_information: Optional[str] = None
    hide_modlog_mod_names: bool = None
    application_email_admins: bool = None
    slur_filter_regex: Optional[str] = None
    actor_name_max_length: int = None
    federation_enabled: bool = None
    captcha_enabled: bool = None
    captcha_difficulty: str = None
    published: str = None
    updated: Optional[str] = None
    registration_mode: str = None
    reports_email_admins: bool = None
    federation_signed_fetch: bool = None
    default_post_listing_mode: str = None
    default_sort_type: str = None


@dataclass
class CustomEmojiKeyword:
    """https://join-lemmy.org/api/interfaces/CustomEmojiKeyword.html"""
    
    custom_emoji_id: int = None
    keyword: str = None


@dataclass
class ModlogListParams:
    """https://join-lemmy.org/api/interfaces/ModlogListParams.html"""
    
    community_id: Optional[int] = None
    mod_person_id: Optional[int] = None
    other_person_id: Optional[int] = None
    post_id: Optional[int] = None
    comment_id: Optional[int] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    hide_modlog_names: bool = None


@dataclass
class ModRemoveComment:
    """https://join-lemmy.org/api/interfaces/ModRemoveComment.html"""
    
    id: int = None
    mod_person_id: int = None
    comment_id: int = None
    reason: Optional[str] = None
    removed: bool = None
    when_: str = None


@dataclass
class GetComments:
    """https://join-lemmy.org/api/interfaces/GetComments.html"""
    
    type_: Optional[str] = None
    sort: Optional[str] = None
    max_depth: Optional[int] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    community_id: Optional[int] = None
    community_name: Optional[str] = None
    post_id: Optional[int] = None
    parent_id: Optional[int] = None
    saved_only: Optional[bool] = None
    liked_only: Optional[bool] = None
    disliked_only: Optional[bool] = None


@dataclass
class ModBanFromCommunity:
    """https://join-lemmy.org/api/interfaces/ModBanFromCommunity.html"""
    
    id: int = None
    mod_person_id: int = None
    other_person_id: int = None
    community_id: int = None
    reason: Optional[str] = None
    banned: bool = None
    expires: Optional[str] = None
    when_: str = None


@dataclass
class MarkPersonMentionAsRead:
    """https://join-lemmy.org/api/interfaces/MarkPersonMentionAsRead.html"""
    
    person_mention_id: int = None
    read: bool = None


@dataclass
class GetCommunity:
    """https://join-lemmy.org/api/interfaces/GetCommunity.html"""
    
    id: Optional[int] = None
    name: Optional[str] = None


@dataclass
class PrivateMessageReport:
    """https://join-lemmy.org/api/interfaces/PrivateMessageReport.html"""
    
    id: int = None
    creator_id: int = None
    private_message_id: int = None
    original_pm_text: str = None
    reason: str = None
    resolved: bool = None
    resolver_id: Optional[int] = None
    published: str = None
    updated: Optional[str] = None


@dataclass
class SavePost:
    """https://join-lemmy.org/api/interfaces/SavePost.html"""
    
    post_id: int = None
    save: bool = None


@dataclass
class PasswordReset:
    """https://join-lemmy.org/api/interfaces/PasswordReset.html"""
    
    email: str = None


@dataclass
class CreateCommentReport:
    """https://join-lemmy.org/api/interfaces/CreateCommentReport.html"""
    
    comment_id: int = None
    reason: str = None


@dataclass
class CreateCommentLike:
    """https://join-lemmy.org/api/interfaces/CreateCommentLike.html"""
    
    comment_id: int = None
    score: int = None


@dataclass
class Register:
    """https://join-lemmy.org/api/interfaces/Register.html"""
    
    username: str = None
    password: str = None
    password_verify: str = None
    show_nsfw: Optional[bool] = None
    email: Optional[str] = None
    captcha_uuid: Optional[str] = None
    captcha_answer: Optional[str] = None
    honeypot: Optional[str] = None
    answer: Optional[str] = None


@dataclass
class FederatedInstances:
    """https://join-lemmy.org/api/interfaces/FederatedInstances.html"""
    
    linked: list[InstanceWithFederationState] = None
    allowed: list[InstanceWithFederationState] = None
    blocked: list[InstanceWithFederationState] = None


@dataclass
class DeleteAccount:
    """https://join-lemmy.org/api/interfaces/DeleteAccount.html"""
    
    password: str = None
    delete_content: bool = None


@dataclass
class MarkPrivateMessageAsRead:
    """https://join-lemmy.org/api/interfaces/MarkPrivateMessageAsRead.html"""
    
    private_message_id: int = None
    read: bool = None


@dataclass
class GetComment:
    """https://join-lemmy.org/api/interfaces/GetComment.html"""
    
    id: int = None


@dataclass
class PurgeCommunity:
    """https://join-lemmy.org/api/interfaces/PurgeCommunity.html"""
    
    community_id: int = None
    reason: Optional[str] = None


@dataclass
class AddAdmin:
    """https://join-lemmy.org/api/interfaces/AddAdmin.html"""
    
    person_id: int = None
    added: bool = None


@dataclass
class ModTransferCommunity:
    """https://join-lemmy.org/api/interfaces/ModTransferCommunity.html"""
    
    id: int = None
    mod_person_id: int = None
    other_person_id: int = None
    community_id: int = None
    when_: str = None


@dataclass
class Person:
    """https://join-lemmy.org/api/interfaces/Person.html"""
    
    id: int = None
    name: str = None
    display_name: Optional[str] = None
    avatar: Optional[str] = None
    banned: bool = None
    published: str = None
    updated: Optional[str] = None
    actor_id: str = None
    bio: Optional[str] = None
    local: bool = None
    banner: Optional[str] = None
    deleted: bool = None
    matrix_user_id: Optional[str] = None
    bot_account: bool = None
    ban_expires: Optional[str] = None
    instance_id: int = None


@dataclass
class Comment:
    """https://join-lemmy.org/api/interfaces/Comment.html"""
    
    id: int = None
    creator_id: int = None
    post_id: int = None
    content: str = None
    removed: bool = None
    published: str = None
    updated: Optional[str] = None
    deleted: bool = None
    ap_id: str = None
    local: bool = None
    path: str = None
    distinguished: bool = None
    language_id: int = None


@dataclass
class OpenGraphData:
    """https://join-lemmy.org/api/interfaces/OpenGraphData.html"""
    
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    embed_video_url: Optional[str] = None


@dataclass
class PurgePerson:
    """https://join-lemmy.org/api/interfaces/PurgePerson.html"""
    
    person_id: int = None
    reason: Optional[str] = None


@dataclass
class BlockCommunity:
    """https://join-lemmy.org/api/interfaces/BlockCommunity.html"""
    
    community_id: int = None
    block: bool = None


@dataclass
class AdminPurgePost:
    """https://join-lemmy.org/api/interfaces/AdminPurgePost.html"""
    
    id: int = None
    admin_person_id: int = None
    community_id: int = None
    reason: Optional[str] = None
    when_: str = None


@dataclass
class ResolvePostReport:
    """https://join-lemmy.org/api/interfaces/ResolvePostReport.html"""
    
    report_id: int = None
    resolved: bool = None


@dataclass
class CreateComment:
    """https://join-lemmy.org/api/interfaces/CreateComment.html"""
    
    content: str = None
    post_id: int = None
    parent_id: Optional[int] = None
    language_id: Optional[int] = None


@dataclass
class ListRegistrationApplications:
    """https://join-lemmy.org/api/interfaces/ListRegistrationApplications.html"""
    
    unread_only: Optional[bool] = None
    page: Optional[int] = None
    limit: Optional[int] = None


@dataclass
class DistinguishComment:
    """https://join-lemmy.org/api/interfaces/DistinguishComment.html"""
    
    comment_id: int = None
    distinguished: bool = None


@dataclass
class CommentReport:
    """https://join-lemmy.org/api/interfaces/CommentReport.html"""
    
    id: int = None
    creator_id: int = None
    comment_id: int = None
    original_comment_text: str = None
    reason: str = None
    resolved: bool = None
    resolver_id: Optional[int] = None
    published: str = None
    updated: Optional[str] = None


@dataclass
class DeleteCustomEmoji:
    """https://join-lemmy.org/api/interfaces/DeleteCustomEmoji.html"""
    
    id: int = None


@dataclass
class BanPerson:
    """https://join-lemmy.org/api/interfaces/BanPerson.html"""
    
    person_id: int = None
    ban: bool = None
    remove_data: Optional[bool] = None
    reason: Optional[str] = None
    expires: Optional[int] = None


@dataclass
class ListCommentReports:
    """https://join-lemmy.org/api/interfaces/ListCommentReports.html"""
    
    comment_id: Optional[int] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    unresolved_only: Optional[bool] = None
    community_id: Optional[int] = None


@dataclass
class ModAdd:
    """https://join-lemmy.org/api/interfaces/ModAdd.html"""
    
    id: int = None
    mod_person_id: int = None
    other_person_id: int = None
    removed: bool = None
    when_: str = None


@dataclass
class EditSite:
    """https://join-lemmy.org/api/interfaces/EditSite.html"""
    
    name: Optional[str] = None
    sidebar: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    banner: Optional[str] = None
    enable_downvotes: Optional[bool] = None
    enable_nsfw: Optional[bool] = None
    community_creation_admin_only: Optional[bool] = None
    require_email_verification: Optional[bool] = None
    application_question: Optional[str] = None
    private_instance: Optional[bool] = None
    default_theme: Optional[str] = None
    default_post_listing_type: Optional[str] = None
    default_sort_type: Optional[str] = None
    legal_information: Optional[str] = None
    application_email_admins: Optional[bool] = None
    hide_modlog_mod_names: Optional[bool] = None
    discussion_languages: Optional[list[int]] = None
    slur_filter_regex: Optional[str] = None
    actor_name_max_length: Optional[int] = None
    rate_limit_message: Optional[int] = None
    rate_limit_message_per_second: Optional[int] = None
    rate_limit_post: Optional[int] = None
    rate_limit_post_per_second: Optional[int] = None
    rate_limit_register: Optional[int] = None
    rate_limit_register_per_second: Optional[int] = None
    rate_limit_image: Optional[int] = None
    rate_limit_image_per_second: Optional[int] = None
    rate_limit_comment: Optional[int] = None
    rate_limit_comment_per_second: Optional[int] = None
    rate_limit_search: Optional[int] = None
    rate_limit_search_per_second: Optional[int] = None
    federation_enabled: Optional[bool] = None
    federation_debug: Optional[bool] = None
    captcha_enabled: Optional[bool] = None
    captcha_difficulty: Optional[str] = None
    allowed_instances: Optional[list[str]] = None
    blocked_instances: Optional[list[str]] = None
    blocked_urls: Optional[list[str]] = None
    taglines: Optional[list[str]] = None
    registration_mode: Optional[str] = None
    reports_email_admins: Optional[bool] = None
    content_warning: Optional[str] = None
    default_post_listing_mode: Optional[str] = None


@dataclass
class Instance:
    """https://join-lemmy.org/api/interfaces/Instance.html"""
    
    id: int = None
    domain: str = None
    published: str = None
    updated: Optional[str] = None
    software: Optional[str] = None
    version: Optional[str] = None


@dataclass
class Post:
    """https://join-lemmy.org/api/interfaces/Post.html"""
    
    id: int = None
    name: str = None
    url: Optional[str] = None
    body: Optional[str] = None
    creator_id: int = None
    community_id: int = None
    removed: bool = None
    locked: bool = None
    published: str = None
    updated: Optional[str] = None
    deleted: bool = None
    nsfw: bool = None
    embed_title: Optional[str] = None
    embed_description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    ap_id: str = None
    local: bool = None
    embed_video_url: Optional[str] = None
    language_id: int = None
    featured_community: bool = None
    featured_local: bool = None
    url_content_type: Optional[str] = None
    alt_text: Optional[str] = None


@dataclass
class GetPosts:
    """https://join-lemmy.org/api/interfaces/GetPosts.html"""
    
    type_: Optional[str] = None
    sort: Optional[str] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    community_id: Optional[int] = None
    community_name: Optional[str] = None
    saved_only: Optional[bool] = None
    liked_only: Optional[bool] = None
    disliked_only: Optional[bool] = None
    show_hidden: Optional[bool] = None
    show_read: Optional[bool] = None
    show_nsfw: Optional[bool] = None
    page_cursor: Optional[str] = None


@dataclass
class GetRegistrationApplication:
    """https://join-lemmy.org/api/interfaces/GetRegistrationApplication.html"""
    
    person_id: int = None


@dataclass
class GetReplies:
    """https://join-lemmy.org/api/interfaces/GetReplies.html"""
    
    sort: Optional[str] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    unread_only: Optional[bool] = None


@dataclass
class AdminPurgePerson:
    """https://join-lemmy.org/api/interfaces/AdminPurgePerson.html"""
    
    id: int = None
    admin_person_id: int = None
    reason: Optional[str] = None
    when_: str = None


@dataclass
class TransferCommunity:
    """https://join-lemmy.org/api/interfaces/TransferCommunity.html"""
    
    community_id: int = None
    person_id: int = None
