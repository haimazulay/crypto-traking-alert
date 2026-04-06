import json
import os
from datetime import datetime

# Class for managing JSON file interactions and storage of price entries
class JsonStorage:
    # Initialization method configuring the path and creating directories
    def __init__(self, file_path):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        # If statement to check if the file does not already exist, and initializes it
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    # Method responsible for saving a new price point into the JSON storage system
    def save_record(self, price):
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "price": price
        }
        
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        
        data.append(record)
        
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)