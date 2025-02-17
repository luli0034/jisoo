from jisoo.models.state import (
    Pass,
    Wait,
    Succeed,
    Fail,
    Choice,
    ChoiceRule,
    Map,
    Parallel,
    Task,
    Chain,
    Graph,
    Retry,
    Catch,
)
from jisoo.models.rule import Rule, Condition
from jisoo.models.common import ErrorEqualsEnum
from jisoo.exception import DuplicateStatesInChain
import pytest


def test_simple_chain():
    first_state = Pass(
        id="PassState1", parameters={"message": "Hello World"}, result_path="$.result"
    )
    secend_state = Pass(
        id="PassState2", parameters={"message": "Hello World"}, result_path="$.result"
    )
    chain = Chain(steps=[first_state, secend_state])
    chain_dict = chain._states
    assert chain_dict["PassState1"]["Type"] == "Pass"
    assert chain_dict["PassState1"]["Parameters"]["message"] == "Hello World"
    assert chain_dict["PassState1"]["ResultPath"] == "$.result"
    assert chain_dict["PassState1"]["Next"] == "PassState2"

    duplicate_state = Pass(
        id="PassState1", parameters={"message": "Hello World"}, result_path="$.result"
    )

    with pytest.raises(DuplicateStatesInChain):
        chain = Chain(steps=[first_state, duplicate_state])


def test_graph_with_state():

    first_state = Pass(
        id="PassState1", parameters={"message": "Hello World"}, result_path="$.result"
    )

    graph = Graph(branch=first_state, comment="Single State Graph", timeout_seconds=60)

    graph_dict = graph.to_dict()
    assert graph_dict["Comment"] == "Single State Graph"
    assert graph_dict["TimeoutSeconds"] == 60
    assert graph_dict["StartAt"] == "PassState1"
    assert graph_dict["States"]["PassState1"]["Type"] == "Pass"
    assert graph_dict["States"]["PassState1"]["End"] == True
    assert graph_dict["States"]["PassState1"]["Parameters"]["message"] == "Hello World"


def test_graph_with_chain():

    first_state = Pass(
        id="PassState1", parameters={"message": "Hello World"}, result_path="$.result"
    )
    secend_state = Pass(
        id="PassState2", parameters={"message": "Hello World"}, result_path="$.result"
    )
    chain = Chain(steps=[first_state, secend_state])

    graph = Graph(branch=chain, comment="Chain State Graph", timeout_seconds=60)

    graph_dict = graph.to_dict()
    assert graph_dict["Comment"] == "Chain State Graph"
    assert graph_dict["TimeoutSeconds"] == 60
    assert graph_dict["StartAt"] == "PassState1"
    assert graph_dict["States"]["PassState1"]["Type"] == "Pass"
    assert graph_dict["States"]["PassState1"]["Parameters"]["message"] == "Hello World"
    assert graph_dict["States"]["PassState1"]["Next"] == "PassState2"
    assert graph_dict["States"]["PassState2"]["Type"] == "Pass"
    assert graph_dict["States"]["PassState2"]["End"] == True
    assert graph_dict["States"]["PassState2"]["Parameters"]["message"] == "Hello World"


