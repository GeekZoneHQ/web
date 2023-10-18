# pip install pillow
# pip install openai

import openai
from API_KEY import api_key
import requests
from PIL import Image
from io import BytesIO

openai.api_key = api_key

def avatar_gen():
    response = openai.Image.create(
        prompt="the bust of a cool robot character from the shoulders up, facing forward",
        n=1,
        size="1024x1024",
    )
    image_url = response["data"][0]["url"]

    # Download the image
    img_data = requests.get(image_url).content
    img = Image.open(BytesIO(img_data))

    # Save the image as "img_avatar.png"
    img.save("img_avatar.png", "PNG")

avatar_gen()