from jisoo.steps import Service, SFNAction, SFNStartExecutionStep, SFNListExecutionsStep
from jisoo.models.common import ServiceType
import pytest
from pydantic import ValidationError
import json


def test_start_execution():
    start_execution_step = SFNStartExecutionStep(
        state_machine_arn="arn:aws:states:::stateMachine:HelloWorld-StateMachine",
        id="example",
        input_path="$.input",
        output_path="$.output",
        result_path="$.result",
        result_selector="$.result",
        parameters={"key": "value"},
        input={"key": "value"},
        name="new-execution",
        trace_header="example",
        integration_pattern="waitForTaskToken",
        integration_type="aws-sdk",
    )

    step_dict = start_execution_step.to_dict()
    assert step_dict["Type"] == "Task"
    assert step_dict["InputPath"] == "$.input"
    assert step_dict["OutputPath"] == "$.output"
    assert step_dict["ResultPath"] == "$.result"
    assert step_dict["ResultSelector"] == "$.result"
    assert step_dict["Parameters"]["Input"] == {"key": "value"}
    assert step_dict["Parameters"]["Name"] == "new-execution"
    assert step_dict["Parameters"]["TraceHeader"] == "example"
    assert (
        step_dict["Resource"]
        == "arn:aws:states:::aws-sdk:states:startExecution.waitForTaskToken"
    )
    assert (
        step_dict["Parameters"]["StateMachineArn"]
        == "arn:aws:states:::stateMachine:HelloWorld-StateMachine"
    )


def test_list_executions():
    list_executions_step = SFNListExecutionsStep(
        state_machine_arn="arn:aws:states:::stateMachine:HelloWorld-StateMachine",
        id="example",
        input_path="$.input",
        output_path="$.output",
        result_path="$.result",
        result_selector="$.result",
        parameters={"key": "value"},
        max_results=10,
        next_token="example",
        integration_pattern="waitForTaskToken",
        integration_type="aws-sdk",
        status_filter="RUNNING",
        redrive_filter="REDRIVEN",
    )

    step_dict = list_executions_step.to_dict()

    assert step_dict["Parameters"]["StatusFilter"] == "RUNNING"
    assert step_dict["Parameters"]["RedriveFilter"] == "REDRIVEN"

    with pytest.raises(ValidationError):
        SFNListExecutionsStep(
            state_machine_arn="arn:aws:states:::stateMachine:HelloWorld-StateMachine",
            id="example",
            input_path="$.input",
            output_path="$.output",
            result_path="$.result",
            result_selector="$.result",
            parameters={"key": "value"},
            max_results=10,
            next_token="example",
            integration_pattern="waitForTaskToken",
            integration_type="aws-sdk",
            status_filter="example",
            redrive_filter="example",
        )
