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


def generate_static_fileID_list():
    # if is_json_file(test_file_name):
    #     test_file = client.files.create(
    #         file=open(test_file_name, "rb"),
    #         purpose="assistants"
    #     )
    #     file_list = [test_file]
    file_list = []
    for dirpath, dirnames, filenames in os.walk(STATIC_DATA_PATH):
        if dirpath.__contains__("data/static/rainfall"):
            continue

        for filename in filenames:
            if is_json_file(os.path.join(dirpath, filename)):
                file = client.files.create(
                    file=open(os.path.join(dirpath, filename), "rb"),
                    purpose="assistants"
                )
                file_list.append(file.id)
    return file_list


def generate_dynamic_fileID_list():
    file_list = []

    for dirpath, dirnames, filenames in os.walk(DYNAMIC_DATA_PATH):
        for filename in filenames:
            if is_json_file(os.path.join(dirpath, filename)):
                file = client.files.create(
                    file=open(os.path.join(dirpath, filename), "rb"),
                    purpose="assistants"
                )
                file_list.append(file)
    file_id_list = []
    for file in file_list:
        file_id_list.append(file.id)
    return file_id_list


class Controller:
    def __init__(self):
        self.client = CLIENT
        self.output = ""
        self.isProcessing = True
        self.assistant = client.beta.assistants.create(
            name="transportGPT",
            description=ASSISTANT_INSTRUCTION,
            model=MODEL,
            tools=TOOLS,
            file_ids=generate_static_fileID_list()
        )

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
        loc = location if location else "Singapore"
        prompt += f"\nI am at this location: " + loc + "\n"
        prompt += f"please recommend me on the best route to take to my destination given my current start location and end destination\n"
        prompt += f"When you are created, there is some static data extracted from route and price api is inserted into you, use these data for the prompt.\n"
        prompt += f"Whenever there is a command, new real-time data is inserted into you, use these data for the prompt later as well.\n"
        prompt += f"please analyse the data and give me the best route to take to my destination\n"
        prompt += f"please consider my preferences on ERP rate and eco-friendliness based on statistical evidence as well\n"
        prompt += f"Just give me the route and the cost-benefit analysis, don't give me anything else other than the route and the cost-benefit analysis\n"

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

            eventHandler = EventHandler()

            ## add assistant files dynamic
            for i in generate_dynamic_fileID_list():
                assistant_file = client.beta.assistants.files.create(
                    assistant_id=self.assistant.id,
                    file_id=i
                )

            # consumer = eventHandler.get_consumer()
            def clean_up():
                with self.client.beta.threads.runs.create_and_stream(
                        thread_id=thread.id,
                        assistant_id=self.assistant.id,
                        instructions=RUN_INSTRUCTION,
                        event_handler=eventHandler,
                ) as stream:
                    stream.until_done()
                    self.isProcessing = False
                    print(
                        f"\n\ndone event\n event_info: done one thread {thread.id}, served by assistant {self.assistant.id}\n\n")
                    eventHandler.close()

            clean_up_thread = threading.Thread(target=clean_up)
            clean_up_thread.start()
            return eventHandler.queue
        except Exception as e:
            print(f"Error in get_ai_res: {e}")
            return None

    def get_ai_image_url(self, prompt):
        message = prompt
        prompt += "please generate an image with specific instruction in delimiter triple quotes"
        prompt += "'''Generate an image of a map. The map should show a route from location A to location B. The route should be highlighted and should take into account the user's preferences for weather conditions and pricing. The route should be the most cost-effective one that avoids areas with bad weather. The map should also show key landmarks and points of interest along the route.'''"
        prompt += "please refer to the context given in the following delimiter triple quotes"
        prompt += "I want to let the image be the map with route suggested by the assistant\
                (assistan generate from user input, with location and destination specified and user\
                preferences from previous user input such as weather conditions and pricing \
                (what ever specified by the user)) the desired way for traveling and route has \
                      been generated by the assistant already, should highlight the route on the \
                        map image generated, shou base on the data files we'''"

        return ImageGeneration().get_image_response(message)
