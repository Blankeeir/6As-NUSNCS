# import the OpenAI Python library for calling the OpenAI API
from openai import OpenAI
import os
import json

from finetune import *



class ChatCompletion(object):
    def __init__(self):
        super().__init__()
        self.model_name = MODEL
        self.client = CLIENT

    def get_chat_response(self, message):

        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",  # role: the role of the messenger (either system, user, assistant or tool)
                    "content": message,  # user messages
                },
                {
                    "role": "user",
                    "content": USER
                },
                {
                    "role": "system",
                    "content": SYSTEM
                },
                {
                    "role": "assistant",
                    "content": ASSISSTANT
                }
            ],

            model = self.model_name,
            temperature=0.8,
            n=1,  # how many choices to get
            stream = True
        )
        # print(response)

    
        for chunk in response:
            print(chunk.choices[0].delta.content, end = "")






