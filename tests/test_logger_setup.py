import logging
import os
from unittest.mock import patch
from src.logger_setup import get_logger

def test_get_logger(tmp_path):
    with patch("os.makedirs") as mock_makedirs, \
         patch("src.logger_setup.RotatingFileHandler") as mock_handler:
        
        logger = get_logger("TestLogger")
        
        assert logger.name == "TestLogger"
        assert logger.level == logging.DEBUG
        mock_makedirs.assert_called_with("output", exist_ok=True)
        mock_handler.assert_called_once()
        
        # Test singleton handler logic
        handler_count = len(logger.handlers)
        
        logger2 = get_logger("TestLogger")
        assert len(logger2.handlers) == handler_count
