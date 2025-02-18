from jisoo.models.state import Chain, Graph, Catch, Succeed, Fail, Map, Pass, Task
from jisoo.steps import ECSRunTaskStep, LambdaInvokeStep
from jisoo.models.input import StepInput, RootInput
from jisoo.table.dynamodb import DynamoDBTable
from jisoo.models.common import KeyValuePair
from jisoo.models.common.ecs import (
    NetworkConfiguration,
    AwsVpcConfiguration,
    TaskOverride,
    ContainerOverride,
)
import os
from examples.dynamodb.mock_data import insert_fake_data, EnvironmentsModel

# Set up environment variables for local DynamoDB
os.environ["AWS_ACCESS_KEY_ID"] = "fakeMyKeyId"
os.environ["AWS_SECRET_ACCESS_KEY"] = "fakeSecretAccessKey"
os.environ["AWS_DEFAULT_REGION"] = "us-west-2"  # Match the region used in tests
TABLE_NAME = "environments"
REGION = "us-west-2"

insert_fake_data(
    "test",
    {
        "LAMBDA_FUNCTION_NAME": "example-lambda-function",
        "ECS_TASK_NAME": "example-ecs-task",
        "CONSUMER_OUTPUT_KEY_ITEMS_KEY": "example-consumer-output-key",
        "ECS_CLUSTER_BATCH_INGESTION": "example-ecs-cluster",
        "ECS_TASK_DEFINITION_BATCH_INGESTION": "example-ecs-task-definition",
        "TASK_PRIVATE_SUBNET_1": "example-subnet-1",
        "TASK_PRIVATE_SUBNET_2": "example-subnet-2",
        "TASK_PRIVATE_SUBNET_3": "example-subnet-3",
    },
)

ddb = DynamoDBTable(
    table_name=TABLE_NAME,
    region_name=REGION,
    hash_key="test",
    attribute_to_get="metadata",
    host="http://localhost:8000",
)

root_input = RootInput(schema={"TASK_TOKEN": str})


def create_lambda_step() -> LambdaInvokeStep:

    lambda_input = StepInput(schema={"foo": str, "bar": int})

    lambda_invoke = LambdaInvokeStep(
        function_name=ddb.get("LAMBDA_FUNCTION_NAME"),
        id="invoke_lambda_example",
        integration_pattern="waitForTaskToken",
        integration_type="optimized",
        payload={
            "TASK_TOKEN": "$$.Task.Token",
            "FOO": lambda_input.get("foo").get_path(),
        },
    )
    return lambda_invoke


def create_ecs_run_task_step() -> ECSRunTaskStep:
    run_task_input = StepInput(
        schema={
            ddb.get("CONSUMER_OUTPUT_KEY_ITEMS_KEY"): str,
        }
    )
    run_task_step = ECSRunTaskStep(
        id="example",
        integration_pattern="waitForTaskToken",
        launch_type="FARGATE",
        cluster=ddb.get("ECS_CLUSTER_BATCH_INGESTION"),
        task_definition=ddb.get("ECS_TASK_DEFINITION_BATCH_INGESTION"),
        network_configuration=NetworkConfiguration(
            awsvpc_configuration=AwsVpcConfiguration(
                subnets=[
                    ddb.get("TASK_PRIVATE_SUBNET_1"),
                    ddb.get("TASK_PRIVATE_SUBNET_2"),
                    ddb.get("TASK_PRIVATE_SUBNET_3"),
                ],
                assign_public_ip="DISABLE",
            )
        ),
        overrides=TaskOverride(
            container_overrides=[
                ContainerOverride(
                    name=ddb.get("ECS_TASK_NAME"),
                    environment=[
                        KeyValuePair(
                            name="OBJECTS",
                            value=run_task_input.get(
                                ddb.get("CONSUMER_OUTPUT_KEY_ITEMS_KEY")
                            ),
                        ),
                        KeyValuePair(
                            name="TASK_TOKEN",
                            value=root_input.get("TASK_TOKEN"),
                        ),
                    ],
                )
            ]
        ),
        result_path="$.TaskResult",
        catch=[
            Catch(error_equals=["States.ALL"], next_steps=Fail(id="run_task_failed"))
        ],
    )
    return run_task_step


def create_main_steps() -> Chain:
    run_task_input = StepInput(
        schema={
            ddb.get("CONSUMER_OUTPUT_KEY_ITEMS_KEY"): str,
        }
    )
    # print(run_task_input.get(ddb.get("CONSUMER_OUTPUT_KEY_ITEMS_KEY")))
    # raise
    map_running_task = Map(
        id="map_running_task",
        items_path=run_task_input.get(
            ddb.get("CONSUMER_OUTPUT_KEY_ITEMS_KEY")
        ).get_path(),
        max_concurrency=5,
        item_processor=Chain(
            steps=[create_ecs_run_task_step(), Succeed(id="run_ecs_success")]
        ),
    )

    transform = Pass(id="transform", input_path="$.TaskResult")

    return Chain(
        steps=[
            create_lambda_step(),
            map_running_task,
            transform,
        ]
    )


graph = Graph(branch=create_main_steps(), comment="Batch Ingestion", timeout_seconds=60)

with open("examples/dynamodb/definition.json", "w") as f:
    f.write(graph.definition)

# Cleanup (Optional)
EnvironmentsModel.delete_table()
