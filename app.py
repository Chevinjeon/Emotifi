from flask import Flask, jsonify, request, send_file, Response, send_from_directory
from flask_cors import CORS, cross_origin
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
import numpy as np
import pandas as pd
import matplotlib
import subprocess
import matplotlib.pyplot as plt
import os, sys, dotenv
import uuid
import gemini_RAG
import imagen
import eeg_analyzer 
from eeg_analyzer import infer
import requests 
import base64

app = Flask(__name__)
CORS(app, support_credentials=True, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/test', methods=['POST'])
@cross_origin()
def test():
    return Response(gemini_RAG.get_test_response())


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

#@app.route('/images/<filename>')
#def serve_image(filename):
#    return send_from_directory('static/images', filename)

@app.route('/handle-selection', methods=['POST', 'OPTIONS'])
@cross_origin(origins="http://localhost:3000", allow_headers=['Content-Type', 'Authorization'], supports_credentials=True)
def handle_selection():
    data = request.get_json()
    selection = data.get('option')
    try:
        if selection == 'sample':
            # Path to the Python script
            script_path = 'image_display_sample_eeg.py'

            # Execute the script
            subprocess.run(['python', script_path], check=True)


            csv_file_path = 'OpenBCI_GUI-v5-meditation.txt'
            temp_csv_path = os.path.join('data_transfer', f"{uuid.uuid4()}.csv")
            df = pd.read_csv(csv_file_path, delimiter=",")
            #df = clean_data(df)
            print("Data Loaded:", df.head())
            df.to_csv(temp_csv_path)

            mood_result = infer_mood(df)  

            # Assuming the script saves images named 'before_processing.png' and 'after_processing.png'
            return jsonify({
                'before': '/images/before_processing.png',
                'after': '/images/after_processing.png',
                'mood_result': mood_result  # This should be generated or retrieved appropriately
            })
        
        
        elif selection == 'own':
            params = BrainFlowInputParams()
            params.serial_port = 'COM3'
            params.board_id = BoardIds.CYTON_BOARD.value
            data = run_full_session(params)
            
            mood_result = infer_mood(data)
            return jsonify({
                'message': 'EEG session completed successfully and processed',
                'mood_result': mood_result
            })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
