from typing import Any, Dict, List

import boto3
from aws_lambda_powertools.utilities.parser import parse
from aws_lambda_powertools.utilities.parser.models import S3Model, S3RecordModel
from aws_lambda_powertools.utilities.typing import LambdaContext

from service.handlers.schemas.env_vars import ConsumerEnvVars
from service.handlers.utils.env_vars_parser import get_environment_variables, init_environment_variables
from service.handlers.utils.observability import logger, tracer
from service.logic.consume_text import consume_text_async


@init_environment_variables(model=ConsumerEnvVars)
@tracer.capture_lambda_handler(capture_response=False)
def start(event: Dict[str, Any], context: LambdaContext) -> None:
    logger.set_correlation_id(context.aws_request_id)
    logger.info('starting to handle text processor event')

    env_vars: ConsumerEnvVars = get_environment_variables(model=ConsumerEnvVars)
    logger.debug('environment variables', extra=env_vars.dict())
    parsed_input: S3Model = parse(event=event, model=S3Model)
    records: List[S3RecordModel] = parsed_input.Records
    s3 = boto3.client('s3')
    for record in records:
        bucket_name = record.s3.bucket.name
        object_key = record.s3.object.key
        # read text file
        obj = s3.get_object(Bucket=bucket_name, Key=object_key)
        text: str = obj['Body'].read().decode('utf-8').replace('\n', '')
        logger.info(f'working on object {object_key} in the bucket {bucket_name}')
        consume_text_async(text, bucket_name)
    logger.info('finished handling text processor event')
