import json
from typing import Optional, List, Dict
from jisoo.utils import process_context
from enum import Enum
from pydantic import (
    BaseModel,
    ConfigDict,
)


class Block(BaseModel):
    """
    Base class for state-related models with custom serialization methods.

    This class extends Pydantic's BaseModel to provide additional functionality for
    converting model instances to dictionary and JSON formats, with special handling
    for enums and lists.

    Attributes:
        model_config (ConfigDict): Configuration to forbid extra attributes

    Note:
        The class automatically excludes None values and 'id' fields (case-insensitive)
        during serialization.
    """

    model_config = ConfigDict(extra="forbid")

    def to_dict(self):
        """
        Converts the model instance to a dictionary with PascalCase keys.

        This method handles special cases for:
        - Enum values (converts to their value property)
        - List of items (processes each item for Enum conversion)
        - None values (excludes them)
        - 'id' fields (excludes them)

        Returns:
            dict: A dictionary representation of the model with processed values
        """
        res = {}
        for k, v in self.model_dump().items():
            if v is None or k.lower() == "id":
                continue
            elif isinstance(v, dict):
                _k, _v = process_context(k, v)
                res[self.to_pascalcase(_k)] = _v
            else:
                res[self.to_pascalcase(k)] = v

        return res

    def to_json(self, pretty=False):
        """
        Converts the model instance to a JSON string.

        Args:
            pretty (bool, optional): If True, formats the JSON with indentation.
                Defaults to False.

        Returns:
            str: A JSON string representation of the model
        """
        if pretty:
            return json.dumps(self.to_dict(), indent=4)
        return json.dumps(self.to_dict())

    def to_pascalcase(self, text):
        """
        Converts a snake_case string to PascalCase.

        Args:
            text (str): The snake_case string to convert

        Returns:
            str: The converted PascalCase string

        Example:
            >>> block = Block()
            >>> block.to_pascalcase("hello_world")
            "HelloWorld"
        """
        return "".join([t.title() for t in text.split("_")])


class State(Block):
    """
    Represents a basic state in a workflow.

    This class extends the Block class to provide the fundamental structure
    for all state types in a workflow chain.

    Attributes:
        id (str): Unique identifier for the state
        type (str): The type of the state (e.g., "Task", "Choice", "Parallel")
        comment (Optional[str]): Optional description or comment about the state.
            Defaults to None.

    Example:
        >>> state = State(id="MyState", type="Task", comment="This is a task state")
        >>> state.to_dict()
        {'Type': 'Task', 'Comment': 'This is a task state'}
    """

    id: str
    type: str
    comment: Optional[str] = None
