### This py implements assistant api
from openai import OpenAI
from chatCompletion import *
from finetune import *
from imageGeneration import *
from eventHandler import *

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

    #print(message)
    
with client.beta.threads.runs.create_and_stream(
  thread_id= thread.id,
  assistant_id= assistant.id,
  instructions="Please address the user as Jane Doe. The user has a premium account.",
  event_handler= EventHandler(),

) as stream:
  stream.until_done()


if __name__ == '__main__':
    addMessage("user", "hello")
