from jisoo.steps import LambdaInvokeStep, DynamoDBGetItemStep, ECSRunTaskStep
from jisoo.models.input.terraform import TFVariables
from jisoo.models.input import StepInput, RootInput
from jisoo.models.common import KeyValuePair
from jisoo.models.common.ecs import (
    NetworkConfiguration,
    AwsVpcConfiguration,
    TaskOverride,
    ContainerOverride,
)

# lambda_invoke = LambdaInvokeStep(
#     function_name="example",
#     id="example",
#     integration_pattern="waitForTaskToken",
#     integration_type="aws-sdk",
#     input_path="$.input",
#     payload={
#         "${STATUS_TABLE_PARTITION_KEY}": {"S.$": "$.${CONSUMER_OUTPUT_KEY_DATASET_ID}"},
#         "${STATUS_TABLE_SORT_KEY}": {"S.$": "$.${CONSUMER_OUTPUT_KEY_OBJECT_KEY}"},
#     },
# )
# state_dict = lambda_invoke.to_dict()
# # print(state_dict)
# dynamodb_get_item = DynamoDBGetItemStep(
#     table_name="example",
#     id="example",
#     integration_pattern="waitForTaskToken",
#     integration_type="aws-sdk",
#     key={
#         "${STATUS_TABLE_PARTITION_KEY}": {"S.$": "$.${CONSUMER_OUTPUT_KEY_DATASET_ID}"},
#         "${STATUS_TABLE_SORT_KEY}": {"S.$": "$.${CONSUMER_OUTPUT_KEY_OBJECT_KEY}"},
#     },
# )
# state_dict = dynamodb_get_item.to_dict()
# print(state_dict)

tfvars = TFVariables()
tfvars.add_variable("ECS_CLUSTER_BATCH_INGESTION")
tfvars.add_variable("ECS_TASK_DEFINITION_BATCH_INGESTION")
tfvars.add_variable("CONSUMER_OUTPUT_KEY_ITEMS_KEY")
tfvars.add_variable("TASK_PRIVATE_SUBNET_1")
tfvars.add_variable("TASK_PRIVATE_SUBNET_2")
tfvars.add_variable("TASK_PRIVATE_SUBNET_3")
tfvars.add_variable("ECS_TASK_NAME")
run_task_input = StepInput(
    schema={
        tfvars.get("CONSUMER_OUTPUT_KEY_ITEMS_KEY"): str,
    }
)
root_input = RootInput(schema={"TASK_TOKEN": str})

run_task_step = ECSRunTaskStep(
    id="example",
    launch_type="FARGATE",
    cluster=tfvars.get_variable("ECS_CLUSTER_BATCH_INGESTION"),
    task_definition=tfvars.get_variable("ECS_TASK_DEFINITION_BATCH_INGESTION"),
    network_configuration=NetworkConfiguration(
        awsvpc_configuration=AwsVpcConfiguration(
            subnets=[
                tfvars.get_variable("TASK_PRIVATE_SUBNET_1"),
                tfvars.get_variable("TASK_PRIVATE_SUBNET_2"),
                tfvars.get_variable("TASK_PRIVATE_SUBNET_3"),
            ],
            assign_public_ip="DISABLE",
        )
    ),
    overrides=TaskOverride(
        container_overrides=[
            ContainerOverride(
                name=tfvars.get_variable("ECS_TASK_NAME"),
                environment=[
                    KeyValuePair(
                        name="OBJECTS",
                        value=run_task_input.get(
                            tfvars.get("CONSUMER_OUTPUT_KEY_ITEMS_KEY")
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
    result_path="$.result",
)
state_dict = run_task_step.to_json()
print(state_dict)
