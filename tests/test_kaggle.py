import os
import subprocess

# Set the kaggle config directory
os.environ['KAGGLE_CONFIG_DIR'] = r'C:\Users\TASNIM\Downloads'

try:
    # Test kaggle CLI
    result = subprocess.run(['kaggle', 'datasets', 'list'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Kaggle is working!")
    else:
        print(f"❌ Kaggle error: {result.stderr}")
except Exception as e:
    print(f"❌ Error: {e}")