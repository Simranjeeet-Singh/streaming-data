import argparse
import os
from src.guardian_api import get_guardian_articles
from src.message_broker import send_to_sqs

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Fetch Guardian articles and send to AWS SQS.')
    parser.add_argument('search_term', type=str, help='Search term for fetching articles from The Guardian API')
    parser.add_argument('--date_from', type=str, help='Optional: Filter articles from this date (format: YYYY-MM-DD)', default=None)
    parser.add_argument('--queue_name', type=str, help='Name of the AWS SQS queue', required=True)

    # Parse the arguments
    args = parser.parse_args()

    # Get the Guardian API key from environment variables
    api_key = os.getenv("GUARDIAN_API_KEY")
    if not api_key:
        raise ValueError("Guardian API key not found. Set the 'GUARDIAN_API_KEY' environment variable.")

    try:
        # Fetch articles from The Guardian API
        articles = get_guardian_articles(api_key, args.search_term, args.date_from)

        if articles:
            # Send articles to AWS SQS
            send_to_sqs(args.queue_name, articles)
            print(f"Successfully sent {len(articles)} articles to SQS.")
        else:
            print("No articles found.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
