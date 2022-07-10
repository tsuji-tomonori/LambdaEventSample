from __future__ import annotations

from typing import Any, NamedTuple
import os
import logging
import json

import boto3


logger = logging.getLogger()
logger.setLevel("INFO")


class AwsBase:
    def __init__(self, profile: str | None = None) -> None:
        if profile:
            self.session = boto3.Session(profile_name=profile)
        else:
            self.session = boto3.Session()


class Dynamodb(AwsBase):
    def __init__(self, profile: str | None = None) -> None:
        super().__init__(profile)
        self.dynamodb = self.session.resource("dynamodb")

    def get_item(self, table_name: str, pkey: str) -> Any:
        table = self.dynamodb.Table(table_name)
        return table.get_item(
            Key={"pkey": pkey},
        )["Item"]


class LambdaEnviron(NamedTuple):
    DB_NAME: str

    @classmethod
    def of(cls) -> LambdaEnviron:
        return LambdaEnviron(**{k: os.environ[k] for k in LambdaEnviron._fields})


class LambdaHandler(NamedTuple):
    lambda_env: LambdaEnviron
    db: Dynamodb
    pkey: dict[str, Any]

    @classmethod
    def of(cls, event) -> LambdaHandler:
        return LambdaHandler(
            lambda_env=LambdaEnviron.of(),
            db=Dynamodb(event.get("profile")),
            pkey=event["pkey"],
        )

    def service(self) -> None:
        item = self.db.get_item(self.lambda_env.DB_NAME, self.pkey)
        logger.info(json.dumps(item, indent=2))

    def __call__(self) -> None:
        return self.service()


def lambda_handler(event, context):
    try:
        handler = LambdaHandler.of(event=event)
        handler()
        return 200
    except:
        logger.exception("Not Retry Error!")
        return 400
