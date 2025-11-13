import os
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi


def setup_kaggle():
    """Setup Kaggle API config directory.

    Behavior:
    - If the environment variable KAGGLE_CONFIG_DIR is set, use it.
    - Otherwise default to ~/.kaggle.
    - Ensure the directory exists. Do NOT embed secrets here.

    The function returns an authenticated KaggleApi instance. The
    actual kaggle.json file must already exist in the chosen directory
    (this file should NOT be checked into source control).
    """
    kaggle_dir = os.environ.get('KAGGLE_CONFIG_DIR')
    if not kaggle_dir:
        kaggle_dir = str(Path.home() / '.kaggle')

    Path(kaggle_dir).mkdir(parents=True, exist_ok=True)
    os.environ['KAGGLE_CONFIG_DIR'] = kaggle_dir

    # It's okay if kaggle.json is missing here; the caller/CI should
    # place it before running code that needs authentication.
    api = KaggleApi()
    # authenticate() will look for kaggle.json inside KAGGLE_CONFIG_DIR
    api.authenticate()
    return api


# Initialize on import so other modules can import kaggle_api
kaggle_api = setup_kaggle()