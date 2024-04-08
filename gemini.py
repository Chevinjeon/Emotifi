# pip install -q -U google-generativeai
import google.generativeai as genai
import os, dotenv, PIL
import gemini_prompts

dotenv.load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

text_model = genai.GenerativeModel('gemini-pro')
vision_model = genai.GenerativeModel('gemini-pro-vision')


def stream_story(img_path, mood):

    img = PIL.Image.open(img_path)
    prompt = gemini_prompts.get_story_prompt(mood)

    response = vision_model.generate_content(
        contents=[prompt, img],
        stream=True,

    )
    response.resolve()

    for chunk in response:
        print(chunk.text)

def get_music(mood):
    """
    music_prompt = get_music_prompt(mood)
    music_response = text_model.generate_content(music_prompt)
    return music_response
    """


