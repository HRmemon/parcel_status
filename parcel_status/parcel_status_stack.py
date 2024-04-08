from os import path
from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_events as events,
    aws_events_targets as targets,
    Duration,
    RemovalPolicy,
    aws_ses as ses,
    aws_iam as iam

)
from constructs import Construct


class ParcelStatusStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # labda layer
        lambda_layer = _lambda.LayerVersion(
            self, "LambdaLayer",
            code=_lambda.Code.from_asset(
                'lambda-layers',
            ),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12]
        )

        # Parcel Status Lambda
        parcel_status_lambda = _lambda.Function(
            self, "ParcelStatusLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="get_parcel.lambda_handler",
            # install requirements.txt
            code=_lambda.Code.from_asset(
                'lambda',
            ),
            layers=[lambda_layer],
            environment={
                "LOG_LEVEL": "INFO"
            },
            timeout=Duration.seconds(7)
        )

        # grant permission to lambda to write to dynamodb
        parcel_status_lambda.add_to_role_policy(
            statement=iam.PolicyStatement(
                actions=["ses:SendEmail", "ses:SendRawEmail", ],
                resources=["*"]
            )
        )

        # schedule lambda
        events.Rule(
            self, "ScheduleRule",
            schedule=events.Schedule.rate(
                Duration.hours(1)
            ),
            targets=[
                targets.LambdaFunction(
                    parcel_status_lambda
                )
            ]
        )

        # SES sending email
        # identity email is awsforhassan@gmail.com without domain
