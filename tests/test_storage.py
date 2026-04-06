import json
import os
from src.storage import JsonStorage

def test_storage_initialization(tmp_path):
    # tmp_path is a built-in pytest fixture for temporary directories
    test_file = tmp_path / "test_data.json"
    storage = JsonStorage(str(test_file))
    
    # Assert file is created and contains an empty list
    assert os.path.exists(str(test_file))
    with open(str(test_file), 'r') as f:
        data = json.load(f)
        assert data == []

def test_save_record(tmp_path):
    test_file = tmp_path / "test_data.json"
    storage = JsonStorage(str(test_file))
    
    # Act: Save two records
    storage.save_record(50000.0)
    storage.save_record(51000.0)
    
    # Assert: Verify both were saved correctly
    with open(str(test_file), 'r') as f:
        data = json.load(f)
        assert len(data) == 2
        assert data[0]['price'] == 50000.0
        assert data[1]['price'] == 51000.0