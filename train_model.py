import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
# 📁 dataset path
DATASET_PATH = "dataset"

# 🔄 Data preprocessing
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(224, 224),
    batch_size=16,
    class_mode="categorical",
    subset="training"
)

val_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(224, 224),
    batch_size=16,
    class_mode="categorical",
    subset="validation"
)

# 🔥 Base model (Transfer Learning)
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224,224,3))
base_model.trainable = False

# 🔥 Custom layers
x = base_model.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(128, activation="relu")(x)
output = layers.Dense(train_data.num_classes, activation="softmax")(x)

model = models.Model(inputs=base_model.input, outputs=output)

# 🔥 Compile
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# 🚀 Train
model.fit(train_data, validation_data=val_data, epochs=8     )

# 💾 Save model
model.save("plant_disease_model.h5")
print("✅ Model training complete!"
       )
import pickle

class_names = list(train_data.class_indices.keys())

with open("class_names.pkl", "wb") as f:
    pickle.dump(class_names, f)