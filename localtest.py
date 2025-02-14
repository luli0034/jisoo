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

from jisoo.models.common import KeyValuePair
from jisoo.utils import to_pascalcase

# print(to_pascalcase("AwsvpcConfiguration"))
# data = {"foo": KeyValuePair(name="foo", value="bar")}
# print(process_context("key", data))

run_task_step = ECSRunTaskStep(
    id="example",
    launch_type="FARGATE",
    cluster="example-cluster",
    task_definition="example-task-definition",
    network_configuration=NetworkConfiguration(
        awsvpc_configuration=AwsVpcConfiguration(
            subnets=[
                "example-subnet-1",
                "example-subnet-2",
                "example-subnet-3",
            ],
            assign_public_ip="DISABLE",
        )
    ),
    overrides=TaskOverride(
        container_overrides=[
            ContainerOverride(
                name="$.example-container",
                environment=[
                    KeyValuePair(
                        name="OBJECTS",
                        value="States.JsonToString($.items)",
                    ),
                    KeyValuePair(
                        name="TASK_TOKEN",
                        value="$$.Task.Token",
                    ),
                    KeyValuePair(
                        name="$.foo",
                        value="$.bar",
                    ),
                ],
            )
        ]
    ),
    result_path="$.result",
    integration_pattern="waitForTaskToken",
    integration_type="optimized",
)
step_dict = run_task_step.to_dict()
print(step_dict)
