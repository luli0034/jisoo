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


def replace_keys_with_prefix(d) -> dict:
    if not isinstance(d, dict):
        return d

    new_dict = {}
    for key, value in d.items():
        new_key = (
            key + ".$"
            if (
                isinstance(value, str)
                and (
                    value.startswith("$.")
                    # TODO: workaround for the intrinsic functions
                    or value.startswith("States.")
                )
                and not key.endswith(".$")
            )
            else key
        )
        new_dict[new_key] = (
            replace_keys_with_prefix(value) if isinstance(value, dict) else value
        )

    return new_dict
