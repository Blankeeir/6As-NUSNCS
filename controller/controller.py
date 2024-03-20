import json

from model.OpenAiModel.ChatCompletion import ChatCompletion
from model.OpenAiModel.OpenAiRequest import MODEL
from model.data.run_dynamic_data import update # do not remove
from openai import OpenAI
import googlemaps
from datetime import datetime
import os


class Controller:
    client = OpenAI()

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
        prompt = f"I am giving you an input. I want to you to read this input and get me the starting point and ending point "\
            f"such that I can simply plug it into Google maps and I can get a route from the starting point to the ending point. "\
            f"I want to the output format to be exactly like this: \n"\
            f"{{'start': 'starting point', 'end': 'ending point'}}. "\
            f"This is basically a JSON object with two keys, 'start' and 'end', and the values are the starting and ending points. "\
            f"Here is the input: \n"\
            f"{input}"
        return self.get_ai_res(prompt)

    def post_accident_bot_res(self):
        return "POST ACCIDENT BOT RES"

    def route_planner_res(self):
        return "POST ACCIDENT BOT"

    def route_info_res(self):
        return "POST ACCIDENT"
        
    def get_ai_res(self,prompt):
        return ChatCompletion(MODEL).get_chat_response(prompt)

    def get_routes_from_input(self, start, end) :
        gmaps = googlemaps.Client(key=os.environ.get("GOOGLE_CLOUD_API_KEY"))
        now = datetime.now()
        directions_result = gmaps.directions(start, end, mode="transit", departure_time=now)
        return directions_result

