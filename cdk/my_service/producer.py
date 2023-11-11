from pathlib import Path

from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3_deploy
from constructs import Construct

from cdk.my_service.constants import DEST_KEY_PREFIX


class InputProducer(Construct):
    def __init__(self, scope: Construct, id_: str, bucket: s3.Bucket) -> None:
        super().__init__(scope, id_)
        self.id_ = id_
        self._upload_s3_objects(bucket)

    def _upload_s3_objects(self, destination_bucket: s3.Bucket) -> None:
        current_path = Path(__file__).parent.parent.parent  # root folder
        text_folder = current_path / ('text/')
        s3_deploy.BucketDeployment(
            self,
            f'{self.id_}PostDeployment',
            sources=[s3_deploy.Source.asset(str(text_folder))],
            destination_bucket=destination_bucket,
            prune=True,
            destination_key_prefix=DEST_KEY_PREFIX,
        )
