from boto3.dynamodb.types import TypeDeserializer


def dynamodb_item_deserialize(dynamodb_response: dict):
    """
    Converts a DynamoDB response to dict.

    Args:

        dynamodb_response (dict): The dictionary returned from DynamoDB.

    Returns:
        Dict[str, str]: The dictionary representation of the DynamoDB response.
    """

    deseializer = TypeDeserializer()
    return {
        key: deseializer.deserialize(value) for key, value in dynamodb_response.items()
    }
