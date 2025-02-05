from jisoo.models.common.services import ServiceType

# ref: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html
# | Integrated Service                  | Request Response      | Run a Job - .sync | Wait for Callback - .waitForTaskToken |
# |-------------------------------------|-----------------------|--------------------|----------------------------------------|
# | Amazon API Gateway                  | Standard & Express    | Not supported       | Standard                               |
# | Amazon Athena                       | Standard & Express    | Standard            | Not supported                           |
# | AWS Batch                           | Standard & Express    | Standard            | Not supported                           |
# | Amazon Bedrock                      | Standard & Express    | Standard            | Standard                               |
# | AWS CodeBuild                       | Standard & Express    | Standard            | Not supported                           |
# | Amazon DynamoDB                     | Standard & Express    | Not supported       | Not supported                           |
# | Amazon ECS/Fargate                 | Standard & Express    | Standard            | Standard                               |
# | Amazon EKS                          | Standard & Express    | Standard            | Standard                               |
# | Amazon EMR                          | Standard & Express    | Standard            | Not supported                           |
# | Amazon EMR on EKS                  | Standard & Express    | Standard            | Not supported                           |
# | Amazon EMR Serverless               | Standard & Express    | Standard            | Not supported                           |
# | Amazon EventBridge                  | Standard & Express    | Not supported       | Standard                               |
# | AWS Glue                            | Standard & Express    | Standard            | Not supported                           |
# | AWS Glue DataBrew                  | Standard & Express    | Standard            | Not supported                           |
# | AWS Lambda                          | Standard & Express    | Not supported       | Standard                               |
# | AWS Elemental MediaConvert         | Standard & Express    | Standard            | Not supported                           |
# | Amazon SageMaker AI                 | Standard & Express    | Standard            | Not supported                           |
# | Amazon SNS                          | Standard & Express    | Not supported       | Standard                               |
# | Amazon SQS                          | Standard & Express    | Not supported       | Standard                               |
# | AWS Step Functions                  | Standard & Express    | Standard            | Standard                               |

INTEGRATION_PATTERN_SUPPORT = {
    ServiceType.APIGateway: ["runTask", "waitForTaskToken"],
    ServiceType.Athena: ["runTask"],
    ServiceType.Batch: ["runTask"],
    ServiceType.Bedrock: ["runTask", "waitForTaskToken"],
    ServiceType.CodeBuild: ["runTask"],
    ServiceType.DynamoDB: [],
    ServiceType.ECS: ["runTask", "waitForTaskToken"],
    ServiceType.EKS: ["runTask", "waitForTaskToken"],
    ServiceType.EMR: ["runTask"],
    ServiceType.EMRonEKS: ["runTask"],
    ServiceType.EMRServerless: ["runTask"],
    ServiceType.EventBridge: ["waitForTaskToken"],
    ServiceType.Glue: ["runTask"],
    ServiceType.GlueDataBrew: ["runTask"],
    ServiceType.Lambda: ["waitForTaskToken"],
    ServiceType.SageMaker: ["runTask"],
    ServiceType.SNS: ["waitForTaskToken"],
    ServiceType.SQS: ["waitForTaskToken"],
    ServiceType.StepFunctions: ["runTask", "waitForTaskToken"],
}
