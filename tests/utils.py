from jisoo.utils import (
    dynamodb_item_deserialize,
    replace_keys_with_prefix,
    process_context,
)
from decimal import Decimal


def test_dynamodb_item_deserialize():
    dynamodb_response = {
        "name": {"S": "jisoo"},
        "age": {"N": "25"},
        "is_student": {"BOOL": True},
    }
    expected = {"name": "jisoo", "age": 25, "is_student": True}
    assert dynamodb_item_deserialize(dynamodb_response) == expected


def test_replace_keys_with_prefix():
    # Example usage
    data = {"foo": {"key": "$.value", "bar": {"key2": "$.value2"}}}
    transformed_data = replace_keys_with_prefix(data)
    assert transformed_data == {
        "foo": {"key.$": "$.value", "bar": {"key2.$": "$.value2"}}
    }

    data = {"foo": "bar"}
    transformed_data = replace_keys_with_prefix(data)
    assert transformed_data == {"foo": "bar"}

    data = {"foo": "$.bar"}
    transformed_data = replace_keys_with_prefix(data)
    assert transformed_data == {"foo.$": "$.bar"}

    data = {"foo.$": "$.bar"}
    transformed_data = replace_keys_with_prefix(data)
    assert transformed_data == {"foo.$": "$.bar"}

    data = {"foo": "States.JsonToString($.bar)"}
    transformed_data = replace_keys_with_prefix(data)
    assert transformed_data == {"foo.$": "States.JsonToString($.bar)"}

    data = {"foo.$": "States.JsonToString($.bar)"}
    transformed_data = replace_keys_with_prefix(data)
    assert transformed_data == {"foo.$": "States.JsonToString($.bar)"}

    data = {"foo": "$$.Task.Token"}
    transformed_data = replace_keys_with_prefix(data)
    assert transformed_data == {"foo.$": "$$.Task.Token"}

    data = {"foo": "$"}
    transformed_data = replace_keys_with_prefix(data)
    assert transformed_data == {"foo.$": "$"}


def test_process_context():
    from jisoo.models.common import KeyValuePair

    data = {"foo": KeyValuePair(name="foo", value="bar")}
    key, transformed_data = process_context("key", data)
    assert transformed_data == {"foo": {"Name": "foo", "Value": "bar"}}

    data = {
        "foo": [
            KeyValuePair(name="foo", value="bar"),
            KeyValuePair(name="foo", value="$.bar"),
            KeyValuePair(name="$.foo", value="$.bar"),
        ]
    }
    key, transformed_data = process_context("key", data)
    print(transformed_data)
    assert transformed_data == {
        "foo": [
            {"Name": "foo", "Value": "bar"},
            {"Name": "foo", "Value.$": "$.bar"},
            {"Name.$": "$.foo", "Value.$": "$.bar"},
        ]
    }
