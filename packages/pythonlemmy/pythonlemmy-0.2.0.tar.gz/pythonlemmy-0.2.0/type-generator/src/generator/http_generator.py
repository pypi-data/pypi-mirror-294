import textwrap
from typing import List, Optional

from openapi_parser.model import ModelEndpoint, ModelSchema, ModelEnumData
from openapi_parser.parser import OpenApiParser, ModelEnumDataImpl
from tree_sitter import Parser, Language
import tree_sitter_typescript as ts_typescript

from ..visitor import ModelVisitor
from ..models import Property, ApiMethod, HttpMethod

parser = Parser()
parser.set_language(Language(ts_typescript.language_typescript(), "TypeScript"))


class HttpGenerator:
    _domain_match = [HttpMethod.GET, HttpMethod.POST, HttpMethod.PUT, HttpMethod.DELETE]
    _retrofit_match = ["get", "post", "put", "delete"]
    _indent_char = "    "
    _processors = {
        "login": """
if result.status_code == 200:
    self._session = create_session(self._headers, result.json()["jwt"])
else:
    raise Exception("Login failed with status code: " + str(result.status_code))
            """.strip(),
        "logout": """
if result.status_code == 200:
    self._session = create_session(self._headers, None)
        """.strip()
    }

    _methods: List[ApiMethod] = []

    def __init__(self, methods: List[ApiMethod], types_dir: str, enums: List[str],
                 openapi: Optional[OpenApiParser] = None):
        self._methods = methods
        self._types_dir = types_dir
        self._enums = enums
        self._openapi = openapi

    def build(self) -> str:
        return self._indent_char + f"""
{textwrap.indent(self._generate_methods(), self._indent_char)}
            """.strip()

    def _generate_methods(self) -> str:
        lines = []
        for method in self._methods:
            properties = self._get_properties(method)

            http_method = self._retrofit_match[self._domain_match.index(method.method)]
            is_get = method.method == HttpMethod.GET
            processor = self._processors[method.name] if method.name in self._processors else ""
            line = f"""
def {method.name}(
{textwrap.indent(self._generate_arguments(properties), self._indent_char)}
):
{textwrap.indent(self._generate_documentation(method, properties), self._indent_char)}
    form = create_form(locals())
    result = {http_method}_handler(self._session, f"{{self._api_url}}{method.url}", json={None if is_get else "form"}, params={"form" if is_get else None})
{textwrap.indent(processor, self._indent_char)}
    return result
            """.strip()
            lines.append(line)

        return "\n\n".join(lines)

    def _generate_arguments(self, properties: List[Property]) -> str:
        if len(properties) == 0:
            return "self"

        args = ["self"]
        for p in properties:
            default = "" if not p.nullable else " = None"
            args.append(f"{p.api_name}: {p.type}{default}")

        return ",\n".join(args)

    def _generate_documentation(self, method: ApiMethod, properties: List[Property]) -> str:
        if self._openapi is None:
            return ""

        if method.url not in self._openapi.path_items:
            print(f"Method name {method.url} not found")
            return ""

        url = self._openapi.path_items[method.url]

        method_rest = self._retrofit_match[self._domain_match.index(method.method)]
        if method_rest not in url.endpoints:
            print(f"Method rest {method_rest} not found in {method.url}")
            return ""

        endpoint = url.endpoints[method_rest]

        input_args_docs = self._generate_input(endpoint, properties)
        input_args_string = f"""
Args:
{textwrap.indent(input_args_docs, self._indent_char)}
        """.strip() if input_args_docs is not None else ""

        return f"""
\"\"\" {endpoint.summary}
{input_args_string}

Returns:
    requests.Response: result of API call (wrap in {method.output} if successful)
\"\"\"
        """.strip()

    def _generate_input(self, endpoint: ModelEndpoint, properties: List[Property]) -> Optional[str]:
        content_type = 'application/json'

        schema_ref = (list(endpoint.all_parameters)[0].schema if len(endpoint.all_parameters) > 0 else
                      endpoint.request_body.content[content_type].schema
                      if endpoint.request_body is not None else None)

        if schema_ref is None:
            return None

        if schema_ref.cls is str:
            return None

        schema: ModelSchema = self._openapi.loaded_objects[schema_ref.cls.path]
        schema_properties = schema.cls.properties

        lines = []
        for property in properties:
            schema_property = schema_properties[property.api_name] if property.api_name in schema_properties else None
            description = ""
            if schema_property is not None:
                if schema_property.description is not None:
                    description = f": {schema_property.description}"
                elif type(schema_property.cls) is ModelEnumDataImpl:
                    description = f": Possible values [{', '.join(schema_property.cls.possible_values)}]"
                else:
                    description = f": {schema_property.summary}"

            lines.append(f"{property.api_name}{description}")

        return "\n".join(lines)

    def _get_properties(self, method: ApiMethod) -> List[Property]:
        if method.input == "object":
            return []

        with open(f"{self._types_dir}/{method.input}.ts", "r") as f:
            tree = parser.parse(bytes(f.read(), "utf-8"))
            visitor = ModelVisitor(tree, self._enums)
        visitor.walk()
        return visitor.properties
