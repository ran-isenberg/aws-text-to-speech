from aws_cdk import Duration, RemovalPolicy, aws_s3_notifications
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_s3 as s3
from aws_cdk.aws_lambda_python_alpha import PythonLayerVersion
from aws_cdk.aws_logs import RetentionDays
from constructs import Construct

from cdk.my_service import constants
from cdk.my_service.constants import DEST_KEY_PREFIX


class TextConsumer(Construct):
    def __init__(self, scope: Construct, id_: str, bucket: s3.Bucket) -> None:
        super().__init__(scope, id_)
        self.id_ = id_
        self.function = self._create_target_lambda(bucket)

    def _build_common_layer(self) -> PythonLayerVersion:
        return PythonLayerVersion(
            self,
            constants.LAMBDA_LAYER_NAME,
            entry=constants.COMMON_LAYER_BUILD_FOLDER,
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            removal_policy=RemovalPolicy.DESTROY,
        )

    def _create_target_lambda(self, bucket: s3.Bucket) -> _lambda.Function:
        lambda_layer = self._build_common_layer()
        role = iam.Role(
            self,
            f'{self.id_}consumer',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            inline_policies={
                'ses': iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=['ses:SendRawEmail'],
                            resources=['*'],
                            effect=iam.Effect.ALLOW,
                        )
                    ]
                ),
                's3': iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=['s3:GetObject', 's3:DeleteObject', 's3:ListBucket', 's3:PutObject'],
                            resources=[bucket.bucket_arn, f'{bucket.bucket_arn}/*'],
                            effect=iam.Effect.ALLOW,
                        ),
                    ]
                ),
                'polly': iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=['polly:StartSpeechSynthesisTask', 'polly:SynthesizeSpeech', 'polly:GetSpeechSynthesisTask'],
                            resources=['*'],
                            effect=iam.Effect.ALLOW,
                        ),
                    ],
                ),
            },
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name=('service-role/AWSLambdaBasicExecutionRole'))],
        )
        function = _lambda.Function(
            self,
            f'{self.id_}TextConsumer',
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset('.build/lambdas/'),
            handler='service.handlers.consumer.start',
            environment={
                'POWERTOOLS_SERVICE_NAME': 'cron',  # for logger, tracer and metrics
                'LOG_LEVEL': 'DEBUG',  # for logger
                'BUCKET_NAME': bucket.bucket_name,
            },
            tracing=_lambda.Tracing.ACTIVE,
            retry_attempts=0,
            timeout=Duration.minutes(10),
            memory_size=512,
            layers=[lambda_layer],
            role=role,
            log_retention=RetentionDays.ONE_DAY,
        )

        # Set up an S3 event trigger for the Lambda function
        trigger = aws_s3_notifications.LambdaDestination(function)
        bucket.add_event_notification(s3.EventType.OBJECT_CREATED, trigger, s3.NotificationKeyFilter(prefix=DEST_KEY_PREFIX))
        return function
