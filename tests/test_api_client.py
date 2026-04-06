import pytest
from unittest.mock import patch, Mock
from src.api_client import CoinbaseApiClient

@patch('src.api_client.requests.get')
def test_get_current_bpi_success(mock_get):
    # Arrange: Setup the mock response
    mock_response = Mock()
    mock_response.json.return_value = {"data": {"amount": "50000.50"}}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    client = CoinbaseApiClient("http://fake-api.url")
    
    # Act: Call the method
    price = client.get_current_bpi()
    
    # Assert: Verify the result
    assert price == 50000.50

@patch('src.api_client.requests.get')
def test_get_current_bpi_failure(mock_get):
    # Arrange: Simulate an exception (e.g., network error)
    mock_get.side_effect = Exception("Network Error")
    
    client = CoinbaseApiClient("http://fake-api.url")
    
    # Act
    price = client.get_current_bpi()
    
    # Assert
    assert price is None