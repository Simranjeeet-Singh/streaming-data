import os
import json
from guardian_api import get_guardian_articles
from message_broker import send_to_sqs

# Main Lambda function entry point
def lambda_handler(event, context):
    """
    AWS Lambda function handler.
    
    Parameters:
    - event (dict): Contains data from the invoking source, usually API Gateway.
    - context (dict): Metadata about the invocation, function, and execution environment.
    """
    
    # Retrieve inputs from the event (query parameters if present, else request body)
    if event.get("queryStringParameters"):
        # Get inputs from query parameters (useful for API Gateway GET requests)
        search_term = event.get("queryStringParameters", {}).get("search_term")
        date_from = event.get("queryStringParameters", {}).get("date_from")
    else:
        # Get inputs from request body (for POST requests)
        body = json.loads(event.get("body", "{}"))
        search_term = body.get("search_term")
        date_from = body.get("date_from")

    # Fetch API key and SQS queue name from environment variables (to avoid hardcoding sensitive information)
    api_key = os.getenv('GUARDIAN_API_KEY')
    queue_name = os.getenv('SQS_QUEUE_NAME')

    # Validate that the required environment variables are available
    if not api_key or not queue_name:
        raise ValueError("API key and/or SQS queue name not set in environment variables.")
    
    # Fetch articles from The Guardian API using the specified search term and date
    articles = get_guardian_articles(api_key, search_term, date_from)

    # Send the retrieved articles to the specified SQS queue
    send_to_sqs(queue_name, articles)

    # Return a successful response to the API Gateway
    return {
        "statusCode": 200,
        "body": f"Successfully sent {len(articles)} articles to SQS."
    }