from flask import Flask, jsonify, request, send_file, Response
from flask_cors import CORS, cross_origin

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os, sys, dotenv
import uuid

import gemini
import imagen
import eeg_analyzer

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/infer-mood', methods=['POST'])
@cross_origin()
def infer_mood():
    assert('eeg' in request.files)
    assert(request.files['eeg'].filename.endswith('.csv'))

    file_id = str(uuid.uuid4())
    request.files['eeg'].save(file_id + '.csv')
    
    result = eeg_analyzer.infer(file_id)
    return {
        'result': result
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
    

@app.route('/generate-text', methods=['POST'])
@cross_origin()
def generate_text():

    mood = request.form.get('mood')
    img_type = request.form.get('img_type')

    input_img_path = 'input_img.png'
    request.files['input_img'].save(input_img_path)

    if img_type == 'abstract':
        return Response(gemini.stream_story(input_img_path, mood), mimetype='text/event-stream')
    
    elif img_type == 'modify':
        return Response(gemini.stream_desc(input_img_path, mood), mimetype='text/event-stream')

    


    