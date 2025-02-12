from enum import Enum


def dynamodb_map_to_dict(dynamodb_response: dict):
    """
    Converts a DynamoDB response to dict.

    Args:

        dynamodb_response (dict): The dictionary returned from DynamoDB.

    Returns:
        Dict[str, str]: The dictionary representation of the DynamoDB response.
    """
    return {key: value["S"] for key, value in dynamodb_response.items()}
