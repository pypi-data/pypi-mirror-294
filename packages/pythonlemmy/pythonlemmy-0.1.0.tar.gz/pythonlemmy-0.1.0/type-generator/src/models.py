from enum import Enum


class ClassType:
    OBJECT = 1
    VIEW = 2
    RESPONSE = 3


class Property(object):
    api_name: str
    type: str
    nullable: bool

    def __init__(self, api_name: str, type: str, nullable: bool):
        self.api_name = api_name
        self.type = type
        self.nullable = nullable

    def wrapped(self) -> str:
        return self.type if not self.nullable else f"Optional[{self.type}]"


class EnumProperty(object):
    api_name: str

    def __init__(self, api_name: str, java_name: str):
        self.api_name = api_name


class HttpMethod(Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4


class ApiMethod(object):
    name: str
    input: str
    output: str
    method: HttpMethod
    url: str

    def __init__(self, name: str, input: str, output: str, method: HttpMethod, url: str):
        self.name = name
        self.input = input
        self.output = output
        self.method = method
        self.url = url
