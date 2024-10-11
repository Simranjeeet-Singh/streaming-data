import os
import json
from guardian_api import get_guardian_articles
from message_broker import send_to_sqs

def lambda_handler(event, context):
    # Retrieve inputs from the event (usually passed by API Gateway)
    if event.get("queryStringParameters"):
        search_term = event.get("queryStringParameters", {}).get("search_term")
        date_from = event.get("queryStringParameters", {}).get("date_from")
    else:
        body = json.loads(event.get("body", "{}"))
        search_term = body.get("search_term")
        date_from = body.get("date_from")

    # Use environment variables for sensitive info like API key and SQS queue name
    api_key = os.getenv('GUARDIAN_API_KEY')
    queue_name = os.getenv('SQS_QUEUE_NAME')

    if not api_key or not queue_name:
        raise ValueError("API key and/or SQS queue name not set in environment variables.")
    
    # Fetch articles and send them to SQS
    articles = get_guardian_articles(api_key, search_term, date_from)
    send_to_sqs(queue_name, articles)

    return {
        "statusCode": 200,
        "body": f"Successfully sent {len(articles)} articles to SQS."
    }

