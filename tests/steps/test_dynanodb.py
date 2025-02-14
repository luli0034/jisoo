from jisoo.steps import (
    Service,
    DynamoDBGetItemStep,
    DynamoDBBatchGetItemStep,
    DynamoDBPutItemStep,
    DynamoDBUpdateItemStep,
    DynamoDBDeleteItemStep,
    DynamoDBBatchWriteItemStep,
    DynamoDBQueryStep,
    DynamoDBScanStep,
)
from jisoo.models.input import StepInput
import pytest
from pydantic import ValidationError


def test_dynamodb_get_item_step():

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
    assert step_dict["Type"] == "Task"
    assert step_dict["Resource"] == "arn:aws:states:::aws-sdk:dynamodb:getItem"
    assert step_dict["Parameters"]["TableName"] == "example"
    assert step_dict["Parameters"]["Key"]["sort_key"]["foo.$"] == "$.bar"
    assert step_dict["Parameters"]["Key"]["sort_key"]["foo2.$"] == "$.bar2"
    assert step_dict["Parameters"]["Key"]["sort_key"]["foo3"] == "bar3"
    assert step_dict["Parameters"]["ConsistentRead"] == True
    assert step_dict["Parameters"]["ReturnConsumedCapacity"] == "TOTAL"
    assert step_dict["Parameters"]["ProjectionExpression.$"] == "$.input_key"
    assert step_dict["Parameters"]["ExpressionAttributeNames"] == {"key": "value"}

    with pytest.raises(ValidationError):
        DynamoDBGetItemStep(
            table_name="example",
            key={"key": {"key": "value"}},
            consistent_read=True,
            return_consumed_capacity="TOTAL",
            projection_expression="example",
        )

    with pytest.raises(ValueError):
        DynamoDBGetItemStep(
            id="example",
            integration_pattern="runTask",
            table_name="example",
            key={"key": {"key": "value"}},
            consistent_read=True,
            return_consumed_capacity="TOTAL",
            projection_expression="example",
            expression_attribute_names={"key": "value"},
        )

    with pytest.raises(ValueError):
        DynamoDBGetItemStep(
            id="example",
            table_name="example",
            key={"key": {"key": "value"}},
            consistent_read=True,
            return_consumed_capacity="TOTAL",
            projection_expression="example",
            expression_attribute_names={"key": "value"},
            integration_pattern="runTask",
        )


def test_dynamodb_batch_get_item_step():

    batch_get_item_step = DynamoDBBatchGetItemStep(
        id="example",
        integration_type="aws-sdk",
        request_items={
            "item_1": {
                "AttributesToGet": ["string"],
                "ConsistentRead": True,
                "ExpressionAttributeNames": {"string": "string"},
                "Keys": [{"string": {"S": "string"}}],
                "ProjectionExpression": "string",
            }
        },
        return_consumed_capacity="TOTAL",
    )
    step_dict = batch_get_item_step.to_dict()

    assert step_dict["Type"] == "Task"
    assert step_dict["Resource"] == "arn:aws:states:::aws-sdk:dynamodb:batchGetItem"
    assert step_dict["Parameters"]["ReturnConsumedCapacity"] == "TOTAL"

    with pytest.raises(ValueError):
        DynamoDBBatchGetItemStep(
            id="example",
            integration_pattern="runTask",
            request_items={
                "item_1": {
                    "AttributesToGet": ["string"],
                    "ConsistentRead": True,
                    "ExpressionAttributeNames": {"string": "string"},
                    "Keys": [{"string": {"S": "string"}}],
                    "ProjectionExpression": "string",
                }
            },
            return_consumed_capacity="TOTAL",
        )


def test_dynanodb_put_item_step():

    put_item_step = DynamoDBPutItemStep(
        id="example",
        table_name="example",
        integration_type="aws-sdk",
        item={"key": {"key": "value"}},
        return_consumed_capacity="TOTAL",
        return_item_collection_metrics="SIZE",
        condition_expression="example",
        expression_attribute_names={"key": "value"},
        expression_attribute_values={"key": {"key": "value"}},
    )
    step_dict = put_item_step.to_dict()

    assert step_dict["Type"] == "Task"
    assert step_dict["Resource"] == "arn:aws:states:::aws-sdk:dynamodb:putItem"
    assert step_dict["Parameters"]["TableName"] == "example"
    assert step_dict["Parameters"]["Item"] == {"key": {"key": "value"}}
    assert step_dict["Parameters"]["ReturnConsumedCapacity"] == "TOTAL"
    assert step_dict["Parameters"]["ReturnItemCollectionMetrics"] == "SIZE"
    assert step_dict["Parameters"]["ConditionExpression"] == "example"
    assert step_dict["Parameters"]["ExpressionAttributeNames"] == {"key": "value"}
    assert step_dict["Parameters"]["ExpressionAttributeValues"] == {
        "key": {"key": "value"}
    }


