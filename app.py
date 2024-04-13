from flask import Flask, jsonify, request, send_file, Response, send_from_directory, url_for
from flask_cors import CORS, cross_origin
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds

import subprocess
import os, sys, dotenv
import uuid

from eeg_analyzer import infer

import gemini_RAG
import gemini
import eeg_analyzer
import create_audio
import stable_diffusion

app = Flask(__name__, static_folder='static')
CORS(app, support_credentials=True, resources={r"/api/*": {"origins": "http://localhost:3000"},  r"/images/*": {"origins": "*"}, r"/get-art": {"origins": "*"}})

@app.route('/test', methods=['POST'])
@cross_origin()
def test():
    return Response(gemini_RAG.get_test_response())


@app.route('/infer-mood-brainwave', methods=['POST'])
@cross_origin()
def infer_mood_brainwave():
    assert(request.files['eeg'].filename.endswith('.csv'))
    
    eeg_input_csv_path = 'eeg.csv'
    request.files['eeg'].save(eeg_input_csv_path)

    mood_result = eeg_analyzer.infer(eeg_input_csv_path)
    return {
        'result': mood_result
    }

@app.route('/infer-mood-audio', methods=['POST'])
@cross_origin()
def infer_mood_audio():
    assert(request.files['audio'].filename.endswith('.mp3'))

    audio_input_mp3_path = 'speech.mp3'
    mood_resul
    

@app.route('/get-art', methods=['POST'])
@cross_origin()
def get_art():
    data = request.json
    mood = request.form.get('mood')

    if mood == 'relaxed':
        mood_description = 'relaxation and peace'
    elif mood == 'stressed':
        mood_description == 'stress and anxiety'
    elif mood == 'angry':
        mood_description == 'anger and frustration'
    elif mood == 'excited':
        mood_description == 'excitement and energy'
    elif mood == 'fear':
        mood == 'fear and unsettled'

    art_output_png_path = 'abstract.png'
    stable_diffusion.get_abstract_art(mood, art_output_png_path)

    return send_file(art_output_png_path, mimetype='image/png')


@app.route('/get-advice', methods=['POST'])
@cross_origin()
def get_advice():

    mood = request.form.get('mood')
    art = request.form.get('art')
    
    if mood == 'excited':
        mood == 'excited and energetic'
    elif mood == 'relaxed':
        mood == 'relaxed and peaceful'
    elif mood == 'stressed':
        mood == 'stressed, tired, and anxious'
    elif mood == 'angry':
        mood = 'angry and irritated'
    elif mood == 'fear':
        mood = 'fear, unsettled, and worried'

    return Response(gemini_RAG.get_advice(mood, art), mimetype='text/event-stream')


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
