import json

from model.OpenAiModel.ChatCompletion import ChatCompletion
from model.OpenAiModel.OpenAiRequest import MODEL
from model.data.run_dynamic_data import update


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

        
    def get_ai_res(self,prompt):
        print(ChatCompletion(MODEL).get_chat_response(prompt))

        # for api in apis:
        #     update(api)

'''
    # Functions to get the AI Model's response data from ../model/openai folder
    def get_ai_res(self, prompt):
        keys = "OpenAI API keys"
        model_name = "gpt-3.5-turbo"
        request_address = "https://api.openai.com/v1/chat/completions"
        requestor = OpenAI_Request(keys,model_name,request_address)

        res = requestor.post_request(prompt)
        
        # if error
        if res.status_code != 200:
            print({"response": "Error: " + res.text})
        print( {"response": res.json()['choices'][0]['message']['content']})'''


    # Functions to fine tune the model with the given static & real-time data
    

