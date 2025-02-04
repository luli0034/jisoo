from pydantic import computed_field
from typing import Optional, List
from jisoo.models.state.base import Block, State
from jisoo.models.state.chain import Chain
from jisoo.models.common import ErrorEqualsEnum


class Catch(Block):
    """
    Represents a Catch configuration for error handling in state machines.

    The Catch block defines how to handle specific errors that occur during state execution.
    It specifies which errors to catch and what action to take when they occur.

    Attributes:
        error_equals (List[ErrorEqualsEnum]): List of error types to catch.
            Can include specific error names or predefined error types like
            "States.ALL", "States.Timeout", etc.
        next_steps (Union[State, Chain]): The state or chain of states to execute
            when one of the specified errors is caught.

    Example:
        >>> from jisoo.models.common import ErrorEqualsEnum
        >>> catch = Catch(
        ...     error_equals=[ErrorEqualsEnum.STATES_ALL],
        ...     next_steps=State(id="ErrorHandler", type="Task")
        ... )

    Note:
        The error_equals list is processed in order, and the first matching error
        type determines which recovery path is taken.
    """

    error_equals: List[ErrorEqualsEnum]
    next_steps: State | Chain

    def to_dict(self) -> dict:
        """
        Converts the Catch configuration to a dictionary format.
        """

        return {
            "ErrorEquals": [error.value for error in self.error_equals],
            "Next": (
                self.next_steps.id
                if isinstance(self.next_steps, State)
                else self.next_steps.steps[0].id
            ),
            "states": (
                Chain(steps=[self.next_steps])._states
                if isinstance(self.next_steps, State)
                else self.next_steps._states
            ),
        }
