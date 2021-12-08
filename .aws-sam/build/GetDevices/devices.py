import json
import os
import boto3
from boto3.dynamodb.conditions import Key

DEVICES_TABLE = os.environ['DEVICES_TABLE']
dynamodb = boto3.resource('dynamodb')

def get_devices(context, event):
    if dynamodb:
        table = dynamodb.Table(DEVICES_TABLE)
        response = table.scan()
        return {
            "statusCode": 200,
            "body": json.dumps(response["Items"]),
            "headers": {'Access-Control-Allow-Origin': '*'}
        }
    else:
        return {
            "statusCode": 400,
            "body": {"nope"},
            "headers": {'Access-Control-Allow-Origin': '*'}
        }


