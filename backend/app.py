from flask import Flask, redirect, request, render_template, send_from_directory, url_for
from gtts import gTTS
import uuid
import os
import requests
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import pickle
import openai

app = Flask(__name__)

# 📁 Folders
UPLOAD_FOLDER = "uploads"
STATIC_AUDIO_FOLDER = "static/audio"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_AUDIO_FOLDER, exist_ok=True)

# 🔥 Load model
model = load_model("plant_disease_model.h5")

# 🔥 Load class names
class_names = pickle.load(open("class_names.pkl", "rb"))

# 🔥 OpenAI key (yaha apni key daalna)
openai.api_key = "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"

# 🔥 AI Description Function
def get_ai_description(disease):

    disease = disease.lower()

    description = ""
    prevention = ""

    if "mold" in disease:
        description = "Leaf mold is a fungal disease that appears as yellow spots on leaves."
        prevention = "Reduce humidity, improve air circulation and use fungicide."

    elif "blight" in disease:
        description = "Blight causes dark spots and rapid damage to plant leaves."
        prevention = "Remove infected leaves and apply fungicide."

    elif "rust" in disease:
        description = "Rust disease forms orange or brown powdery spots on leaves."
        prevention = "Use resistant plant varieties and apply fungicide."

    elif "spot" in disease:
        description = "Leaf spot causes dark circular patches on leaves."
        prevention = "Avoid overwatering and remove infected parts."

    elif "healthy" in disease:
        description = "The plant appears healthy with no visible disease."
        prevention = "Maintain proper watering and sunlight."

    else:
        description = "This disease is not clearly identified."
        prevention = "Try uploading a clearer image or consult an expert."

    return description, prevention
     
# 🔥 Serve uploaded image
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# 🔥 Prediction
def predict_disease(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)

    class_index = np.argmax(predictions)
    confidence = round(np.max(predictions) * 100, 2)

    if class_index < len(class_names):
        prediction = class_names[class_index]
    else:
        prediction = "Unknown Disease"

    # clean name
    clean_prediction = prediction.replace("___", " ").replace("_", " ")

    return clean_prediction, confidence

# 🔥 AI fallback (optional)
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

    # 🔥 Prediction
    prediction, confidence = predict_disease(file_path)

    # 🔥 fallback
    if confidence < 60:
        prediction, confidence = ai_fallback(file_path)

    # 🔥 AI description
    description, prevention = get_ai_description(prediction)

    return render_template(
        "detect.html",
        prediction=prediction,
        confidence=confidence,
        filename=unique_filename,
        description=description,
        prevention=prevention
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