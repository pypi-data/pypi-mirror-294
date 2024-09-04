import textwrap
from typing import List

from tree_sitter import Node, Tree

from ..models import Property, ClassType
from ..util import normalize_type
from .visitor import Visitor


class ModelVisitor(Visitor):
    _encoding = "utf-8"
    _number_type = "long"

    class_name = ""
    class_type = ClassType.OBJECT
    properties: List[Property] = []

    def __init__(self, tree: Tree, enums: List[str]):
        self.tree = tree
        self._enums = enums
        self.class_name = ""
        self.class_type = ClassType.OBJECT
        self.properties = []

    def visit_interface_declaration(self, node: Node):
        self.class_name = node.child_by_field_name("name").text.decode(self._encoding)

        if self.class_name.endswith("Response"):
            self.class_type = ClassType.RESPONSE
        elif self.class_name.endswith("View") or self.class_name == "MyUserInfo":
            self.class_type = ClassType.VIEW
        else:
            self.class_type = ClassType.OBJECT

        self._accept_list(node.children)

    def visit_property_signature(self, node: Node):
        name = node.child_by_field_name("name").text.decode(self._encoding)
        nullable = any(n.type == "?" for n in node.children)

        self.properties.append(Property(
            name,
            "Object",
            nullable
        ))
        self._accept_list(node.children)

    def visit_type_annotation(self, node: Node):
        type_identifier = node.child(1).text.decode(self._encoding)
        if "<" in type_identifier:
            return self._accept(node.child(1))

        if type_identifier in self._enums:
            type_identifier = "str"

        last_idx = len(self.properties) - 1

        self.properties[last_idx].type = normalize_type(type_identifier)

    def visit_generic_type(self, node: Node):
        last_idx = len(self.properties) - 1
        type_identifier = node.child(0).text.decode(self._encoding)
        type_parameter = normalize_type(node.child(1).child(1).text.decode(self._encoding))

        if type_parameter in self._enums:
            type_parameter = "str"

        if type_identifier == "Array":
            out_type = f"list[{type_parameter}]"
        else:
            raise f"Unhandled Type {type_identifier}!"

        self.properties[last_idx].type = out_type
