import json

def get_devices(context, event):
    return {
        "statusCode": 400,
        "body": json.dumps([{"id": "a", "devType": "co2", "name": "device1"},
                {"id": "b", "devType": "temperature", "name": "device2"}]),
        "headers": {'Access-Control-Allow-Origin': '*'}
        }