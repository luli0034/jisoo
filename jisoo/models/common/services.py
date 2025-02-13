from enum import Enum


class ServiceType(str, Enum):
    APIGateway = "apigateway"
    Athena = "athena"
    Batch = "batch"
    Bedrock = "bedrock"
    CodeBuild = "codebuild"
    DynamoDB = "dynamodb"
    ECS = "ecs"
    EKS = "eks"
    EMR = "emr"
    EMRonEKS = "emr-containers"
    EMRServerless = "emr-serverless"
    EventBridge = "events"
    Glue = "glue"
    GlueDataBrew = "databrew"
    Lambda = "lambda"
    SageMaker = "sagemaker"
    SNS = "sns"
    SQS = "sqs"
    StepFunctions = "states"


# reference https://docs.aws.amazon.com/step-functions/latest/dg/supported-services-awssdk.html#supported-services-awssdk-list
INTEGRATION_SDK_RESOURCES = {
    ServiceType.APIGateway: "apigateway",
    ServiceType.Athena: "athena",
    ServiceType.Batch: "batch",
    ServiceType.Bedrock: "bedrock",
    ServiceType.CodeBuild: "codebuild",
    ServiceType.DynamoDB: "dynamodb",
    ServiceType.ECS: "ecs",
    ServiceType.EKS: "eks",
    ServiceType.EMR: "emr",
    ServiceType.EMRonEKS: "emrcontainers",
    ServiceType.EMRServerless: "emrserverless",
    ServiceType.EventBridge: "eventbridge",
    ServiceType.Glue: "glue",
    ServiceType.GlueDataBrew: "databrew",
    ServiceType.Lambda: "lambda",
    ServiceType.SageMaker: "sagemaker",
    ServiceType.SNS: "sns",
    ServiceType.SQS: "sqs",
    ServiceType.StepFunctions: "sfn",
}
