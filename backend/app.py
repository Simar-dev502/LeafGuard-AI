from flask import Flask, redirect, request, render_template, send_from_directory, url_for
from gtts import gTTS
import uuid
import os
import requests
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

app = Flask(__name__)

# 📁 Folders
UPLOAD_FOLDER = "uploads"
STATIC_AUDIO_FOLDER = "static/audio"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_AUDIO_FOLDER, exist_ok=True)

# 🔥 Load trained model
model = load_model("plant_disease_model.h5")

# 🔥 Class names (dataset ke folder names)
class_names = [
    "Apple___Black_rot",
    "Apple___healthy",
    "Corn___Cercospora_leaf_spot",
    "Corn___healthy",
    "Grape___Black_rot",
    "Grape___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___healthy"
]

# 🔥 Disease info
disease_info = {
    "Apple___Black_rot": {
        "description": "Fungal disease causing dark lesions on apple leaves.",
        "prevention": "Remove infected leaves and apply fungicide."
    },
    "Tomato___Leaf_Mold": {
        "description": "Yellow spots on upper leaves, mold underneath.",
        "prevention": "Avoid humidity and improve air circulation."
    },
    "Potato___Early_blight": {
        "description": "Dark spots with concentric rings.",
        "prevention": "Use fungicide and remove infected plants."
    }
}

# 🔥 Serve uploaded image
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# 🔥 REAL prediction function
def predict_disease(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)

    class_index = np.argmax(predictions)
    confidence = round(np.max(predictions) * 100, 2)

    prediction = class_names[class_index]

    return prediction, confidence

# 🔥 AI fallback
def ai_fallback(image_path):
    try:
        url = "https://api.plant.id/v2/identify"
        files = {'images': open(image_path, 'rb')}
        response = requests.post(url, files=files)

        result = response.json()
        return result["suggestions"][0]["plant_name"], 80
    except:
        return "Unknown Plant", 50

# 🌿 Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/detect")
def detect():
    return render_template("detect.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# 📤 Upload route
@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return redirect(url_for("detect"))

    file = request.files["file"]

    if file.filename == "":
        return redirect(url_for("detect"))

    unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(file_path)

    # 🔥 Real model prediction
    prediction, confidence = predict_disease(file_path)

    # 🔥 fallback (real-world handling)
    if confidence < 60:
        prediction, confidence = ai_fallback(file_path)

    # 🔥 dynamic info
    info = disease_info.get(prediction, {
        "description": "This disease is not in our dataset.",
        "prevention": "Try uploading a clearer plant leaf image."
    })

    return render_template(
        "detect.html",
        prediction=prediction,
        confidence=confidence,
        filename=unique_filename,
        description=info["description"],
        prevention=info["prevention"]
    )

# 🎤 Text-to-Speech
@app.route("/speak")
def speak():
    text = request.args.get("text")
    lang = request.args.get("lang", "en")

    filename = f"audio_{uuid.uuid4().hex}.mp3"
    file_path = os.path.join(STATIC_AUDIO_FOLDER, filename)

    tts = gTTS(text=text, lang=lang)
    tts.save(file_path)

    return {"audio": f"/static/audio/{filename}"}


if __name__ == "__main__":
    app.run(debug=True)