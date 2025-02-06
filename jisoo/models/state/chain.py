import json
from typing import Optional, List, Dict
from enum import Enum
from pydantic import (
    BaseModel,
    model_validator,
    computed_field,
)

from jisoo.exception import EmptyStateInChain, DuplicateStatesInChain
from jisoo.models.state.base import State


class Chain(BaseModel):
    """
    Represents a sequence of states in a workflow chain.

    This class manages a collection of states and their transitions, ensuring that:
    - The chain is not empty
    - Each state has a unique ID
    - States are properly connected based on their type

    Attributes:
        steps (List[State]): A list of State objects representing the workflow steps
    """

    steps: List[State]

    @model_validator(mode="after")
    def unique_step_in_chain(self):
        """
        Validates that the chain is not empty and all state IDs are unique.

        Raises:
            EmptyStateInChain: If the chain contains no steps
            DuplicateStatesInChain: If there are multiple states with the same ID

        Returns:
            Chain: The validated chain instance
        """
        if not self.steps:
            raise EmptyStateInChain("The chain is empty")

        unique_list = []
        for step in self.steps:
            if step.id in unique_list:
                raise DuplicateStatesInChain(f"Duplicate id: {step.id}")

            unique_list.append(step.id)

        return self

    @computed_field
    def _states(self) -> Dict[str, dict]:
        """
        Processes all states in the chain and creates a dictionary representation.

        This method:
        - Processes each state based on its type (Choice, Task, etc.)
        - Sets up transitions between states
        - Converts states to their dictionary representation

        Returns:
            Dict[str, dict]: A dictionary mapping state IDs to their dictionary representations
        """
        states = {}
        for i, current_state in enumerate(self.steps):

            if current_state.type == "Choice":
                self._process_choice_state(
                    states,
                    current=current_state,
                    next=self.steps[i + 1] if (i + 1) < len(self.steps) else None,
                )

            elif current_state.type in ["Task", "Parallel", "Map", "Pass", "Wait"]:
                self._process_standard_state(
                    current=current_state,
                    next=self.steps[i + 1] if (i + 1) < len(self.steps) else None,
                )
                if current_state.type in ["Map", "Parallel", "Task"]:
                    self._process_catch(states, current_state)

            states[current_state.id] = current_state.to_dict()

        return states

    def _process_choice_state(
        self, states: dict, current: State, next: State = None
    ) -> None:
        """
        Processes a Choice state and its transitions.

        Args:
            states (dict): Dictionary of all states in the chain
            current (State): The Choice state being processed
            next (State, optional): The next state in the chain sequence

        Raises:
            ValueError: If the Choice state is missing required fields
        """
        self._validate_state_has_field(current, "_default")
        choices = []
        for choice_rule in current.choices:
            choices.append(choice_rule.to_dict())
            self._process_choice_rule(states, choice_rule)
            current.choices = choices

            if next:
                current._default = next.id

    def _process_choice_rule(self, states: dict, choice_rule) -> None:
        """
        Processes a single choice rule and sets up its transitions.

        Args:
            states (dict): Dictionary of all states in the chain
            choice_rule: The choice rule to process

        Note:
            This method handles both direct state transitions and nested chain transitions
        """
        if isinstance(choice_rule.next, State):
            choice_rule.rule._next = choice_rule.next.id
        elif isinstance(choice_rule.next, Chain):
            choice_rule.rule._next = choice_rule.next.steps[0].id
            # Recursively process the chain
            states.update(choice_rule.next._states)

    def _process_catch(self, states: dict, current_state) -> None:
        """
        Processes a single choice rule and sets up its transitions.

        Args:
            states (dict): Dictionary of all states in the chain
            choice_rule: The choice rule to process

        Note:
            This method handles both direct state transitions and nested chain transitions
        """
        if not hasattr(current_state, "catch") or current_state.catch is None:
            return

        for catch in current_state.catch:
            catch_states = catch.pop("states")
            states.update(catch_states)

    def _process_standard_state(self, current: State, next: State) -> None:
        """
        Processes a standard state (Task, Parallel, Map, Pass, Wait) and its transition.

        Args:
            current (State): The current state being processed
            next (State): The next state in the chain sequence

        Note:
            If there is no next state and the current state has an 'end' attribute,
            it will be marked as an end state
        """
        self._validate_state_has_field(current, "_next")

        # Set the next state
        if next:
            current._next = next.id
        else:
            if hasattr(current, "_end"):
                current._end = True

    def _validate_state_has_field(self, state: State, field: str) -> None:
        """
        Validates that a state has the required field.

        Args:
            state (State): The state to validate
            field (str): The name of the field to check for

        Raises:
            ValueError: If the state doesn't have the required field
        """
        if not hasattr(state, field):
            raise ValueError(f"Invalid key {field} in {state.type} state: {state.id}.")
