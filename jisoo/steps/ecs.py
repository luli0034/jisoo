from jisoo.steps.base import Service
from jisoo.models.common import ServiceType
from jisoo.models.common.ecs import NetworkConfiguration, TaskOverride
from enum import Enum
from pydantic import Field, BaseModel, model_validator
from typing import Optional, Dict, List, Literal

# Follow the Amazon ECS API Reference
# https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_Operations.html


class ECSAction(Enum):
    CreateCluster = "createCluster"
    DeleteCluster = "deleteCluster"
    DescribeClusters = "describeClusters"
    ListClusters = "listClusters"
    UpdateCluster = "updateCluster"
    CreateService = "createService"
    DeleteService = "deleteService"
    DescribeServices = "describeServices"
    ListServices = "listServices"
    UpdateService = "updateService"
    RegisterTaskDefinition = "registerTaskDefinition"
    DeregisterTaskDefinition = "deregisterTaskDefinition"
    DescribeTaskDefinition = "describeTaskDefinition"
    ListTaskDefinitions = "listTaskDefinitions"
    RunTask = "runTask"
    StartTask = "startTask"
    StopTask = "stopTask"
    DescribeTasks = "describeTasks"
    ListTasks = "listTasks"


class ECSCreateClusterStep(Service):
    service: ServiceType = Field(ServiceType.ECS, frozen=True)
    action: ECSAction = Field(ECSAction.CreateCluster, frozen=True)
    cluster_name: str
    tags: Optional[List[Dict[str, str]]] = None
    settings: Optional[List[Dict[str, str]]] = None
    capacity_providers: Optional[List[str]] = None
    default_capacity_provider_strategy: Optional[List[Dict[str, str]]] = None


class ECSDeleteClusterStep(Service):
    service: ServiceType = Field(ServiceType.ECS, frozen=True)
    action: ECSAction = Field(ECSAction.DeleteCluster, frozen=True)
    cluster: str


class ECSDescribeClustersStep(Service):
    service: ServiceType = Field(ServiceType.ECS, frozen=True)
    action: ECSAction = Field(ECSAction.DescribeClusters, frozen=True)
    clusters: List[str]
    include: Optional[List[str]] = None


class ECSListClustersStep(Service):
    service: ServiceType = Field(ServiceType.ECS, frozen=True)
    action: ECSAction = Field(ECSAction.ListClusters, frozen=True)
    next_token: Optional[str] = None
    max_results: Optional[int] = None


class ECSCreateServiceStep(Service):
    service: ServiceType = Field(ServiceType.ECS, frozen=True)
    action: ECSAction = Field(ECSAction.CreateService, frozen=True)
    cluster: Optional[str] = None
    service_name: str
    task_definition: Optional[str] = None
    load_balancers: Optional[List[Dict[str, str]]] = None
    service_registries: Optional[List[Dict[str, str]]] = None
    desired_count: Optional[int] = None
    client_token: Optional[str] = None
    launch_type: Optional[str] = None
    capacity_provider_strategy: Optional[List[Dict[str, str]]] = None
    platform_version: Optional[str] = None
    role: Optional[str] = None
    deployment_configuration: Optional[Dict[str, str]] = None
    placement_constraints: Optional[List[Dict[str, str]]] = None
    placement_strategy: Optional[List[Dict[str, str]]] = None
    network_configuration: Optional[Dict[str, str]] = None
    health_check_grace_period_seconds: Optional[int] = None
    scheduling_strategy: Optional[str] = None
    deployment_controller: Optional[Dict[str, str]] = None
    tags: Optional[List[Dict[str, str]]] = None
    enable_ecs_managed_tags: Optional[bool] = None
    propagate_tags: Optional[str] = None
    enable_execute_command: Optional[bool] = None


class ECSDeleteServiceStep(Service):
    service: ServiceType = Field(ServiceType.ECS, frozen=True)
    action: ECSAction = Field(ECSAction.DeleteService, frozen=True)
    cluster: Optional[str] = None
    service: str
    force: Optional[bool] = None


class ECSDescribeServicesStep(Service):
    service: ServiceType = Field(ServiceType.ECS, frozen=True)
    action: ECSAction = Field(ECSAction.DescribeServices, frozen=True)
    cluster: Optional[str] = None
    services: List[str]
    include: Optional[List[str]] = None


