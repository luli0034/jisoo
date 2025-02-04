from jisoo.models.state import State
from jisoo.models.state.handler import NextHandler
from typing import Optional, Literal
from pydantic import Field, PrivateAttr


"""
# State Types and Fields (JSONPath)

| Field              | Task     | Parallel | Map      | Pass     | Wait     | Choice   | Succeed  | Fail     |
|-------------------|----------|----------|----------|----------|----------|----------|----------|----------|
| Type              | Required | Required | Required | Required | Required | Required | Required | Required |
| Comment           | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  |
| InputPath         | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | -        |
| OutputPath        | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | -        |
| Assign            | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | Allowed  | -        | -        |
| _next/"End":true   | Required | Required | Required | Required | Required | -        | -        | -        |
| ResultPath        | Allowed  | Allowed  | Allowed  | Allowed  | -        | -        | -        | -        |
| Parameters        | Allowed  | Allowed  | Allowed  | Allowed  | -        | -        | -        | -        |
| ResultSelector    | Allowed  | Allowed  | Allowed  | -        | -        | -        | -        | -        |
| Retry             | Allowed  | Allowed  | Allowed  | -        | -        | -        | -        | -        |
| Catch             | Allowed  | Allowed  | Allowed  | -        | -        | -        | -        | -        |
"""


class Pass(State, NextHandler):
    """
    Represents a Pass state that passes its input to its output, optionally transforming the data.

    A Pass state can:
    - Modify its input using Parameters
    - Filter its output using ResultPath
    - Pass data unmodified
    - Inject static data into the workflow

    Attributes:
        type (str): Fixed as "Pass", defines the state type
        input_path (Optional[str]): JSONPath that selects part of the input to be processed.
            Defaults to None (entire input)
        output_path (Optional[str]): JSONPath that selects part of the output to be returned.
            Defaults to None (entire output)
        result_path (Optional[str]): JSONPath that specifies where to place the output.
            Defaults to None
        parameters (Optional[dict]): Collection of key-value pairs that are passed as input.
            Defaults to None

    Example:
        >>> pass_state = Pass(
        ...     id="MyPassState",
        ...     parameters={"message": "Hello World"},
        ...     result_path="$.result"
        ... )
    """

    type: str = Field("Pass", frozen=True)
    input_path: Optional[str] = None
    output_path: Optional[str] = None
    result_path: Optional[str] = None
    parameters: Optional[dict] = None


class Wait(State, NextHandler):
    """
    Represents a Wait state that delays the state machine from continuing for a specified time.

    The Wait state can pause execution for:
    - A fixed time interval
    - Until a specified timestamp
    - Until a timestamp specified in the state input

    Attributes:
        type (str): Fixed as "Wait", defines the state type
        input_path (Optional[str]): JSONPath that selects part of the input to be processed.
            Defaults to None (entire input)
        output_path (Optional[str]): JSONPath that selects part of the output to be returned.
            Defaults to None (entire output)

    Example:
        >>> wait_state = Wait(
        ...     id="MyWaitState",
        ...     seconds=10  # Waits for 10 seconds
        ... )
    """

    type: str = Field("Wait", frozen=True)
    input_path: Optional[str] = None
    output_path: Optional[str] = None


class Succeed(State):
    """
    Represents a Succeed state that terminates the state machine execution successfully.

    The Succeed state:
    - Ends the state machine execution
    - Marks the execution as successful
    - Can transform its input using InputPath and OutputPath

    Attributes:
        type (str): Fixed as "Succeed", defines the state type
        input_path (Optional[str]): JSONPath that selects part of the input to be processed.
            Defaults to None (entire input)
        output_path (Optional[str]): JSONPath that selects part of the output to be returned.
            Defaults to None (entire output)

    Example:
        >>> succeed_state = Succeed(
        ...     id="MySucceedState",
        ...     comment="Workflow completed successfully"
        ... )
    """

    type: str = Field("Succeed", frozen=True)
    input_path: Optional[str] = None
    output_path: Optional[str] = None


class Fail(State):
    """
    Represents a Fail state that terminates the state machine execution with a failure.

    The Fail state:
    - Ends the state machine execution
    - Marks the execution as failed
    - Cannot be followed by any other state
    - Does not accept InputPath, OutputPath, or any other optional fields

    Attributes:
        type (Literal["Fail"]): Fixed as "Fail", defines the state type

    Example:
        >>> fail_state = Fail(
        ...     id="MyFailState",
        ...     comment="Workflow failed due to invalid input"
        ... )
    """

    type: Literal["Fail"] = "Fail"
