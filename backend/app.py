from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Home page with upload form
@app.route("/")
def home():
    return render_template_string("""
        <h2>LeafGuard AI - Upload Image 🌿</h2>
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" />
            <button type="submit">Upload</button>
        </form>
    """)

# Upload API
@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return "No file uploaded ❌"

    file = request.files["file"]

    if file.filename == "":
        return "No selected file ❌"

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return f"File uploaded successfully ✅: {file.filename}"

if __name__ == "__main__":
    app.run(debug=True)