class ECSListServicesStep(Service):
    service: ServiceType = Field(ServiceType.ECS, frozen=True)
    action: ECSAction = Field(ECSAction.ListServices, frozen=True)
    cluster: Optional[str] = None
    next_token: Optional[str] = None
    max_results: Optional[int] = None
    launch_type: Optional[str] = None
    scheduling_strategy: Optional[str] = None


class ECSUpdateServiceStep(Service):
    service: ServiceType = Field(ServiceType.ECS, frozen=True)
    action: ECSAction = Field(ECSAction.UpdateService, frozen=True)
    cluster: Optional[str] = None
    service: str
    desired_count: Optional[int] = None
    task_definition: Optional[str] = None
    capacity_provider_strategy: Optional[List[Dict[str, str]]] = None
    deployment_configuration: Optional[Dict[str, str]] = None
    network_configuration: Optional[Dict[str, str]] = None
    placement_constraints: Optional[List[Dict[str, str]]] = None
    placement_strategy: Optional[List[Dict[str, str]]] = None
    platform_version: Optional[str] = None
    force_new_deployment: Optional[bool] = None
    health_check_grace_period_seconds: Optional[int] = None
    enable_execute_command: Optional[bool] = None


class ECSRegisterTaskDefinitionStep(Service):
    service: ServiceType = Field(ServiceType.ECS, frozen=True)
    action: ECSAction = Field(ECSAction.RegisterTaskDefinition, frozen=True)
    family: str
    container_definitions: List[Dict]
    task_role_arn: Optional[str] = None
    execution_role_arn: Optional[str] = None
    network_mode: Optional[str] = None
    volumes: Optional[List[Dict]] = None
    tags: Optional[List[Dict[str, str]]] = None


class ECSDeregisterTaskDefinitionStep(Service):
    service: ServiceType = Field(ServiceType.ECS, frozen=True)
    action: ECSAction = Field(ECSAction.DeregisterTaskDefinition, frozen=True)
    task_definition: str


class ECSDescribeTaskDefinitionStep(Service):
    service: ServiceType = Field(ServiceType.ECS, frozen=True)
    action: ECSAction = Field(ECSAction.DescribeTaskDefinition, frozen=True)
    task_definition: str


class ECSListTaskDefinitionsStep(Service):
    service: ServiceType = Field(ServiceType.ECS, frozen=True)
    action: ECSAction = Field(ECSAction.ListTaskDefinitions, frozen=True)
    family_prefix: Optional[str] = None
    status: Optional[str] = None
    sort: Optional[str] = None
    max_results: Optional[int] = None
    next_token: Optional[str] = None


class ECSRunTaskStep(Service):
    service: ServiceType = Field(ServiceType.ECS, frozen=True)
    action: ECSAction = Field(ECSAction.RunTask, frozen=True)
    launch_type: Literal["EC2", "FARGATE", "EXTERNAL"] = "EC2"
    cluster: Optional[str] = None
    task_definition: str
    network_configuration: Optional[NetworkConfiguration] | Optional[Dict] = None
    overrides: Optional[TaskOverride] | Optional[Dict] = None
    count: Optional[int] = None
    started_by: Optional[str] = None
    tags: Optional[List[Dict[str, str]]] = None


class ECSStartTaskStep(Service):
    service: ServiceType = Field(ServiceType.ECS, frozen=True)
    action: ECSAction = Field(ECSAction.StartTask, frozen=True)
    cluster: str
    task_definition: Optional[str] = None
    container_instances: List[str]
    overrides: Optional[Dict] = None
    started_by: Optional[str] = None


class ECSStopTaskStep(Service):
    service: ServiceType = Field(ServiceType.ECS, frozen=True)
    action: ECSAction = Field(ECSAction.StopTask, frozen=True)
    cluster: Optional[str] = None
    task: str
    reason: Optional[str] = None


class ECSDescribeTasksStep(Service):
    service: ServiceType = Field(ServiceType.ECS, frozen=True)
    action: ECSAction = Field(ECSAction.DescribeTasks, frozen=True)
    cluster: Optional[str] = None
    tasks: List[str]
    include: Optional[List[str]] = None


class ECSListTasksStep(Service):
    service: ServiceType = Field(ServiceType.ECS, frozen=True)
    action: ECSAction = Field(ECSAction.ListTasks, frozen=True)
    cluster: Optional[str] = None
    family: Optional[str] = None
    desired_status: Optional[str] = None
    launch_type: Optional[str] = None
    max_results: Optional[int] = None
    next_token: Optional[str] = None


# Additional ECS Dataclass
