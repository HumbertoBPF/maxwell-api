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
        "items": {
            "type": "array",
            "items": {
                "type": "object"
            },
        },
    },
    "required": ["table", "items"],
}


def get_dynamodb_items(items, table):
    dynamodb_items = []

    for item in items:
        item_to_dynamo_db = {
            'table': {
                'S': table,
            },
        }

        for key, value in item.items():
            item_to_dynamo_db[key] = {
                "S": f"{value}"
            }

        if item.get("deleted", False):
            dynamodb_items.append({
                'DeleteRequest': {
                    'Key': {
                        'table': item_to_dynamo_db["table"],
                        'id': item_to_dynamo_db["id"]
                    },
                },
            },)
        else:
            dynamodb_items.append({
                'PutRequest': {
                    'Item': item_to_dynamo_db,
                },
            },)

    return dynamodb_items


def lambda_handler(event, context):
    data = event.get("body")
    headers = event.get("headers", {})
    content_type = headers.get("Content-Type")

    if (data is not None) and (content_type == "application/json"):
        data_json = json.loads(data)

        try:
            validate(instance=data_json, schema=schema)

            items = data_json["items"]
            table = data_json["table"]

            unprocessed_items = {}

            if len(items) != 0:

                items_to_dynamo_db = get_dynamodb_items(items, f"{table}")

                response = client.batch_write_item(
                    RequestItems={
                        'maxwell-app-backup': items_to_dynamo_db
                    },
                )

                unprocessed_items = response.get("UnprocessedItems")

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "unprocessed_items": unprocessed_items
                })
            }
        except ValidationError:
            pass

    return {
        "statusCode": 400
    }
