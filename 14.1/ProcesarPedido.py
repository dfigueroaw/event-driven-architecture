import json
import boto3
import os

def lambda_handler(event, context):

    # Create SQS client
    sqs = boto3.client('sqs')
    queue_url = os.environ['SQS_QUEUE_URL']
    
    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=3,
        WaitTimeSeconds=10
    )
    
    print(response)
    
    messages = response.get('Messages', [])
    pedidos = []
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_pedidos_procesados')

    for message in messages:
        pedido = json.loads(message['Body'])
        print(pedido)
        pedidos.append(pedido)
        table.put_item(Item=pedido)
        receipt_handle = message['ReceiptHandle']
        # Delete received message from queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "pedidos_procesados": pedidos
        })
    }
