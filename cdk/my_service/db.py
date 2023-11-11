from aws_cdk import RemovalPolicy
from aws_cdk import aws_s3 as s3
from constructs import Construct


class DB(Construct):
    def __init__(self, scope: Construct, id_: str) -> None:
        super().__init__(scope, id_)
        self.id_ = id_
        self.bucket = self._create_bucket()

    def _create_bucket(self) -> s3.Bucket:
        return s3.Bucket(
            self,
            f'{self.id_}PollyBucket',
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
