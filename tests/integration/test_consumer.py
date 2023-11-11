from typing import Any, Dict

# from service.handlers.consumer import start
# from tests.utils import generate_context


def generate_event() -> Dict[str, Any]:
    return {
        'Records': [
            {
                'eventVersion': '2.1',
                'eventSource': 'aws:s3',
                'awsRegion': 'us-east-1',
                'eventTime': '2023-05-03T18:59:44.899Z',
                'eventName': 'ObjectCreated:Put',
                'userIdentity': {'principalId': 'AWS:AROAVVU4MKNOYNQ4XK3X6:root-polly-tYDSecegEybl'},
                'requestParameters': {'sourceIPAddress': '54.44.17.170'},
                'responseElements': {
                    'x-amz-request-id': '466PYXR74X9P5JGH',
                    'x-amz-id-2': 'hJyrb3865TCRR8gS3bw3TbA6gy53zn3fjj323ZW/339b0ERsZUCoNTYOA+',
                },
                's3': {
                    's3SchemaVersion': '1.0',
                    'configurationId': 'ZWVmZDU0ZGYtZDkxOS00MGQxLTlhM2QtNTFhYTc0NTg0ZGY2',
                    'bucket': {
                        'name': 'root-polly-polly-rootpollb-lchrizjciyc',
                        'ownerIdentity': {'principalId': 'A2G6MV2NMHUMK5'},
                        'arn': 'arn:aws:s3:::root-polly-polly-rootpollb-lchrizjciyct',
                    },
                    'object': {
                        'key': 'input/sample.txt',
                        'size': 10220,
                        'eTag': '2d9f1d19904b369348683ab891835a2e',
                        'sequencer': '006452AF20D855DE8D',
                    },
                },
            }
        ]
    }


def test_consumer_success() -> None:
    return
    # run locally
    # start(generate_event(), generate_context())
