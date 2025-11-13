import os
import subprocess
import zipfile
import shutil
from pathlib import Path
import sys

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.config import DATA_DIR, KAGGLE_DATASET
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_dataset():
    """Download dataset using kaggle CLI without importing kaggle"""
    
    # Create data directory
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    logger.info("Downloading dataset from Kaggle...")
    
    try:
        # Use subprocess to call kaggle CLI directly
        # This avoids the import/authentication issue
        result = subprocess.run([
            'kaggle', 'datasets', 'download',
            '-d', KAGGLE_DATASET,
            '-p', str(DATA_DIR),
            '--unzip'
        ], capture_output=True, text=True, check=True)
        
        logger.info("Dataset downloaded and extracted successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error downloading dataset: {e}")
        logger.error(f"STDERR: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

def organize_data():
    """Verify the data structure"""
    
    training_path = DATA_DIR / "training_set" / "training_set"
    test_path = DATA_DIR / "test_set" / "test_set"
    
    if training_path.exists():
        logger.info("✅ Data structure is correct!")
        logger.info(f"Training data: {training_path}")
        logger.info(f"Test data: {test_path}")
        
        # Count files
        cat_train_count = len(list((training_path / "cats").glob("*")))
        dog_train_count = len(list((training_path / "dogs").glob("*")))
        
        logger.info(f"Training: {cat_train_count} cats, {dog_train_count} dogs")
        return True
    else:
        logger.error("❌ Data structure not as expected")
        return False

if __name__ == "__main__":
    # Note: do NOT hardcode KAGGLE_CONFIG_DIR here. CI or the developer
    # should set the environment variable or place kaggle.json in
    # ~/.kaggle. The code below assumes the environment is already
    # prepared by the caller (local dev or CI).
    success = download_dataset()
    if success:
        organize_data()
        print("✅ Data preparation completed!")
    else:
        print("❌ Data preparation failed!")