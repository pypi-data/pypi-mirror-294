import textwrap
from typing import List

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

    def __init__(self, methods: List[ApiMethod], types_dir: str, enums: List[str]):
        self._methods = methods
        self._types_dir = types_dir
        self._enums = enums

    def build(self) -> str:
        return self._indent_char + f"""
{textwrap.indent(self._generate_methods(), self._indent_char)}
            """.strip()

    def _generate_methods(self) -> str:
        lines = []
        for method in self._methods:
            http_method = self._retrofit_match[self._domain_match.index(method.method)]
            is_get = method.method == HttpMethod.GET
            processor = self._processors[method.name] if method.name in self._processors else ""
            line = f"""
def {method.name}(
{textwrap.indent(self._generate_arguments(method), self._indent_char)}
):
    form = create_form(locals())
    result = {http_method}_handler(self._session, f"{{self._api_url}}{method.url}", json={None if is_get else "form"}, params={"form" if is_get else None})
{textwrap.indent(processor, self._indent_char)}
    return result
            """.strip()
            lines.append(line)

        return "\n\n".join(lines)

    def _generate_arguments(self, method: ApiMethod) -> str:
        if method.input == "object":
            return "self"

        with open(f"{self._types_dir}/{method.input}.ts", "r") as f:
            tree = parser.parse(bytes(f.read(), "utf-8"))
            visitor = ModelVisitor(tree, self._enums)
        visitor.walk()

        args = ["self"]
        for p in visitor.properties:
            default = "" if not p.nullable else " = None"
            args.append(f"{p.api_name}: {p.type}{default}")

        return ",\n".join(args)

