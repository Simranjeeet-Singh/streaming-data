import unittest
from unittest.mock import patch, MagicMock
from message_broker import send_to_sqs

class TestMessageBroker(unittest.TestCase):

    @patch('message_broker.boto3.client')
    def test_send_to_sqs_success(self, mock_boto_client):
        # Mock the SQS client and its methods
        mock_sqs = MagicMock()
        mock_boto_client.return_value = mock_sqs

        # Mock the get_queue_url response
        mock_sqs.get_queue_url.return_value = {"QueueUrl": "https://sqs.fake-queue-url"}

        # Mock the send_message response
        mock_sqs.send_message.return_value = {"MessageId": "12345"}

        # Sample articles to send
        articles = [
            {
                "webPublicationDate": "2023-09-11T10:00:00Z",
                "webTitle": "Sample Article",
                "webUrl": "https://www.theguardian.com/sample-article"
            }
        ]

        # Call the actual function
        queue_name = "test_queue"
        send_to_sqs(queue_name, articles)

        # Assertions: check that get_queue_url and send_message were called
        mock_sqs.get_queue_url.assert_called_once_with(QueueName=queue_name)
        mock_sqs.send_message.assert_called_once_with(
            QueueUrl="https://sqs.fake-queue-url", 
            MessageBody=unittest.mock.ANY
        )

if __name__ == "__main__":
    unittest.main()
