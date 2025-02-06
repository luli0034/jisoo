from jisoo.steps import Service, LambdaInvokeStep
from jisoo.models.common import ServiceType
import pytest
from pydantic import ValidationError


def test_lambda_step():

    lambda_step = LambdaInvokeStep(
        function_name="example",
        id="example",
        integration_pattern="waitForTaskToken",
        integration_type="aws-sdk",
        input_path="$.input",
        output_path="$.output",
        result_path="$.result",
        result_selector="$.result",
        credentials={"roleArn": "example-role-arn"},
        timeout_seconds=10,
        timeout_seconds_path="$.timeout",
        heartbeat_seconds=10,
        heartbeat_seconds_path="$.heartbeat",
        payload={"key": "value"},
        qualifier="example",
        log_type="Tail",
        client_context="example",
        invocation_type="RequestResponse",
    )
    step_dict = lambda_step.to_dict()
    """
    {'Type': 'Task', 'InputPath': '$.input', 'OutputPath': '$.output', 'ResultPath': '$.result', 'ResultSelector': '$.result', 'Parameters': {'Payload': {'key': 'value'}, 'Qualifier': 'example', 'LogType': 'Tail', 'ClientContext': 'example', 'InvocationType': 'RequestResponse'}, 'Resource': 'arn:aws:states:::aws-sdk:lambda:invoke.waitForTaskToken', 'Credentials': {'access_key': 'key', 'secret_key': 'key'}, 'TimeoutSeconds': 10, 'TimeoutSecondsPath': '$.timeout', 'HeartbeatSeconds': 10, 'HeartbeatSecondsPath': '$.heartbeat'}
    """

    assert step_dict["Type"] == "Task"
    assert step_dict["InputPath"] == "$.input"
    assert step_dict["OutputPath"] == "$.output"
    assert step_dict["ResultPath"] == "$.result"
    assert step_dict["ResultSelector"] == "$.result"
    assert step_dict["Parameters"]["Payload"] == {"key": "value"}
    assert step_dict["Parameters"]["Qualifier"] == "example"
    assert step_dict["Parameters"]["LogType"] == "Tail"
    assert step_dict["Parameters"]["ClientContext"] == "example"
    assert step_dict["Parameters"]["InvocationType"] == "RequestResponse"
    assert (
        step_dict["Resource"]
        == "arn:aws:states:::aws-sdk:lambda:invoke.waitForTaskToken"
    )
    assert step_dict["Credentials"]["roleArn"] == "example-role-arn"
    assert step_dict["TimeoutSeconds"] == 10
    assert step_dict["TimeoutSecondsPath"] == "$.timeout"
    assert step_dict["HeartbeatSeconds"] == 10
    assert step_dict["HeartbeatSecondsPath"] == "$.heartbeat"

    with pytest.raises(ValueError):
        LambdaInvokeStep(
            function_name="example",
            id="example",
            integration_pattern="runTask",
            integration_type="aws-sdk",
        )

    with pytest.raises(ValidationError):
        LambdaInvokeStep(
            function_name="example",
            id="example",
            integration_pattern="runTask",
            integration_type="optimided",
        )
