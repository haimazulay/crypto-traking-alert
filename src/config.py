import os
from dotenv import load_dotenv

load_dotenv()

# API Settings
API_URL = "https://api.coinbase.com/v2/prices/BTC-USD/spot"

# Timing Settings (in seconds)
INTERVAL_SECONDS = 60
TOTAL_MINUTES = 60

# File Paths
OUTPUT_DIR = "output"
JSON_FILE_PATH = os.path.join(OUTPUT_DIR, "bpi_data.json")
GRAPH_FILE_PATH = os.path.join(OUTPUT_DIR, "bpi_graph.png")

# Email Settings
SENDER_EMAIL = "haimazulai@gmail.com"
RECEIVER_EMAIL = "superazulay@gmail.com"
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")