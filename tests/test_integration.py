import unittest
from unittest.mock import patch, MagicMock
import os
from main import lambda_handler

class TestIntegration(unittest.TestCase):

    @patch('boto3.client')
    @patch('requests.get')
    @patch.dict(os.environ, {"GUARDIAN_API_KEY": "test_api_key", "SQS_QUEUE_NAME": "test_queue_name"})  # Mock environment variables
    def test_lambda_handler(self, mock_requests_get, mock_boto3_client):
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
    
        # Mock event input for Lambda
        event = {
            "search_term": "machine learning",
            "date_from": "2023-01-01"
        }
    
        # Run the Lambda handler function
        response = lambda_handler(event, None)
    
        # Ensure Lambda handler executed properly
        mock_sqs_client.get_queue_url.assert_called_once_with(QueueName='test_queue_name')
        self.assertEqual(response['statusCode'], 200)

if __name__ == '__main__':
    unittest.main()
