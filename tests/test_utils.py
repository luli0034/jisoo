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

    transformed_data = replace_keys_with_prefix(key="foo", value="bar")
    assert transformed_data == ("foo", "bar")
    transformed_data = replace_keys_with_prefix(key="foo", value="$.bar")
    assert transformed_data == ("foo.$", "$.bar")

    transformed_data = replace_keys_with_prefix("foo.$", "$.bar")
    assert transformed_data == ("foo.$", "$.bar")

    transformed_data = replace_keys_with_prefix("foo", "States.JsonToString($.bar)")
    assert transformed_data == ("foo.$", "States.JsonToString($.bar)")

    transformed_data = replace_keys_with_prefix("foo.$", "States.JsonToString($.bar)")
    assert transformed_data == ("foo.$", "States.JsonToString($.bar)")

    transformed_data = replace_keys_with_prefix("foo", "$$.Task.Token")
    assert transformed_data == ("foo.$", "$$.Task.Token")

    transformed_data = replace_keys_with_prefix("foo", "$")
    assert transformed_data == ("foo.$", "$")


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

    assert transformed_data == {
        "foo": [
            {"Name": "foo", "Value": "bar"},
            {"Name": "foo", "Value.$": "$.bar"},
            {"Name.$": "$.foo", "Value.$": "$.bar"},
        ]
    }

    data = {"foo": {"key": "$.VALUE", "key2": "States.JsonToString($.VALUE2)"}}
    key, transformed_data = process_context("key", data)
    assert transformed_data == {
        "foo": {"key.$": "$.VALUE", "key2.$": "States.JsonToString($.VALUE2)"}
    }
