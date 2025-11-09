import os
import kaggle

def setup_kaggle():
    """Setup Kaggle with custom config path"""
    kaggle_dir = r'C:\Users\TASNIM\Downloads'
    os.environ['KAGGLE_CONFIG_DIR'] = kaggle_dir
    
    # Manually configure Kaggle API
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.set_config_value('path', kaggle_dir)
    return api

# Call this when module is imported
kaggle_api = setup_kaggle()