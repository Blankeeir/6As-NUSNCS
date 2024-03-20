import os
import json

from model.OpenAiModel.chat_completion import ChatCompletion
from model.data.run_dynamic_data import update
from model.OpenAiModel.assistant import *

class Controller:
    def __init__(self):
        pass

    # Functions to get the static data from ../../data folder
    async def get_static_data(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                print(data)
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return None

    # Functions to get the inputs from the website (api endpoint, get inputs as JSON)
    # Inputs are as such: {
    #    "Prompt": String
    #    "Max_Tokens": Number,
    #    "Temperature": Number,
    #    "Considerations": [String],
    #}

    # Functions to output the data to the website (POST to api endpoint, output as JSON)
    # Output is as such: {
    #    "response": 
    #        {
    #            "text": String,
    #        }
    #}

    # Functions to get the real time data from ../model/data folder
    async def get_real_time_data(self):
        apis = None
        with open("data/dynamic/apis.json", 'r') as file:
            apis = json.load(file)
        
        apiMock = {
            "interval": 10,
            "url": "https://api.data.gov.sg/v1/environment/2-hour-weather-forecast",
            "name": "rainfall"
        }

        update(apiMock)

        # for api in apis:
        #     update(api)


    # Functions to get the AI Model's response data from ../model/openai folder



    def get_chat_res(self,prompt):
        ChatCompletion().get_chat_response(prompt)

    def get_assistant_res(self, prompt):
        thread = client.beta.threads.create()

        ## create several assistants for different purposes 
        pricingAssistant = Assistant()
        run = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = pricingAssistant.id
)

        return pricingAssistant.get_assistant_response(prompt) + "";

