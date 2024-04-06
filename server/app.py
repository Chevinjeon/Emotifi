from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os, sys, dotenv
import gemini
import server.eeg_analysis as eeg_analysis


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/generate', methods=['POST'])
@cross_origin()
def generate_content():

    mood = eeg_analysis.analyze()

    if request.form.get('art'):
        pass

    if request.form.get('music'):
        music_text = gemini.get_music(mood)
        music = 



    