import os
from src.guardian_api import get_guardian_articles
from src.message_broker import send_to_sqs

def main():
    # Fetch the SQS queue name from environment variables
    queue_name = os.getenv('SQS_QUEUE_NAME')  # Using queue name, not URL
    if not queue_name:
        raise ValueError("SQS queue name is not set. Please set it in the environment.")

    # Fetch the Guardian API key from environment variables
    api_key = os.getenv("GUARDIAN_API_KEY")
    if not api_key:
        raise ValueError("Guardian API key is not set. Please set it in the environment.")

    # Example search term and date
    search_term = "machine learning"  # This can be user input or command-line args
    date_from = None  # Optional filter

    # Fetch articles from The Guardian API
    articles = get_guardian_articles(api_key, search_term, date_from)

    if articles:
        print(f"Fetched {len(articles)} articles, sending to SQS...")
        send_to_sqs(queue_name, articles)  # Passing queue name instead of URL
    else:
        print("No articles found.")

if __name__ == "__main__":
    main()