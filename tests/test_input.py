from jisoo.models.input import ExecutionInput, StepInput, JSONPath
import pytest


def test_json_path():

    schema = {"user": {"name": "John", "scores": [1, 2, 3]}}

    path = JSONPath(schema)

    assert "$.user.name" == path.get("user").get("name").get_path()
    assert (
        "$.user.scores[0]" == path.get("user").get("scores").get_by_index(0).get_path()
    )

    with pytest.raises(KeyError):
        invalid_path = path.get("invalid_key")

    with pytest.raises(TypeError):
        invalid_path = path.get_by_index(0)

    with pytest.raises(IndexError):
        invalid_path = path.get("user").get("scores").get_by_index(3)


def test_execution_input():

    schema = {"user": {"name": "John", "scores": [1, 2, 3]}}

    path = ExecutionInput(schema=schema)

    assert "$$.Execution.Input.user.name" == path.get("user").get("name").get_path()
    assert (
        "$$.Execution.Input.user.scores[0]"
        == path.get("user").get("scores").get_by_index(0).get_path()
    )

    with pytest.raises(KeyError):
        invalid_path = path.get("invalid_key")

    with pytest.raises(TypeError):
        invalid_path = path.get_by_index(0)

    with pytest.raises(IndexError):
        invalid_path = path.get("user").get("scores").get_by_index(3)


def test_step_input():
    schema = {"user": {"name": "John", "scores": [1, 2, 3]}}

    path = StepInput(schema)

    assert "$.user.name" == path.get("user").get("name").get_path()
    assert (
        "$.user.scores[0]" == path.get("user").get("scores").get_by_index(0).get_path()
    )

    with pytest.raises(KeyError):
        invalid_path = path.get("invalid_key")

    with pytest.raises(TypeError):
        invalid_path = path.get_by_index(0)

    with pytest.raises(IndexError):
        invalid_path = path.get("user").get("scores").get_by_index(3)
