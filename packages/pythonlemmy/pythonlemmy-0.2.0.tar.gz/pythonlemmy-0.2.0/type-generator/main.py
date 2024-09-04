import os
import sys
from typing import Optional, Tuple

import requests
import yaml
from openapi_parser.parser import OpenApiParser
from tree_sitter import Parser, Language
import tree_sitter_typescript as ts_typescript
from src import ModelVisitor, EnumVisitor, HttpVisitor, ClassType, ModelGenerator, HttpGenerator

parser = Parser()
parser.set_language(Language(ts_typescript.language_typescript(), "TypeScript"))
model_dir = "../pythonlemmy"
# model_dir = "./test_output"

enum_names = []

objects = []
responses = []
views = []

openapi_docs = "https://raw.githubusercontent.com/MV-GH/lemmy_openapi_spec/master/lemmy_spec.yaml"


def list_enums():
    types_dir = f"{current_dir()}lemmy-js-client/src/types/"
    files = os.listdir(types_dir)

    for file in files:
        if file.endswith("Id.ts"):
            continue
        with open(f"{types_dir}{file}", "r") as f:
            parse_enum(f.read())


def generate_types():
    types_dir = f"{current_dir()}lemmy-js-client/src/types/"

    files = os.listdir(types_dir)
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    for file in files:
        if file.endswith("Id.ts"):
            continue
        with open(f"{types_dir}{file}", "r") as f:
            parse_model(f.read())

    with open(f"./headers/object_header.py", "r") as f:
        object_header = f.read()
    with open(f"./headers/response_header.py", "r") as f:
        response_header = f.read()
    with open(f"./headers/view_header.py", "r") as f:
        view_header = f.read()

    with open(f"{model_dir}/views.py", "w") as f:
        f.write(view_header)
        f.write("\n\n\n".join(views))
        f.write("\n")
    with open(f"{model_dir}/objects.py", "w") as f:
        f.write(object_header)
        f.write("\n\n\n".join(objects))
        f.write("\n")
    with open(f"{model_dir}/responses.py", "w") as f:
        f.write(response_header)
        f.write("\n\n\n".join(responses))
        f.write("\n")


def parse_enum(model_contents: str):
    tree = parser.parse(bytes(model_contents, "utf-8"))

    if "export type" not in model_contents:
        return

    visitor = EnumVisitor(tree)
    visitor.walk()

    enum_names.append(visitor.enum_name)


def parse_model(model_contents: str):
    tree = parser.parse(bytes(model_contents, "utf-8"))

    if "export interface" not in model_contents:
        return
    visitor = ModelVisitor(tree, enum_names)
    visitor.walk()
    result = ModelGenerator(visitor.class_name, visitor.properties, visitor.class_type).build()
    if visitor.class_type == ClassType.VIEW:
        views.append(result)
    elif visitor.class_type == ClassType.RESPONSE:
        responses.append(result)
    elif visitor.class_type == ClassType.OBJECT:
        objects.append(result)


def generate_http():
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    with open(f"./headers/lemmyhttp_header.py", "r") as f:
        http_header = f.read()

    with open(f"{model_dir}/lemmyhttp.py", "w") as f:
        f.write(http_header)
        f.write(parse_http())
        f.write("\n")


def parse_http() -> str:
    types_dir = f"{current_dir()}lemmy-js-client/src/types/"
    docs = get_docs()

    with open(f"{current_dir()}lemmy-js-client/src/http.ts", "r") as f:
        tree = parser.parse(bytes(f.read(), "utf-8"))
        visitor = HttpVisitor(tree)
        visitor.walk()
        result = HttpGenerator(visitor.methods, types_dir, enum_names, docs).build()
        return result


def current_dir():
    return sys.argv[0][:-len("main.py")]


def get_docs() -> Optional[OpenApiParser]:
    if openapi_docs is None:
        return None

    content = requests.get(openapi_docs).text

    openapi_parser = OpenApiParser(yaml.safe_load(content))
    openapi_parser.load_all()

    return openapi_parser


if __name__ == '__main__':
    print(current_dir())
    list_enums()
    generate_http()
    generate_types()
