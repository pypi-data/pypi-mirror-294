import re


def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def to_lower_camel_case(snake_str):
    # We capitalize the first letter of each component except the first one
    # with the 'capitalize' method and join them together.
    camel_string = to_camel_case(snake_str)
    return snake_str[0].lower() + camel_string[1:]


def to_enum_case(camel_case):
    enum_str = camel_case[0].lower() + camel_case[1:]
    return re.sub(r"([A-Z])", r"_\1", enum_str).upper()


def to_snake_case(camel_case):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_case).lower()


def normalize_type(type_identifier: str) -> str:
    if type_identifier.endswith("Id"):
        return "int"
    elif type_identifier == "number":
        return "int"
    elif type_identifier == "string":
        return "str"
    elif type_identifier == "boolean":
        return "bool"

    if type_identifier.endswith("[]"):
        return f"List[{type_identifier[:-2]}]"

    return type_identifier