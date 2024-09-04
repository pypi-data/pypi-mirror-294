from typing import Optional
from dataclasses import dataclass


@dataclass
class ListCommunities:
    type_: Optional[str] = None
    sort: Optional[str] = None
    show_nsfw: Optional[bool] = None
    page: Optional[int] = None
    limit: Optional[int] = None


@dataclass
class RegistrationApplication:
    id: int = None
    local_user_id: int = None
    answer: str = None
    admin_id: Optional[int] = None
    deny_reason: Optional[str] = None
    published: str = None


@dataclass
class AdminPurgeComment:
    id: int = None
    admin_person_id: int = None
    post_id: int = None
    reason: Optional[str] = None
    when_: str = None


@dataclass
class CreateSite:
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
    comment_id: int = None
    deleted: bool = None


@dataclass
class CreateCommunity:
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
    id: int = None
    admin_person_id: int = None
    reason: Optional[str] = None
    when_: str = None


@dataclass
class ModRemoveCommunity:
    id: int = None
    mod_person_id: int = None
    community_id: int = None
    reason: Optional[str] = None
    removed: bool = None
    when_: str = None


@dataclass
class LocalSiteUrlBlocklist:
    id: int = None
    url: str = None
    published: str = None
    updated: Optional[str] = None


@dataclass
class PostReport:
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
    comment_id: int = None
    score: int = None
    upvotes: int = None
    downvotes: int = None
    published: str = None
    child_count: int = None


@dataclass
class FeaturePost:
    post_id: int = None
    featured: bool = None
    feature_type: str = None


@dataclass
class GetSiteMetadata:
    url: str = None


@dataclass
class ModLockPost:
    id: int = None
    mod_person_id: int = None
    post_id: int = None
    locked: bool = None
    when_: str = None


@dataclass
class ResolveCommentReport:
    report_id: int = None
    resolved: bool = None


@dataclass
class DeleteCommunity:
    community_id: int = None
    deleted: bool = None


@dataclass
class GetPersonMentions:
    sort: Optional[str] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    unread_only: Optional[bool] = None


@dataclass
class ModHideCommunity:
    id: int = None
    community_id: int = None
    mod_person_id: int = None
    when_: str = None
    reason: Optional[str] = None
    hidden: bool = None


@dataclass
class HideCommunity:
    community_id: int = None
    hidden: bool = None
    reason: Optional[str] = None


@dataclass
class RemoveCommunity:
    community_id: int = None
    removed: bool = None
    reason: Optional[str] = None


@dataclass
class EditComment:
    comment_id: int = None
    content: Optional[str] = None
    language_id: Optional[int] = None


@dataclass
class EditCustomEmoji:
    id: int = None
    category: str = None
    image_url: str = None
    alt_text: str = None
    keywords: list[str] = None


@dataclass
class PersonMention:
    id: int = None
    recipient_id: int = None
    comment_id: int = None
    read: bool = None
    published: str = None


@dataclass
class HidePost:
    post_ids: list[int] = None
    hide: bool = None


@dataclass
class CreatePrivateMessageReport:
    private_message_id: int = None
    reason: str = None


@dataclass
class ReadableFederationState:
    instance_id: int = None
    last_successful_id: Optional[int] = None
    last_successful_published_time: Optional[str] = None
    fail_count: int = None
    last_retry: Optional[str] = None
    next_retry: Optional[str] = None


@dataclass
class Login:
    username_or_email: str = None
    password: str = None
    totp_2fa_token: Optional[str] = None


@dataclass
class BlockInstance:
    instance_id: int = None
    block: bool = None


@dataclass
class LoginToken:
    user_id: int = None
    published: str = None
    ip: Optional[str] = None
    user_agent: Optional[str] = None


@dataclass
class PasswordChangeAfterReset:
    token: str = None
    password: str = None
    password_verify: str = None


@dataclass
class LocalUser:
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
    person_id: int = None
    post_count: int = None
    comment_count: int = None


@dataclass
class MarkCommentReplyAsRead:
    comment_reply_id: int = None
    read: bool = None


@dataclass
class Search:
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
    local_user_id: int = None
    score: bool = None
    upvotes: bool = None
    downvotes: bool = None
    upvote_percentage: bool = None


@dataclass
class LockPost:
    post_id: int = None
    locked: bool = None


@dataclass
class ChangePassword:
    new_password: str = None
    new_password_verify: str = None
    old_password: str = None


@dataclass
class ResolveObject:
    q: str = None


