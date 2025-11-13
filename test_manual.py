import tensorflow as tf
import numpy as np
from pathlib import Path
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.config import MODELS_DIR, IMG_HEIGHT, IMG_WIDTH

def predict_image(image_path):
    """Predict if image is cat or dog"""
    
    model_path = MODELS_DIR / "cat_dog_model.h5"
    if not model_path.exists():
        print("❌ Model not found! Train the model first.")
        return
    
    print("Loading model...")
    model = tf.keras.models.load_model(model_path)
    
    # Load and preprocess the image
    try:
        img = tf.keras.preprocessing.image.load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Create batch
        img_array /= 255.0  # Normalize like in training
        
        print(f"🔍 Analyzing image: {image_path}")
        
        # Make prediction
        prediction = model.predict(img_array, verbose=0)
        confidence = prediction[0][0]
        
        # Interpret results
        if confidence > 0.5:
            result = "DOG 🐶"
            confidence_pct = confidence * 100
        else:
            result = "CAT 🐱"
            confidence_pct = (1 - confidence) * 100
        
        print("\n" + "="*50)
        print(f"🎯 PREDICTION: {result}")
        print(f"📊 CONFIDENCE: {confidence_pct:.2f}%")
        print("="*50)
        
        # Show probabilities
        print(f"\n📈 Detailed probabilities:")
        print(f"   Cat probability: {(1-confidence)*100:.2f}%")
        print(f"   Dog probability: {confidence*100:.2f}%")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure the image path is correct and it's a valid image file.")

def list_sample_images():
    """List some sample images you can test with"""
    test_dir = Path("data/test_set/test_set")
    
    if test_dir.exists():
        print("\n📁 Available sample images:")
        
        # Get some cat images
        cat_images = list((test_dir / "cats").glob("*.jpg"))[:5]
        print("\n🐱 Cat images:")
        for i, img in enumerate(cat_images, 1):
            print(f"   {i}. {img}")
        
        # Get some dog images
        dog_images = list((test_dir / "dogs").glob("*.jpg"))[:5]
        print("\n🐶 Dog images:")
        for i, img in enumerate(dog_images, 1):
            print(f"   {i}. {img}")
        
        print(f"\💡 Tip: Copy any of these paths to test!")

if __name__ == "__main__":
    print("🐱🐶 CAT/DOG CLASSIFIER TEST")
    print("="*30)
    
    # List available images
    list_sample_images()
    
    print(f"\nEnter the path to an image you want to test:")
    print("Examples:")
    print("  - data/test_set/test_set/cats/cat.4001.jpg")
    print("  - data/test_set/test_set/dogs/dog.4001.jpg")
    print("  - Or any image from your computer!")
    print()
    
    # Get image path from user
    image_path = input("📁 Image path: ").strip().replace('"', '').replace("'", "")
    
    if not image_path:
        print("❌ Please enter an image path!")
        exit()
    
    image_path = Path(image_path)
    
    if image_path.exists():
        predict_image(image_path)
    else:
        print(f"❌ Image not found: {image_path}")
        print("💡 Make sure the path is correct and the file exists.")