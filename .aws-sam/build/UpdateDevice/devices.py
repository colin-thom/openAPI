import json
# import get_settings
import os
import boto3
from botocore.exceptions import ClientError
import uuid
from boto3.dynamodb.conditions import Key, Attr


DEVICES_TABLE = os.environ['DEVICES_TABLE']
dynamodb = boto3.resource('dynamodb')

def get_devices(context, event):
    if dynamodb:
        table = dynamodb.Table(DEVICES_TABLE)
        result = table.scan()
        print(result)
        return { 
                "statusCode": 200, 
                "body": json.dumps(result["Items"]),
                "headers": {'Access-Control-Allow-Origin': '*'} 
                }
    else:
        print("else")
        return { 
                "statusCode": 400, 
                "body": {"error": "error bitch"},
                "headers": {'Access-Control-Allow-Origin': '*'} 
                }

def add_device(context, event):
    if dynamodb:
        table = dynamodb.Table(DEVICES_TABLE)
        params = context['multiValueQueryStringParameters']
        status = 200
        try:
            result = table.put_item(
                    Item={
                        'deviceId': uuid.uuid4().hex, 
                        'deviceName': str(params['deviceName'][0]), 
                        'deviceType': str(params["deviceType"][0]),
                        }
                    )
            result = json.dumps(result)
        except ClientError as e:
            result = e
            status = 400
        return {
                "statusCode": status, 
                "body": {"device add": result},
                "headers": {'Access-Control-Allow-Origin': '*'} 
                }


def update_device(context, event):
    if dynamodb:
        table = dynamodb.Table(DEVICES_TABLE)
        params = context['multiValueQueryStringParameters']
        result = table.update_item(
                Key={'deviceId': str(params['deviceId'][0])},
                UpdateExpression='SET deviceName = :name, deviceType = :type',
                ExpressionAttributeValues={
                        ':name': str(params['deviceName'][0]),
                        ':type': str(params['deviceType'][0])
                    }
                )
        return { 
                "statusCode": 200, 
                "body": {"device update": json.dumps(result)},
                "headers": {'Access-Control-Allow-Origin': '*'} 
                }
    else:
        print("else")
        return "flute"

def delete_device(context, event):
    if dynamodb:
        table = dynamodb.Table(DEVICES_TABLE)
        params = context['multiValueQueryStringParameters']
        result = table.delete_item(
                Key={'deviceId': str(params['deviceId'][0])}
                )
        return { 
                "statusCode": 200, 
                "body": {"device delete": json.dumps(result)},
                "headers": {'Access-Control-Allow-Origin': '*'} 
                }
    else:
        print("else")
        return "flute"