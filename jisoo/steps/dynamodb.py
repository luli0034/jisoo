from jisoo.steps.base import Service
from jisoo.models.common import ServiceType
from enum import Enum
from pydantic import Field
from typing import Optional, Dict, List

# Follow the Amazon DynamoDB API Reference
# https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Operations_Amazon_DynamoDB.html


class DynamoDBAction(Enum):
    GetItem = "getItem"
    PutItem = "putItem"
    UpdateItem = "updateItem"
    DeleteItem = "deleteItem"
    Query = "query"
    Scan = "scan"
    BatchGetItem = "batchGetItem"
    BatchWriteItem = "batchWriteItem"


class DynamoDBGetItemStep(Service):
    service: ServiceType = Field(ServiceType.DynamoDB, frozen=True)
    action: DynamoDBAction = Field(DynamoDBAction.GetItem, frozen=True)
    table_name: str
    key: Dict[str, Dict[str, str]]
    consistent_read: Optional[bool] = None
    return_consumed_capacity: Optional[str] = None
    projection_expression: Optional[str] = None
    expression_attribute_names: Optional[Dict[str, str]] = None


class DynamoDBPutItemStep(Service):
    service: ServiceType = Field(ServiceType.DynamoDB, frozen=True)
    action: DynamoDBAction = Field(DynamoDBAction.PutItem, frozen=True)
    table_name: str
    item: Dict[str, Dict[str, str]]
    condition_expression: Optional[str] = None
    expression_attribute_names: Optional[Dict[str, str]] = None
    expression_attribute_values: Optional[Dict[str, Dict[str, str]]] = None
    return_consumed_capacity: Optional[str] = None
    return_item_collection_metrics: Optional[str] = None


class DynamoDBUpdateItemStep(Service):
    service: ServiceType = Field(ServiceType.DynamoDB, frozen=True)
    action: DynamoDBAction = Field(DynamoDBAction.UpdateItem, frozen=True)
    table_name: str
    key: Dict[str, Dict[str, str]]
    update_expression: str
    condition_expression: Optional[str] = None
    expression_attribute_names: Optional[Dict[str, str]] = None
    expression_attribute_values: Optional[Dict[str, Dict[str, str]]] = None
    return_consumed_capacity: Optional[str] = None
    return_item_collection_metrics: Optional[str] = None


class DynamoDBDeleteItemStep(Service):
    service: ServiceType = Field(ServiceType.DynamoDB, frozen=True)
    action: DynamoDBAction = Field(DynamoDBAction.DeleteItem, frozen=True)
    table_name: str
    key: Dict[str, Dict[str, str]]
    condition_expression: Optional[str] = None
    expression_attribute_names: Optional[Dict[str, str]] = None
    expression_attribute_values: Optional[Dict[str, Dict[str, str]]] = None
    return_consumed_capacity: Optional[str] = None
    return_item_collection_metrics: Optional[str] = None


class DynamoDBQueryStep(Service):
    service: ServiceType = Field(ServiceType.DynamoDB, frozen=True)
    action: DynamoDBAction = Field(DynamoDBAction.Query, frozen=True)
    table_name: str
    index_name: Optional[str] = None
    select: Optional[str] = None
    attributes_to_get: Optional[List[str]] = None
    limit: Optional[int] = None
    consistent_read: Optional[bool] = None
    key_conditions: Optional[Dict[str, Dict[str, List[Dict[str, str]]]]] = None
    query_filter: Optional[Dict[str, Dict[str, List[Dict[str, str]]]]] = None
    conditional_operator: Optional[str] = None
    scan_index_forward: Optional[bool] = None
    exclusive_start_key: Optional[Dict[str, Dict[str, str]]] = None
    return_consumed_capacity: Optional[str] = None
    projection_expression: Optional[str] = None
    filter_expression: Optional[str] = None
    expression_attribute_names: Optional[Dict[str, str]] = None
    expression_attribute_values: Optional[Dict[str, Dict[str, str]]] = None


class DynamoDBScanStep(Service):
    service: ServiceType = Field(ServiceType.DynamoDB, frozen=True)
    action: DynamoDBAction = Field(DynamoDBAction.Scan, frozen=True)
    table_name: str
    index_name: Optional[str] = None
    attributes_to_get: Optional[List[str]] = None
    limit: Optional[int] = None
    select: Optional[str] = None
    scan_filter: Optional[Dict[str, Dict[str, List[Dict[str, str]]]]] = None
    conditional_operator: Optional[str] = None
    exclusive_start_key: Optional[Dict[str, Dict[str, str]]] = None
    return_consumed_capacity: Optional[str] = None
    total_segments: Optional[int] = None
    segment: Optional[int] = None
    projection_expression: Optional[str] = None
    filter_expression: Optional[str] = None
    expression_attribute_names: Optional[Dict[str, str]] = None
    expression_attribute_values: Optional[Dict[str, Dict[str, str]]] = None


class DynamoDBBatchGetItemStep(Service):
    service: ServiceType = Field(ServiceType.DynamoDB, frozen=True)
    action: DynamoDBAction = Field(DynamoDBAction.BatchGetItem, frozen=True)
    request_items: Dict
    return_consumed_capacity: Optional[str] = None


class DynamoDBBatchWriteItemStep(Service):
    service: ServiceType = Field(ServiceType.DynamoDB, frozen=True)
    action: DynamoDBAction = Field(DynamoDBAction.BatchWriteItem, frozen=True)
    request_items: Dict
    return_consumed_capacity: Optional[str] = None
    return_item_collection_metrics: Optional[str] = None
