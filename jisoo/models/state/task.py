from jisoo.models.state import State
from jisoo.models.state.handler import ErrorHandler, NextHandler
from typing import Optional
from pydantic import Field


"""
# State Types and Fields (JSONPath)

| Field              | Task     | Parallel | Map      | Pass     | Wait     | Choice   | Succeed  | Fail     |
|-------------------|----------|----------|----------|----------|----------|----------|----------|----------|
| Type              | Required | Required | Required | Required | Required | Required | Required | Required |
| Comment           | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  |
| InputPath         | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | -        |
| OutputPath        | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | -        |
| Assign            | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | -        | -        |
| Next/"End":true   | Required | Required | Required | Required | Required | -        | -        | -        |
| ResultPath        | Allowed  | Allowed  | Allowed  | Allowed  | -        | -        | -        | -        |
| Parameters        | Allowed  | Allowed  | Allowed  | Allowed  | -        | -        | -        | -        |
| ResultSelector    | Allowed  | Allowed  | Allowed  | -        | -        | -        | -        | -        |
| Retry             | Allowed  | Allowed  | Allowed  | -        | -        | -        | -        | -        |
| Catch             | Allowed  | Allowed  | Allowed  | -        | -        | -        | -        | -        |
"""


class Task(State, ErrorHandler, NextHandler):
    """
    Represents a Task state that executes a specific task or activity in the workflow.

    A Task state is used to perform an action or execute a specific piece of work.
    It can invoke various types of tasks such as Lambda functions, API operations,
    or other integrated services.

    Attributes:
        type (str): Fixed as "Task", defines the state type
        resource (str): The resource to be executed (e.g., Lambda ARN, API endpoint)
        input_path (Optional[str]): JSONPath that selects part of the input to be processed.
            Defaults to None (entire input)
        output_path (Optional[str]): JSONPath that selects part of the output to be returned.
            Defaults to None (entire output)
        result_path (Optional[str]): JSONPath that specifies where to place the output.
            Defaults to None
        result_selector (Optional[str]): Optional path to select specific data from results.
            Defaults to None
        parameters (Optional[dict]): Parameters to be passed to the task.
            Defaults to None
        credentials (Optional[dict]): Credentials for accessing the resource.
            Defaults to None
        timeout_seconds (Optional[int]): Maximum time in seconds to wait for task completion.
            Defaults to None
        timeout_seconds_path (Optional[str]): JSONPath to a field containing the timeout value.
            Defaults to None
        heartbeat_seconds (Optional[int]): Time in seconds between heartbeat notifications.
            Defaults to None
        heartbeat_seconds_path (Optional[str]): JSONPath to a field containing the heartbeat interval.
            Defaults to None

    Example:
        >>> task_state = Task(
        ...     id="ProcessData",
        ...     resource="arn:aws:lambda:REGION:ACCOUNT:function:FUNCTION_NAME",
        ...     parameters={"input": "$.data"},
        ...     result_path="$.taskResult",
        ...     timeout_seconds=30
        ... )

    Note:
        - Either timeout_seconds or timeout_seconds_path can be specified, not both
        - Either heartbeat_seconds or heartbeat_seconds_path can be specified, not both
        - Error handling can be configured using Retry and Catch configurations
        - The task will fail if it exceeds its timeout period
    """

    type: str = Field("Task", frozen=True)
    input_path: Optional[str] = None
    output_path: Optional[str] = None
    result_path: Optional[str] = None
    result_selector: Optional[str] = None
    parameters: Optional[dict] = None

    # Task specific fields
    resource: Optional[str] = None
    credentials: Optional[dict] = None
    timeout_seconds: Optional[int] = None
    timeout_seconds_path: Optional[str] = None
    heartbeat_seconds: Optional[int] = None
    heartbeat_seconds_path: Optional[str] = None
