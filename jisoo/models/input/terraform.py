import json


class TFVariables:
    """
    A class to manage Terraform variables.
    """

    def __init__(self):
        """
        Initializes an empty dictionary to store variables.
        """
        self._variables = {}

    def add_variable(self, key: str) -> None:
        """
        Adds a variable to the dictionary with the key in uppercase.

        Args:
            key (str): The variable key to add.
        """
        self._variables[key.upper()] = f"${{{key}}}"

    def get(self, key: str) -> str:
        """
        Retrieves the value of a variable by its key in uppercase.

        Args:
            key (str): The variable key to retrieve.

        Returns:
            str: The value of the variable in uppercase.
        """
        return self._variables[key.upper()].upper()

    def get_variable(self, key: str) -> str:
        """
        Formats the variable for Terraform usage.

        Args:
            key (str): The variable key to format.

        Returns:
            str: The formatted variable string.
        """
        return f"$.{self.get(key)}"

    def to_dict(self) -> dict:
        """
        Returns the dictionary of variables.

        Returns:
            dict: The dictionary containing all variables.
        """
        return self._variables

    @property
    def variables(self) -> list:
        """
        Returns a list of formatted variable strings.

        Returns:
            list: A list of formatted variable strings.
        """
        return [self.get_variable(key) for key in self._variables.keys()]

    def dump_keys(self, path: str) -> None:
        """
        Writes the variable keys to a file, one per line.

        Args:
            path (str): The file path to write the keys to.
        """
        with open(path, "w+") as f:
            for key in self._variables.keys():
                f.write(key + "\n")
