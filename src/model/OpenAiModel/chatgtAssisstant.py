### This py implements assistant api
from openai import OpenAI
from ChatCompletion import *

#### If request manually:
'''import requests

headers = {
    "OpenAI-Beta": "assistants=v1",
    "Authorization": "Bearer YOUR_OPENAI_API_KEY"
}

response = requests.post("https://api.openai.com/v1/assistants", headers=headers)

# Handle the response...'''




client = OpenAI()


class Assisstant(object):
     def __init__(self,api_key,assistant_name):
         super().__init__()
         self.api_key = api_key
         self.assisstant_name = assistant_name


assistant = client.beta.assistants.create(
  name="testing assistant",
  instructions="user instructions here",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4-turbo-preview",
)

thread = client.beta.threads.create()


message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="say hello"

)
