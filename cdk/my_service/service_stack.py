import getpass
import os
from pathlib import Path

from aws_cdk import Stack, Tags
from constructs import Construct
from git import Repo
from my_service.consumer import TextConsumer  # type: ignore
from my_service.db import DB  # type: ignore
from my_service.producer import InputProducer  # type: ignore

import cdk.my_service.constants as constants


def get_username() -> str:
    try:
        return getpass.getuser().replace('.', '-')
    except Exception:
        return 'github'


def get_stack_name() -> str:
    repo = Repo(Path.cwd())
    username = get_username()
    cicd_environment = os.getenv('ENVIRONMENT', 'dev')
    try:
        branch_name = f'{repo.active_branch}'.replace('/', '-').replace('_', '-')
        return f'{username}-{branch_name}-{constants.SERVICE_NAME}-{cicd_environment}'
    except TypeError:
        # we're running in detached mode (HEAD)
        # see https://github.com/gitpython-developers/GitPython/issues/633
        return f'{username}-{constants.SERVICE_NAME}-{cicd_environment}'


class ServiceStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.id_ = id
        Tags.of(self).add('schedule', constants.SERVICE_NAME)
        Tags.of(self).add('owner', get_username())
        self.db = DB(self, self.shorten_construct_id('DB'))
        self.text_consumer = TextConsumer(self, self.shorten_construct_id('AudioMaker'), self.db.bucket)
        self.input_producer = InputProducer(self, self.shorten_construct_id('Producer'), self.db.bucket)
        self.input_producer.node.add_dependency(self.text_consumer)  # upload files only after producer is ready

    def shorten_construct_id(self, construct_name: str) -> str:
        return f'{self.id_}_{construct_name}'[0:64]
