import unittest
from unittest.mock import patch, MagicMock
from src.guardian_api import get_guardian_articles

class TestGuardianAPI(unittest.TestCase):

    @patch('src.guardian_api.requests.get')  # Patch 'requests.get'
    def test_get_guardian_articles_success(self, mock_get):
        # Mock the response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": {
                "status": "ok",
                "results": [
                    {
                        "webPublicationDate": "2023-09-11T10:00:00Z",
                        "webTitle": "Sample Article",
                        "webUrl": "https://www.theguardian.com/sample-article"
                    }
                ]
            }
        }

        # Set the mock response object to be returned by requests.get
        mock_get.return_value = mock_response

        # Call the actual function
        api_key = "test_api_key"
        search_term = "test"
        articles = get_guardian_articles(api_key, search_term)

        # Check the results
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]['webTitle'], "Sample Article")
        self.assertEqual(articles[0]['webUrl'], "https://www.theguardian.com/sample-article")

if __name__ == "__main__":
    unittest.main()
