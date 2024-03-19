# import the OpenAI Python library for calling the OpenAI API
from openai import OpenAI
import os
import json
from model.OpenAiModel.envVar import *



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
                    "content": EXAMPLE
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

if __name__ == '__main__':
    requestor = ChatCompletion()
    input_s = input('user input: ')
    requestor.get_chat_response(input_s)
    '''print(res)

    response = res

    print(f"chatGPT: {response}")'''

        # To get number of tokens
        # print(num_tokens_from_messages(messages, MODEL))



