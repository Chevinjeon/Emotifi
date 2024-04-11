from flask import Flask, jsonify, request, send_file, Response
from flask_cors import CORS, cross_origin
from flask import send_from_directory

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
import uuid 

app = Flask(__name__)
cors = CORS(app)

@app.route('/test', methods=['POST'])
@cross_origin()
def test():
    return Response(gemini_RAG.get_test_response())


@app.route('/infer-mood', methods=['POST'])
@cross_origin()
def infer_mood():
    assert('eeg' in request.files)
    assert(request.files['eeg'].filename.endswith('.csv'))

    file_id = str(uuid.uuid4())
    request.files['eeg'].save(os.path.join('data_transfer', file_id + '.csv'))
    
    mood_result = eeg_analyzer.infer(file_id)
    return {
        'result': mood_result
    }

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image = request.files['image']
    image_bytes = image.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    # Infer mood from eeg_analyzer ? , placeholder for actual implementation
    # mood_result = eeg_analyzer.infer(file_id)
    mood_result = "happy"  # Placeholder for demonstration

    # Dynamically construct the prompt with the mood result (ideally)
    prompt = f"You are a professional art therapist and you are analyzing an artwork generated from a person with ADHD. Their mood is {mood_result}. The artwork was created based on the mood they are feeling. Tell us your artistic interpretation of the art and how the person with ADHD might be feeling at the psychological level."

    API_KEY = os.getenv('GEMINI_API_KEY')
    headers = {'Authorization': f'Bearer {API_KEY}'}
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    { "text": prompt },
                    {
                        "inlineData": {
                            "mimeType": image.content_type,
                            "data": base64_image
                        }
                    },
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

    # EEG filtering visualizations for frontend
    @app.route('/images/<filename>')
    def serve_image(filename):
        return send_from_directory('static/images', filename)
    

    @app.route('/handle-selection', methods=['POST'])
    @cross_origin()
    def handle_selection():
        data = request.get_json()  # is the selection sent as JSON?
        selection = data.get('option')

        if selection == 'sample':
            # Path to  EEGMeditation.csv?? file
            csv_file_path = 'OpenBCI_GUI-v5-meditation.txt'
            df = pd.read_csv(file_path, delimiter=",") # Check delimiter
            file_id = str(uuid.uuid4())
            temp_csv_path = os.path.join('data_transfer', file_id + '.csv')
            df.to_csv(temp_csv_path)
            mood_result = eeg_analyzer.infer(file_id)
            # Cleanup?
            os.remove(temp_csv_path)
            return jsonify({'result': mood_result})
        
        elif selection == 'own':
            # Path to OpenBCICyton.py script
            script_path = 'OpenBCIConnection.py'
            subprocess.run(['python', script_path])
            return jsonify({'message': 'Script started successfully'})
        else:
            return jsonify({'error': 'Invalid selection'}), 400


"""
@app.route('/generate-text', methods=['POST'])
@cross_origin()
def generate_text():

    mood = request.form.get('mood')
    response_type = request.form.get('response_type')

    if response_type == 'advice':
        return Response(gemini_RAG.get_advice(mood))
    elif response_type == 'music':
        return 'dadsad'
"""
    
app.run(host='0.0.0.0', port=5001)