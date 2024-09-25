import unittest
from unittest.mock import patch
import os
from src.main import main

class TestIntegration(unittest.TestCase):

    @patch('src.guardian_api.get_guardian_articles')
    @patch('src.message_broker.send_to_sqs')
    def test_full_integration(self, mock_send_to_sqs, mock_get_guardian_articles):
        # Mock Guardian API response
        mock_get_guardian_articles.return_value = [
            {"webPublicationDate": "2024-01-01", "webTitle": "Test Article", "webUrl": "https://example.com"}
        ]
        
        # Set environment variables
        os.environ['GUARDIAN_API_KEY'] = 'fake_api_key'
        os.environ['SQS_QUEUE_NAME'] = 'fake_queue_name'

        # Run the main function
        main()

        # Ensure articles were fetched and sent to SQS
        mock_get_guardian_articles.assert_called_once()
        mock_send_to_sqs.assert_called_once_with('fake_queue_name', mock_get_guardian_articles.return_value)

if __name__ == '__main__':
    unittest.main()
