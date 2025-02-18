from jisoo.models.common.base import KeyValuePair


def test_key_value_pais():
    assert KeyValuePair(name="foo", value="bar").to_dict() == {
        "Name": "foo",
        "Value": "bar",
    }