@dataclass
class VerifyEmail:
    token: str = None


@dataclass
class ModAddCommunity:
    id: int = None
    mod_person_id: int = None
    other_person_id: int = None
    community_id: int = None
    removed: bool = None
    when_: str = None


@dataclass
class BlockPerson:
    person_id: int = None
    block: bool = None


@dataclass
class ListPrivateMessageReports:
    page: Optional[int] = None
    limit: Optional[int] = None
    unresolved_only: Optional[bool] = None


@dataclass
class SiteAggregates:
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
    post_id: int = None
    reason: str = None


@dataclass
class CustomEmoji:
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
    post_id: int = None
    reason: Optional[str] = None


@dataclass
class PostAggregates:
    post_id: int = None
    comments: int = None
    score: int = None
    upvotes: int = None
    downvotes: int = None
    published: str = None
    newest_comment_time: str = None


@dataclass
class Language:
    id: int = None
    code: str = None
    name: str = None


@dataclass
class GetReportCount:
    community_id: Optional[int] = None


@dataclass
class DeletePrivateMessage:
    private_message_id: int = None
    deleted: bool = None


@dataclass
class Community:
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
    page: Optional[int] = None
    limit: Optional[int] = None
    unresolved_only: Optional[bool] = None
    community_id: Optional[int] = None
    post_id: Optional[int] = None


@dataclass
class ModFeaturePost:
    id: int = None
    mod_person_id: int = None
    post_id: int = None
    featured: bool = None
    when_: str = None
    is_featured_community: bool = None


@dataclass
class GetPersonDetails:
    person_id: Optional[int] = None
    username: Optional[str] = None
    sort: Optional[str] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    community_id: Optional[int] = None
    saved_only: Optional[bool] = None


@dataclass
class AddModToCommunity:
    community_id: int = None
    person_id: int = None
    added: bool = None


@dataclass
class Site:
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
    id: int = None
    approve: bool = None
    deny_reason: Optional[str] = None


@dataclass
class EditPost:
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
    id: Optional[int] = None
    comment_id: Optional[int] = None


@dataclass
class FollowCommunity:
    community_id: int = None
    follow: bool = None


@dataclass
class GetPrivateMessages:
    unread_only: Optional[bool] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    creator_id: Optional[int] = None


@dataclass
class ModBan:
    id: int = None
    mod_person_id: int = None
    other_person_id: int = None
    reason: Optional[str] = None
    banned: bool = None
    expires: Optional[str] = None
    when_: str = None


@dataclass
class Tagline:
    id: int = None
    local_site_id: int = None
    content: str = None
    published: str = None
    updated: Optional[str] = None


@dataclass
class RemoveComment:
    comment_id: int = None
    removed: bool = None
    reason: Optional[str] = None


@dataclass
class UpdateTotp:
    totp_token: str = None
    enabled: bool = None


@dataclass
class MarkPostAsRead:
    post_ids: list[int] = None
    read: bool = None


@dataclass
class ResolvePrivateMessageReport:
    report_id: int = None
    resolved: bool = None


@dataclass
class LinkMetadata:
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    embed_video_url: Optional[str] = None
    content_type: Optional[str] = None


@dataclass
class PrivateMessage:
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
    post_id: int = None
    deleted: bool = None


@dataclass
class PurgeComment:
    comment_id: int = None
    reason: Optional[str] = None


@dataclass
class CreatePost:
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
    category: str = None
    shortcode: str = None
    image_url: str = None
    alt_text: str = None
    keywords: list[str] = None


@dataclass
class InstanceWithFederationState:
    id: int = None
    domain: str = None
    published: str = None
    updated: Optional[str] = None
    software: Optional[str] = None
    version: Optional[str] = None
    federation_state: Optional[ReadableFederationState] = None


@dataclass
class CommunityAggregates:
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
    local_user_id: Optional[int] = None
    pictrs_alias: str = None
    pictrs_delete_token: str = None
    published: str = None


@dataclass
class EditCommunity:
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
    post_id: int = None
    page: Optional[int] = None
    limit: Optional[int] = None


@dataclass
class CommentReply:
    id: int = None
    recipient_id: int = None
    comment_id: int = None
    read: bool = None
    published: str = None


@dataclass
class ModRemovePost:
    id: int = None
    mod_person_id: int = None
    post_id: int = None
    reason: Optional[str] = None
    removed: bool = None
    when_: str = None


@dataclass
class BanFromCommunity:
    community_id: int = None
    person_id: int = None
    ban: bool = None
    remove_data: Optional[bool] = None
    reason: Optional[str] = None
    expires: Optional[int] = None


