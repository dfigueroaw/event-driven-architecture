import json
import boto3

def lambda_handler(event, context):
    pedido = json.dumps(event)

    # Create SQS client
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/891377132613/sqs-pedidos'

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=(pedido)
    )

    # Salida (json)
    return {
        'statusCode': 200,
        'respuesta': response
    }