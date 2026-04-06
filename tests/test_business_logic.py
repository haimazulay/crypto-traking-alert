import pytest
from unittest.mock import patch, MagicMock
from src.business_logic import TrackerBusinessLogic

@pytest.fixture
def mock_config():
    # Create a fake configuration for testing purposes
    config = MagicMock()
    config.API_URL = "http://fake-url"
    config.JSON_FILE_PATH = "fake.json"
    config.OUTPUT_DIR = "fake_dir"
    config.TOTAL_MINUTES = 3
    config.INTERVAL_SECONDS = 0  # CRITICAL: Overrides sleep time so tests run instantly
    config.SENDER_PASSWORD = None  # Skip email initialization
    return config

@patch('src.business_logic.TrackerBusinessLogic.generate_html_dashboard')
@patch('src.business_logic.BpiGraphGenerator')
@patch('src.business_logic.JsonStorage')
@patch('src.business_logic.CoinbaseApiClient')
@patch('src.business_logic.time.sleep')
def test_business_logic_run(mock_sleep, MockApiClient, MockStorage, MockVisualizer, mock_html, mock_config):
    # Arrange: Setup the API to return 3 different prices
    mock_api_instance = MockApiClient.return_value
    mock_api_instance.get_current_bpi.side_effect = [60000.0, 62000.0, 59000.0]
    
    mock_visualizer_instance = MockVisualizer.return_value
    mock_visualizer_instance.generate_all_graphs.return_value = ("line.png", "candle.png")

    bl = TrackerBusinessLogic(mock_config)
    
    # Act
    max_price = bl.run()
    
    # Assert: Verify the max price logic works
    assert max_price == 62000.0
    
    # Verify the loop ran exactly 3 times as configured
    assert mock_api_instance.get_current_bpi.call_count == 3
    
    # Verify we attempted to save records 3 times
    mock_storage_instance = MockStorage.return_value
    assert mock_storage_instance.save_record.call_count == 3
    
    # Verify visualizers were triggered at the end
    mock_visualizer_instance.generate_all_graphs.assert_called_once()
    mock_html.assert_called_once()