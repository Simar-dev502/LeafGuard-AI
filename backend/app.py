from flask import Flask, request, jsonify, render_template_string
import os
import numpy as np
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dummy model function
def predict_disease(image_path):
    # 🔥 Fake logic (replace later with ML model)
    classes = ["Healthy", "Powdery Mildew", "Leaf Spot", "Rust"]
    return np.random.choice(classes)

@app.route("/")
def home():
    return render_template_string("""
        <h2>LeafGuard AI - Upload Image 🌿</h2>
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" />
            <button type="submit">Upload</button>
        </form>
    """)

@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return "No file uploaded ❌"

    file = request.files["file"]

    if file.filename == "":
        return "No selected file ❌"

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # 🧠 Image preprocessing
    image = Image.open(file_path)
    image = image.resize((224, 224))  # standard size

    # 🔥 Prediction
    prediction = predict_disease(file_path)

    return f"""
    File uploaded successfully ✅ <br>
    Prediction: {prediction}
    """

if __name__ == "__main__":
    app.run(debug=True)