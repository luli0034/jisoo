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
