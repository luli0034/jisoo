from jisoo.models.state import State, Chain, Graph
from jisoo.models.state.handler import ErrorHandler, NextHandler
from typing import Optional, List
from pydantic import field_validator, Field, PrivateAttr


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


class Parallel(State, ErrorHandler, NextHandler):
    """
    Represents a Parallel state that executes multiple branches of states concurrently.

    A Parallel state enables simultaneous execution of multiple branches of workflow steps.
    Each branch is an independent set of states that executes in parallel with other branches.
    The state completes when all branches have finished their execution.

    Attributes:
        type (str): Fixed as "Parallel", defines the state type
        branches (List[Union[Chain, dict]]): List of workflow branches to execute in parallel.
            Each branch can be a Chain object or a dictionary defining the workflow
        input_path (Optional[str]): JSONPath that selects part of the input to be processed.
            Defaults to None (entire input)
        output_path (Optional[str]): JSONPath that selects part of the output to be returned.
            Defaults to None (entire output)
        result_path (Optional[str]): JSONPath that specifies where to place the output.
            Defaults to None
        result_selector (Optional[str]): Optional path to select specific data from results.
            Defaults to None
        parameters (Optional[dict]): Parameters to be passed to each branch.
            Defaults to None

    Example:
        >>> parallel_state = Parallel(
        ...     id="ProcessInParallel",
        ...     branches=[
        ...         Chain(steps=[State(id="Branch1Task", type="Task")]),
        ...         Chain(steps=[State(id="Branch2Task", type="Task")])
        ...     ],
        ...     result_path="$.parallel_results"
        ... )

    Note:
        - All branches start executing simultaneously
        - The state completes only when all branches have completed
        - Each branch receives the same input
        - The output is an array containing results from all branches in order
        - Error handling can be configured using Retry and Catch configurations
    """

    type: str = Field("Parallel", frozen=True)
    branches: List[Chain] | List[dict]
    input_path: Optional[str] = None
    output_path: Optional[str] = None
    result_path: Optional[str] = None
    result_selector: Optional[str] = None
    parameters: Optional[dict] = None

    @field_validator("branches", mode="after")
    @classmethod
    def set_branches(cls, branches: List[Chain]) -> List[dict]:
        """
        Validates and transforms the branches into the required dictionary format.

        This method converts each branch Chain into a dictionary format suitable
        for workflow execution.

        Args:
            branches (List[Chain]): List of Chain objects defining parallel workflows

        Returns:
            List[dict]: List of processed branch configurations

        Note:
            Each branch is processed through a Graph to ensure proper state connections
            and formatting.
        """
        outputs = []
        for chain in branches:
            outputs.append(Graph(branch=chain).to_dict())
        return outputs
