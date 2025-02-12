from enum import Enum


def dynamodb_to_enum(class_name: str, dynamodb_response: dict):
    """
    Converts a DynamoDB response to an Enum class.

    Args:
        class_name (str): The name of the Enum class.
        dynamodb_response (dict): The dictionary returned from DynamoDB.

    Returns:
        Enum: A dynamically created Enum class.
    """
    enum_dict = {key: value["S"] for key, value in dynamodb_response.items()}

    return Enum(class_name, enum_dict)