def test_graph_with_error_handle():
    retry = Retry(error_equals=[ErrorEqualsEnum.Events.TaskFailed])
    catch = Catch(
        error_equals=[ErrorEqualsEnum.Events.TaskFailed],
        next_steps=Fail(id="FailState"),
    )
    task_state = Task(
        id="TaskState",
        input_path="$.input",
        output_path="$.output",
        resource="arn:aws:states:::lambda:invoke",
        parameters={"FunctionName": "my-function"},
        result_path="$.result",
        retry=retry,
        catch=catch,
    )

    graph = Graph(branch=task_state, comment="Task State Graph", timeout_seconds=60)
    graph_dict = graph.to_dict()
    assert graph_dict["Comment"] == "Task State Graph"
    assert graph_dict["TimeoutSeconds"] == 60
    assert graph_dict["StartAt"] == "TaskState"
    assert graph_dict["States"]["TaskState"]["Type"] == "Task"
    assert graph_dict["States"]["TaskState"]["InputPath"] == "$.input"
    assert graph_dict["States"]["TaskState"]["OutputPath"] == "$.output"
    assert (
        graph_dict["States"]["TaskState"]["Resource"]
        == "arn:aws:states:::lambda:invoke"
    )
    assert (
        graph_dict["States"]["TaskState"]["Parameters"]["FunctionName"] == "my-function"
    )
    assert graph_dict["States"]["TaskState"]["ResultPath"] == "$.result"
    assert graph_dict["States"]["TaskState"]["Retry"][0]["ErrorEquals"] == [
        "States.TaskFailed"
    ]
    assert graph_dict["States"]["TaskState"]["Catch"][0]["ErrorEquals"] == [
        "States.TaskFailed"
    ]


def test_nested_graph():

    update_ddb_success = Succeed(id="Success")
    update_fail = Fail(id="Fail")
    is_task_failed = Choice(
        input_path="$.TaskResult",
        id="Choice",
        choices=[
            ChoiceRule(
                rule=Condition.Not(Condition.NumericEquals("$.status", 0)),
                next=Chain(steps=[update_fail, update_ddb_success]),
            )
        ],
    )

    main = Map(
        id="MapUpdateDDB",
        input_path=f"$.TaskResult",
        item_processor=Chain(
            steps=[
                is_task_failed,
                Succeed(id="TaskSuccess"),
                update_ddb_success,
            ],
        ),  # Define the states within the Map
        result_path=None,
    )

    main = Map(
        id="Map",
        items_path=f"$.items",
        max_concurrency=2,
        item_processor=Chain(
            steps=[
                main,
            ]
        ),
    )

    graph = Graph(branch=main, comment="Task State Graph", timeout_seconds=60)
    graph_dict = graph.to_dict()
    print(graph_dict)
    assert graph_dict["Comment"] == "Task State Graph"
    assert graph_dict["TimeoutSeconds"] == 60
    assert graph_dict["StartAt"] == "Map"
    assert graph_dict["States"]["Map"]["Type"] == "Map"
    assert graph_dict["States"]["Map"]["ItemsPath"] == "$.items"
    assert graph_dict["States"]["Map"]["MaxConcurrency"] == 2
    assert graph_dict["States"]["Map"]["End"] == True
    assert (
        graph_dict["States"]["Map"]["ItemProcessor"]["States"]["MapUpdateDDB"]["Type"]
        == "Map"
    )
    assert (
        graph_dict["States"]["Map"]["ItemProcessor"]["States"]["MapUpdateDDB"][
            "InputPath"
        ]
        == "$.TaskResult"
    )
    assert (
        graph_dict["States"]["Map"]["ItemProcessor"]["States"]["MapUpdateDDB"][
            "ItemProcessor"
        ]["States"]["Choice"]["Type"]
        == "Choice"
    )
    assert (
        graph_dict["States"]["Map"]["ItemProcessor"]["States"]["MapUpdateDDB"][
            "ItemProcessor"
        ]["States"]["Choice"]["InputPath"]
        == "$.TaskResult"
    )
    assert (
        graph_dict["States"]["Map"]["ItemProcessor"]["States"]["MapUpdateDDB"][
            "ItemProcessor"
        ]["States"]["Choice"]["Choices"][0]["Not"]["NumericEquals"]
        == 0
    )
    assert (
        graph_dict["States"]["Map"]["ItemProcessor"]["States"]["MapUpdateDDB"][
            "ItemProcessor"
        ]["States"]["Choice"]["Choices"][0]["Next"]
        == "Fail"
    )
    assert (
        graph_dict["States"]["Map"]["ItemProcessor"]["States"]["MapUpdateDDB"][
            "ItemProcessor"
        ]["States"]["TaskSuccess"]["Type"]
        == "Succeed"
    )
