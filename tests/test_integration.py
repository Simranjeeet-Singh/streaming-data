import unittest
from unittest.mock import patch, MagicMock
import os
from src.main import main

class TestIntegration(unittest.TestCase):

    @patch('boto3.client')  # Mock the SQS client
    @patch('requests.get')  # Mock the actual requests call
    def test_full_integration(self, mock_requests_get, mock_boto3_client):
        # Mock Guardian API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'response': {
                'results': [
                    {"webPublicationDate": "2024-01-01", "webTitle": "Test Article", "webUrl": "https://example.com"}
                ]
            }
        }
        mock_requests_get.return_value = mock_response
    
        # Mock the boto3 SQS client
        mock_sqs_client = MagicMock()
        mock_boto3_client.return_value = mock_sqs_client
        mock_sqs_client.get_queue_url.return_value = {'QueueUrl': 'https://fake-queue-url'}
    
        # Set environment variables
        os.environ['GUARDIAN_API_KEY'] = 'test_api_key'
        os.environ['SQS_QUEUE_NAME'] = 'test_queue_name'
    
        # Run the main function
        main()

        # Ensure SQS interaction occurred
        mock_sqs_client.get_queue_url.assert_called_once_with(QueueName='test_queue_name')

if __name__ == '__main__':
    unittest.main()
