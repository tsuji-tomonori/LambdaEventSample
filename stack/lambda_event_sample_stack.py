from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    aws_logs as logs,
)
from constructs import Construct


def resource_name(resource_type: str) -> str:
    return f"{resource_type}_LambdaEventSample_cdk"


class LambdaEventSampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = iam.Role(
            self, resource_name("rol"),
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole")
            ],
            role_name=resource_name("rol"),
        )

        fn = lambda_.Function(
            self, resource_name("lmd"),
            code=lambda_.AssetCode.from_asset("src"),
            handler="lambda_function.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            function_name=resource_name("lmd"),
            timeout=Duration.seconds(30),
            memory_size=256,
            role=role
        )

        table = dynamodb.Table(
            self, resource_name("dyn"),
            billing_mode=dynamodb.BillingMode.PROVISIONED,
            partition_key=dynamodb.Attribute(
                name="pkey", type=dynamodb.AttributeType.STRING),
            read_capacity=1,
            write_capacity=1,
            table_name=resource_name("dyn")
        )
        table.grant_read_data(role)
        fn.add_environment(
            key="DB_NAME",
            value=table.table_name,
        )

        loggroup_name = f"/aws/lambda/{fn.function_name}"
        logs.LogGroup(
            self, resource_name("log"),
            log_group_name=loggroup_name,
            retention=logs.RetentionDays.ONE_DAY,
        )
