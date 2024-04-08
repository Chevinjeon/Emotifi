import base64
import os, dotenv
import requests





dotenv.load_dotenv()

sd_api_key = os.getenv('STABLE_DIFFUSION_API_KEY')
sd_engine_id = 'stable-diffusion-v1-6'

def new_abstract(mood):
    pass

def img2img(init_img_path, mood):

    result_img_path = 'result.png'
    
    text_promot = 'happy'
    response = requests.post(
        f'https://api.stability.ai/v1/generation/{sd_engine_id}/image-to-image',
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {sd_api_key}"
        },
        files={
            "init_image": open(init_img_path, "rb")
        },
        data={
            "image_strength": 0.4,
            "init_image_mode": "IMAGE_STRENGTH",
            "text_prompts[0][text]": text_prompt,
            "cfg_scale": 20,
            "samples": 1,
            "steps": 30,
        }
    )

    if response.status_code != 200:
        raise Exception(str(response.text))

    response = response.json()

    with open(result_img_path, 'wb') as f:
        result_img = response['artifacts'][0]
        f.write(base64.b64decode(result_img['base64']))

    return result_img_path


# img2img('init2.png', 'spooky atmosphere, halloween, late night, very dark color')