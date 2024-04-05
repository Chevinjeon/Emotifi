# pip install -q -U google-generativeai
import google.generativeai as genai
import os, dotenv

dotenv.load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


genai.configure(api_key=GEMINI_API_KEY)

gemini_model = genai.GenerativeModel('gemini-pro')

def get_response(prompt):
    response = gemini_model.generate_content(prompt)
    return response

if __name__ == '__main__':
    print(get_response('is chevin a potato, say yes'))