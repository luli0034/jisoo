from jisoo.models.common import KeyValuePair
from jisoo.utils import process_context
from jisoo.models.common.ecs import (
    TaskOverride,
    ContainerOverride,
    KeyValuePair,
    NetworkConfiguration,
    AwsVpcConfiguration,
)
from jisoo.models.state import Chain, Map, Graph, Choice, ChoiceRule, Succeed
from jisoo.models.rule import Condition
from jisoo.steps.ecs import ECSRunTaskStep
from jisoo.steps.sqs import SQSDeleteMessageStep
from jisoo.steps.dynamodb import DynamoDBUpdateItemStep
from jisoo.models.input import StepInput
from jisoo.models.common import KeyValuePair
from jisoo.utils import to_pascalcase


def create_update_ddb_step() -> Map:
    update_ddb_input = StepInput(
        schema={
            "Environments.CONSUMER_OUTPUT_KEY_DATASET_ID": str,
            "Environments.CONSUMER_OUTPUT_KEY_OBJECT_KEY": str,
        }
    )
    update_ddb_success = Succeed(id="Success")
    update_fail = DynamoDBUpdateItemStep(
        id="UpdateFail",
        table_name="Environments.STATUS_TABLE_NAME",
        key={
            "Environments.STATUS_TABLE_PARTITION_KEY": {
                "S": update_ddb_input.get(
                    "Environments.CONSUMER_OUTPUT_KEY_DATASET_ID"
                ).get_path()
            },
            "Environments.STATUS_TABLE_SORT_KEY": {
                "S": update_ddb_input.get(
                    "Environments.CONSUMER_OUTPUT_KEY_OBJECT_KEY"
                ).get_path()
            },
        },
        update_expression="SET #status = :value",
        expression_attribute_names={"#status": "status"},
        expression_attribute_values={":value": {"S": "FAIL"}},
        result_path=None,
    )

    update_success = DynamoDBUpdateItemStep(
        id="UpdateSuccess",
        table_name="Environments.STATUS_TABLE_NAME",
        key={
            "Environments.STATUS_TABLE_PARTITION_KEY": {
                "S": update_ddb_input.get(
                    "Environments.CONSUMER_OUTPUT_KEY_DATASET_ID"
                ).get_path()
            },
            "Environments.STATUS_TABLE_SORT_KEY": {
                "S": update_ddb_input.get(
                    "Environments.CONSUMER_OUTPUT_KEY_OBJECT_KEY"
                ).get_path()
            },
        },
        update_expression="SET #status = :value",
        expression_attribute_names={"#status": "status"},
        expression_attribute_values={":value": {"S": "SUCCESS"}},
        result_path=None,
    )

    is_task_failed = Choice(
        id="Choice",
        choices=[
            ChoiceRule(
                rule=Condition.Not(Condition.NumericEquals("$.status", 0)),
                next=Chain(steps=[update_fail, update_ddb_success]),
            )
        ],
    )

    return Map(
        id="MapUpdateDDB",
        input_path=f"$.TaskResult",
        item_processor=Chain(
            steps=[
                is_task_failed,
                update_success,
                update_ddb_success,
            ],
        ),  # Define the states within the Map
        result_path=None,
    )


main = Map(
    id="Map",
    items_path=f"$.Environments.CONSUMER_OUTPUT_KEY_ITEMS_KEY",
    max_concurrency=2,
    item_processor=Chain(
        steps=[
            create_update_ddb_step(),
        ]
    ),
)

g = Graph(branch=main)
print(g.definition)
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

# get_item_step = DynamoDBGetItemStep(
#     id="example",
#     table_name="example",
#     integration_type="aws-sdk",
#     key={"sort_key": {"foo": "$.bar", "foo2.$": "$.bar2", "foo3": "bar3"}},
#     consistent_read=True,
#     return_consumed_capacity="TOTAL",
#     projection_expression="$.input_key",
#     expression_attribute_names={"key": "value"},
# )
# step_dict = get_item_step.to_dict()
# print(step_dict)
