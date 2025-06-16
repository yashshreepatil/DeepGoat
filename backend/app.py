from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from PIL import Image

app = Flask(__name__)
CORS(app)


# Load the trained model
MODEL_PATH = "model/Resnet50_2.h5"
model = load_model(MODEL_PATH)

# Define class names in the same order as your training labels
class_names = ['Anthrax', 'Brucellosis', 'CLA', 'Endo parasite', 'FMD', 'Healthy']  # Update based on your dataset

# Image preprocessing function
def preprocess(img_path):
    img = Image.open(img_path).convert('RGB')
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route("/predict", methods=["POST"])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img_file = request.files['image']
    img_path = os.path.join("uploads", img_file.filename)

    # Make sure uploads folder exists
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    img_file.save(img_path)

    # Preprocess and predict
    processed_img = preprocess(img_path)
    predictions = model.predict(processed_img)
    predicted_index = np.argmax(predictions[0])
    predicted_class = class_names[predicted_index]
    confidence = float(np.max(predictions[0]))

    # Clean up the uploaded file
    os.remove(img_path)

    return jsonify({
        "prediction": predicted_class,
        "confidence": round(confidence * 100, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
