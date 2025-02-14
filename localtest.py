from jisoo.models.common import KeyValuePair
from jisoo.utils import process_context
from jisoo.models.common.ecs import (
    TaskOverride,
    ContainerOverride,
    KeyValuePair,
    NetworkConfiguration,
    AwsVpcConfiguration,
)
from jisoo.steps.ecs import ECSRunTaskStep
from jisoo.steps.dynamodb import DynamoDBGetItemStep

from jisoo.models.common import KeyValuePair
from jisoo.utils import to_pascalcase

print(to_pascalcase("projection_expression.$"))
# data = {"foo": KeyValuePair(name="foo", value="bar")}
# print(process_context("key", data))

# run_task_step = ECSRunTaskStep(
#     id="example",
#     launch_type="FARGATE",
#     cluster="example-cluster",
#     task_definition="example-task-definition",
#     network_configuration=NetworkConfiguration(
#         awsvpc_configuration=AwsVpcConfiguration(
#             subnets=[
#                 "example-subnet-1",
#                 "example-subnet-2",
#                 "example-subnet-3",
#             ],
#             assign_public_ip="DISABLE",
#         )
#     ),
#     overrides=TaskOverride(
#         container_overrides=[
#             ContainerOverride(
#                 name="$.example-container",
#                 environment=[
#                     KeyValuePair(
#                         name="OBJECTS",
#                         value="States.JsonToString($.items)",
#                     ),
#                     KeyValuePair(
#                         name="TASK_TOKEN",
#                         value="$$.Task.Token",
#                     ),
#                     KeyValuePair(
#                         name="$.foo",
#                         value="$.bar",
#                     ),
#                 ],
#             )
#         ]
#     ),
#     result_path="$.result",
#     integration_pattern="waitForTaskToken",
#     integration_type="optimized",
#     tags=[
#         {"key": "example-key-1", "value": "example-value-1"},
#         {"key": "example-key-2", "value": "example-value-2"},
#         {"key": "example-key-3", "value": "example-value-3"},
#     ]
# )
# step_dict = run_task_step.to_dict()
# print(step_dict)

get_item_step = DynamoDBGetItemStep(
    id="example",
    table_name="example",
    integration_type="aws-sdk",
    key={"sort_key": {"foo": "$.bar", "foo2.$": "$.bar2", "foo3": "bar3"}},
    consistent_read=True,
    return_consumed_capacity="TOTAL",
    projection_expression="$.input_key",
    expression_attribute_names={"key": "value"},
)
step_dict = get_item_step.to_dict()
print(step_dict)