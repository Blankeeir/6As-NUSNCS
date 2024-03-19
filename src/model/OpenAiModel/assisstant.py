### This py implements assistant api
from openai import OpenAI
from chatCompletion import *
from finetune import *
from imageGeneration import *
from dynamicPricing import *

### instantiate an assistant
client = CLIENT
thread = client.beta.threads.create()
assistant = client.beta.assistants.create(
        name="testing assistant",
        instructions="user instructions here",
        tools = TOOLS,
        model="gpt-4-turbo-preview",
        ) 




def addMessage(role, content):
    message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = role,
    content = content
    )

    print(message)
    


addMessage("user", "hello")