from jisoo.models.common.base import BaseErrors


class LambdaErrorEqualsEnum(BaseErrors):
    # reference: https://docs.aws.amazon.com/lambda/latest/api/API_Invoke.html#API_Invoke_Errors
    ServiceException = "Lambda.ServiceException"
    AWSLambdaException = "Lambda.AWSLambdaException"
    SdkClientException = "Lambda.SdkClientException"
    ClientExecutionTimeoutException = "Lambda.ClientExecutionTimeoutException"
    TooManyRequestsException = "Lambda.TooManyRequestsException"
