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

