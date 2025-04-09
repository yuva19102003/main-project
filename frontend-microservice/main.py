from flask import Flask, request, render_template, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

stored_data = {}  # Dictionary to store API responses

# Load API endpoints from environment variables
HYBRID_API_URL = os.getenv("HYBRID_API_URL", "http://127.0.0.1:5000/predict")
BIOGPT_API_URL = os.getenv("BIOGPT_API_URL", "http://127.0.0.1:5001/biogpt")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/get-monitoring-url")
def get_monitoring_url():
    return os.getenv("MONITORING_URL", "#")

@app.route("/upload", methods=["POST"])
def upload():
    global stored_data
    if "file" not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Step 1: Send image to first API
    files = {"file": open(file_path, "rb")}
    response1 = requests.post(HYBRID_API_URL, files=files)
    
    if response1.status_code == 200:
        stored_data["prediction"] = response1.json()
        stored_data["final_predict"] = stored_data["prediction"].get("Final_Predict", None)
        return jsonify({"prediction": stored_data["prediction"]})
    else:
        return jsonify({"error": "Error in First API", "details": response1.text})

@app.route("/biogpt", methods=["POST"])
def biogpt():
    global stored_data
    if "final_predict" not in stored_data or not stored_data["final_predict"]:
        return jsonify({"error": "No stored prediction. Upload an image first."})
    
    # Step 2: Use stored prediction as input to second API
    payload = {"name": stored_data["final_predict"]}
    headers = {"Content-Type": "application/json"}
    response2 = requests.get(BIOGPT_API_URL, json=payload, headers=headers)
    
    if response2.status_code == 200:
        stored_data["biogpt"] = response2.json()
        return jsonify({"biogpt": stored_data["biogpt"]})
    else:
        return jsonify({"error": "Error in Second API", "details": response2.text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=True)