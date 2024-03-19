### This py implements assistant api
from openai import OpenAI
from chatCompletion import ChatCompletion
from finetune import *
from imageGeneration import *
from dynamicPricing import *
### instantiate an assistant


class Assisstant(object):
    def __init__(self, assistant_name):
        super().__init__()
        client = CLIENT
        self.name = assistant_name
        self.thread = client.beta.threads.create()
        self.assistant = client.beta.assistants.create(
        name="testing assistant",
        instructions="user instructions here",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4-turbo-preview",
        )   



            ### assisstant create user message
    def addMessage(self, role, message):
        message = self.client.beta.threads.messages.create(
        thread_id = self.thread.id,
        role = role,
        content = message
    )
    
    

