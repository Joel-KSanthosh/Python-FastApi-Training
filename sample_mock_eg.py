import unittest
from unittest.mock import Mock

# Let's say we have a function that calls an external service
def fetch_data_from_api(api_client):
    response = api_client.get('/data')
    if response.status_code == 200:
        return response.json()
    else:
        return None

class TestFetchData(unittest.TestCase):

    def test_fetch_data_success(self):
        # Create a mock for the api_client
        mock_api_client = Mock()

        # Set up the mock to return a mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_api_client.get.return_value = mock_response

        # Now call the function with the mock
        result = fetch_data_from_api(mock_api_client)

        # Assert that the mock was called correctly and the result is as expected
        mock_api_client.get.assert_called_once_with('/data')
        self.assertEqual(result, {"key": "value"})

    def test_fetch_data_failure(self):
        # Create a mock for the api_client
        mock_api_client = Mock()

        # Set up the mock to return a failed response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_api_client.get.return_value = mock_response

        # Now call the function with the mock
        result = fetch_data_from_api(mock_api_client)

        # Assert the result is None for a failure
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()

