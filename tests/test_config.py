import os

def test_config_initialization():
    from src import config
    assert config.API_URL is not None
    assert config.INTERVAL_SECONDS >= 0
