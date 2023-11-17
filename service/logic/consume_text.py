from pathlib import Path

import boto3

from service.dal.polly_handler import PollyWrapper
from service.handlers.utils.observability import logger
from service.logic.email import send_binary_file


def consume_text() -> None:
    polly_wrapper = PollyWrapper()
    current_path = Path(__file__).parent.parent.parent
    text_file_path = current_path / ('text/sample.txt')
    file_contents = text_file_path.read_text().replace('\n', ' ')
    audio_stream, _ = polly_wrapper.synthesize(text=file_contents, engine='neural', voice='Ruth', audio_format='mp3')
    with open('sample.mp3', 'wb') as f:
        f.write(audio_stream.read())


def consume_text_async(bucket_name: str, object_key: str) -> None:
    # read text file
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket_name, Key=object_key)
    text: str = obj['Body'].read().decode('utf-8').replace('\n', '')
    logger.info(f'working on object {object_key} in the bucket {bucket_name}')
    polly_wrapper = PollyWrapper()
    (
        audio_stream,
        _,
    ) = polly_wrapper.do_synthesis_task(
        text=text,
        engine='neural',
        voice='Danielle',
        audio_format='mp3',
        s3_bucket=bucket_name,
    )
    send_binary_file(audio_stream.read())
