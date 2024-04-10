from flask import Flask, jsonify, request, send_file, Response
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


@app.route('/generate-image', methods=['POST'])
@cross_origin()
def generate_image():

    mood = request.form.get('mood')
    img_type = request.form.get('img_type')

    if img_type == 'abstract':
        result_img_path = imagen.new_abstract(mood)

    elif img_type == 'modify':
        init_img_path = 'init_img.png'
        request.files['init_img'].save(init_img_path)
        result_img_path = imagen.img2img(init_img_path, mood)
        os.remove(init_img_path)
    
    return send_file(result_img_path, mimetype='image/gif')
    
@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    # Check for image in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    # Retrieve the prompt from the form data, if provided
    prompt = request.form.get('prompt', '')

    image = request.files['image']
    image_bytes = image.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    API_KEY = os.getenv('GEMINI_API_KEY')
    headers = {'Authorization': f'Bearer {API_KEY}'}
    payload = {
        # Add your API-specific configuration here
        "contents": [
            {
                "role": "user",
                "parts": [
                    { "text": prompt },
                    {
                        "inlineData": {
                            "mimeType": image.content_type,  # Using the content type from the uploaded file
                            "data": base64_image
                        }
                    },
                ],
            },
        ],
    }

    # Send request to the Google Gemini API
    response = requests.post('https://api.google-gemini.com/v1/generate', json=payload, headers=headers)

    if response.status_code == 200:
        analysis_result = response.json()
        return jsonify(analysis_result)
    else:
        return jsonify({'error': 'Failed to analyze image'}), response.status_code


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