def test_dynamodb_update_item_step():

    update_item_step = DynamoDBUpdateItemStep(
        id="example",
        table_name="example",
        integration_type="aws-sdk",
        key={"key": {"key": "value"}},
        update_expression="example",
        return_consumed_capacity="TOTAL",
        return_item_collection_metrics="SIZE",
        condition_expression="example",
        expression_attribute_names={"key": "value"},
        expression_attribute_values={"key": {"key": "value"}},
    )
    step_dict = update_item_step.to_dict()

    assert step_dict["Type"] == "Task"
    assert step_dict["Resource"] == "arn:aws:states:::aws-sdk:dynamodb:updateItem"
    assert step_dict["Parameters"]["TableName"] == "example"
    assert step_dict["Parameters"]["Key"] == {"key": {"key": "value"}}
    assert step_dict["Parameters"]["UpdateExpression"] == "example"
    assert step_dict["Parameters"]["ReturnConsumedCapacity"] == "TOTAL"
    assert step_dict["Parameters"]["ReturnItemCollectionMetrics"] == "SIZE"
    assert step_dict["Parameters"]["ConditionExpression"] == "example"
    assert step_dict["Parameters"]["ExpressionAttributeNames"] == {"key": "value"}
    assert step_dict["Parameters"]["ExpressionAttributeValues"] == {
        "key": {"key": "value"}
    }


def test_dynamodb_delete_item_step():

    delete_item_step = DynamoDBDeleteItemStep(
        id="example",
        table_name="example",
        integration_type="aws-sdk",
        key={"key": {"key": "value"}},
        return_consumed_capacity="TOTAL",
        return_item_collection_metrics="SIZE",
        condition_expression="example",
        expression_attribute_names={"key": "value"},
        expression_attribute_values={"key": {"key": "value"}},
    )
    step_dict = delete_item_step.to_dict()

    assert step_dict["Type"] == "Task"
    assert step_dict["Resource"] == "arn:aws:states:::aws-sdk:dynamodb:deleteItem"
    assert step_dict["Parameters"]["TableName"] == "example"
    assert step_dict["Parameters"]["Key"] == {"key": {"key": "value"}}
    assert step_dict["Parameters"]["ReturnConsumedCapacity"] == "TOTAL"
    assert step_dict["Parameters"]["ReturnItemCollectionMetrics"] == "SIZE"
    assert step_dict["Parameters"]["ConditionExpression"] == "example"
    assert step_dict["Parameters"]["ExpressionAttributeNames"] == {"key": "value"}
    assert step_dict["Parameters"]["ExpressionAttributeValues"] == {
        "key": {"key": "value"}
    }


def test_dynamodb_batch_write_item_step():

    batch_write_item_step = DynamoDBBatchWriteItemStep(
        id="example",
        integration_type="aws-sdk",
        request_items={
            "item_1": [
                {
                    "PutRequest": {
                        "Item": {"key": {"key": "value"}},
                    }
                }
            ]
        },
        return_consumed_capacity="TOTAL",
        return_item_collection_metrics="SIZE",
    )
    step_dict = batch_write_item_step.to_dict()

    assert step_dict["Type"] == "Task"
    assert step_dict["Resource"] == "arn:aws:states:::aws-sdk:dynamodb:batchWriteItem"
    assert step_dict["Parameters"]["ReturnConsumedCapacity"] == "TOTAL"
    assert step_dict["Parameters"]["ReturnItemCollectionMetrics"] == "SIZE"


def test_dynamodb_query_step():

    query_step = DynamoDBQueryStep(
        id="example",
        table_name="example",
        integration_type="aws-sdk",
        conditional_operator="example",
        return_consumed_capacity="TOTAL",
        projection_expression="example",
        expression_attribute_names={"key": "value"},
        expression_attribute_values={"key": {"key": "value"}},
        index_name="example",
        limit=10,
        consistent_read=True,
        scan_index_forward=True,
        select="ALL_ATTRIBUTES",
    )
    step_dict = query_step.to_dict()

    assert step_dict["Type"] == "Task"
    assert step_dict["Resource"] == "arn:aws:states:::aws-sdk:dynamodb:query"
    assert step_dict["Parameters"]["TableName"] == "example"
    assert step_dict["Parameters"]["ConditionalOperator"] == "example"
    assert step_dict["Parameters"]["ReturnConsumedCapacity"] == "TOTAL"
    assert step_dict["Parameters"]["ProjectionExpression"] == "example"
    assert step_dict["Parameters"]["ExpressionAttributeNames"] == {"key": "value"}
    assert step_dict["Parameters"]["ExpressionAttributeValues"] == {
        "key": {"key": "value"}
    }
    assert step_dict["Parameters"]["IndexName"] == "example"
    assert step_dict["Parameters"]["Limit"] == 10
    assert step_dict["Parameters"]["Select"] == "ALL_ATTRIBUTES"


def test_dynamodb_scan_step():

    scan_step = DynamoDBScanStep(
        id="example",
        table_name="example",
        integration_type="aws-sdk",
        return_consumed_capacity="TOTAL",
        projection_expression="example",
        expression_attribute_names={"key": "value"},
        expression_attribute_values={"key": {"key": "value"}},
        index_name="example",
        limit=10,
        select="ALL_ATTRIBUTES",
    )
    step_dict = scan_step.to_dict()

    assert step_dict["Type"] == "Task"
    assert step_dict["Resource"] == "arn:aws:states:::aws-sdk:dynamodb:scan"
    assert step_dict["Parameters"]["TableName"] == "example"
    assert step_dict["Parameters"]["ReturnConsumedCapacity"] == "TOTAL"
    assert step_dict["Parameters"]["ProjectionExpression"] == "example"
    assert step_dict["Parameters"]["ExpressionAttributeNames"] == {"key": "value"}
    assert step_dict["Parameters"]["ExpressionAttributeValues"] == {
        "key": {"key": "value"}
    }
    assert step_dict["Parameters"]["IndexName"] == "example"
    assert step_dict["Parameters"]["Limit"] == 10
    assert step_dict["Parameters"]["Select"] == "ALL_ATTRIBUTES"
