import json
import os
import boto3
import uuid
from boto3.dynamodb.conditions import Key
from pprint import pprint
from decimal import Decimal

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

def add_device(context, event):
    if dynamodb:
        table = dynamodb.Table(DEVICES_TABLE)
        params = context['multiValueQueryStringParameters']
        response = table.put_item(
                Item={
                    'id': uuid.uuid4().hex,
                    'deviceName': str(params['name'][0]),
                    'deviceType': str(params["type"][0])
                    }
                )
        return {
            "statusCode": 200,
            "body": {'ajouté correctement': 'ok'},
            "headers": {'Access-Control-Allow-Origin': '*'}
        }
    else: 
        return {
            "statusCode": 400,
            "body": {"nope"},
            "headers": {'Access-Control-Allow-Origin': '*'}
        }

def update_device(context, event):
    if dynamodb:
        table = dynamodb.Table(DEVICES_TABLE)
        params = context['multiValueQueryStringParameters']
        response = table.update_item(
            Key={
                'id': str(params['id'][0]),
            },
            UpdateExpression="SET \
                    deviceName= :n,\
                    deviceType= :t",
            ExpressionAttributeValues={
                ':n': str(params['name'][0]),
                ':t': str(params["type"][0])
            },
            ReturnValues="UPDATED_NEW"
        )
        return {
            "statusCode": 200,
            "body": {'modifié correctement' : 'ok'},
            "headers": {'Access-Control-Allow-Origin': '*'}
        }

def delete_device(context, event):
    if dynamodb:
        table = dynamodb.Table(DEVICES_TABLE)
        params = context['multiValueQueryStringParameters']
        response = table.delete_item(
            Key={
                'id': str(params['id'][0]),
            }
        )
        return {
            "statusCode": 200,
            "body": {'supprimé correctement' : 'ok'},
            "headers": {'Access-Control-Allow-Origin': '*'}
        }


