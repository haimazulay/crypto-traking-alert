import pytest
from unittest.mock import patch, MagicMock
from src.business_logic import TrackerBusinessLogic

@pytest.fixture
def mock_config():
    # Create a fake configuration for testing purposes
    config = MagicMock()
    config.API_URL = "http://fake-url"
    config.JSON_FILE_PATH = "fake_dir/fake.json"
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

@patch('src.business_logic.Console.export_html', return_value="<html></html>")
@patch('src.business_logic.JsonStorage')
@patch('builtins.open', new_callable=MagicMock)
def test_generate_html_dashboard(mock_open_file, MockStorage, mock_export, mock_config):
    bl = TrackerBusinessLogic(mock_config)
    bl.generate_html_dashboard(60000.0, "line.png", "candle.png")
    
    mock_export.assert_called_once()
    mock_open_file.assert_called_once()

@patch('src.business_logic.TrackerBusinessLogic.generate_html_dashboard')
@patch('src.business_logic.BpiGraphGenerator')
@patch('src.business_logic.JsonStorage')
@patch('src.business_logic.CoinbaseApiClient')
@patch('src.business_logic.time.sleep')
@patch('src.business_logic.EmailNotifier')
def test_business_logic_run_with_missing_prices_and_notifier(MockNotifier, mock_sleep, MockApiClient, MockStorage, MockVisualizer, mock_html, mock_config):
    # Test path when SENDER_PASSWORD is provided and prices fail to fetch (None)
    mock_config.SENDER_PASSWORD = "password"
    mock_config.TOTAL_MINUTES = 2
    
    mock_api_instance = MockApiClient.return_value
    mock_api_instance.get_current_bpi.side_effect = [None, None]
    
    mock_visualizer_instance = MockVisualizer.return_value
    mock_visualizer_instance.generate_all_graphs.return_value = (None, None)

    bl = TrackerBusinessLogic(mock_config)
    
    # Assert notifier was instantiated because SENDER_PASSWORD exists
    assert bl.notifier is not None
    
    max_price = bl.run()
    
    # Max price remains 0 since no prices were valid
    assert max_price == 0
    # generate_html should not be called because graph paths are None
    mock_html.assert_not_called()
    # Notifier should not send email because graph paths are None
    MockNotifier.return_value.send_email.assert_not_called()

@patch('src.business_logic.TrackerBusinessLogic.generate_html_dashboard')
@patch('src.business_logic.BpiGraphGenerator')
@patch('src.business_logic.JsonStorage')
@patch('src.business_logic.CoinbaseApiClient')
@patch('src.business_logic.time.sleep')
@patch('src.business_logic.EmailNotifier')
def test_business_logic_run_with_notify(MockNotifier, mock_sleep, MockApiClient, MockStorage, MockVisualizer, mock_html, mock_config):
    mock_config.SENDER_PASSWORD = "password"
    mock_config.TOTAL_MINUTES = 1
    
    # 1 valid price
    MockApiClient.return_value.get_current_bpi.side_effect = [60000.0]
    
    # Return valid paths
    MockVisualizer.return_value.generate_all_graphs.return_value = ("line.png", "candle.png")

    bl = TrackerBusinessLogic(mock_config)
    bl.run()
    
    # Assert notifier send email branch was hit
    MockNotifier.return_value.send_email.assert_called_once_with(60000.0, "line.png")