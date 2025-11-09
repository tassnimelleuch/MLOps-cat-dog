import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data.download_data import download_dataset
from src.utils.config import DATA_DIR

def test_data_download():
    """Test that data can be downloaded"""
    success = download_dataset()
    assert success == True, "Data download failed"
    assert DATA_DIR.exists(), "Data directory not created"
    print("✅ Data download test passed!")

if __name__ == "__main__":
    test_data_download()