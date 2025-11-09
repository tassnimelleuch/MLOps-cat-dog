# Quick debug script - create debug_data.py in project root
from pathlib import Path

data_dir = Path("data")
print("Data directory contents:")
for item in data_dir.iterdir():
    if item.is_dir():
        print(f"📁 {item.name}")
        for subitem in item.iterdir():
            if subitem.is_dir():
                print(f"  └── 📁 {subitem.name}")
                for file in list(subitem.iterdir())[:3]:  # Show first 3 items
                    print(f"      └── {file.name}")