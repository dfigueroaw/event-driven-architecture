import json
import boto3
import os

def lambda_handler(event, context):
    # Entrada (json)
    archivo_id = event['Records'][0]['s3']['object']['key']
    tenant_id = archivo_id.split('/')[0] # UTEC, UNIV1, etc.
    archivo_last_modified = event['Records'][0]['eventTime']
    archivo_size = event['Records'][0]['s3']['object']['size']
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    archivo = {
        'tenant_id': tenant_id,
        'archivo_id': archivo_id,
        'archivo_datos': {
            'last_modified': archivo_last_modified,
            'size': archivo_size,
            'bucket_name': bucket_name
        }    
    }
    # Publicar en SNS
    sns_client = boto3.client('sns')
    topic_arn = os.environ['TEMA_NUEVO_ARCHIVO_ARN']
    response_sns = sns_client.publish(
        TopicArn = topic_arn,
        Subject = 'Nuevo Archivo',
        Message = json.dumps(archivo),
        MessageAttributes = {
            'tenant_id': {'DataType': 'String', 'StringValue': tenant_id }
        }
    )    
    # TODO implement
    return {
        'statusCode': 200,
        'body': response_sns
    }