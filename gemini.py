# pip install -q -U google-generativeai
import google.generativeai as genai
import os, dotenv, pathlib
from gemini_prompts import get_music_prompt

dotenv.load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

text_model = genai.GenerativeModel('gemini-pro')
vision_model = genai.GenerativeModel('gemini-pro-vision')



def get_music(mood)
    music_prompt = get_music_prompt(mood)
    music_response = text_model.generate_content(music_prompt)
    return music_response


def get_img2img(mood, init_img):
    img2img_prompt = get_img2img_prompt(mood)

    input_img = [{
        'mime_type': 'image/png',
        'data': pathlib.Path(init_img).read_bytes()
    }]
    img2img_response = vision_model.generate_content(
        content=[img2img_prompt, input_img]
    )
    return img2img_response
    
