from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
import os

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


def insert_fake_data(env, items):

    # Insert fake data to local-dynamodb for testing

    """Fixture to create and set up the DynamoDB table before tests."""
    if not EnvironmentsModel.exists():
        EnvironmentsModel.create_table(wait=True)
    for k, v in items.items():
        EnvironmentsModel(
            env=env,
            resource_name=k,
            metadata=v,
        ).save()