@dataclass
class CreatePostLike:
    post_id: int = None
    score: int = None


@dataclass
class RemovePost:
    post_id: int = None
    removed: bool = None
    reason: Optional[str] = None


@dataclass
class EditPrivateMessage:
    private_message_id: int = None
    content: str = None


@dataclass
class ImageDetails:
    link: str = None
    width: int = None
    height: int = None
    content_type: str = None


@dataclass
class GetModlog:
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
    content: str = None
    recipient_id: int = None


@dataclass
class LocalSiteRateLimit:
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
    comment_id: int = None
    page: Optional[int] = None
    limit: Optional[int] = None


@dataclass
class SaveComment:
    comment_id: int = None
    save: bool = None


@dataclass
class ListMedia:
    page: Optional[int] = None
    limit: Optional[int] = None


@dataclass
class LocalSite:
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
    custom_emoji_id: int = None
    keyword: str = None


@dataclass
class ModlogListParams:
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
    id: int = None
    mod_person_id: int = None
    comment_id: int = None
    reason: Optional[str] = None
    removed: bool = None
    when_: str = None


@dataclass
class GetComments:
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
    person_mention_id: int = None
    read: bool = None


@dataclass
class GetCommunity:
    id: Optional[int] = None
    name: Optional[str] = None


@dataclass
class PrivateMessageReport:
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
    post_id: int = None
    save: bool = None


@dataclass
class PasswordReset:
    email: str = None


@dataclass
class CreateCommentReport:
    comment_id: int = None
    reason: str = None


@dataclass
class CreateCommentLike:
    comment_id: int = None
    score: int = None


@dataclass
class Register:
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
    linked: list[InstanceWithFederationState] = None
    allowed: list[InstanceWithFederationState] = None
    blocked: list[InstanceWithFederationState] = None


@dataclass
class DeleteAccount:
    password: str = None
    delete_content: bool = None


@dataclass
class MarkPrivateMessageAsRead:
    private_message_id: int = None
    read: bool = None


@dataclass
class GetComment:
    id: int = None


@dataclass
class PurgeCommunity:
    community_id: int = None
    reason: Optional[str] = None


@dataclass
class AddAdmin:
    person_id: int = None
    added: bool = None


@dataclass
class ModTransferCommunity:
    id: int = None
    mod_person_id: int = None
    other_person_id: int = None
    community_id: int = None
    when_: str = None


@dataclass
class Person:
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
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    embed_video_url: Optional[str] = None


@dataclass
class PurgePerson:
    person_id: int = None
    reason: Optional[str] = None


@dataclass
class BlockCommunity:
    community_id: int = None
    block: bool = None


@dataclass
class AdminPurgePost:
    id: int = None
    admin_person_id: int = None
    community_id: int = None
    reason: Optional[str] = None
    when_: str = None


@dataclass
class ResolvePostReport:
    report_id: int = None
    resolved: bool = None


@dataclass
class CreateComment:
    content: str = None
    post_id: int = None
    parent_id: Optional[int] = None
    language_id: Optional[int] = None


@dataclass
class ListRegistrationApplications:
    unread_only: Optional[bool] = None
    page: Optional[int] = None
    limit: Optional[int] = None


@dataclass
class DistinguishComment:
    comment_id: int = None
    distinguished: bool = None


@dataclass
class CommentReport:
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
    id: int = None


@dataclass
class BanPerson:
    person_id: int = None
    ban: bool = None
    remove_data: Optional[bool] = None
    reason: Optional[str] = None
    expires: Optional[int] = None


@dataclass
class ListCommentReports:
    comment_id: Optional[int] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    unresolved_only: Optional[bool] = None
    community_id: Optional[int] = None


@dataclass
class ModAdd:
    id: int = None
    mod_person_id: int = None
    other_person_id: int = None
    removed: bool = None
    when_: str = None


@dataclass
class EditSite:
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
    id: int = None
    domain: str = None
    published: str = None
    updated: Optional[str] = None
    software: Optional[str] = None
    version: Optional[str] = None


@dataclass
class Post:
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
    person_id: int = None


@dataclass
class GetReplies:
    sort: Optional[str] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    unread_only: Optional[bool] = None


@dataclass
class AdminPurgePerson:
    id: int = None
    admin_person_id: int = None
    reason: Optional[str] = None
    when_: str = None


@dataclass
class TransferCommunity:
    community_id: int = None
    person_id: int = None
