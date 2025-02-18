from typing import Any, Dict
import re


def dynamodb_item_deserialize(dynamodb_response: dict):
    from boto3.dynamodb.types import TypeDeserializer

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


def replace_keys_with_prefix(key, value) -> tuple[str, Any]:
    from jisoo.models.input.base import JSONPath

    if isinstance(value, JSONPath):
        value = value.get_path()
        if not key.endswith(".$"):
            key = key + ".$"
    elif isinstance(value, str) and (
        # TODO: workarounds for intrinsic function
        value.startswith("$.")
        or value.startswith("States.")
        or value.startswith("$$.")
        or value == "$"
    ):
        if not key.endswith(".$"):
            key = key + ".$"
    return key, value


def to_pascalcase(text: str) -> str:
    """Convert snake_case or camelCase to PascalCase correctly."""
    return "".join([t.title() for t in text.split("_")])


def transform_value(
    key: str, value: Any, depth: int = 0, max_depth: int = 100
) -> tuple[str, Any]:
    """
    Recursively transform values in nested structures, handling CommonObjects at any depth.

    Supports:
    - Nested CommonObjects within other CommonObjects
    - Lists and dictionaries with mixed values
    - Path references with $ notation

    Args:
        value: Any value that might contain CommonObject instances
        depth: Current recursion depth
        max_depth: Maximum allowed recursion depth to prevent stack overflow

    Returns:
        Transformed value with all CommonObject instances converted to dictionaries
    """
    from jisoo.models.common import CommonObject
    from jisoo.models.input.base import JSONPath

    if depth > max_depth:
        raise RecursionError("Maximum recursion depth exceeded in transform_value")

    # Process dictionary values
    if isinstance(value, dict):
        transformed_dict = {
            transform_value(k, v, depth + 1, max_depth)[0]: transform_value(
                k, v, depth + 1, max_depth
            )[1]
            for k, v in value.items()
        }
        return key, transformed_dict

    # Process list values
    elif isinstance(value, list):
        transformed_list = [
            transform_value(key, item, depth + 1, max_depth)[1] for item in value
        ]
        return key, transformed_list

    # Process CommonObjects, including KeyValuePair
    elif isinstance(value, CommonObject):
        transformed_dict = {
            new_k: new_v
            for k, v in value.to_dict().items()
            for new_k, new_v in [transform_value(k, v, depth + 1, max_depth)]
        }
        return key, transformed_dict

    elif isinstance(value, (str, JSONPath)):
        return replace_keys_with_prefix(key, value)

    # Base case: transform key if needed and return value
    return key, value


def process_context(name: str, value: Any, transform=None) -> tuple[str, Any]:
    """
    Process a context value and return its formatted key and transformed value.

    Args:
        name: The parameter name
        value: The parameter value to process
        transform: Optional transform function (defaults to transform_value)

    Returns:
        tuple[str, Any]: Formatted key and transformed value
    """
    from jisoo.models.input.base import JSONPath

    transform = transform or transform_value

    if isinstance(value, (str, JSONPath)):
        if isinstance(value, JSONPath):
            value = value.get_path()
        return replace_keys_with_prefix(name, value)

    return transform(name, value)
