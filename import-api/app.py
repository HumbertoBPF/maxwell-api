import json
import boto3
from jsonschema import validate
from jsonschema.exceptions import ValidationError

client = boto3.client('dynamodb')

schema = {
    "type": "object",
    "properties": {
        "table": {
            "type": "string",
            "minLength": 1
        },
        "start_key": {
            "type": "object",
            "properties": {
                "table": {
                    "type": "object",
                    "properties": {
                        "S": {
                            "type": "string",
                            "minLength": 1
                        }
                    },
                    "required": ["S"],
                },
                "id": {
                    "type": "object",
                    "properties": {
                        "S": {
                            "type": "string",
                            "minLength": 1
                        }
                    },
                    "required": ["S"],
                },
            },
            "required": ["table", "id"],
        },
    },
    "required": ["table"],
}


def get_api_items(dynamodb_items):
    api_items = []

    for dynamodb_item in dynamodb_items:
        api_item = {}

        for key, value in dynamodb_item.items():
            api_item[key] = value.get("S")

        api_items.append(api_item)

    return api_items


def lambda_handler(event, context):
    data = event.get("body")
    headers = event.get("headers", {})
    content_type = headers.get("Content-Type")

    if (data is not None) and (content_type == "application/json"):
        data_json = json.loads(data)

        try:
            validate(instance=data_json, schema=schema)

            table = data_json["table"]
            start_key = data_json.get("start_key")

            if start_key is None:
                response = client.query(
                    ExpressionAttributeNames={
                        '#t': "table"
                    },
                    ExpressionAttributeValues={
                        ':table': {
                            'S': table,
                        }
                    },
                    KeyConditionExpression='#t = :table',
                    TableName='maxwell-app-backup',
                    Limit=10
                )
            else:
                response = client.query(
                    ExpressionAttributeNames={
                        '#t': "table"
                    },
                    ExpressionAttributeValues={
                        ':table': {
                            'S': table,
                        }
                    },
                    KeyConditionExpression='#t = :table',
                    TableName='maxwell-app-backup',
                    ExclusiveStartKey=start_key,
                    Limit=10
                )

            dynamodb_items = response["Items"]
            api_items = get_api_items(dynamodb_items)

            last_evaluated_key = response.get("LastEvaluatedKey")

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "items": api_items,
                    "last_evaluated_key": last_evaluated_key
                })
            }
        except ValidationError:
            pass

    return {
        "statusCode": 400,
    }
