from pydantic import BaseModel, model_validator
from jisoo.models.rule import BaseRule
from jisoo.models.state.base import State
from jisoo.models.state.chain import Chain


class ChoiceRule(BaseModel):
    """
    Represents a rule in a Choice state that determines the next state based on conditions.

    A ChoiceRule defines a condition and the next state to transition to when that condition
    is met. It's used within Choice states to implement conditional branching logic in
    the workflow.

    Attributes:
        rule (BaseRule): The condition rule that determines when this choice should be taken.
            Can be a comparison rule (e.g., StringEquals, NumericLessThan) or a logical
            rule (And, Or, Not).
        next (Union[State, Chain]): The state or chain of states to transition to when
            the rule evaluates to true.

    Example:
        >>> from jisoo.models.rule import StringEquals
        >>> choice_rule = ChoiceRule(
        ...     rule=StringEquals(variable="$.type", value="test"),
        ...     next=State(id="TestState", type="Task")
        ... )
        >>> rule_dict = choice_rule.to_dict()

    Note:
        When converted to a dictionary using to_dict(), the 'next' field will be
        converted to the ID of the first state in the chain or the state itself.
    """

    rule: BaseRule
    next: State | Chain

    @model_validator(mode="after")
    def set_next_state(self):
        if isinstance(self.next, State):
            self.next = Chain(steps=[self.next])
        return self

    def to_dict(self) -> dict:
        """
        Converts the ChoiceRule to a dictionary format.

        This method processes the rule and next state/chain into a format suitable
        for workflow definitions. For the 'next' field, it extracts either:
        - The ID of the specified state, or
        - The ID of the first state in the chain

        Returns:
            dict: A dictionary containing the rule and the next state identifier
        """
        rule = self.rule.to_dict()
        if isinstance(self.next, State):
            rule["Next"] = self.next.id
        elif isinstance(self.next, Chain):
            rule["Next"] = self.next.steps[0].id

        return rule
