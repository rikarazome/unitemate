import json
import os

import boto3
from pydantic import BaseModel, ValidationError

dynamodb = boto3.resource("dynamodb")
queue = dynamodb.Table(os.environ["MATCH_QUEUE"])


class DequeueModel(BaseModel):
    namespace: str = "default"
    user_id: str


def handle(event, _):
    try:
        model = DequeueModel(**json.loads(event["body"]))
    except ValidationError as e:
        return {"statusCode": 422, "body": e.json()}

    queue.delete_item(Key=model.model_dump())
    return {"statusCode": 200, "body": None}
