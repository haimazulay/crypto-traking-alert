import json
import os
from datetime import datetime

class JsonStorage:
    def __init__(self, file_path):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

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