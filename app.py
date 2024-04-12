from flask import Flask, jsonify, request, send_file, Response, send_from_directory
from flask_cors import CORS, cross_origin
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, sys, dotenv
import uuid
import gemini_RAG
import imagen
import eeg_analyzer
import requests 
import base64

app = Flask(__name__)
CORS(app, support_credentials=True, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/test', methods=['POST'])
@cross_origin()
def test():
    return Response(gemini_RAG.get_test_response())

@app.route('/test-test')
def test_test():
    return "Test endpoint works!"

@app.route('/infer-mood', methods=['POST'])
@cross_origin()
def infer_mood():
    mood_result = "relaxed"
    return jsonify({'result': mood_result})

@app.route('/analyze-image', methods=['POST'])
@cross_origin()
def analyze_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    image = request.files['image']
    image_bytes = image.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    mood_result = "happy"  # Placeholder for demonstration
    prompt = f"You are a professional art therapist and you are analyzing an artwork generated from a person with ADHD. Their mood is {mood_result}. The artwork was created based on the mood they are feeling. Tell us your artistic interpretation of the art and how the person with ADHD might be feeling at the psychological level."
    API_KEY = os.getenv('GEMINI_API_KEY')
    headers = {'Authorization': f'Bearer {API_KEY}'}
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {"inlineData": {"mimeType": image.content_type, "data": base64_image}}
                ],
            },
        ],
    }
    response = requests.post('https://api.google-gemini.com/v1/generate', json=payload, headers=headers)
    if response.status_code == 200:
        analysis_result = response.json()
        return jsonify(analysis_result)
    else:
        return jsonify({'error': 'Failed to analyze image'}), response.status_code

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

@app.route('/handle-selection', methods=['POST', 'OPTIONS'])
@cross_origin(origins="http://localhost:3000", allow_headers=['Content-Type', 'Authorization'], supports_credentials=True)
def handle_selection():
    if request.method == "POST":
        data = request.get_json()
        selection = data.get('option')
        if selection == 'sample':
            csv_file_path = 'OpenBCI_GUI-v5-meditation.txt'
            df = pd.read_csv(csv_file_path, delimiter=",")
            file_id = str(uuid.uuid4())
            temp_csv_path = os.path.join('data_transfer', file_id + '.csv')
            df.to_csv(temp_csv_path)
            mood_result = eeg_analyzer.infer(file_id)
            os.remove(temp_csv_path)
            return jsonify({'result': mood_result})
        elif selection == 'own':
            script_path = 'OpenBCIConnection.py'
            subprocess.run(['python', script_path])
            return jsonify({'message': 'Script started successfully'})
        else:
            return jsonify({'error': 'Invalid selection'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
