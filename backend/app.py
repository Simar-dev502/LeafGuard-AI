from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "LeafGuard AI Backend Running 🚀"

# Test API route
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "API is working!"})

if __name__ == "__main__":
    app.run(debug=True)

   
    
   
