import pytest
import pandas as pd
from unittest.mock import patch, mock_open
from src.visualizer import BpiGraphGenerator

@pytest.fixture
def graph_gen():
    return BpiGraphGenerator("fake.json", "fake_dir")

@patch("src.visualizer.json.load")
@patch("builtins.open", new_callable=mock_open)
def test_load_data_empty(mock_file, mock_json, graph_gen):
    mock_json.return_value = []
    df = graph_gen.load_data()
    assert df.empty

@patch("src.visualizer.json.load")
@patch("builtins.open", new_callable=mock_open)
def test_load_data_valid(mock_file, mock_json, graph_gen):
    mock_json.return_value = [{"timestamp": "2023-01-01 12:00:00", "price": "50000.0"}]
    df = graph_gen.load_data()
    assert not df.empty
    assert "price" in df.columns

@patch("src.visualizer.plt.savefig")
def test_generate_line_chart(mock_savefig, graph_gen):
    df = pd.DataFrame({"price": [50000.0]}, index=pd.to_datetime(["2023-01-01 12:00:00"]))
    graph_gen.generate_line_chart(df)
    mock_savefig.assert_called_once()

@patch("src.visualizer.mpf.plot")
def test_generate_candlestick_chart(mock_mpf, graph_gen):
    df = pd.DataFrame({"price": [50000.0, 51000.0]}, index=pd.to_datetime(["2023-01-01 12:00:00", "2023-01-01 12:00:05"]))
    graph_gen.generate_candlestick_chart(df)
    mock_mpf.assert_called_once()

def test_generate_candlestick_chart_empty(graph_gen):
    # Pass empty df with DatetimeIndex, plotting should just return
    df = pd.DataFrame({"price": []}, index=pd.DatetimeIndex([]))
    graph_gen.generate_candlestick_chart(df)

@patch.object(BpiGraphGenerator, 'load_data')
@patch.object(BpiGraphGenerator, 'generate_line_chart')
@patch.object(BpiGraphGenerator, 'generate_candlestick_chart')
def test_generate_all_graphs(mock_candle, mock_line, mock_load, graph_gen):
    mock_load.return_value = pd.DataFrame({"price": [1]})
    l, c = graph_gen.generate_all_graphs()
    mock_line.assert_called_once()
    mock_candle.assert_called_once()
    assert l == graph_gen.line_graph_path
    assert c == graph_gen.candle_graph_path

@patch.object(BpiGraphGenerator, 'load_data')
def test_generate_all_graphs_empty(mock_load, graph_gen):
    mock_load.return_value = pd.DataFrame()
    l, c = graph_gen.generate_all_graphs()
    assert l is None
    assert c is None
