import json
import os

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
queue = dynamodb.Table(os.environ["MATCH_QUEUE"])


def handle(event, context):
    response_body = {
        "queue_count": get_inqueued_user_count(),  # マッチキューの待ち人数
    }
    return {"statusCode": 200, "body": json.dumps(response_body)}


def get_inqueued_user_count():
    response1 = queue.query(
        Select="COUNT",
        KeyConditionExpression=Key("namespace").eq("default"),
    )
    response2 = queue.query(
        Select="COUNT",
        KeyConditionExpression=Key("namespace").eq("default") & Key("user_id").eq("#meta#"),
    )
    return response1["Count"] - response2["Count"]
