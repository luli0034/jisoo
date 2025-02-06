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
    Retry,
    Catch,
)
from jisoo.models.rule import Rule, Condition
from jisoo.models.common import ErrorEqualsEnum


def test_pass():
    pass_state = Pass(
        id="PassState", parameters={"message": "Hello World"}, result_path="$.result"
    )

    state_dict = pass_state.to_dict()
    assert state_dict["Type"] == "Pass"
    assert state_dict["Parameters"]["message"] == "Hello World"
    assert state_dict["ResultPath"] == "$.result"

    pass_state_with_paths = Pass(
        id="PassWithPaths",
        input_path="$.input",
        output_path="$.output",
        parameters={"message": "Hello"},
    )

    state_dict = pass_state_with_paths.to_dict()
    assert state_dict["InputPath"] == "$.input"
    assert state_dict["OutputPath"] == "$.output"


def test_wait():
    wait_state = Wait(id="WaitState", comment="Wait for 10 seconds")

    state_dict = wait_state.to_dict()
    assert state_dict["Type"] == "Wait"
    assert state_dict["Comment"] == "Wait for 10 seconds"

    wait_state_with_paths = Wait(
        id="WaitWithPaths",
        input_path="$.input",
        output_path="$.output",
    )

    state_dict = wait_state_with_paths.to_dict()
    assert state_dict["InputPath"] == "$.input"
    assert state_dict["OutputPath"] == "$.output"


def test_succeed():
    succeed_state = Succeed(
        id="SucceedState", comment="Workflow completed successfully"
    )

    state_dict = succeed_state.to_dict()
    assert state_dict["Type"] == "Succeed"
    assert state_dict["Comment"] == "Workflow completed successfully"

    succeed_state_with_paths = Succeed(
        id="SucceedWithPaths",
        input_path="$.input",
        output_path="$.output",
    )

    state_dict = succeed_state_with_paths.to_dict()
    assert state_dict["InputPath"] == "$.input"
    assert state_dict["OutputPath"] == "$.output"


def test_fail():
    fail_state = Fail(id="FailState", comment="Workflow failed")

    state_dict = fail_state.to_dict()
    assert state_dict["Type"] == "Fail"
    assert state_dict["Comment"] == "Workflow failed"


def test_choice():
    cond = Condition.StringEquals(variable="$.type", value="test")
    choice_rule = ChoiceRule(rule=cond, next=Pass(id="TestState"))
    rule_dict = choice_rule.to_dict()
    assert rule_dict["Variable"] == "$.type"
    assert rule_dict["StringEquals"] == "test"

    choice_state = Choice(
        id="ChoiceState",
        input_path="$.input",
        output_path="$.output",
        choices=[choice_rule],
    )

    state_dict = choice_state.to_dict()
    assert state_dict["Type"] == "Choice"
    assert state_dict["InputPath"] == "$.input"
    assert state_dict["OutputPath"] == "$.output"


def test_map():
    map_state = Map(
        id="MapState",
        input_path="$.input",
        output_path="$.output",
        result_path="$.result",
        parameters={"message": "Hello World"},
        result_selector="$.result",
        item_processor=Chain(steps=[Pass(id="Task1"), Pass(id="Task2")]),
    )

    state_dict = map_state.to_dict()
    assert state_dict["Type"] == "Map"
    assert state_dict["InputPath"] == "$.input"
    assert state_dict["OutputPath"] == "$.output"
    assert state_dict["ResultPath"] == "$.result"
    assert state_dict["Parameters"]["message"] == "Hello World"
    assert state_dict["ResultSelector"] == "$.result"
    assert state_dict["ItemProcessor"]["States"]["Task1"]["Type"] == "Pass"
    assert state_dict["ItemProcessor"]["States"]["Task2"]["Type"] == "Pass"


def test_parallel():
    parallel_state = Parallel(
        id="ParallelState",
        input_path="$.input",
        output_path="$.output",
        branches=[
            Chain(steps=[Pass(id="Task1"), Pass(id="Task2")]),
            Chain(steps=[Pass(id="Task3"), Pass(id="Task4")]),
        ],
    )

    state_dict = parallel_state.to_dict()
    assert state_dict["Type"] == "Parallel"
    assert state_dict["InputPath"] == "$.input"
    assert state_dict["OutputPath"] == "$.output"
    assert state_dict["Branches"][0]["States"]["Task1"]["Type"] == "Pass"
    assert state_dict["Branches"][0]["States"]["Task2"]["Type"] == "Pass"
    assert state_dict["Branches"][1]["States"]["Task3"]["Type"] == "Pass"


def test_task():
    task_state = Task(
        id="TaskState",
        input_path="$.input",
        output_path="$.output",
        resource="arn:aws:states:::lambda:invoke",
        parameters={"FunctionName": "my-function"},
        result_path="$.result",
    )

    state_dict = task_state.to_dict()
    assert state_dict["Type"] == "Task"
    assert state_dict["InputPath"] == "$.input"
    assert state_dict["OutputPath"] == "$.output"
    assert state_dict["Resource"] == "arn:aws:states:::lambda:invoke"
    assert state_dict["Parameters"]["FunctionName"] == "my-function"
    assert state_dict["ResultPath"] == "$.result"


def test_task_with_error_control():
    retry = Retry(error_equals=[ErrorEqualsEnum.TaskFailed])
    catch = Catch(
        error_equals=[ErrorEqualsEnum.TaskFailed], next_steps=Fail(id="FailState")
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

    state_dict = task_state.to_dict()

    assert state_dict["Type"] == "Task"
    assert state_dict["InputPath"] == "$.input"
    assert state_dict["OutputPath"] == "$.output"
    assert state_dict["Resource"] == "arn:aws:states:::lambda:invoke"
    assert state_dict["Parameters"]["FunctionName"] == "my-function"
    assert state_dict["ResultPath"] == "$.result"
    assert state_dict["Retry"][0]["ErrorEquals"] == ["States.TaskFailed"]
    assert state_dict["Catch"][0]["ErrorEquals"] == ["States.TaskFailed"]
