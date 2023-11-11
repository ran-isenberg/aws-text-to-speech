from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

import boto3

from service.handlers.utils.observability import logger


def send_binary_file(data: bytes):
    # Replace these with your own values
    sender_email = 'ran.isenberg@ranthebuilder.cloud'
    recipient_email = 'ran.isenberg@ranthebuilder.cloud'

    # Create a multipart/mixed message object
    msg = MIMEMultipart()
    msg['Subject'] = 'Your Binary Attachment'
    msg['From'] = sender_email
    msg['To'] = recipient_email
    logger.info('sending email')
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(data)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename='audio.mp3')
    msg.attach(attachment)
    # Convert message to string and send
    ses_client = boto3.client(
        'ses',
    )
    ses_client.send_raw_email(
        Source=sender_email,
        Destinations=[recipient_email],
        RawMessage={'Data': msg.as_string()},
    )
    logger.info('finished')
