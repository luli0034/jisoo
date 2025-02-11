from jisoo.steps import Service, ECSRunTaskStep
from jisoo.models.common import ServiceType
from jisoo.models.input import RootInput
from jisoo.models.common.ecs import (
    NetworkConfiguration,
    TaskOverride,
    ContainerOverride,
    KeyValuePair,
    AwsVpcConfiguration,
)
import pytest
from pydantic import ValidationError


def test_runtask_step():

    root_input = RootInput(schema={"TASK_TOKEN": str})

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
                    name="example-container",
                    environment=[
                        KeyValuePair(
                            name="OBJECTS",
                            value="objects",
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
        integration_pattern="waitForTaskToken",
        integration_type="optimized",
    )
    step_dict = run_task_step.to_dict()
    assert step_dict["Type"] == "Task"
    assert step_dict["Resource"] == "arn:aws:states:::ecs:runTask.waitForTaskToken"
    assert step_dict["Parameters"]["Cluster"] == "example-cluster"
    assert step_dict["Parameters"]["TaskDefinition"] == "example-task-definition"
    assert step_dict["Parameters"]["LaunchType"] == "FARGATE"
    assert step_dict["Parameters"]["NetworkConfiguration"]["AwsvpcConfiguration"][
        "Subnets"
    ] == [
        "example-subnet-1",
        "example-subnet-2",
        "example-subnet-3",
    ]
    assert (
        step_dict["Parameters"]["NetworkConfiguration"]["AwsvpcConfiguration"][
            "AssignPublicIp"
        ]
        == "DISABLE"
    )
    assert (
        step_dict["Parameters"]["Overrides"]["ContainerOverrides"][0]["Name"]
        == "example-container"
    )
    assert step_dict["Parameters"]["Overrides"]["ContainerOverrides"][0][
        "Environment"
    ] == [
        {"Name": "OBJECTS", "Value": "objects"},
        {"Name": "TASK_TOKEN", "Value.$": "$$.TASK_TOKEN"},
    ]
    assert step_dict["ResultPath"] == "$.result"
