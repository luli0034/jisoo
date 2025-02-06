terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "ap-northeast-1"
}

locals {
  state_machine_defniition = templatefile("${path.module}/definition.json", {
    LAMBDA_FUNCTION_NAME                = "mock_lambda_function",
    ECS_CLUSTER_BATCH_INGESTION         = "mock_ecs_cluster",
    ECS_TASK_DEFINITION_BATCH_INGESTION = "mock_ecs_task_definition",
    CONSUMER_OUTPUT_KEY_ITEMS_KEY       = "items",
    TASK_PRIVATE_SUBNET_1               = "subnet-12345678",
    TASK_PRIVATE_SUBNET_2               = "subnet-23456789",
    TASK_PRIVATE_SUBNET_3               = "subnet-34567890",
    ECS_TASK_NAME                       = "mock_ecs_task_name",
  })
}

output "state_machine_definition" {
  value = local.state_machine_defniition

}

# cd examples/terraform
# terraform init
# terraform apply -auto-approve
