from openai import OpenAI
import chatCompletion
import os



### Finetune using clear instructions:
    #https://platform.openai.com/docs/guides/prompt-engineering/strategy-write-clear-instructions
MODEL = "gpt-4-1106-preview"
SYSTEM = "When I ask for help to give me an optimal route from my current location to my destination, \
    you should reply concisely with the optimized route and their"
USER = "please provide an optimiized route with my current location delimited by the first pair of triple quotes and "
ASSISSTANT = "Example: "










# Code here for file upload (fine-tuning purpose)



class finetuneWithFile(object):
    


    def __init__(self,training_file,model):
        super().__init__()
        self.training_file = training_file
        self.model = model

    def create_finetune(self):
        client = OpenAI(
            # This is the default and can be omitted
            api_key= os.environ.get("OPENAI_API_KEY")  # see .env
        )

        response = client.fine_tuning.jobs.create(
            training_file=self.training_file,
            model=self.model
        )

        return response


