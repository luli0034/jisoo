from jisoo.models.state import State
from jisoo.models.state.handler import ErrorHandler, NextHandler
from jisoo.models.state.chain import Chain
from jisoo.models.state.graph import Graph
from typing import Optional, Dict
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


class Map(State, ErrorHandler, NextHandler):
    """
    Represents a Map state that processes an array of items in parallel or sequentially.

    A Map state iterates over an array of items and executes the same processing steps
    for each item. It can process items concurrently up to a specified maximum, or
    process them sequentially if max_concurrency is 1.

    Attributes:
        type (str): Fixed as "Map", defines the state type
        input_path (Optional[str]): JSONPath that selects part of the input to be processed.
            Defaults to None (entire input)
        output_path (Optional[str]): JSONPath that selects part of the output to be returned.
            Defaults to None (entire output)
        result_path (Optional[str]): JSONPath that specifies where to place the output.
            Defaults to None
        result_selector (Optional[Dict]): Optional path to select specific data from results.
            Defaults to None
        parameters (Optional[dict]): Parameters to be passed to each iteration.
            Defaults to None
        item_processor (Chain): The workflow to execute for each item.
            Can be a Chain object or a dictionary defining the workflow
        items_path (Optional[str]): JSONPath that specifies where to find the array
            of items to process. Defaults to None (uses entire input)
        max_concurrency (Optional[int]): Maximum number of parallel executions.
            Defaults to None (unlimited concurrency)

    Example:
        >>> map_state = Map(
        ...     id="ProcessItems",
        ...     items_path="$.array",
        ...     item_processor=Chain(steps=[
        ...         State(id="ProcessItem", type="Task")
        ...     ]),
        ...     max_concurrency=5
        ... )

    Note:
        - The item_processor defines the workflow that processes each item
        - If max_concurrency is not specified, all items may be processed in parallel
        - Error handling can be configured using Retry and Catch configurations
        - The result will be an array containing the output from each item's processing
    """

    type: str = Field("Map", frozen=True)
    input_path: Optional[str] = None
    output_path: Optional[str] = None
    result_path: Optional[str] = None
    result_selector: Optional[Dict] = None
    parameters: Optional[dict] = None
    item_processor: Chain | dict
    items_path: Optional[str] = None
    max_concurrency: Optional[int] = None

    @field_validator("item_processor", mode="after")
    @classmethod
    def set_item_processor(cls, value: Chain) -> Dict[str, any]:
        """
        Validates and transforms the item_processor into the required format.

        This method converts the item_processor Chain into a dictionary format and
        adds the required ProcessorConfig configuration.

        Args:
            value (Chain): The Chain object defining the item processing workflow

        Returns:
            dict: The processed item_processor configuration with ProcessorConfig added

        Note:
            The ProcessorConfig is set to "INLINE" mode, indicating that the
            processor definition is included directly in the state definition.
        """
        graph = Graph(branch=value).to_dict()
        graph["ProcessorConfig"] = {"Mode": "INLINE"}
        return graph
