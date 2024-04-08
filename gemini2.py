# pip install -q -U google-generativeai
import google.generativeai as genai
import os, dotenv, PIL
import gemini_prompts

dotenv.load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

text_model = genai.GenerativeModel('gemini-pro')
vision_model = genai.GenerativeModel('gemini-pro-vision')


def stream_story():

    prompt = 'write a story'

    response = text_model.generate_content(
        contents=prompt,
        stream=True,
    )
    response.resolve()

    for chunk in response:
        print(chunk.text)

stream_story()
