import json
import boto3
import os

def lambda_handler(event, context):
    pedido = json.loads(event['body'])

    # Create SQS client
    sqs = boto3.client('sqs')
    queue_url = os.environ['SQS_QUEUE_URL']

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(pedido)
    )

    # Salida (json)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "Pedido enviado correctamente",
            "message_id": response["MessageId"]
        })
    }
