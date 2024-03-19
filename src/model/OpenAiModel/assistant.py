from openai import OpenAI
from chatCompletion import *
from envVar import *
from imageGeneration import *
from eventHandler import *


#### assisstants are for data feeds 
# assistant list: decoder assistant & pricing model assistant &  
### This py implements assistant api

client = CLIENT


### specify assistant file ids here



class Assistant:
    def __init__(self, fileids):
        ### upload file for this assistant
        self.file = self.client.files.create(
            file=open("data/static/ERP Rates.json", "rb"),
            purpose='assistants'
        )
        self.file_ids = [self.file.id]
        self.thread = self.client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": "Create 3 data visualizations based on the trends in this file.",
                    "file_ids": self.file_ids
                }
            ]
        )
        self.assistant = self.client.beta.assistants.create(
            name="transportGPT",
            description = ASSISSTANT_INSTRUCTION,
            model= MODEL,
            tools= TOOLS,
            file_ids=[self.file.id]
        )

    def addMessage(self, role, content):
        message = client.beta.threads.messages.create(
            thread_id =self.thread.id,
            role = role,
            content = content,
            file_id = self.file_ids
        )

    def run(self):
        with self.client.beta.threads.runs.create_and_stream(
                thread_id = self.thread.id,
                assistant_id = self.assistant.id,
                instructions=ASSISSTANT_INSTRUCTION,
                event_handler=EventHandler(),
        ) as stream:
            stream.until_done()






#code interpreter
            
image_data = client.files.content("file-abc123")
image_data_bytes = image_data.read()

with open("./my-image.png", "wb") as file:
    file.write(image_data_bytes)




if __name__ == '__main__':
    assistant = Assistant()
    assistant.addMessage("user", "what's this file about?")
    assistant.run()
