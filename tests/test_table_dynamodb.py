from jisoo.table.dynamodb import DynamoDBTable
from jisoo.steps import LambdaInvokeStep
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pynamodb.exceptions import GetError, TableDoesNotExist, PynamoDBConnectionError
import pytest
import os
import time

# Set up environment variables for local DynamoDB
os.environ["AWS_ACCESS_KEY_ID"] = "fakeMyKeyId"
os.environ["AWS_SECRET_ACCESS_KEY"] = "fakeSecretAccessKey"
os.environ["AWS_DEFAULT_REGION"] = "us-west-2"  # Match the region used in tests
TABLE_NAME = "environments"
REGION = "us-west-2"


# Define the test DynamoDB model
class EnvironmentsModel(Model):
    class Meta:
        table_name = TABLE_NAME
        host = "http://localhost:8000"  # Use DynamoDB Local
        read_capacity_units = 1
        write_capacity_units = 1
        region = REGION

    env = UnicodeAttribute(hash_key=True)
    resource_name = UnicodeAttribute(range_key=True)
    metadata = UnicodeAttribute()


@pytest.fixture(scope="module")
def environment_table():
    """Fixture to create and set up the DynamoDB table before tests."""
    if not EnvironmentsModel.exists():
        EnvironmentsModel.create_table(wait=True)

    # Insert test data
    EnvironmentsModel(
        env="test",
        resource_name="example_lambda_function",
        metadata="example-lambda-function",
    ).save()

    yield

    # Cleanup (Optional)
    EnvironmentsModel.delete_table()


def test_dynamodb_table(environment_table):
    """Test DynamoDBTable interaction with a local DynamoDB instance."""
    env_table = DynamoDBTable(
        table_name=TABLE_NAME,
        region_name=REGION,  # Use the same region as in env vars
        hash_key="test",
        attribute_to_get="metadata",
        host="http://localhost:8000",
    )

    metadata_value = env_table.get("example_lambda_function")  # Use correct keys
    assert metadata_value == "example-lambda-function"

    # Test with incorrect keys
    with pytest.raises(GetError):
        env_table.get("incorrect_resource_name")

    with pytest.raises(GetError):
        env_table.get("example_lambda_function", attribute_to_get="incorrect_attribute")


def test_table_not_exist(environment_table):

    with pytest.raises(TableDoesNotExist):
        DynamoDBTable(
            table_name="non_existent_table",
            region_name=REGION,
            hash_key="test",
            attribute_to_get="metadata",
            host="http://localhost:8000",
        )


def test_get_in_method_call(environment_table):
    env_table = DynamoDBTable(
        table_name=TABLE_NAME,
        region_name=REGION,
        host="http://localhost:8000",
    )

    metadata_value = env_table.get(
        range_key="example_lambda_function",
        hash_key="test",
        attribute_to_get="metadata",
    )
    assert metadata_value == "example-lambda-function"

    # Test with invalid hash key
    with pytest.raises(ValueError):
        env_table.get(range_key="example_lambda_function")

    with pytest.raises(ValueError):
        env_table.get(hash_key="test", range_key="example_lambda_function")
