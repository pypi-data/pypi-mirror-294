import textwrap
from typing import List

from tree_sitter import Node, Tree
from ..models import HttpMethod, ApiMethod
from ..util import to_snake_case, normalize_type
from ..generator.http_generator import HttpGenerator
from .visitor import Visitor


class HttpVisitor(Visitor):
    _encoding = "utf-8"
    _number_type = "long"
    _ts_match = ["HttpType.Get", "HttpType.Post", "HttpType.Put", "HttpType.Delete"]
    _domain_match = [HttpMethod.GET, HttpMethod.POST, HttpMethod.PUT, HttpMethod.DELETE]

    def __init__(self, tree: Tree):
        self.tree = tree
        self.methods = []
        self._current_name = None
        self._current_input = None
        self._current_output = None
        self._current_method = None
        self._current_url = None

    def _push_and_reset(self):
        if (
            self._current_name is not None and
            self._current_input is not None and
            self._current_output is not None and
            self._current_method is not None and
            self._current_url is not None
        ):
            self.methods.append(
                ApiMethod(
                    self._current_name,
                    self._current_input,
                    self._current_output,
                    self._current_method,
                    self._current_url
                )
            )

        self._current_name = None
        self._current_input = None
        self._current_output = None
        self._current_method = None
        self._current_url = None

    def visit_method_definition(self, node: Node):
        self._push_and_reset()
        name = node.child_by_field_name("name").text.decode(self._encoding)
        if name in [
            "constructor",
            "#buildFullUrl",
            "#wrapper",
            "#fetchFunction",
            "setHeaders",
            "encodeGetParams",
            "createFormData",
            "uploadImage",
            "deleteImage"
        ]:
            return

        self._current_name = to_snake_case(name)
        self._accept(node.child_by_field_name("body"))

    def visit_function_declaration(self, node: Node):
        self.visit_method_definition(node)

    def visit_type_arguments(self, node: Node):
        self._current_input = normalize_type(node.children[1].text.decode(self._encoding))
        self._current_output = normalize_type(node.children[3].text.decode(self._encoding))

    def visit_arguments(self, node: Node):
        if self._current_name is None:
            return

        ts_http_method = node.children[1].text.decode(self._encoding)
        self._current_method = self._domain_match[self._ts_match.index(ts_http_method)]
        self._current_url = node.children[3].children[1].text.decode(self._encoding)

