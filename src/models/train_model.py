import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import json
from pathlib import Path
import logging
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils.config import DATA_DIR, MODELS_DIR, IMG_HEIGHT, IMG_WIDTH, BATCH_SIZE, EPOCHS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_model():
    """Create a CNN model for cat/dog classification"""
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        layers.MaxPooling2D((2, 2)),
        
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def prepare_data():
    """Prepare data generators for training"""
    
    # Use the actual path where data was downloaded
    training_path = DATA_DIR / "training_set" / "training_set"
    
    if not training_path.exists():
        logger.error(f"Training data not found at {training_path}")
        return None, None
    
    logger.info(f"Using training data from: {training_path}")
    
    # Data generators
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )
    
    train_generator = train_datagen.flow_from_directory(
        training_path,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='training'
    )
    
    validation_generator = train_datagen.flow_from_directory(
        training_path,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='validation'
    )
    
    logger.info(f"Classes: {train_generator.class_indices}")
    logger.info(f"Training samples: {train_generator.samples}")
    logger.info(f"Validation samples: {validation_generator.samples}")
    
    return train_generator, validation_generator

def train_model():
    """Train the cat/dog classification model"""
    
    # Create models directory
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    logger.info("Preparing data...")
    train_gen, val_gen = prepare_data()
    
    if train_gen is None:
        logger.error("Failed to prepare data!")
        return False
    
    logger.info("Creating model...")
    model = create_model()
    
    logger.info("Model architecture:")
    model.summary()
    
    logger.info("Starting training...")
    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        verbose=1
    )
    
    # Save model
    model_path = MODELS_DIR / "cat_dog_model.h5"
    model.save(model_path)
    logger.info(f"Model saved to: {model_path}")
    
    # Save training history
    history_path = MODELS_DIR / "training_history.json"
    with open(history_path, 'w') as f:
        # Convert numpy values to Python types for JSON serialization
        history_dict = {k: [float(val) for val in v] for k, v in history.history.items()}
        json.dump(history_dict, f, indent=2)
    
    # Plot training history
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(MODELS_DIR / "training_history.png")
    plt.close()
    
    logger.info("Training completed successfully!")
    
    # Print final metrics
    final_train_acc = history.history['accuracy'][-1]
    final_val_acc = history.history['val_accuracy'][-1]
    logger.info(f"Final Training Accuracy: {final_train_acc:.4f}")
    logger.info(f"Final Validation Accuracy: {final_val_acc:.4f}")
    
    return True

if __name__ == "__main__":
    success = train_model()
    if success:
        print("✅ Model training completed!")
    else:
        print("❌ Model training failed!")