from jisoo.utils import dynamodb_item_deserialize
from decimal import Decimal


def test_dynamodb_item_deserialize():
    dynamodb_response = {
        "name": {"S": "jisoo"},
        "age": {"N": "25"},
        "is_student": {"BOOL": True},
    }
    expected = {"name": "jisoo", "age": 25, "is_student": True}
    assert dynamodb_item_deserialize(dynamodb_response) == expected
