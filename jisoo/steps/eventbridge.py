from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from enum import Enum
from jisoo.models.common import ServiceType
from jisoo.models.common.eventbridge import PutEventsRequestEntry
from jisoo.steps.base import Service


class EventBridgeAction(Enum):
    PutRule = "putRule"
    DeleteRule = "deleteRule"
    DescribeRule = "describeRule"
    ListRules = "listRules"
    PutTargets = "putTargets"
    RemoveTargets = "removeTargets"
    ListTargetsByRule = "listTargetsByRule"
    EnableRule = "enableRule"
    DisableRule = "disableRule"
    PutEvents = "putEvents"


class EventBridgePutRuleStep(Service):
    service: ServiceType = Field(ServiceType.EventBridge, frozen=True)
    action: EventBridgeAction = Field(EventBridgeAction.PutRule, frozen=True)
    name: str
    event_pattern: Optional[Dict] = None
    schedule_expression: Optional[str] = None
    state: Optional[str] = None
    description: Optional[str] = None
    role_arn: Optional[str] = None
    tags: Optional[List[Dict[str, str]]] = None


class EventBridgeDeleteRuleStep(Service):
    service: ServiceType = Field(ServiceType.EventBridge, frozen=True)
    action: EventBridgeAction = Field(EventBridgeAction.DeleteRule, frozen=True)
    name: str
    force: Optional[bool] = None


class EventBridgeDescribeRuleStep(Service):
    service: ServiceType = Field(ServiceType.EventBridge, frozen=True)
    action: EventBridgeAction = Field(EventBridgeAction.DescribeRule, frozen=True)
    name: str


class EventBridgeListRulesStep(Service):
    service: ServiceType = Field(ServiceType.EventBridge, frozen=True)
    action: EventBridgeAction = Field(EventBridgeAction.ListRules, frozen=True)
    event_bus_name: Optional[str] = None
    next_token: Optional[str] = None
    limit: Optional[int] = None


class EventBridgePutTargetsStep(Service):
    service: ServiceType = Field(ServiceType.EventBridge, frozen=True)
    action: EventBridgeAction = Field(EventBridgeAction.PutTargets, frozen=True)
    rule: str
    targets: List[Dict]
    event_bus_name: Optional[str] = None


class EventBridgeRemoveTargetsStep(Service):
    service: ServiceType = Field(ServiceType.EventBridge, frozen=True)
    action: EventBridgeAction = Field(EventBridgeAction.RemoveTargets, frozen=True)
    rule: str
    ids: List[str]
    event_bus_name: Optional[str] = None
    force: Optional[bool] = None


class EventBridgeListTargetsByRuleStep(Service):
    service: ServiceType = Field(ServiceType.EventBridge, frozen=True)
    action: EventBridgeAction = Field(EventBridgeAction.ListTargetsByRule, frozen=True)
    rule: str
    event_bus_name: Optional[str] = None
    next_token: Optional[str] = None
    limit: Optional[int] = None


class EventBridgeEnableRuleStep(Service):
    service: ServiceType = Field(ServiceType.EventBridge, frozen=True)
    action: EventBridgeAction = Field(EventBridgeAction.EnableRule, frozen=True)
    name: str
    event_bus_name: Optional[str] = None


class EventBridgeDisableRuleStep(Service):
    service: ServiceType = Field(ServiceType.EventBridge, frozen=True)
    action: EventBridgeAction = Field(EventBridgeAction.DisableRule, frozen=True)
    name: str
    event_bus_name: Optional[str] = None


class EventBridgePutEventsStep(Service):
    service: ServiceType = Field(ServiceType.EventBridge, frozen=True)
    action: EventBridgeAction = Field(EventBridgeAction.PutEvents, frozen=True)
    entries: List[PutEventsRequestEntry] | List[Dict]
