import textwrap
from datetime import datetime, timezone
from typing import List

from ..models import Property, ClassType


class Generator:
    _indent_char = "    "

    _class_name: str
    _properties: List[Property] = []

    def __init__(self, class_name: str, properties: List[Property]):
        self._class_name = class_name
        self._properties = properties

    def build(self) -> str:
        pass

    def _generate_property_list(self) -> str:
        lines = []
        for prop in self._properties:
            lines.append(f"""
    {prop.api_name}: {prop.wrapped()} = None
                    """.strip())

        return "\n".join(lines)


class ModelGenerator(Generator):
    _class_type: ClassType

    def __init__(self, class_name: str, properties: List[Property], class_type: ClassType):
        super().__init__(class_name, properties)
        self._class_type = class_type

    def build(self) -> str:
        if self._class_type is ClassType.OBJECT:
            return ObjectModelGenerator(self._class_name, self._properties).build()
        if self._class_type is ClassType.RESPONSE:
            return ResponseModelGenerator(self._class_name, self._properties).build()
        if self._class_type is ClassType.VIEW:
            return ViewModelGenerator(self._class_name, self._properties).build()


class ObjectModelGenerator(Generator):

    def __init__(self, class_name: str, properties: List[Property]):
        super().__init__(class_name, properties)

    def build(self) -> str:
        return f"""
@dataclass
class {self._class_name}:
{textwrap.indent(self._generate_property_list(), self._indent_char)}
        """.strip()


class ResponseModelGenerator(Generator):

    def __init__(self, class_name: str, properties: List[Property]):
        super().__init__(class_name, properties)

    def build(self) -> str:
        return f"""
class {self._class_name}(object):
{textwrap.indent(self._generate_property_list(), self._indent_char)}

    def __init__(self, api_response: requests.Response) -> None:
        response = api_response.json()
{textwrap.indent(self._generate_constructor(), self._indent_char * 2)}
        """.strip()

    def _generate_constructor(self) -> str:
        lines = []
        for prop in self._properties:
            if prop.type in ["bool", "str", "int", "float"]:
                lines.append(f"""
self.{prop.api_name} = response["{prop.api_name}"]
                """.strip())
            elif prop.type.startswith("list"):
                inner = prop.type[len("list["):-1]
                lines.append(f"""
self.{prop.api_name} = [{inner}(e) for e in response["{prop.api_name}"]]
                """.strip())
            else:
                lines.append(f"""
self.{prop.api_name} = {prop.type}(response["{prop.api_name}"])
                """.strip())

        return "\n".join(lines)


class ViewModelGenerator(Generator):
    def __init__(self, class_name: str, properties: List[Property]):
        super().__init__(class_name, properties)

    def build(self) -> str:
        return f"""
class {self._class_name}(ViewObject):
{textwrap.indent(self._generate_property_list(), self._indent_char)}

    def parse(self) -> None:
{textwrap.indent(self._generate_parse(), self._indent_char * 2)}
            """.strip()

    def _generate_parse(self) -> str:
        lines = []
        for prop in self._properties:
            line = ""
            if prop.type in ["bool", "str", "int", "float"]:
                line = f"""
self.{prop.api_name} = self._view["{prop.api_name}"]
                """.strip()
            else:
                line = f"""
self.{prop.api_name} = call_with_filtered_kwargs({prop.type}, self._view["{prop.api_name}"])
                """.strip()
            if not prop.nullable:
                lines.append(line)
                continue

            lines.append(f"""
if "{prop.api_name}" in self._view.keys():
{textwrap.indent(line, self._indent_char)}
else:
    self.{prop.api_name} = None      
""".strip())

        return "\n".join(lines)