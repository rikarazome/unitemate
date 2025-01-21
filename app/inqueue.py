import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import boto3
from pydantic import BaseModel, ValidationError, field_serializer

dynamodb = boto3.resource("dynamodb")
queue = dynamodb.Table(os.environ["MATCH_QUEUE"])


class InqueueModel(BaseModel):
    namespace: str = "default"
    user_id: str
    rate: int
    inqueued_unixtime: datetime = datetime.now(ZoneInfo("Asia/Tokyo")).replace(microsecond=0)

    @field_serializer("inqueued_unixtime")
    def serialize_inqueued_unixtime(self, inqueued_unixtime: datetime) -> int:
        return int(inqueued_unixtime.timestamp())


def handle(event, _):
    # バリデーションチェック
    try:
        model = InqueueModel(**json.loads(event["body"]))
    except ValidationError as e:
        return {"statusCode": 422, "body": e.json()}

    queue.put_item(Item=model.model_dump())
    return {"statusCode": 200, "body": None}
