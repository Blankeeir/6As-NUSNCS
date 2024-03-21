import json
import threading

from flask import Response

from model.OpenAiModel.chat_completion import ChatCompletion
from model.OpenAiModel.envVar import *
from model.data.run_dynamic_data import update  # do not remove
from model.OpenAiModel.event_handler import EventHandler
from openai import OpenAI
import googlemaps
from datetime import datetime
import os
import json
from model.OpenAiModel.imageGeneration import ImageGeneration

client = CLIENT



def is_json_file(filename):
    try:
        with open(filename, 'r') as f:
            json.load(f)
        return True
    except json.JSONDecodeError:
        return False
    

class Controller:
    def __init__(self):
        self.client = CLIENT
        self.output = ""
        self.isProcessing = True

    # Functions to get the static data from ../../data folder
    def get_static_data(self, file_path):
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
    # }

    # Functions to output the data to the website (POST to api endpoint, output as JSON)
    # Output is as such: {
    #    "response":
    #        {
    #            "text": String,
    #        }
    # }

    # Functions to get the real time data from ../model/data folder

    def get_ai_res(self, prompt):
        return ChatCompletion(MODEL).get_chat_response(prompt)

    def parse_input(self, input) -> str:
        """
        This function takes an input string and constructs a prompt for the AI model. 
        The prompt instructs the AI to parse the input and extract the starting and ending points 
        for a route that can be used in Google Maps. The output format is a JSON object with two keys, 
        'start' and 'end', and the values are the starting and ending points.

        Args:
            input (str): The input string to be parsed by the AI model.

        Returns:
            str: The AI model's response to the constructed prompt.
        """
        prompt = f"I am giving you an input. I want to you to read this input and get me the starting point and ending point " \
                 f"such that I can simply plug it into Google maps and I can get a route from the starting point to the ending point. " \
                 f"I want to the output format to be exactly like this: \n" \
                 f"{{'start': 'starting point', 'end': 'ending point'}}. " \
                 f"This is basically a JSON object with two keys, 'start' and 'end', and the values are the starting and ending points. " \
                 f"Here is the input: \n" \
                 f"{input}"
        
        return ChatCompletion().get_chat_response(prompt)

    def post_accident_bot_res(self, prompt, thread):
        accident_description = prompt
        location = self.parse_input(prompt)
        loc = location if location else "Singapore"
        prompt = f"I am at this location: "
        prompt += loc + "\n"
        prompt += f"I just had an vehicular accident, "
        prompt += accident_description + "\n"
        prompt += f"please recommend me on the best medical advice" \
                  f"and legal advice given my current situation"

        # add userinput to thread
        client.beta.threads.messages.create(
            thread.id,
            role="user",
            content=prompt
        )

        self.get_ai_res(thread)

    def greetings(self):
        greetings = f"Hello there! I'm TransportGPT, I have 3 versions of myself:\n" \
                    f"1. I can help you with legal and medical advice using the latest data in a vehicular accident\n" \
                    f"2. I can help you plan a route given your current start and end location given your preferences on ERP, weather conditions and eco-friendliness\n" \
                    f"3. I can give you some route information to aide you in your travels.\n"
        return greetings

    def route_planner_res(self, prompt, thread):
        location = self.parse_input(prompt)
        ## prompt engineering according to choices
        client.beta.threads.messages.create(
            thread.id,
            role="user",
            content=prompt
        )
        self.get_ai_res(thread)

    def route_info_res(self, prompt, thread):
        client.beta.threads.messages.create(
            thread.id,
            role="user",
            content=prompt
        )
        return self.get_ai_res(thread)

    '''
    def get_ai_res(self,prompt):
        return ChatCompletion().get_chat_response(prompt)'''

    def get_routes_from_input(self, start, end):
        gmaps = googlemaps.Client(key=os.environ.get("GOOGLE_CLOUD_API_KEY"))
        now = datetime.now()
        directions_result = gmaps.directions(start, end, mode="transit", departure_time=now)
        return directions_result

    def get_ai_res(self, thread):
        try: 
            self.output = ""
            self.isProcessing = True

            file_list = []
            test_file_name = "data/dynamic/carpark_availability/carpark_availability.json"
            if is_json_file(test_file_name):
                test_file = client.files.create(
                            file = open(test_file_name, "rb"),
                            purpose ="assistants"
                        )
                file_list = [test_file]

            '''
            for dirpath, dirnames, filenames in os.walk("data/dynamic"):
                for filename in filenames:
                    if is_json_file(os.path.join(dirpath, filename)):
                        file = client.files.create(
                            file=open(os.path.join(dirpath, filename), "rb"),
                            purpose="assistants"
                        )
                        file_list.append(file)


            for dirpath, dirnames, filenames in os.walk("data/static"):
                for filename in filenames:
                    if is_json_file(os.path.join(dirpath, filename)):
                        file = client.files.create(
                            file=open(os.path.join(dirpath, filename), "rb"),
                            purpose="assistants"
                        )
                        file_list.append(file)
            '''

            file_id_list = []

            for file in file_list:
                file_id_list.append(file.id)

            assistant = client.beta.assistants.create(
                name="transportGPT",
                description=ASSISTANT_INSTRUCTION,
                model= MODEL,
                tools= TOOLS,
                file_ids = file_id_list
            )

            eventHandler = EventHandler()
            #consumer = eventHandler.get_consumer()
            def clean_up():
                with self.client.beta.threads.runs.create_and_stream(
                    thread_id=thread.id,
                    assistant_id=assistant.id,
                    instructions = ASSISTANT_INSTRUCTION,
                    event_handler = eventHandler,
                ) as stream:
                    stream.until_done()
                    self.isProcessing = False
                    print(f"\n\ndone event\n event_info: done one thread {thread.id}, served by assistant {assistant.id}\n\n")
                    eventHandler.close()
            clean_up_thread = threading.Thread(target= clean_up)
            return eventHandler.queue
        finally: 
            clean_up_thread.start()
           

    def get_ai_image_url(self,prompt):
        return ImageGeneration().get_image_response(prompt)
        
