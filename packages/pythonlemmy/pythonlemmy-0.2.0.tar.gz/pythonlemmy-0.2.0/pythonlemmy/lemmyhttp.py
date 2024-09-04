import logging

import requests
from typing import List, Optional

from .types import File
from .utils import create_session, post_handler, put_handler, get_handler, \
    create_form, file_handler

API_VERSION = "v3"


class LemmyHttp(object):

    def __init__(self, base_url: str, headers: dict = None,
                 jwt: str = None):
        """ LemmyHttp object: handles all POST, PUT, and GET operations from
        the LemmyHttp API (https://join-lemmy.org/api/classes/LemmyHttp.html)

        Args:
            base_url (str): Lemmy instance to connect to (e.g.,
                "https://lemmy.world")
            headers (dict, optional): optional headers
            jwt (str, optional): login token if not immediately using
                `LemmyHttp.login`
        """

        if not base_url.startswith("http://") and not base_url.startswith("https://"):
            base_url = "https://" + base_url

        self._base_url = base_url
        self._api_url = base_url + f"/api/{API_VERSION}"
        self._headers = headers
        self._session = create_session(self._headers, jwt)
        self.logger = logging.getLogger(__name__)

    def get_site(
        self
    ):
        """ Gets the site, and your user data.


        Returns:
            requests.Response: result of API call (wrap in GetSiteResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/site", json=None, params=form)

        return result

    def create_site(
        self,
        name: str,
        sidebar: str = None,
        description: str = None,
        icon: str = None,
        banner: str = None,
        enable_downvotes: bool = None,
        enable_nsfw: bool = None,
        community_creation_admin_only: bool = None,
        require_email_verification: bool = None,
        application_question: str = None,
        private_instance: bool = None,
        default_theme: str = None,
        default_post_listing_type: str = None,
        default_sort_type: str = None,
        legal_information: str = None,
        application_email_admins: bool = None,
        hide_modlog_mod_names: bool = None,
        discussion_languages: list[int] = None,
        slur_filter_regex: str = None,
        actor_name_max_length: int = None,
        rate_limit_message: int = None,
        rate_limit_message_per_second: int = None,
        rate_limit_post: int = None,
        rate_limit_post_per_second: int = None,
        rate_limit_register: int = None,
        rate_limit_register_per_second: int = None,
        rate_limit_image: int = None,
        rate_limit_image_per_second: int = None,
        rate_limit_comment: int = None,
        rate_limit_comment_per_second: int = None,
        rate_limit_search: int = None,
        rate_limit_search_per_second: int = None,
        federation_enabled: bool = None,
        federation_debug: bool = None,
        captcha_enabled: bool = None,
        captcha_difficulty: str = None,
        allowed_instances: list[str] = None,
        blocked_instances: list[str] = None,
        taglines: list[str] = None,
        registration_mode: str = None,
        content_warning: str = None,
        default_post_listing_mode: str = None
    ):
        """ Create your site.
        Args:
            name: CreateSite.name
            sidebar: CreateSite.sidebar
            description: CreateSite.description
            icon: CreateSite.icon
            banner: CreateSite.banner
            enable_downvotes: CreateSite.enable_downvotes
            enable_nsfw: CreateSite.enable_nsfw
            community_creation_admin_only: CreateSite.community_creation_admin_only
            require_email_verification: CreateSite.require_email_verification
            application_question: CreateSite.application_question
            private_instance: CreateSite.private_instance
            default_theme: CreateSite.default_theme
            default_post_listing_type: Possible values [All, Local, Subscribed, ModeratorView]
            default_sort_type: Possible values [Active, Hot, New, Old, TopDay, TopWeek, TopMonth, TopYear, TopAll, MostComments, NewComments, TopHour, TopSixHour, TopTwelveHour, TopThreeMonths, TopSixMonths, TopNineMonths, Controversial, Scaled]
            legal_information: CreateSite.legal_information
            application_email_admins: CreateSite.application_email_admins
            hide_modlog_mod_names: CreateSite.hide_modlog_mod_names
            discussion_languages: CreateSite.discussion_languages
            slur_filter_regex: CreateSite.slur_filter_regex
            actor_name_max_length: CreateSite.actor_name_max_length
            rate_limit_message: CreateSite.rate_limit_message
            rate_limit_message_per_second: CreateSite.rate_limit_message_per_second
            rate_limit_post: CreateSite.rate_limit_post
            rate_limit_post_per_second: CreateSite.rate_limit_post_per_second
            rate_limit_register: CreateSite.rate_limit_register
            rate_limit_register_per_second: CreateSite.rate_limit_register_per_second
            rate_limit_image: CreateSite.rate_limit_image
            rate_limit_image_per_second: CreateSite.rate_limit_image_per_second
            rate_limit_comment: CreateSite.rate_limit_comment
            rate_limit_comment_per_second: CreateSite.rate_limit_comment_per_second
            rate_limit_search: CreateSite.rate_limit_search
            rate_limit_search_per_second: CreateSite.rate_limit_search_per_second
            federation_enabled: CreateSite.federation_enabled
            federation_debug: CreateSite.federation_debug
            captcha_enabled: CreateSite.captcha_enabled
            captcha_difficulty: CreateSite.captcha_difficulty
            allowed_instances: CreateSite.allowed_instances
            blocked_instances: CreateSite.blocked_instances
            taglines: CreateSite.taglines
            registration_mode: Possible values [Closed, RequireApplication, Open]
            content_warning: CreateSite.content_warning
            default_post_listing_mode: Possible values [List, Card, SmallCard]

        Returns:
            requests.Response: result of API call (wrap in SiteResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/site", json=form, params=None)

        return result

    def edit_site(
        self,
        name: str = None,
        sidebar: str = None,
        description: str = None,
        icon: str = None,
        banner: str = None,
        enable_downvotes: bool = None,
        enable_nsfw: bool = None,
        community_creation_admin_only: bool = None,
        require_email_verification: bool = None,
        application_question: str = None,
        private_instance: bool = None,
        default_theme: str = None,
        default_post_listing_type: str = None,
        default_sort_type: str = None,
        legal_information: str = None,
        application_email_admins: bool = None,
        hide_modlog_mod_names: bool = None,
        discussion_languages: list[int] = None,
        slur_filter_regex: str = None,
        actor_name_max_length: int = None,
        rate_limit_message: int = None,
        rate_limit_message_per_second: int = None,
        rate_limit_post: int = None,
        rate_limit_post_per_second: int = None,
        rate_limit_register: int = None,
        rate_limit_register_per_second: int = None,
        rate_limit_image: int = None,
        rate_limit_image_per_second: int = None,
        rate_limit_comment: int = None,
        rate_limit_comment_per_second: int = None,
        rate_limit_search: int = None,
        rate_limit_search_per_second: int = None,
        federation_enabled: bool = None,
        federation_debug: bool = None,
        captcha_enabled: bool = None,
        captcha_difficulty: str = None,
        allowed_instances: list[str] = None,
        blocked_instances: list[str] = None,
        blocked_urls: list[str] = None,
        taglines: list[str] = None,
        registration_mode: str = None,
        reports_email_admins: bool = None,
        content_warning: str = None,
        default_post_listing_mode: str = None
    ):
        """ Edit your site.
        Args:
            name: EditSite.name
            sidebar: EditSite.sidebar
            description: EditSite.description
            icon: EditSite.icon
            banner: EditSite.banner
            enable_downvotes: EditSite.enable_downvotes
            enable_nsfw: EditSite.enable_nsfw
            community_creation_admin_only: EditSite.community_creation_admin_only
            require_email_verification: EditSite.require_email_verification
            application_question: EditSite.application_question
            private_instance: EditSite.private_instance
            default_theme: EditSite.default_theme
            default_post_listing_type: Possible values [All, Local, Subscribed, ModeratorView]
            default_sort_type: Possible values [Active, Hot, New, Old, TopDay, TopWeek, TopMonth, TopYear, TopAll, MostComments, NewComments, TopHour, TopSixHour, TopTwelveHour, TopThreeMonths, TopSixMonths, TopNineMonths, Controversial, Scaled]
            legal_information: EditSite.legal_information
            application_email_admins: EditSite.application_email_admins
            hide_modlog_mod_names: EditSite.hide_modlog_mod_names
            discussion_languages: EditSite.discussion_languages
            slur_filter_regex: EditSite.slur_filter_regex
            actor_name_max_length: EditSite.actor_name_max_length
            rate_limit_message: EditSite.rate_limit_message
            rate_limit_message_per_second: EditSite.rate_limit_message_per_second
            rate_limit_post: EditSite.rate_limit_post
            rate_limit_post_per_second: EditSite.rate_limit_post_per_second
            rate_limit_register: EditSite.rate_limit_register
            rate_limit_register_per_second: EditSite.rate_limit_register_per_second
            rate_limit_image: EditSite.rate_limit_image
            rate_limit_image_per_second: EditSite.rate_limit_image_per_second
            rate_limit_comment: EditSite.rate_limit_comment
            rate_limit_comment_per_second: EditSite.rate_limit_comment_per_second
            rate_limit_search: EditSite.rate_limit_search
            rate_limit_search_per_second: EditSite.rate_limit_search_per_second
            federation_enabled: EditSite.federation_enabled
            federation_debug: EditSite.federation_debug
            captcha_enabled: EditSite.captcha_enabled
            captcha_difficulty: EditSite.captcha_difficulty
            allowed_instances: EditSite.allowed_instances
            blocked_instances: EditSite.blocked_instances
            blocked_urls: EditSite.blocked_urls
            taglines: EditSite.taglines
            registration_mode: Possible values [Closed, RequireApplication, Open]
            reports_email_admins: EditSite.reports_email_admins
            content_warning: EditSite.content_warning
            default_post_listing_mode: Possible values [List, Card, SmallCard]

        Returns:
            requests.Response: result of API call (wrap in SiteResponse if successful)
        """
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/site", json=form, params=None)

        return result

    def leave_admin(
        self
    ):
        """ Leave the Site admins.


        Returns:
            requests.Response: result of API call (wrap in GetSiteResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/leave_admin", json=form, params=None)

        return result

    def generate_totp_secret(
        self
    ):
        """ Generate a TOTP / two-factor secret.         Afterwards you need to call `/user/totp/update` with a valid token to enable it.


        Returns:
            requests.Response: result of API call (wrap in GenerateTotpSecretResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/totp/generate", json=form, params=None)

        return result

    def export_settings(
        self
    ):
        """ Export a backup of your user settings, including your saved content,         followed communities, and blocks.


        Returns:
            requests.Response: result of API call (wrap in str if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/user/export_settings", json=None, params=form)

        return result

    def import_settings(
        self
    ):
        """ Import a backup of your user settings.


        Returns:
            requests.Response: result of API call (wrap in SuccessResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/import_settings", json=form, params=None)

        return result

    def list_logins(
        self
    ):
        """ List login tokens for your user


        Returns:
            requests.Response: result of API call (wrap in List[LoginToken] if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/user/list_logins", json=None, params=form)

        return result

    def validate_auth(
        self
    ):
        """ Returns an error message if your auth token is invalid


        Returns:
            requests.Response: result of API call (wrap in SuccessResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/user/validate_auth", json=None, params=form)

        return result

    def list_media(
        self,
        page: int = None,
        limit: int = None
    ):
        """ List all the media for your user
        Args:
            page: ListMedia.page
            limit: ListMedia.limit

        Returns:
            requests.Response: result of API call (wrap in ListMediaResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/account/list_media", json=None, params=form)

        return result

    def list_all_media(
        self,
        page: int = None,
        limit: int = None
    ):
        """ List all the media known to your instance.
        Args:
            page: ListMedia.page
            limit: ListMedia.limit

        Returns:
            requests.Response: result of API call (wrap in ListMediaResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/admin/list_all_media", json=None, params=form)

        return result

    def update_totp(
        self,
        totp_token: str,
        enabled: bool
    ):
        """ Enable / Disable TOTP / two-factor authentication.         To enable, you need to first call `/user/totp/generate` and then pass a valid token to this.         Disabling is only possible if 2FA was previously enabled. Again it is necessary to pass a valid token.
        Args:
            totp_token: UpdateTotp.totp_token
            enabled: UpdateTotp.enabled

        Returns:
            requests.Response: result of API call (wrap in UpdateTotpResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/totp/update", json=form, params=None)

        return result

    def get_modlog(
        self,
        mod_person_id: int = None,
        community_id: int = None,
        page: int = None,
        limit: int = None,
        type_: str = None,
        other_person_id: int = None,
        post_id: int = None,
        comment_id: int = None
    ):
        """ Get the modlog.
        Args:
            mod_person_id: PersonId
            community_id: CommunityId
            page: GetModlog.page
            limit: GetModlog.limit
            type_: Possible values [All, ModRemovePost, ModLockPost, ModFeaturePost, ModRemoveComment, ModRemoveCommunity, ModBanFromCommunity, ModAddCommunity, ModTransferCommunity, ModAdd, ModBan, ModHideCommunity, AdminPurgePerson, AdminPurgeCommunity, AdminPurgePost, AdminPurgeComment]
            other_person_id: PersonId
            post_id: PostId
            comment_id: CommentId

        Returns:
            requests.Response: result of API call (wrap in GetModlogResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/modlog", json=None, params=form)

        return result

    def search(
        self,
        q: str,
        community_id: int = None,
        community_name: str = None,
        creator_id: int = None,
        type_: str = None,
        sort: str = None,
        listing_type: str = None,
        page: int = None,
        limit: int = None
    ):
        """ Search lemmy.
        Args:
            q: Search.q
            community_id: CommunityId
            community_name: Search.community_name
            creator_id: PersonId
            type_: Possible values [All, Comments, Posts, Communities, Users, Url]
            sort: Possible values [Active, Hot, New, Old, TopDay, TopWeek, TopMonth, TopYear, TopAll, MostComments, NewComments, TopHour, TopSixHour, TopTwelveHour, TopThreeMonths, TopSixMonths, TopNineMonths, Controversial, Scaled]
            listing_type: Possible values [All, Local, Subscribed, ModeratorView]
            page: Search.page
            limit: Search.limit

        Returns:
            requests.Response: result of API call (wrap in SearchResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/search", json=None, params=form)

        return result

    def resolve_object(
        self,
        q: str
    ):
        """ Fetch a non-local / federated object.
        Args:
            q: ResolveObject.q

        Returns:
            requests.Response: result of API call (wrap in ResolveObjectResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/resolve_object", json=None, params=form)

        return result

    def create_community(
        self,
        name: str,
        title: str,
        description: str = None,
        icon: str = None,
        banner: str = None,
        nsfw: bool = None,
        posting_restricted_to_mods: bool = None,
        discussion_languages: list[int] = None,
        visibility: str = None
    ):
        """ Create a new community.
        Args:
            name: CreateCommunity.name
            title: CreateCommunity.title
            description: CreateCommunity.description
            icon: CreateCommunity.icon
            banner: CreateCommunity.banner
            nsfw: CreateCommunity.nsfw
            posting_restricted_to_mods: CreateCommunity.posting_restricted_to_mods
            discussion_languages: CreateCommunity.discussion_languages
            visibility: Possible values [Public, LocalOnly]

        Returns:
            requests.Response: result of API call (wrap in CommunityResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/community", json=form, params=None)

        return result

    def get_community(
        self,
        id: int = None,
        name: str = None
    ):
        """ Get / fetch a community.
        Args:
            id: CommunityId
            name: GetCommunity.name

        Returns:
            requests.Response: result of API call (wrap in GetCommunityResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/community", json=None, params=form)

        return result

    def edit_community(
        self,
        community_id: int,
        title: str = None,
        description: str = None,
        icon: str = None,
        banner: str = None,
        nsfw: bool = None,
        posting_restricted_to_mods: bool = None,
        discussion_languages: list[int] = None,
        visibility: str = None
    ):
        """ Edit a community.
        Args:
            community_id: CommunityId
            title: EditCommunity.title
            description: EditCommunity.description
            icon: EditCommunity.icon
            banner: EditCommunity.banner
            nsfw: EditCommunity.nsfw
            posting_restricted_to_mods: EditCommunity.posting_restricted_to_mods
            discussion_languages: EditCommunity.discussion_languages
            visibility: Possible values [Public, LocalOnly]

        Returns:
            requests.Response: result of API call (wrap in CommunityResponse if successful)
        """
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/community", json=form, params=None)

        return result

    def list_communities(
        self,
        type_: str = None,
        sort: str = None,
        show_nsfw: bool = None,
        page: int = None,
        limit: int = None
    ):
        """ List communities, with various filters.
        Args:
            type_: Possible values [All, Local, Subscribed, ModeratorView]
            sort: Possible values [Active, Hot, New, Old, TopDay, TopWeek, TopMonth, TopYear, TopAll, MostComments, NewComments, TopHour, TopSixHour, TopTwelveHour, TopThreeMonths, TopSixMonths, TopNineMonths, Controversial, Scaled]
            show_nsfw: ListCommunities.show_nsfw
            page: ListCommunities.page
            limit: ListCommunities.limit

        Returns:
            requests.Response: result of API call (wrap in ListCommunitiesResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/community/list", json=None, params=form)

        return result

    def follow_community(
        self,
        community_id: int,
        follow: bool
    ):
        """ Follow / subscribe to a community.
        Args:
            community_id: CommunityId
            follow: FollowCommunity.follow

        Returns:
            requests.Response: result of API call (wrap in CommunityResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/community/follow", json=form, params=None)

        return result

    def block_community(
        self,
        community_id: int,
        block: bool
    ):
        """ Block a community.
        Args:
            community_id: CommunityId
            block: BlockCommunity.block

        Returns:
            requests.Response: result of API call (wrap in BlockCommunityResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/community/block", json=form, params=None)

        return result

    def delete_community(
        self,
        community_id: int,
        deleted: bool
    ):
        """ Delete a community.
        Args:
            community_id: CommunityId
            deleted: DeleteCommunity.deleted

        Returns:
            requests.Response: result of API call (wrap in CommunityResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/community/delete", json=form, params=None)

        return result

    def hide_community(
        self,
        community_id: int,
        hidden: bool,
        reason: str = None
    ):
        """ Hide a community from public / "All" view. Admins only.
        Args:
            community_id: CommunityId
            hidden: HideCommunity.hidden
            reason: HideCommunity.reason

        Returns:
            requests.Response: result of API call (wrap in SuccessResponse if successful)
        """
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/community/hide", json=form, params=None)

        return result

    def remove_community(
        self,
        community_id: int,
        removed: bool,
        reason: str = None
    ):
        """ A moderator remove for a community.
        Args:
            community_id: CommunityId
            removed: RemoveCommunity.removed
            reason: RemoveCommunity.reason

        Returns:
            requests.Response: result of API call (wrap in CommunityResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/community/remove", json=form, params=None)

        return result

    def transfer_community(
        self,
        community_id: int,
        person_id: int
    ):
        """ Transfer your community to an existing moderator.
        Args:
            community_id: CommunityId
            person_id: PersonId

        Returns:
            requests.Response: result of API call (wrap in GetCommunityResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/community/transfer", json=form, params=None)

        return result

    def ban_from_community(
        self,
        community_id: int,
        person_id: int,
        ban: bool,
        remove_data: bool = None,
        reason: str = None,
        expires: int = None
    ):
        """ Ban a user from a community.
        Args:
            community_id: CommunityId
            person_id: PersonId
            ban: BanFromCommunity.ban
            remove_data: BanFromCommunity.remove_data
            reason: BanFromCommunity.reason
            expires: BanFromCommunity.expires

        Returns:
            requests.Response: result of API call (wrap in BanFromCommunityResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/community/ban_user", json=form, params=None)

        return result

    def add_mod_to_community(
        self,
        community_id: int,
        person_id: int,
        added: bool
    ):
        """ Add a moderator to your community.
        Args:
            community_id: CommunityId
            person_id: PersonId
            added: AddModToCommunity.added

        Returns:
            requests.Response: result of API call (wrap in AddModToCommunityResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/community/mod", json=form, params=None)

        return result

    def create_post(
        self,
        name: str,
        community_id: int,
        url: str = None,
        body: str = None,
        alt_text: str = None,
        honeypot: str = None,
        nsfw: bool = None,
        language_id: int = None,
        custom_thumbnail: str = None
    ):
        """ Create a post.
        Args:
            name: CreatePost.name
            community_id: CommunityId
            url: CreatePost.url
            body: CreatePost.body
            alt_text: CreatePost.alt_text
            honeypot: CreatePost.honeypot
            nsfw: CreatePost.nsfw
            language_id: LanguageId
            custom_thumbnail: CreatePost.custom_thumbnail

        Returns:
            requests.Response: result of API call (wrap in PostResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/post", json=form, params=None)

        return result

    def get_post(
        self,
        id: int = None,
        comment_id: int = None
    ):
        """ Get / fetch a post.
        Args:
            id: PostId
            comment_id: CommentId

        Returns:
            requests.Response: result of API call (wrap in GetPostResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/post", json=None, params=form)

        return result

    def edit_post(
        self,
        post_id: int,
        name: str = None,
        url: str = None,
        body: str = None,
        alt_text: str = None,
        nsfw: bool = None,
        language_id: int = None,
        custom_thumbnail: str = None
    ):
        """ Edit a post.
        Args:
            post_id: PostId
            name: EditPost.name
            url: EditPost.url
            body: EditPost.body
            alt_text: EditPost.alt_text
            nsfw: EditPost.nsfw
            language_id: LanguageId
            custom_thumbnail: EditPost.custom_thumbnail

        Returns:
            requests.Response: result of API call (wrap in PostResponse if successful)
        """
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/post", json=form, params=None)

        return result

    def delete_post(
        self,
        post_id: int,
        deleted: bool
    ):
        """ Delete a post.
        Args:
            post_id: PostId
            deleted: DeletePost.deleted

        Returns:
            requests.Response: result of API call (wrap in PostResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/post/delete", json=form, params=None)

        return result

    def remove_post(
        self,
        post_id: int,
        removed: bool,
        reason: str = None
    ):
        """ A moderator remove for a post.
        Args:
            post_id: PostId
            removed: RemovePost.removed
            reason: RemovePost.reason

        Returns:
            requests.Response: result of API call (wrap in PostResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/post/remove", json=form, params=None)

        return result

    def mark_post_as_read(
        self,
        post_ids: list[int],
        read: bool
    ):
        """ Mark a post as read.
        Args:
            post_ids: MarkPostAsRead.post_ids
            read: MarkPostAsRead.read

        Returns:
            requests.Response: result of API call (wrap in SuccessResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/post/mark_as_read", json=form, params=None)

        return result

    def hide_post(
        self,
        post_ids: list[int],
        hide: bool
    ):
        """ Hide a post from list views.
        Args:
            post_ids: HidePost.post_ids
            hide: HidePost.hide

        Returns:
            requests.Response: result of API call (wrap in SuccessResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/post/hide", json=form, params=None)

        return result

    def lock_post(
        self,
        post_id: int,
        locked: bool
    ):
        """ A moderator can lock a post ( IE disable new comments ).
        Args:
            post_id: PostId
            locked: LockPost.locked

        Returns:
            requests.Response: result of API call (wrap in PostResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/post/lock", json=form, params=None)

        return result

    def feature_post(
        self,
        post_id: int,
        featured: bool,
        feature_type: str
    ):
        """ A moderator can feature a community post ( IE stick it to the top of a community ).
        Args:
            post_id: PostId
            featured: FeaturePost.featured
            feature_type: Possible values [Local, Community]

        Returns:
            requests.Response: result of API call (wrap in PostResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/post/feature", json=form, params=None)

        return result

    def get_posts(
        self,
        type_: str = None,
        sort: str = None,
        page: int = None,
        limit: int = None,
        community_id: int = None,
        community_name: str = None,
        saved_only: bool = None,
        liked_only: bool = None,
        disliked_only: bool = None,
        show_hidden: bool = None,
        show_read: bool = None,
        show_nsfw: bool = None,
        page_cursor: str = None
    ):
        """ Get / fetch posts, with various filters.
        Args:
            type_: Possible values [All, Local, Subscribed, ModeratorView]
            sort: Possible values [Active, Hot, New, Old, TopDay, TopWeek, TopMonth, TopYear, TopAll, MostComments, NewComments, TopHour, TopSixHour, TopTwelveHour, TopThreeMonths, TopSixMonths, TopNineMonths, Controversial, Scaled]
            page: GetPosts.page
            limit: GetPosts.limit
            community_id: CommunityId
            community_name: GetPosts.community_name
            saved_only: GetPosts.saved_only
            liked_only: GetPosts.liked_only
            disliked_only: GetPosts.disliked_only
            show_hidden: GetPosts.show_hidden
            show_read
            show_nsfw
            page_cursor: PaginationCursor

        Returns:
            requests.Response: result of API call (wrap in GetPostsResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/post/list", json=None, params=form)

        return result

    def like_post(
        self,
        post_id: int,
        score: int
    ):
        """ Like / vote on a post.
        Args:
            post_id: PostId
            score: CreatePostLike.score

        Returns:
            requests.Response: result of API call (wrap in PostResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/post/like", json=form, params=None)

        return result

    def list_post_likes(
        self,
        post_id: int,
        page: int = None,
        limit: int = None
    ):
        """ List a post's likes. Admin-only.
        Args:
            post_id: PostId
            page: ListPostLikes.page
            limit: ListPostLikes.limit

        Returns:
            requests.Response: result of API call (wrap in ListPostLikesResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/post/like/list", json=None, params=form)

        return result

    def save_post(
        self,
        post_id: int,
        save: bool
    ):
        """ Save a post.
        Args:
            post_id: PostId
            save: SavePost.save

        Returns:
            requests.Response: result of API call (wrap in PostResponse if successful)
        """
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/post/save", json=form, params=None)

        return result

    def create_post_report(
        self,
        post_id: int,
        reason: str
    ):
        """ Report a post.
        Args:
            post_id: PostId
            reason: CreatePostReport.reason

        Returns:
            requests.Response: result of API call (wrap in PostReportResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/post/report", json=form, params=None)

        return result

    def resolve_post_report(
        self,
        report_id: int,
        resolved: bool
    ):
        """ Resolve a post report. Only a mod can do this.
        Args:
            report_id: PostReportId
            resolved: ResolvePostReport.resolved

        Returns:
            requests.Response: result of API call (wrap in PostReportResponse if successful)
        """
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/post/report/resolve", json=form, params=None)

        return result

    def list_post_reports(
        self,
        page: int = None,
        limit: int = None,
        unresolved_only: bool = None,
        community_id: int = None,
        post_id: int = None
    ):
        """ List post reports.
        Args:
            page: ListPostReports.page
            limit: ListPostReports.limit
            unresolved_only: ListPostReports.unresolved_only
            community_id: CommunityId
            post_id: PostId

        Returns:
            requests.Response: result of API call (wrap in ListPostReportsResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/post/report/list", json=None, params=form)

        return result

    def get_site_metadata(
        self,
        url: str
    ):
        """ Fetch metadata for any given site.
        Args:
            url: GetSiteMetadata.url

        Returns:
            requests.Response: result of API call (wrap in GetSiteMetadataResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/post/site_metadata", json=None, params=form)

        return result

    def create_comment(
        self,
        content: str,
        post_id: int,
        parent_id: int = None,
        language_id: int = None
    ):
        """ Create a comment.
        Args:
            content: CreateComment.content
            post_id: PostId
            parent_id: CommentId
            language_id: LanguageId

        Returns:
            requests.Response: result of API call (wrap in CommentResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/comment", json=form, params=None)

        return result

    def edit_comment(
        self,
        comment_id: int,
        content: str = None,
        language_id: int = None
    ):
        """ Edit a comment.
        Args:
            comment_id: CommentId
            content: EditComment.content
            language_id: LanguageId

        Returns:
            requests.Response: result of API call (wrap in CommentResponse if successful)
        """
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/comment", json=form, params=None)

        return result

    def delete_comment(
        self,
        comment_id: int,
        deleted: bool
    ):
        """ Delete a comment.
        Args:
            comment_id: CommentId
            deleted: DeleteComment.deleted

        Returns:
            requests.Response: result of API call (wrap in CommentResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/comment/delete", json=form, params=None)

        return result

    def remove_comment(
        self,
        comment_id: int,
        removed: bool,
        reason: str = None
    ):
        """ A moderator remove for a comment.
        Args:
            comment_id: CommentId
            removed: RemoveComment.removed
            reason: RemoveComment.reason

        Returns:
            requests.Response: result of API call (wrap in CommentResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/comment/remove", json=form, params=None)

        return result

    def mark_comment_reply_as_read(
        self,
        comment_reply_id: int,
        read: bool
    ):
        """ Mark a comment as read.
        Args:
            comment_reply_id: CommentReplyId
            read: MarkCommentReplyAsRead.read

        Returns:
            requests.Response: result of API call (wrap in CommentReplyResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/comment/mark_as_read", json=form, params=None)

        return result

    def like_comment(
        self,
        comment_id: int,
        score: int
    ):
        """ Like / vote on a comment.
        Args:
            comment_id: CommentId
            score: CreateCommentLike.score

        Returns:
            requests.Response: result of API call (wrap in CommentResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/comment/like", json=form, params=None)

        return result

    def list_comment_likes(
        self,
        comment_id: int,
        page: int = None,
        limit: int = None
    ):
        """ List a comment's likes. Admin-only.
        Args:
            comment_id: CommentId
            page: ListCommentLikes.page
            limit: ListCommentLikes.limit

        Returns:
            requests.Response: result of API call (wrap in ListCommentLikesResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/comment/like/list", json=None, params=form)

        return result

    def save_comment(
        self,
        comment_id: int,
        save: bool
    ):
        """ Save a comment.
        Args:
            comment_id: CommentId
            save: SaveComment.save

        Returns:
            requests.Response: result of API call (wrap in CommentResponse if successful)
        """
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/comment/save", json=form, params=None)

        return result

    def distinguish_comment(
        self,
        comment_id: int,
        distinguished: bool
    ):
        """ Distinguishes a comment (speak as moderator)
        Args:
            comment_id: CommentId
            distinguished: DistinguishComment.distinguished

        Returns:
            requests.Response: result of API call (wrap in CommentResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/comment/distinguish", json=form, params=None)

        return result

    def get_comments(
        self,
        type_: str = None,
        sort: str = None,
        max_depth: int = None,
        page: int = None,
        limit: int = None,
        community_id: int = None,
        community_name: str = None,
        post_id: int = None,
        parent_id: int = None,
        saved_only: bool = None,
        liked_only: bool = None,
        disliked_only: bool = None
    ):
        """ Get / fetch comments.
        Args:
            type_: Possible values [All, Local, Subscribed, ModeratorView]
            sort: Possible values [Hot, Top, New, Old, Controversial]
            max_depth: GetComments.max_depth
            page: GetComments.page
            limit: GetComments.limit
            community_id: CommunityId
            community_name: GetComments.community_name
            post_id: PostId
            parent_id: CommentId
            saved_only: GetComments.saved_only
            liked_only: GetComments.liked_only
            disliked_only: GetComments.disliked_only

        Returns:
            requests.Response: result of API call (wrap in GetCommentsResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/comment/list", json=None, params=form)

        return result

    def get_comment(
        self,
        id: int
    ):
        """ Get / fetch comment.
        Args:
            id: CommentId

        Returns:
            requests.Response: result of API call (wrap in CommentResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/comment", json=None, params=form)

        return result

    def create_comment_report(
        self,
        comment_id: int,
        reason: str
    ):
        """ Report a comment.
        Args:
            comment_id: CommentId
            reason: CreateCommentReport.reason

        Returns:
            requests.Response: result of API call (wrap in CommentReportResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/comment/report", json=form, params=None)

        return result

    def resolve_comment_report(
        self,
        report_id: int,
        resolved: bool
    ):
        """ Resolve a comment report. Only a mod can do this.
        Args:
            report_id: CommentReportId
            resolved: ResolveCommentReport.resolved

        Returns:
            requests.Response: result of API call (wrap in CommentReportResponse if successful)
        """
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/comment/report/resolve", json=form, params=None)

        return result

    def list_comment_reports(
        self,
        comment_id: int = None,
        page: int = None,
        limit: int = None,
        unresolved_only: bool = None,
        community_id: int = None
    ):
        """ List comment reports.
        Args:
            comment_id: CommentId
            page: ListCommentReports.page
            limit: ListCommentReports.limit
            unresolved_only: ListCommentReports.unresolved_only
            community_id: CommunityId

        Returns:
            requests.Response: result of API call (wrap in ListCommentReportsResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/comment/report/list", json=None, params=form)

        return result

    def get_private_messages(
        self,
        unread_only: bool = None,
        page: int = None,
        limit: int = None,
        creator_id: int = None
    ):
        """ Get / fetch private messages.
        Args:
            unread_only: GetPrivateMessages.unread_only
            page: GetPrivateMessages.page
            limit: GetPrivateMessages.limit
            creator_id: PersonId

        Returns:
            requests.Response: result of API call (wrap in PrivateMessagesResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/private_message/list", json=None, params=form)

        return result

    def create_private_message(
        self,
        content: str,
        recipient_id: int
    ):
        """ Create a private message.
        Args:
            content: CreatePrivateMessage.content
            recipient_id: PersonId

        Returns:
            requests.Response: result of API call (wrap in PrivateMessageResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/private_message", json=form, params=None)

        return result

    def edit_private_message(
        self,
        private_message_id: int,
        content: str
    ):
        """ Edit a private message.
        Args:
            private_message_id: PrivateMessageId
            content: EditPrivateMessage.content

        Returns:
            requests.Response: result of API call (wrap in PrivateMessageResponse if successful)
        """
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/private_message", json=form, params=None)

        return result

    def delete_private_message(
        self,
        private_message_id: int,
        deleted: bool
    ):
        """ Delete a private message.
        Args:
            private_message_id: PrivateMessageId
            deleted: DeletePrivateMessage.deleted

        Returns:
            requests.Response: result of API call (wrap in PrivateMessageResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/private_message/delete", json=form, params=None)

        return result

    def mark_private_message_as_read(
        self,
        private_message_id: int,
        read: bool
    ):
        """ Mark a private message as read.
        Args:
            private_message_id: PrivateMessageId
            read: MarkPrivateMessageAsRead.read

        Returns:
            requests.Response: result of API call (wrap in PrivateMessageResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/private_message/mark_as_read", json=form, params=None)

        return result

    def create_private_message_report(
        self,
        private_message_id: int,
        reason: str
    ):
        """ Create a report for a private message.
        Args:
            private_message_id: PrivateMessageId
            reason: CreatePrivateMessageReport.reason

        Returns:
            requests.Response: result of API call (wrap in PrivateMessageReportResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/private_message/report", json=form, params=None)

        return result

    def resolve_private_message_report(
        self,
        report_id: int,
        resolved: bool
    ):
        """ Resolve a report for a private message.
        Args:
            report_id: PrivateMessageReportId
            resolved: ResolvePrivateMessageReport.resolved

        Returns:
            requests.Response: result of API call (wrap in PrivateMessageReportResponse if successful)
        """
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/private_message/report/resolve", json=form, params=None)

        return result

    def list_private_message_reports(
        self,
        page: int = None,
        limit: int = None,
        unresolved_only: bool = None
    ):
        """ List private message reports.
        Args:
            page: ListPrivateMessageReports.page
            limit: ListPrivateMessageReports.limit
            unresolved_only: ListPrivateMessageReports.unresolved_only

        Returns:
            requests.Response: result of API call (wrap in ListPrivateMessageReportsResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/private_message/report/list", json=None, params=form)

        return result

    def register(
        self,
        username: str,
        password: str,
        password_verify: str,
        show_nsfw: bool = None,
        email: str = None,
        captcha_uuid: str = None,
        captcha_answer: str = None,
        honeypot: str = None,
        answer: str = None
    ):
        """ Register a new user.
        Args:
            username: Register.username
            password: Register.password
            password_verify: Register.password_verify
            show_nsfw: Register.show_nsfw
            email: Register.email
            captcha_uuid: Register.captcha_uuid
            captcha_answer: Register.captcha_answer
            honeypot: Register.honeypot
            answer: Register.answer

        Returns:
            requests.Response: result of API call (wrap in LoginResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/register", json=form, params=None)

        return result

    def login(
        self,
        username_or_email: str,
        password: str,
        totp_2fa_token: str = None
    ):
        """ Log into lemmy.
        Args:
            username_or_email: Login.username_or_email
            password: Login.password
            totp_2fa_token: Login.totp_2fa_token

        Returns:
            requests.Response: result of API call (wrap in LoginResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/login", json=form, params=None)
        if result.status_code == 200:
            self._session = create_session(self._headers, result.json()["jwt"])
        else:
            raise Exception("Login failed with status code: " + str(result.status_code))
        return result

    def logout(
        self
    ):
        """ [MANUAL] Logout your user, which clears the cookie and invalidates the auth token


        Returns:
            requests.Response: result of API call (wrap in SuccessResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/logout", json=form, params=None)
        if result.status_code == 200:
            self._session = create_session(self._headers, None)
        return result

    def get_person_details(
        self,
        person_id: int = None,
        username: str = None,
        sort: str = None,
        page: int = None,
        limit: int = None,
        community_id: int = None,
        saved_only: bool = None
    ):
        """ Get the details for a person.
        Args:
            person_id: PersonId
            username: GetPersonDetails.username
            sort: Possible values [Active, Hot, New, Old, TopDay, TopWeek, TopMonth, TopYear, TopAll, MostComments, NewComments, TopHour, TopSixHour, TopTwelveHour, TopThreeMonths, TopSixMonths, TopNineMonths, Controversial, Scaled]
            page: GetPersonDetails.page
            limit: GetPersonDetails.limit
            community_id: CommunityId
            saved_only: GetPersonDetails.saved_only

        Returns:
            requests.Response: result of API call (wrap in GetPersonDetailsResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/user", json=None, params=form)

        return result

    def get_person_mentions(
        self,
        sort: str = None,
        page: int = None,
        limit: int = None,
        unread_only: bool = None
    ):
        """ Get mentions for your user.
        Args:
            sort: Possible values [Hot, Top, New, Old, Controversial]
            page: GetPersonMentions.page
            limit: GetPersonMentions.limit
            unread_only: GetPersonMentions.unread_only

        Returns:
            requests.Response: result of API call (wrap in GetPersonMentionsResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/user/mention", json=None, params=form)

        return result

    def mark_person_mention_as_read(
        self,
        person_mention_id: int,
        read: bool
    ):
        """ Mark a person mention as read.
        Args:
            person_mention_id: PersonMentionId
            read: MarkPersonMentionAsRead.read

        Returns:
            requests.Response: result of API call (wrap in PersonMentionResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/mention/mark_as_read", json=form, params=None)

        return result

    def get_replies(
        self,
        sort: str = None,
        page: int = None,
        limit: int = None,
        unread_only: bool = None
    ):
        """ Get comment replies.
        Args:
            sort: Possible values [Hot, Top, New, Old, Controversial]
            page: GetReplies.page
            limit: GetReplies.limit
            unread_only: GetReplies.unread_only

        Returns:
            requests.Response: result of API call (wrap in GetRepliesResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/user/replies", json=None, params=form)

        return result

    def ban_person(
        self,
        person_id: int,
        ban: bool,
        remove_data: bool = None,
        reason: str = None,
        expires: int = None
    ):
        """ Ban a person from your site.
        Args:
            person_id: PersonId
            ban: BanPerson.ban
            remove_data: BanPerson.remove_data
            reason: BanPerson.reason
            expires: BanPerson.expires

        Returns:
            requests.Response: result of API call (wrap in BanPersonResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/ban", json=form, params=None)

        return result

    def get_banned_persons(
        self
    ):
        """ Get a list of banned users


        Returns:
            requests.Response: result of API call (wrap in BannedPersonsResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/user/banned", json=None, params=form)

        return result

    def block_person(
        self,
        person_id: int,
        block: bool
    ):
        """ Block a person.
        Args:
            person_id: PersonId
            block: BlockPerson.block

        Returns:
            requests.Response: result of API call (wrap in BlockPersonResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/block", json=form, params=None)

        return result

    def get_captcha(
        self
    ):
        """ Fetch a Captcha.


        Returns:
            requests.Response: result of API call (wrap in GetCaptchaResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/user/get_captcha", json=None, params=form)

        return result

    def delete_account(
        self,
        password: str,
        delete_content: bool
    ):
        """ Delete your account.
        Args:
            password: DeleteAccount.password
            delete_content: DeleteAccount.delete_content

        Returns:
            requests.Response: result of API call (wrap in SuccessResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/delete_account", json=form, params=None)

        return result

    def password_reset(
        self,
        email: str
    ):
        """ Reset your password.
        Args:
            email: PasswordReset.email

        Returns:
            requests.Response: result of API call (wrap in SuccessResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/password_reset", json=form, params=None)

        return result

    def password_change_after_reset(
        self,
        token: str,
        password: str,
        password_verify: str
    ):
        """ Change your password from an email / token based reset.
        Args:
            token: PasswordChangeAfterReset.token
            password: PasswordChangeAfterReset.password
            password_verify: PasswordChangeAfterReset.password_verify

        Returns:
            requests.Response: result of API call (wrap in SuccessResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/password_change", json=form, params=None)

        return result

    def mark_all_as_read(
        self
    ):
        """ Mark all replies as read.


        Returns:
            requests.Response: result of API call (wrap in GetRepliesResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/mark_all_as_read", json=form, params=None)

        return result

    def save_user_settings(
        self,
        show_nsfw: bool = None,
        blur_nsfw: bool = None,
        auto_expand: bool = None,
        theme: str = None,
        default_sort_type: str = None,
        default_listing_type: str = None,
        interface_language: str = None,
        avatar: str = None,
        banner: str = None,
        display_name: str = None,
        email: str = None,
        bio: str = None,
        matrix_user_id: str = None,
        show_avatars: bool = None,
        send_notifications_to_email: bool = None,
        bot_account: bool = None,
        show_bot_accounts: bool = None,
        show_read_posts: bool = None,
        discussion_languages: list[int] = None,
        open_links_in_new_tab: bool = None,
        infinite_scroll_enabled: bool = None,
        post_listing_mode: str = None,
        enable_keyboard_navigation: bool = None,
        enable_animated_images: bool = None,
        collapse_bot_comments: bool = None,
        show_scores: bool = None,
        show_upvotes: bool = None,
        show_downvotes: bool = None,
        show_upvote_percentage: bool = None
    ):
        """ Save your user settings.
        Args:
            show_nsfw: SaveUserSettings.show_nsfw
            blur_nsfw: SaveUserSettings.blur_nsfw
            auto_expand: SaveUserSettings.auto_expand
            theme: SaveUserSettings.theme
            default_sort_type: Possible values [Active, Hot, New, Old, TopDay, TopWeek, TopMonth, TopYear, TopAll, MostComments, NewComments, TopHour, TopSixHour, TopTwelveHour, TopThreeMonths, TopSixMonths, TopNineMonths, Controversial, Scaled]
            default_listing_type: Possible values [All, Local, Subscribed, ModeratorView]
            interface_language: SaveUserSettings.interface_language
            avatar: SaveUserSettings.avatar
            banner: SaveUserSettings.banner
            display_name: SaveUserSettings.display_name
            email: SaveUserSettings.email
            bio: SaveUserSettings.bio
            matrix_user_id: SaveUserSettings.matrix_user_id
            show_avatars: SaveUserSettings.show_avatars
            send_notifications_to_email: SaveUserSettings.send_notifications_to_email
            bot_account: SaveUserSettings.bot_account
            show_bot_accounts: SaveUserSettings.show_bot_accounts
            show_read_posts: SaveUserSettings.show_read_posts
            discussion_languages: SaveUserSettings.discussion_languages
            open_links_in_new_tab: SaveUserSettings.open_links_in_new_tab
            infinite_scroll_enabled: SaveUserSettings.infinite_scroll_enabled
            post_listing_mode: Possible values [List, Card, SmallCard]
            enable_keyboard_navigation: SaveUserSettings.enable_keyboard_navigation
            enable_animated_images: SaveUserSettings.enable_animated_images
            collapse_bot_comments: SaveUserSettings.collapse_bot_comments
            show_scores: SaveUserSettings.show_scores
            show_upvotes: SaveUserSettings.show_upvotes
            show_downvotes: SaveUserSettings.show_downvotes
            show_upvote_percentage: SaveUserSettings.show_upvote_percentage

        Returns:
            requests.Response: result of API call (wrap in SuccessResponse if successful)
        """
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/user/save_user_settings", json=form, params=None)

        return result

    def change_password(
        self,
        new_password: str,
        new_password_verify: str,
        old_password: str
    ):
        """ Change your user password.
        Args:
            new_password: ChangePassword.new_password
            new_password_verify: ChangePassword.new_password_verify
            old_password: ChangePassword.old_password

        Returns:
            requests.Response: result of API call (wrap in LoginResponse if successful)
        """
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/user/change_password", json=form, params=None)

        return result

    def get_report_count(
        self,
        community_id: int = None
    ):
        """ Get counts for your reports
        Args:
            community_id: CommunityId

        Returns:
            requests.Response: result of API call (wrap in GetReportCountResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/user/report_count", json=None, params=form)

        return result

    def get_unread_count(
        self
    ):
        """ Get your unread counts


        Returns:
            requests.Response: result of API call (wrap in GetUnreadCountResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/user/unread_count", json=None, params=form)

        return result

    def verify_email(
        self,
        token: str
    ):
        """ Verify your email
        Args:
            token: VerifyEmail.token

        Returns:
            requests.Response: result of API call (wrap in SuccessResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/verify_email", json=form, params=None)

        return result

    def add_admin(
        self,
        person_id: int,
        added: bool
    ):
        """ Add an admin to your site.
        Args:
            person_id: PersonId
            added: AddAdmin.added

        Returns:
            requests.Response: result of API call (wrap in AddAdminResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/admin/add", json=form, params=None)

        return result

    def get_unread_registration_application_count(
        self
    ):
        """ Get the unread registration applications count.


        Returns:
            requests.Response: result of API call (wrap in GetUnreadRegistrationApplicationCountResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/admin/registration_application/count", json=None, params=form)

        return result

    def list_registration_applications(
        self,
        unread_only: bool = None,
        page: int = None,
        limit: int = None
    ):
        """ List the registration applications.
        Args:
            unread_only: ListRegistrationApplications.unread_only
            page: ListRegistrationApplications.page
            limit: ListRegistrationApplications.limit

        Returns:
            requests.Response: result of API call (wrap in ListRegistrationApplicationsResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/admin/registration_application/list", json=None, params=form)

        return result

    def approve_registration_application(
        self,
        id: int,
        approve: bool,
        deny_reason: str = None
    ):
        """ Approve a registration application
        Args:
            id: ApproveRegistrationApplication.id
            approve: ApproveRegistrationApplication.approve
            deny_reason: ApproveRegistrationApplication.deny_reason

        Returns:
            requests.Response: result of API call (wrap in RegistrationApplicationResponse if successful)
        """
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/admin/registration_application/approve", json=form, params=None)

        return result

    def get_registration_application(
        self,
        person_id: int
    ):

        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/admin/registration_application", json=None, params=form)

        return result

    def purge_person(
        self,
        person_id: int,
        reason: str = None
    ):
        """ Purge / Delete a person from the database.
        Args:
            person_id: PersonId
            reason: PurgePerson.reason

        Returns:
            requests.Response: result of API call (wrap in SuccessResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/admin/purge/person", json=form, params=None)

        return result

    def purge_community(
        self,
        community_id: int,
        reason: str = None
    ):
        """ Purge / Delete a community from the database.
        Args:
            community_id: CommunityId
            reason: PurgeCommunity.reason

        Returns:
            requests.Response: result of API call (wrap in SuccessResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/admin/purge/community", json=form, params=None)

        return result

    def purge_post(
        self,
        post_id: int,
        reason: str = None
    ):
        """ Purge / Delete a post from the database.
        Args:
            post_id: PostId
            reason: PurgePost.reason

        Returns:
            requests.Response: result of API call (wrap in SuccessResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/admin/purge/post", json=form, params=None)

        return result

    def purge_comment(
        self,
        comment_id: int,
        reason: str = None
    ):
        """ Purge / Delete a comment from the database.
        Args:
            comment_id: CommentId
            reason: PurgeComment.reason

        Returns:
            requests.Response: result of API call (wrap in SuccessResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/admin/purge/comment", json=form, params=None)

        return result

    def create_custom_emoji(
        self,
        category: str,
        shortcode: str,
        image_url: str,
        alt_text: str,
        keywords: list[str]
    ):
        """ Create a new custom emoji
        Args:
            category: CreateCustomEmoji.category
            shortcode: CreateCustomEmoji.shortcode
            image_url: CreateCustomEmoji.image_url
            alt_text: CreateCustomEmoji.alt_text
            keywords: CreateCustomEmoji.keywords

        Returns:
            requests.Response: result of API call (wrap in CustomEmojiResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/custom_emoji", json=form, params=None)

        return result

    def edit_custom_emoji(
        self,
        id: int,
        category: str,
        image_url: str,
        alt_text: str,
        keywords: list[str]
    ):
        """ Edit an existing custom emoji
        Args:
            id: CustomEmojiId
            category: EditCustomEmoji.category
            image_url: EditCustomEmoji.image_url
            alt_text: EditCustomEmoji.alt_text
            keywords: EditCustomEmoji.keywords

        Returns:
            requests.Response: result of API call (wrap in CustomEmojiResponse if successful)
        """
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/custom_emoji", json=form, params=None)

        return result

    def delete_custom_emoji(
        self,
        id: int
    ):
        """ Delete a custom emoji
        Args:
            id: CustomEmojiId

        Returns:
            requests.Response: result of API call (wrap in SuccessResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/custom_emoji/delete", json=form, params=None)

        return result

    def get_federated_instances(
        self
    ):
        """ Fetch federated instances.


        Returns:
            requests.Response: result of API call (wrap in GetFederatedInstancesResponse if successful)
        """
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/federated_instances", json=None, params=form)

        return result

    def block_instance(
        self,
        instance_id: int,
        block: bool
    ):
        """ Block an instance.
        Args:
            instance_id: InstanceId
            block: BlockInstance.block

        Returns:
            requests.Response: result of API call (wrap in BlockInstanceResponse if successful)
        """
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/site/block", json=form, params=None)

        return result
