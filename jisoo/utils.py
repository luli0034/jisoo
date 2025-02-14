from boto3.dynamodb.types import TypeDeserializer
from typing import Any


def dynamodb_item_deserialize(dynamodb_response: dict):
    """
    Converts a DynamoDB response to dict.

    Args:

        dynamodb_response (dict): The dictionary returned from DynamoDB.

    Returns:
        Dict[str, str]: The dictionary representation of the DynamoDB response.
    """

    deseializer = TypeDeserializer()
    return {
        key: deseializer.deserialize(value) for key, value in dynamodb_response.items()
    }


def replace_keys_with_prefix(d) -> dict:
    if not isinstance(d, dict):
        return d

    new_dict = {}
    for key, value in d.items():
        new_key = (
            key + ".$"
            if (
                isinstance(value, str)
                and (
                    value.startswith("$")
                    # TODO: workaround for the intrinsic functions
                    or value.startswith("States.")
                )
                and not key.endswith(".$")
            )
            else key
        )
        new_dict[new_key] = (
            replace_keys_with_prefix(value) if isinstance(value, dict) else value
        )

    return new_dict


def to_pascalcase(text: str) -> str:
    return "".join([t.title() for t in text.split("_")])


def transform_value(value: Any) -> Any:
    """
    Recursively transform values in nested structures, converting CommonObject instances
    to dictionaries.

    Args:
        value: Any value that might contain CommonObject instances

    Returns:
        The transformed value with all CommonObject instances converted to dictionaries
    """
    from jisoo.models.common import CommonObject

    if isinstance(value, CommonObject):
        return value.to_dict()

    if isinstance(value, dict):
        return {k: transform_value(v) for k, v in value.items()}

    if isinstance(value, list):
        return [transform_value(item) for item in value]

    return value


def process_context(name: str, value: Any, transfom=None) -> tuple[str, Any]:
    from jisoo.models.input.base import JSONPath

    if isinstance(value, (str, JSONPath)):
        key = name if name.endswith(".$") else f"{name}.$"
        if isinstance(value, str) and value.startswith("$."):
            return to_pascalcase(key), value
        if isinstance(value, JSONPath):
            return to_pascalcase(key), value.get_path()

    return to_pascalcase(name), replace_keys_with_prefix(transform_value(value))
