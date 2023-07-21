from typing import Any, Dict, List

from aws_lambda_env_modeler import get_environment_variables, init_environment_variables
from aws_lambda_powertools.utilities.parser import parse
from aws_lambda_powertools.utilities.parser.models import S3Model, S3RecordModel
from aws_lambda_powertools.utilities.typing import LambdaContext

from service.handlers.schemas.env_vars import ConsumerEnvVars
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
    for record in records:
        bucket_name = record.s3.bucket.name
        object_key = record.s3.object.key
        consume_text_async(bucket_name, object_key)
    logger.info('finished handling text processor event')
