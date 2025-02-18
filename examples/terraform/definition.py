from jisoo.models.state import Chain, Graph, Catch, Succeed, Fail, Map, Pass, Task
from jisoo.steps import ECSRunTaskStep, LambdaInvokeStep
from jisoo.models.input import StepInput, RootInput
from jisoo.models.input.terraform import TFVariables
from jisoo.models.common import KeyValuePair
from jisoo.models.common.ecs import (
    NetworkConfiguration,
    AwsVpcConfiguration,
    TaskOverride,
    ContainerOverride,
)

tfvars = TFVariables()
tfvars.add_variable("LAMBDA_FUNCTION_NAME")
tfvars.add_variable("ECS_CLUSTER_BATCH_INGESTION")
tfvars.add_variable("ECS_TASK_DEFINITION_BATCH_INGESTION")
tfvars.add_variable("CONSUMER_OUTPUT_KEY_ITEMS_KEY")
tfvars.add_variable("TASK_PRIVATE_SUBNET_1")
tfvars.add_variable("TASK_PRIVATE_SUBNET_2")
tfvars.add_variable("TASK_PRIVATE_SUBNET_3")
tfvars.add_variable("ECS_TASK_NAME")
root_input = RootInput(schema={"TASK_TOKEN": str})


def create_lambda_step() -> LambdaInvokeStep:

    lambda_input = StepInput(schema={"foo": str, "bar": int})

    lambda_invoke = LambdaInvokeStep(
        function_name=tfvars.get("LAMBDA_FUNCTION_NAME"),
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
            tfvars.get("CONSUMER_OUTPUT_KEY_ITEMS_KEY"): str,
        }
    )
    run_task_step = ECSRunTaskStep(
        id="example",
        integration_pattern="waitForTaskToken",
        launch_type="FARGATE",
        cluster=tfvars.get("ECS_CLUSTER_BATCH_INGESTION"),
        task_definition=tfvars.get("ECS_TASK_DEFINITION_BATCH_INGESTION"),
        network_configuration=NetworkConfiguration(
            awsvpc_configuration=AwsVpcConfiguration(
                subnets=[
                    tfvars.get("TASK_PRIVATE_SUBNET_1"),
                    tfvars.get("TASK_PRIVATE_SUBNET_2"),
                    tfvars.get("TASK_PRIVATE_SUBNET_3"),
                ],
                assign_public_ip="DISABLE",
            )
        ),
        overrides=TaskOverride(
            container_overrides=[
                ContainerOverride(
                    name=tfvars.get("ECS_TASK_NAME"),
                    environment=[
                        KeyValuePair(
                            name="OBJECTS",
                            value=tfvars.get_variable("CONSUMER_OUTPUT_KEY_ITEMS_KEY"),
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

    map_running_task = Map(
        id="map_running_task",
        items_path=tfvars.get("CONSUMER_OUTPUT_KEY_ITEMS_KEY"),
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
tfvars.dump_keys("examples/terraform/tfvars.txt")
with open("examples/terraform/definition.json", "w") as f:
    f.write(graph.definition)
