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
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/site", json=form, params=None)

        return result

    def leave_admin(
        self
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/leave_admin", json=form, params=None)

        return result

    def generate_totp_secret(
        self
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/totp/generate", json=form, params=None)

        return result

    def export_settings(
        self
    ):
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/user/export_settings", json=None, params=form)

        return result

    def import_settings(
        self
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/import_settings", json=form, params=None)

        return result

    def list_logins(
        self
    ):
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/user/list_logins", json=None, params=form)

        return result

    def validate_auth(
        self
    ):
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/user/validate_auth", json=None, params=form)

        return result

    def list_media(
        self,
        page: int = None,
        limit: int = None
    ):
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/account/list_media", json=None, params=form)

        return result

    def list_all_media(
        self,
        page: int = None,
        limit: int = None
    ):
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/admin/list_all_media", json=None, params=form)

        return result

    def update_totp(
        self,
        totp_token: str,
        enabled: bool
    ):
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
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/search", json=None, params=form)

        return result

    def resolve_object(
        self,
        q: str
    ):
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
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/community", json=form, params=None)

        return result

    def get_community(
        self,
        id: int = None,
        name: str = None
    ):
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
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/community/list", json=None, params=form)

        return result

    def follow_community(
        self,
        community_id: int,
        follow: bool
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/community/follow", json=form, params=None)

        return result

    def block_community(
        self,
        community_id: int,
        block: bool
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/community/block", json=form, params=None)

        return result

    def delete_community(
        self,
        community_id: int,
        deleted: bool
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/community/delete", json=form, params=None)

        return result

    def hide_community(
        self,
        community_id: int,
        hidden: bool,
        reason: str = None
    ):
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/community/hide", json=form, params=None)

        return result

    def remove_community(
        self,
        community_id: int,
        removed: bool,
        reason: str = None
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/community/remove", json=form, params=None)

        return result

    def transfer_community(
        self,
        community_id: int,
        person_id: int
    ):
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
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/community/ban_user", json=form, params=None)

        return result

    def add_mod_to_community(
        self,
        community_id: int,
        person_id: int,
        added: bool
    ):
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
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/post", json=form, params=None)

        return result

    def get_post(
        self,
        id: int = None,
        comment_id: int = None
    ):
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
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/post", json=form, params=None)

        return result

    def delete_post(
        self,
        post_id: int,
        deleted: bool
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/post/delete", json=form, params=None)

        return result

    def remove_post(
        self,
        post_id: int,
        removed: bool,
        reason: str = None
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/post/remove", json=form, params=None)

        return result

    def mark_post_as_read(
        self,
        post_ids: list[int],
        read: bool
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/post/mark_as_read", json=form, params=None)

        return result

    def hide_post(
        self,
        post_ids: list[int],
        hide: bool
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/post/hide", json=form, params=None)

        return result

    def lock_post(
        self,
        post_id: int,
        locked: bool
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/post/lock", json=form, params=None)

        return result

    def feature_post(
        self,
        post_id: int,
        featured: bool,
        feature_type: str
    ):
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
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/post/list", json=None, params=form)

        return result

    def like_post(
        self,
        post_id: int,
        score: int
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/post/like", json=form, params=None)

        return result

    def list_post_likes(
        self,
        post_id: int,
        page: int = None,
        limit: int = None
    ):
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/post/like/list", json=None, params=form)

        return result

    def save_post(
        self,
        post_id: int,
        save: bool
    ):
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/post/save", json=form, params=None)

        return result

    def create_post_report(
        self,
        post_id: int,
        reason: str
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/post/report", json=form, params=None)

        return result

    def resolve_post_report(
        self,
        report_id: int,
        resolved: bool
    ):
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
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/post/report/list", json=None, params=form)

        return result

    def get_site_metadata(
        self,
        url: str
    ):
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
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/comment", json=form, params=None)

        return result

    def edit_comment(
        self,
        comment_id: int,
        content: str = None,
        language_id: int = None
    ):
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/comment", json=form, params=None)

        return result

    def delete_comment(
        self,
        comment_id: int,
        deleted: bool
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/comment/delete", json=form, params=None)

        return result

    def remove_comment(
        self,
        comment_id: int,
        removed: bool,
        reason: str = None
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/comment/remove", json=form, params=None)

        return result

    def mark_comment_reply_as_read(
        self,
        comment_reply_id: int,
        read: bool
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/comment/mark_as_read", json=form, params=None)

        return result

    def like_comment(
        self,
        comment_id: int,
        score: int
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/comment/like", json=form, params=None)

        return result

    def list_comment_likes(
        self,
        comment_id: int,
        page: int = None,
        limit: int = None
    ):
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/comment/like/list", json=None, params=form)

        return result

    def save_comment(
        self,
        comment_id: int,
        save: bool
    ):
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/comment/save", json=form, params=None)

        return result

    def distinguish_comment(
        self,
        comment_id: int,
        distinguished: bool
    ):
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
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/comment/list", json=None, params=form)

        return result

    def get_comment(
        self,
        id: int
    ):
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/comment", json=None, params=form)

        return result

    def create_comment_report(
        self,
        comment_id: int,
        reason: str
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/comment/report", json=form, params=None)

        return result

    def resolve_comment_report(
        self,
        report_id: int,
        resolved: bool
    ):
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
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/private_message/list", json=None, params=form)

        return result

    def create_private_message(
        self,
        content: str,
        recipient_id: int
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/private_message", json=form, params=None)

        return result

    def edit_private_message(
        self,
        private_message_id: int,
        content: str
    ):
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/private_message", json=form, params=None)

        return result

    def delete_private_message(
        self,
        private_message_id: int,
        deleted: bool
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/private_message/delete", json=form, params=None)

        return result

    def mark_private_message_as_read(
        self,
        private_message_id: int,
        read: bool
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/private_message/mark_as_read", json=form, params=None)

        return result

    def create_private_message_report(
        self,
        private_message_id: int,
        reason: str
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/private_message/report", json=form, params=None)

        return result

    def resolve_private_message_report(
        self,
        report_id: int,
        resolved: bool
    ):
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/private_message/report/resolve", json=form, params=None)

        return result

    def list_private_message_reports(
        self,
        page: int = None,
        limit: int = None,
        unresolved_only: bool = None
    ):
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
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/register", json=form, params=None)

        return result

    def login(
        self,
        username_or_email: str,
        password: str,
        totp_2fa_token: str = None
    ):
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
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/user/mention", json=None, params=form)

        return result

    def mark_person_mention_as_read(
        self,
        person_mention_id: int,
        read: bool
    ):
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
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/ban", json=form, params=None)

        return result

    def get_banned_persons(
        self
    ):
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/user/banned", json=None, params=form)

        return result

    def block_person(
        self,
        person_id: int,
        block: bool
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/block", json=form, params=None)

        return result

    def get_captcha(
        self
    ):
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/user/get_captcha", json=None, params=form)

        return result

    def delete_account(
        self,
        password: str,
        delete_content: bool
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/delete_account", json=form, params=None)

        return result

    def password_reset(
        self,
        email: str
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/password_reset", json=form, params=None)

        return result

    def password_change_after_reset(
        self,
        token: str,
        password: str,
        password_verify: str
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/password_change", json=form, params=None)

        return result

    def mark_all_as_read(
        self
    ):
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
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/user/save_user_settings", json=form, params=None)

        return result

    def change_password(
        self,
        new_password: str,
        new_password_verify: str,
        old_password: str
    ):
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/user/change_password", json=form, params=None)

        return result

    def get_report_count(
        self,
        community_id: int = None
    ):
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/user/report_count", json=None, params=form)

        return result

    def get_unread_count(
        self
    ):
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/user/unread_count", json=None, params=form)

        return result

    def verify_email(
        self,
        token: str
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/user/verify_email", json=form, params=None)

        return result

    def add_admin(
        self,
        person_id: int,
        added: bool
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/admin/add", json=form, params=None)

        return result

    def get_unread_registration_application_count(
        self
    ):
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/admin/registration_application/count", json=None, params=form)

        return result

    def list_registration_applications(
        self,
        unread_only: bool = None,
        page: int = None,
        limit: int = None
    ):
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/admin/registration_application/list", json=None, params=form)

        return result

    def approve_registration_application(
        self,
        id: int,
        approve: bool,
        deny_reason: str = None
    ):
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
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/admin/purge/person", json=form, params=None)

        return result

    def purge_community(
        self,
        community_id: int,
        reason: str = None
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/admin/purge/community", json=form, params=None)

        return result

    def purge_post(
        self,
        post_id: int,
        reason: str = None
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/admin/purge/post", json=form, params=None)

        return result

    def purge_comment(
        self,
        comment_id: int,
        reason: str = None
    ):
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
        form = create_form(locals())
        result = put_handler(self._session, f"{self._api_url}/custom_emoji", json=form, params=None)

        return result

    def delete_custom_emoji(
        self,
        id: int
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/custom_emoji/delete", json=form, params=None)

        return result

    def get_federated_instances(
        self
    ):
        form = create_form(locals())
        result = get_handler(self._session, f"{self._api_url}/federated_instances", json=None, params=form)

        return result

    def block_instance(
        self,
        instance_id: int,
        block: bool
    ):
        form = create_form(locals())
        result = post_handler(self._session, f"{self._api_url}/site/block", json=form, params=None)

        return result
