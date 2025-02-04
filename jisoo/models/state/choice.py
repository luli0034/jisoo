from jisoo.models.state.base import State
from jisoo.models.state.handler import NextHandler
from jisoo.models.state.choice_rule import ChoiceRule
from typing import Optional, List
from pydantic import Field, model_validator, BaseModel, PrivateAttr, computed_field


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


class Choice(State, NextHandler):
    """
    Represents a Choice state that adds branching logic to the workflow.

    A Choice state enables conditional branching in the workflow based on the state input.
    It evaluates a list of choice rules in order and transitions to the first matching rule's
    next state. The default transition is automatically set by the Chain when processing
    the workflow steps.

    Attributes:
        type (str): Fixed as "Choice", defines the state type
        input_path (Optional[str]): JSONPath that selects part of the input to be processed.
            Defaults to None (entire input)
        output_path (Optional[str]): JSONPath that selects part of the output to be returned.
            Defaults to None (entire output)
        choices (List[Union[ChoiceRule, dict]]): List of rules to evaluate. Each rule
            specifies a condition and the next state to transition to if the condition is met.
        _default (str): Private attribute automatically set by the Chain
            to handle cases where no choice rules match. This represents the next state
            in the workflow sequence.

    Example:
        >>> from jisoo.models.rule import StringEquals
        >>> choice_state = Choice(
        ...     id="MyChoiceState",
        ...     choices=[
        ...         ChoiceRule(
        ...             rule=StringEquals(variable="$.type", value="test"),
        ...             next=State(id="TestState", type="Task")
        ...         )
        ...     ]
        ... )

    Note:
        - Choice rules are evaluated in order, and the first matching rule determines
          the next state.
        - The default transition is automatically set by the Chain based on the workflow
          sequence - you don't need to set it manually.
        - Unlike other state types, Choice states don't use the "Next" field directly as
          the next state is determined by either the choice rules or the default transition.
    """

    type: str = Field("Choice", frozen=True)
    input_path: Optional[str] = None
    output_path: Optional[str] = None
    choices: List[ChoiceRule] | List[dict]
    _default: str = PrivateAttr(None)

    @computed_field
    def default(self) -> str:
        return self._default
