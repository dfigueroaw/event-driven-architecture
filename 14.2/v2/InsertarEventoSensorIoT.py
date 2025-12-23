import json
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    body = json.loads(event['Records'][0]['body'])
    lectura_sensor = json.loads(body['Message'])
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_sensor_iot_FAB1')
    response = table.put_item(Item=lectura_sensor)
    print(lectura_sensor) # Para logs en Cloud Watch
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }
