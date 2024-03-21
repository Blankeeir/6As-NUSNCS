import requests
import json
from model.OpenAiModel.envVar import *
from model.OpenAiModel.chat_completion import *
from controller.controller import Controller
import requests
from PIL import Image
from io import BytesIO

###
def test_image_generation(prompt_history):
    image_url = Controller.get_ai_image_url(prompt_history)  # Replace with your image URL
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = response.content
        image = Image.open(BytesIO(image_data))
        image.show()  # Display the image
        return "Image displayed successfully"
    else:
        return "Failed to retrieve image"


# if __name__ == '__main__':
#     requestor = ChatCompletion()
#     input_s = input('user input: ')
#     requestor.get_chat_response(input_s)

    '''print(res)

    response = res

    print(f"chatGPT: {response}")'''

        # To get number of tokens
        # print(num_tokens_from_messages(messages, MODEL))

