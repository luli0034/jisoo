from __future__ import annotations
import json
from typing import Optional, Union, Dict, Any
from pydantic import computed_field, PrivateAttr, model_validator
from jisoo.exception import DuplicateStateError, InvalidGraph, EmptyStateInGraph
from jisoo.models.state.base import Block, State
from jisoo.models.state.chain import Chain


class Graph(Block):
    """A class representing a directed graph structure for state management.

    This class implements a graph that can contain either a single state or a chain
    of states, with support for timeouts and comments. It provides functionality
    to convert the graph structure to dictionary and JSON formats.

    Attributes:
        comment (Optional[str]): Optional description or comment about the graph
        timeout_seconds (Optional[int]): Maximum execution time in seconds
        branch (Union[State, Chain]): The main branch containing either a single state
            or a chain of states
        _first_state (State): Private attribute storing the initial state

    Raises:
        InvalidGraph: When the branch type is invalid or graph structure is incorrect
    """

    comment: Optional[str] = None
    timeout_seconds: Optional[int] = None
    branch: State | Chain
    _first_state: State = PrivateAttr(None)

    @computed_field
    def first_state(self) -> str:
        """Get the ID of the first state in the graph.

        Returns:
            str: The ID of the first state
        """
        return self._first_state

    @model_validator(mode="after")
    def set_first_state(self) -> "Graph":
        """Validate and set the first state of the graph.

        This method is automatically called after model initialization to set
        the first state based on the branch type.

        Returns:
            Graph: The validated graph instance

        Raises:
            InvalidGraph: If the branch type is neither State nor Chain
        """
        if isinstance(self.branch, Chain):
            self._first_state = self.branch.steps[0]
        elif isinstance(self.branch, State):
            self._first_state = self.branch
        else:
            raise InvalidGraph(f"Invalid branch type: {type(self.branch)}")
        return self

    def to_dict(self) -> Dict[str, Any]:
        """Convert the graph to a dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary containing the graph structure with states,
                           start state, and optional fields

        Raises:
            InvalidGraph: If the branch type is invalid
        """
        states = (
            self.branch._states
            if isinstance(self.branch, Chain)
            else Chain(steps=[self.branch])._states
        )

        graph: Dict[str, Any] = {
            "States": states,
            "StartAt": self._first_state.id,
        }

        # Add optional fields if they exist
        if self.comment is not None:
            graph["Comment"] = self.comment
        if self.timeout_seconds is not None:
            graph["TimeoutSeconds"] = self.timeout_seconds

        return graph

    def to_json(self, pretty: bool = False) -> str:
        """Convert the statemachine to a JSON string representation.

        Args:
            pretty (bool, optional): If True, formats the JSON with indentation.
                                   Defaults to False.

        Returns:
            str: JSON string representation of the statemachine
        """
        indent = 4 if pretty else None
        return json.dumps(self.to_dict(), indent=indent)

    @property
    def definition(self) -> Dict[str, Any]:
        """Get the definition of the statemachine.

        Returns:
            Dict[str, Any]: The dictionary representation of the graph
        """
        return self.to_json(pretty=True)
