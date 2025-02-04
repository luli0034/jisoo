from typing import Any, List, Union, Optional


class JSONPath:
    """A class for handling JSON path traversal and manipulation.

    This class provides functionality to traverse JSON-like structures and maintain
    a path reference using dot notation and array indices.

    Attributes:
        _schema (Any): The JSON schema structure being traversed.
        _path (str): The current path in dot notation.
    """

    def __init__(
        self,
        schema: Any,
        path: Optional[str] = None,
    ) -> None:
        """Initialize a new JSONPath instance.

        Args:
            schema: The JSON schema to traverse.
            path: The current path in dot notation (default: "$").
        """
        self._schema = schema
        self._path = path or "$"

    def get(self, key: str) -> "JSONPath":
        """Access a dictionary key in the JSON schema.

        Args:
            key: The key to access.

        Returns:
            JSONPath: A new JSONPath instance for the accessed key.

        Raises:
            KeyError: If the key does not exist in the schema.
        """
        if not isinstance(self._schema, dict):
            raise TypeError(f"Expected a dictionary at path '{self._path}'")
        if key not in self._schema:
            raise KeyError(f"Key '{key}' not found at path '{self._path}'")
        return JSONPath(self._schema[key], f"{self._path}.{key}")

    def get_by_index(self, index: int) -> "JSONPath":
        """Access a list index in the JSON schema.

        Args:
            index: The index to access.

        Returns:
            JSONPath: A new JSONPath instance for the accessed index.

        Raises:
            TypeError: If the schema is not a list.
            IndexError: If the index is out of range.
        """
        if not isinstance(self._schema, list):
            raise TypeError(f"Expected a list at path '{self._path}'")
        if index < 0 or index >= len(self._schema):
            raise IndexError(f"Index '{index}' out of range at path '{self._path}'")
        return JSONPath(self._schema[index], f"{self._path}[{index}]")

    def get_path(self) -> str:
        """Get the current JSON path.

        Returns:
            str: The current path in dot notation.
        """
        return self._path

    def __str__(self) -> str:
        """Return the current JSON path as a string.

        Returns:
            str: The current path in dot notation.
        """
        return self.get_path()

    def __repr__(self) -> str:
        """Return the string representation of the JSONPath instance.

        Returns:
            str: The string representation of the JSONPath instance.
        """
        return f"JSONPath(schema={self._schema}, path='{self._path}')"


class ExecutionInput(JSONPath):
    """Handler for execution input placeholders in workflow definitions.

    This class provides a specialized JSONPath implementation for accessing
    execution input values in workflow definitions.
    """

    def __init__(self, schema: Optional[Any] = None) -> None:
        """Initialize a new ExecutionInput instance.

        Args:
            schema: Optional schema structure for the execution input.
        """
        super().__init__(schema, path="$$.Execution.Input")


class StepInput(JSONPath):
    """Handler for step input placeholders in workflow definitions.

    This class provides a specialized JSONPath implementation for accessing
    step input values in workflow definitions.
    """

    def __init__(self, schema: Optional[Any] = None) -> None:
        """Initialize a new StepInput instance.

        Args:
            schema: Optional schema structure for the step input.
        """
        super().__init__(schema, path="$")
