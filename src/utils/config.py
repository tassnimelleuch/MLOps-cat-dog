import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
SRC_DIR = PROJECT_ROOT / "src"

# Kaggle dataset
KAGGLE_DATASET = "tongpython/cat-and-dog"
DATASET_NAME = "cat-and-dog"

# Model parameters
IMG_HEIGHT = 150
IMG_WIDTH = 150
BATCH_SIZE = 32
EPOCHS = 10
VALIDATION_SPLIT = 0.2

# API configuration
API_HOST = "0.0.0.0"
API_PORT = 5000