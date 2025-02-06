from jisoo.steps import LambdaInvokeStep, DynamoDBGetItemStep


lambda_invoke = LambdaInvokeStep(
    function_name="example",
    id="example",
    integration_pattern="waitForTaskToken",
    integration_type="aws-sdk",
    input_path="$.input",
    payload={
        "${STATUS_TABLE_PARTITION_KEY}": {"S.$": "$.${CONSUMER_OUTPUT_KEY_DATASET_ID}"},
        "${STATUS_TABLE_SORT_KEY}": {"S.$": "$.${CONSUMER_OUTPUT_KEY_OBJECT_KEY}"},
    },
)
state_dict = lambda_invoke.to_dict()
# print(state_dict)
dynamodb_get_item = DynamoDBGetItemStep(
    table_name="example",
    id="example",
    integration_pattern="waitForTaskToken",
    integration_type="aws-sdk",
    key={
        "${STATUS_TABLE_PARTITION_KEY}": {"S.$": "$.${CONSUMER_OUTPUT_KEY_DATASET_ID}"},
        "${STATUS_TABLE_SORT_KEY}": {"S.$": "$.${CONSUMER_OUTPUT_KEY_OBJECT_KEY}"},
    },
)
state_dict = dynamodb_get_item.to_dict()
print(state_dict)
