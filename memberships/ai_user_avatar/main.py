import openai
from API_KEY import api_key

openai.api_key = api_key


def avatar_gen():
    response = openai.Image.create(
        prompt="a user avatar that is a depiction of an alien, facing forward, shoulder up, gender ambiguous, a random color, make the style of the avatar abstract, and make sure the image avatar fills the space of the image",
        n=1,
        size="1024x1024",
    )
    image_url = response["data"][0]["url"]

    print(image_url)


avatar_gen()
