import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name="BpiMonitor"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console handler - shows only INFO and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # File handler - saves DEBUG and above, rotates files
    os.makedirs("output", exist_ok=True)
    file_handler = RotatingFileHandler('output/app.log', maxBytes=1048576, backupCount=3)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger