# !pip install -U -q google.generativeai

import google.generativeai as genai
import os, json, dotenv
from PIL import Image

dotenv.load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

text_model = genai.GenerativeModel('gemini-pro')
vision_model = genai.GenerativeModel('gemini-pro-vision')
audio_model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

""" ANALYSIS """

def get_analysis(mood, img_path):

    img = Image.open(img_path)
    prompt = f"""You are a professional art therapist and you are analyzing an abstract artwork based on a person with ADHD. 
    Their current mood is {mood}. The artwork was created based on the mood they are feeling. 
    Tell us your artistic interpretation of the art and how the person with ADHD might be feeling at the psychological level."
    """

    for chunk in vision_model.generate_content([prompt, img], stream=True):
        print(chunk.text)
        yield chunk.text


#def get_mood_from_audio(audio_path):
#    return
#    audio = genai.upload_file(path=audio_path)
#    prompt = f"""The given audio is a conversation between an ADHD patient and a psychological therapist.
#    Based on the content of the conversation, deduce the current mood of the ADHD patient as exactly one of the following
#    relaxed
#    stressed
#   angry
#   fear
#   excited
#    Respond in the form of the following json
#    {
#        "mood": mood_result
#   }
#    where mood_result is one of relaxed, stressed, angry, fear, excited
#   """
#    response = audio_model.generate_content([prompt, audio], stream=True):
    # filter out json
#    response = '{' + response.split('{')[1]
#   response = response.split('}')[0] + '}'
#   response = json.loads(response)
#   return response.mood
