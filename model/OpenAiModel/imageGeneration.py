from openai import OpenAI
import os
import json

from model.OpenAiModel.envVar import *


client = CLIENT
class ImageGeneration(object):
    def __init__(self):
        super().__init__()
        self.model_name = MODEL
        client = CLIENT
    
    def get_image_response(self, message):
        response = client.images.generate(
            model="dall-e-3",
            prompt="a white siamese cat",
            size= IMAGE_SIZE,
            quality="hd",
            n=1,
        )

        ##response_format ('url' or 'b64_json'): 
        ##The format in which the generated images are returned. Must be one of "url" or "b64_json". Defaults to "url".

        image_url = response.data[0].url  

        return image_url