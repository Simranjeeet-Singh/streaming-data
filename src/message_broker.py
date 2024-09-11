import boto3
import json

def send_to_sqs(queue_name, articles):
    """
    Sends a list of articles to AWS SQS as individual messages.

    Args:
        queue_name (str): The name of the SQS queue.
        articles (list): The list of articles to send to SQS.
    """
    sqs = boto3.client('sqs')

    # Get the queue URL
    response = sqs.get_queue_url(QueueName=queue_name)
    queue_url = response['QueueUrl']

    # Send each article as a message to the SQS queue
    for article in articles:
        message = {
            "webPublicationDate": article.get('webPublicationDate'),
            "webTitle": article.get('webTitle'),
            "webUrl": article.get('webUrl'),
        }

        sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))

    print(f"Sent {len(articles)} articles to SQS queue: {queue_name}")
