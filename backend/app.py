from flask import Flask, redirect, request, render_template, send_from_directory, url_for
from gtts import gTTS
import uuid
import os
import random

app = Flask(__name__)

# 📁 Folders setup
UPLOAD_FOLDER = "uploads"
STATIC_AUDIO_FOLDER = "static/audio"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_AUDIO_FOLDER, exist_ok=True)

# 🔥 Serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# 🔥 Disease info (IMPORTANT 🔥)
disease_info = {
    "Healthy": {
        "description": "Plant is healthy and shows no signs of disease.",
        "prevention": "Maintain proper watering and sunlight."
    },
    "Powdery Mildew": {
        "description": "White powdery fungal growth on leaves.",
        "prevention": "Avoid humidity and apply fungicide."
    },
    "Leaf Spot": {
        "description": "Dark brown or black spots on leaves.",
        "prevention": "Remove infected leaves and avoid overwatering."
    },
    "Rust": {
        "description": "Orange or rust-colored spots on leaves.",
        "prevention": "Use resistant varieties and fungicide spray."
    }
}

# 🔥 Prediction function
def predict_disease(image_path):
    classes = ["Healthy", "Powdery Mildew", "Leaf Spot", "Rust"]
    
    prediction = random.choice(classes)
    confidence = round(random.uniform(70, 99), 2)

    return prediction, confidence

# 🌿 Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/detect")
def detect():
    return render_template("detect.html")

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

    # 🔥 unique filename
    unique_filename = f"{uuid.uuid4().hex}_{file.filename}"

    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(file_path)

    prediction, confidence = predict_disease(file_path)

    # 🔥 dynamic info (SAFE)
    info = disease_info.get(prediction, {
        "description": "No data available",
        "prevention": "Consult agricultural expert"
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