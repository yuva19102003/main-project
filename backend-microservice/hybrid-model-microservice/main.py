from flask import Flask, request, jsonify
from models import load_image, get_prediction, majority_vote, class_names
from metrics import request_processing_time, failed_requests, efficientnet_predictions, resnet_predictions, densenet_predictions, model_errors
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
@request_processing_time.time()
def predict():
    if "file" not in request.files:
        failed_requests.inc()
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    image = load_image(file)

    # Get predictions & confidence scores
    eff_pred, eff_conf = get_prediction("efficientnet", image)
    res_pred, res_conf = get_prediction("resnet", image)
    densenet_pred, dense_conf = get_prediction("densenet", image)

    # Log predictions
    efficientnet_predictions.labels(class_names[eff_pred]).inc()
    resnet_predictions.labels(class_names[res_pred]).inc()
    densenet_predictions.labels(class_names[densenet_pred]).inc()

    # Majority voting
    predictions = [eff_pred, res_pred, densenet_pred]
    final_prediction = majority_vote(predictions)

    # Track model errors
    if eff_pred != final_prediction:
        model_errors.labels("EfficientNet").inc()
    if res_pred != final_prediction:
        model_errors.labels("ResNet").inc()
    if densenet_pred != final_prediction:
        model_errors.labels("DenseNet").inc()

    return jsonify({
        "EfficientNet_Predict": class_names[eff_pred],
        "EfficientNet_Confidence": eff_conf,
        "ResNet_Predict": class_names[res_pred],
        "ResNet_Confidence": res_conf,
        "DenseNet_Predict": class_names[densenet_pred],
        "DenseNet_Confidence": dense_conf,
        "Final_Predict": class_names[final_prediction]
    })

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
