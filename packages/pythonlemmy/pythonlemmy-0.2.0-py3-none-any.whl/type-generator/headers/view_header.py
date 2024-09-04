from typing import Optional

from .objects import *
from .utils import call_with_filtered_kwargs


class ViewObject(object):
    """ ViewObject: parent object to all view-related objects """

    def __init__(self, view: dict) -> None:
        self._view = view
        self.parse()


