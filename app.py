from flask import Flask, jsonify, request, send_file, Response, send_from_directory, url_for
from flask_cors import CORS, cross_origin
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
import numpy as np
import pandas as pd
import matplotlib
import subprocess
import matplotlib.pyplot as plt
import os, sys, dotenv
import uuid
import imagen
import eeg_analyzer 
from eeg_analyzer import infer
import requests 
import base64

import gemini_RAG
import eeg_analyzer
import create_audio

app = Flask(__name__)
CORS(app, support_credentials=True, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/test', methods=['POST'])
@cross_origin()
def test():
    return Response(gemini_RAG.get_test_response())


@app.route('/infer-mood', methods=['POST'])
@cross_origin()
def infer_mood():
    assert(request.files['eeg'].filename.endswith('.csv'))

    file_id = str(uuid.uuid4())
    request.files['eeg'].save(os.path.join(file_id + '.csv'))

    mood_result = eeg_analyzer.infer(file_id)
    return {
        'result': mood_result
    }


@app.route('/get-art', methods=['POST'])
@cross_origin()
def get_art():

    mood = request.form.get('mood')

    if mood == 'relaxed':
        mood = 'relaxation and peace'
    elif mood == 'stressed':
        mood == 'stress and anxiety'
    elif mood == 'angry':
        mood == 'anger and frustration'
    elif mood == 'excited':
        mood == 'excite and energetic'
    elif mood == 'fear':
        mood == 'fear and unsettled'

    img_path = 'abstract_art.png'
    imagen.get_abstract_art(mood, img_path)

    return send_file(img_path, mimetype='image/png')


@app.route('/get-advice', methods=['POST'])
@cross_origin()
def get_advice():

    mood = request.form.get('mood')
    
    if mood == 'excited':
        mood == 'excited, energetic'
    elif mood == 'relaxed':
        mood == 'relaxed, peaceful'
    elif mood == 'stressed':
        mood == 'stressed, tired, and worn out from anxiety'
    elif mood == 'angry':
        mood = 'angry, irritated'
    elif mood == 'fear':
        mood = 'fear, unsettled, and worried'

    return Response(gemini_RAG.get_advice(mood), mimetype='text/event-stream')


@app.route('/analyze-image', methods=['POST'])
@cross_origin()
def analyze_image():

    mood = request.form.get('mood')
    img = request.files['img']
    
    return Response(gemini_RAG.get_analysis(mood, img), mimetype='text/event-stream')





@app.route('/infer-mood-hardcoded', methods=['POST'])
@cross_origin()
def infer_mood_test():
    mood_result = "relaxed"
    return jsonify({'result': mood_result})



@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(app.static_folder + '/images', filename)

@app.route('/handle-selection', methods=['POST', 'OPTIONS'])
@cross_origin(origins="http://localhost:3000", allow_headers=['Content-Type', 'Authorization'], supports_credentials=True)
def handle_selection():
    data = request.get_json()
    selection = data.get('option')
    try:
        if selection == 'sample':
            script_path = 'image_display_sample_eeg.py'
            subprocess.run(['python', script_path], check=True)
            return jsonify({
                'before': url_for('serve_image', filename='before_processing.png'),
                'after': url_for('serve_image', filename='after_processing.png'),
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
