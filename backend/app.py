from flask import Flask, request, render_template_string
import os
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🔥 Load model


# Dummy class names (adjust later)
class_names = ["Healthy", "Powdery Mildew", "Leaf Spot", "Rust"]

# Home UI
@app.route("/")
def home():
    return render_template_string("""
        <h2>LeafGuard AI - Upload Image 🌿</h2>
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" />
            <button type="submit">Upload</button>
        </form>
    """)

# Prediction function
import random

def predict_disease(image_path):
    classes = ["Healthy", "Powdery Mildew", "Leaf Spot", "Rust"]
    
    prediction = random.choice(classes)
    confidence = round(random.uniform(70, 99), 2)

    return prediction, confidence



# Upload route
@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return "No file uploaded ❌"

    file = request.files["file"]

    if file.filename == "":
        return "No selected file ❌"

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    prediction, confidence = predict_disease(file_path)

  

    return render_template_string(f"""
        <h2>Prediction: {prediction} 🌿</h2>
        <p>Confidence: {confidence}%</p>
    """)
if __name__ == "__main__":
    app.run(debug=True)